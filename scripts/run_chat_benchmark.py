"""Multi-turn chat benchmark for agentic-chat task.

Uses Ollama's /api/chat endpoint with structured tool calling to test
models the way they're used in tool-calling applications like OpenClaw.
"""

import json
import os
import re
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import requests

from config import (
    OLLAMA_CHAT_URL,
    REQUIREMENTS_DIR,
    get_model_results_dir,
)

# Import tool definitions and dispatch from requirements
sys.path.insert(0, REQUIREMENTS_DIR)
from agentic_chat_tools import TOOL_DEFINITIONS, dispatch_tool_call


def parse_prompt_for_chat(prompt_text: str) -> tuple[str, str]:
    """Split a prompt file into system and user messages.

    Looks for ## System Message and ## User Message headers.
    Returns (system_msg, user_msg).
    """
    system_msg = ""
    user_msg = ""

    # Split on ## headers
    parts = re.split(r'^##\s+', prompt_text, flags=re.MULTILINE)

    for part in parts:
        lower = part.lower()
        if lower.startswith("system message"):
            # Everything after the header line
            lines = part.split("\n", 1)
            system_msg = lines[1].strip() if len(lines) > 1 else ""
        elif lower.startswith("user message"):
            lines = part.split("\n", 1)
            user_msg = lines[1].strip() if len(lines) > 1 else ""

    return system_msg, user_msg


def run_chat_benchmark(
    model: str,
    system_msg: str,
    user_msg: str,
    tools: list[dict],
    num_ctx: int,
    num_predict: int,
    timeout_total: int,
    num_threads: int | None = None,
) -> dict:
    """Run a multi-turn chat benchmark with tool calling.

    Args:
        model: Ollama model name.
        system_msg: System message content.
        user_msg: User message content.
        tools: List of tool definitions (OpenAI format).
        num_ctx: Context window size.
        num_predict: Max tokens per response.
        timeout_total: Total timeout for the entire conversation in seconds.
        num_threads: CPU thread count (None = Ollama default).

    Returns:
        Dict with messages, turn_metrics, tool_calls_log, total_turns,
        completed, final_response.
    """
    messages = [
        {"role": "system", "content": system_msg},
        {"role": "user", "content": user_msg},
    ]

    turn_metrics = []
    tool_calls_log = []
    max_turns = 30
    completed = False
    final_response = ""
    start_time = time.time()

    options = {"num_ctx": num_ctx, "num_predict": num_predict}
    if num_threads is not None:
        options["num_thread"] = num_threads

    for turn in range(max_turns):
        elapsed = time.time() - start_time
        if elapsed >= timeout_total:
            print(f"  Chat timeout after {elapsed:.0f}s ({turn} turns)")
            break

        remaining = timeout_total - elapsed
        turn_start = time.time()

        try:
            resp = requests.post(
                OLLAMA_CHAT_URL,
                json={
                    "model": model,
                    "messages": messages,
                    "tools": tools,
                    "stream": False,
                    "options": options,
                },
                timeout=min(remaining, 300),  # Per-turn cap of 5 min
            )
            resp.raise_for_status()
            data = resp.json()
        except requests.RequestException as e:
            turn_metrics.append({
                "turn": turn,
                "error": str(e),
                "duration_s": round(time.time() - turn_start, 2),
            })
            break

        turn_duration = time.time() - turn_start
        message = data.get("message", {})

        # Collect per-turn metrics from Ollama response
        tm = {
            "turn": turn,
            "duration_s": round(turn_duration, 2),
            "prompt_eval_count": data.get("prompt_eval_count", 0),
            "eval_count": data.get("eval_count", 0),
            "prompt_eval_duration_ns": data.get("prompt_eval_duration", 0),
            "eval_duration_ns": data.get("eval_duration", 0),
        }

        tool_calls = message.get("tool_calls", [])

        if tool_calls:
            # Model wants to call tools
            tm["tool_calls"] = len(tool_calls)
            turn_metrics.append(tm)

            # Append the assistant message (with tool_calls) to history
            messages.append(message)

            # Execute each tool call and append results
            for tc in tool_calls:
                fn = tc.get("function", {})
                tool_name = fn.get("name", "unknown")
                tool_args = fn.get("arguments", {})

                call_start = time.time()
                result = dispatch_tool_call(tool_name, tool_args)
                call_duration = time.time() - call_start

                # Serialize result for the chat message
                if isinstance(result, str):
                    result_str = result
                else:
                    result_str = json.dumps(result, default=str)

                tool_calls_log.append({
                    "turn": turn,
                    "tool": tool_name,
                    "arguments": tool_args if isinstance(tool_args, dict) else str(tool_args),
                    "result_preview": result_str[:500],
                    "success": "error" not in (result if isinstance(result, dict) else {}),
                    "duration_s": round(call_duration, 4),
                })

                # Add tool response to messages
                messages.append({
                    "role": "tool",
                    "content": result_str,
                })

            print(f"  Turn {turn}: {len(tool_calls)} tool call(s) in {turn_duration:.1f}s")

        else:
            # No tool calls -- model is done (or stuck)
            tm["tool_calls"] = 0
            turn_metrics.append(tm)

            content = message.get("content", "")
            if content:
                messages.append({"role": "assistant", "content": content})
                final_response = content
                completed = True
                print(f"  Turn {turn}: final response ({len(content)} chars) in {turn_duration:.1f}s")
            else:
                # Empty response with no tool calls -- model is stuck
                print(f"  Turn {turn}: empty response, ending")

            break

    return {
        "messages": messages,
        "turn_metrics": turn_metrics,
        "tool_calls_log": tool_calls_log,
        "total_turns": len(turn_metrics),
        "completed": completed,
        "final_response": final_response,
    }


def aggregate_chat_metrics(turn_metrics: list[dict], tool_calls_log: list[dict]) -> dict:
    """Aggregate per-turn metrics into summary statistics.

    Returns a dict compatible with the standard metrics.json schema,
    plus chat-specific fields.
    """
    total_prompt_eval = sum(t.get("prompt_eval_count", 0) for t in turn_metrics)
    total_eval = sum(t.get("eval_count", 0) for t in turn_metrics)
    total_prompt_eval_ns = sum(t.get("prompt_eval_duration_ns", 0) for t in turn_metrics)
    total_eval_ns = sum(t.get("eval_duration_ns", 0) for t in turn_metrics)
    total_duration_s = sum(t.get("duration_s", 0) for t in turn_metrics)

    prompt_eval_s = total_prompt_eval_ns / 1e9
    eval_s = total_eval_ns / 1e9

    prompt_tps = (total_prompt_eval / prompt_eval_s) if prompt_eval_s > 0 else 0
    eval_tps = (total_eval / eval_s) if eval_s > 0 else 0

    # Chat-specific stats
    tools_used = set(tc["tool"] for tc in tool_calls_log)
    all_tools = {td["function"]["name"] for td in TOOL_DEFINITIONS}
    successful_calls = sum(1 for tc in tool_calls_log if tc.get("success", False))
    total_calls = len(tool_calls_log)

    return {
        "timing": {
            "total_duration_s": round(total_duration_s, 2),
            "prompt_eval_duration_s": round(prompt_eval_s, 2),
            "eval_duration_s": round(eval_s, 2),
        },
        "tokens": {
            "prompt_eval_count": total_prompt_eval,
            "eval_count": total_eval,
            "prompt_eval_tokens_per_sec": round(prompt_tps, 2),
            "eval_tokens_per_sec": round(eval_tps, 2),
        },
        "chat": {
            "total_turns": len(turn_metrics),
            "total_tool_calls": total_calls,
            "successful_tool_calls": successful_calls,
            "tool_call_success_rate": round(successful_calls / total_calls, 2) if total_calls > 0 else 0,
            "tools_used": sorted(tools_used),
            "tools_available": sorted(all_tools),
            "tool_coverage": round(len(tools_used) / len(all_tools), 2) if all_tools else 0,
        },
    }


def classify_chat_result(
    chat_result: dict,
    wall_clock_s: float,
    total_eval_tokens: int,
) -> dict:
    """Classify the outcome of a chat benchmark run.

    Returns a dict with:
      - classification: one of success, partial_success, empty_response,
                        stalled_inference, text_narration, no_tool_support
      - description: human-readable explanation
    """
    tool_calls = chat_result.get("tool_calls_log", [])
    messages = chat_result.get("messages", [])
    completed = chat_result.get("completed", False)
    total_turns = chat_result.get("total_turns", 0)

    num_tool_calls = len(tool_calls)
    tools_used = set(tc["tool"] for tc in tool_calls)

    # Success cases: model made structured tool calls
    if num_tool_calls > 0:
        if completed and len(tools_used) >= 4:
            return {
                "classification": "success",
                "description": f"Made {num_tool_calls} tool calls using {len(tools_used)} tools, completed with final response",
            }
        else:
            reasons = []
            if not completed:
                reasons.append("no final text response")
            if len(tools_used) < 4:
                reasons.append(f"only {len(tools_used)} tools used")
            return {
                "classification": "partial_success",
                "description": f"Made {num_tool_calls} tool calls but {', '.join(reasons)}",
            }

    # Failure cases: 0 structured tool calls
    # Check if model generated any tokens at all
    if total_eval_tokens == 0:
        if wall_clock_s < 1.0:
            return {
                "classification": "empty_response",
                "description": "Model returned instantly with no tokens -- likely does not support tool-calling chat format",
            }
        else:
            return {
                "classification": "stalled_inference",
                "description": f"Model loaded ({wall_clock_s:.0f}s) but generated 0 tokens -- may produce unparseable output in tool-calling mode",
            }

    # Model generated tokens but made 0 structured tool calls
    # Check if the text mentions tool names (narration pattern)
    assistant_text = ""
    for msg in messages:
        if msg.get("role") == "assistant":
            content = msg.get("content", "")
            if content:
                assistant_text += content + "\n"

    tool_names_in_text = sum(
        1 for tool in ALL_TOOL_NAMES if tool in assistant_text
    )

    if tool_names_in_text >= 2:
        return {
            "classification": "text_narration",
            "description": f"Generated {total_eval_tokens} tokens describing tool calls in text ({tool_names_in_text} tool names referenced) but made 0 structured calls",
        }
    else:
        return {
            "classification": "no_tool_support",
            "description": f"Generated {total_eval_tokens} tokens of plain text with no tool references -- model does not appear to understand tool-calling protocol",
        }


# Tool names for classification text-scanning
ALL_TOOL_NAMES = {
    "get_stock_prices", "get_portfolio_holdings", "calculate_portfolio_value",
    "calculate_volatility_score", "check_risk_threshold", "generate_report",
    "send_notification", "log_operation",
}


def save_chat_results(
    model: str,
    task: str,
    chat_result: dict,
    metrics: dict,
    mode: str,
    ctx_size: int | None = None,
):
    """Save chat benchmark results to the standard results directory.

    Writes three files:
    - output.md: human-readable transcript
    - metrics.json: standard + chat-specific metrics
    - transcript.json: raw messages array for evaluation
    """
    results_dir = get_model_results_dir(model, task, mode=mode, ctx_size=ctx_size)
    os.makedirs(results_dir, exist_ok=True)

    # 1. output.md -- human-readable transcript
    output_lines = [f"# Agentic Chat Transcript: {model}\n"]
    output_lines.append(f"**Turns:** {chat_result['total_turns']}  ")
    output_lines.append(f"**Completed:** {chat_result['completed']}  ")
    output_lines.append(f"**Tool calls:** {len(chat_result['tool_calls_log'])}\n")

    for msg in chat_result["messages"]:
        role = msg.get("role", "unknown")

        if role == "system":
            output_lines.append(f"## System\n\n{msg.get('content', '')}\n")
        elif role == "user":
            output_lines.append(f"## User\n\n{msg.get('content', '')}\n")
        elif role == "assistant":
            content = msg.get("content", "")
            tool_calls = msg.get("tool_calls", [])
            if tool_calls:
                output_lines.append("## Assistant (tool calls)\n")
                for tc in tool_calls:
                    fn = tc.get("function", {})
                    name = fn.get("name", "?")
                    args = fn.get("arguments", {})
                    args_str = json.dumps(args, indent=2, default=str) if isinstance(args, dict) else str(args)
                    output_lines.append(f"### Call: `{name}`\n\n```json\n{args_str}\n```\n")
            if content:
                output_lines.append(f"## Assistant\n\n{content}\n")
        elif role == "tool":
            content = msg.get("content", "")
            # Truncate long tool results in the transcript
            preview = content[:1000] + "..." if len(content) > 1000 else content
            output_lines.append(f"## Tool Result\n\n```json\n{preview}\n```\n")

    output_path = os.path.join(results_dir, "output.md")
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(output_lines))

    # 2. metrics.json
    metrics_path = os.path.join(results_dir, "metrics.json")
    with open(metrics_path, "w", encoding="utf-8") as f:
        json.dump(metrics, f, indent=2)

    # 3. transcript.json -- raw messages for evaluation
    transcript_path = os.path.join(results_dir, "transcript.json")
    with open(transcript_path, "w", encoding="utf-8") as f:
        # Make messages JSON-serializable (tool_calls may have non-serializable bits)
        json.dump(chat_result["messages"], f, indent=2, default=str)

    print(f"  Saved chat results to {results_dir}")
