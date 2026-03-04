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

import copy
import hashlib
from collections import Counter


# Spin detection parameters
_SPIN_WINDOW = 8       # Look at last N tool calls — wider to span portfolio transitions
_SPIN_REPEAT_THRESHOLD = 3  # Same signature this many times in window → spinning


def _call_signature(tool_name: str, tool_args) -> str:
    """Create a hashable signature for a tool call (name + sorted args)."""
    if isinstance(tool_args, dict):
        args_str = json.dumps(tool_args, sort_keys=True, default=str)
    else:
        args_str = str(tool_args)
    return hashlib.md5(f"{tool_name}:{args_str}".encode()).hexdigest()


def detect_spinning(tool_calls_log: list[dict], window: int = _SPIN_WINDOW) -> dict | None:
    """Check if recent tool calls show a spinning pattern.

    Returns a dict with spin details if spinning detected, else None.

    Uses argument signatures (tool_name + hashed args) so that legitimate
    repeated tool names with different arguments (e.g. get_stock_prices for
    different portfolios) are NOT flagged.
    """
    if len(tool_calls_log) < window:
        return None

    recent = tool_calls_log[-window:]

    signatures = [_call_signature(tc["tool"], tc["arguments"]) for tc in recent]
    sig_counts = Counter(signatures)
    most_common_sig, most_common_count = sig_counts.most_common(1)[0]

    if most_common_count >= _SPIN_REPEAT_THRESHOLD:
        # Find the representative call for reporting
        for tc in reversed(recent):
            if _call_signature(tc["tool"], tc["arguments"]) == most_common_sig:
                return {
                    "reason": "repeated_call",
                    "tool": tc["tool"],
                    "repeat_count": most_common_count,
                    "window": window,
                }

    return None


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


def estimate_token_count(messages: list[dict]) -> int:
    """Estimate token count for a list of chat messages.

    Heuristic: ~4 chars per token for JSON content, plus per-message framing overhead.
    """
    total_chars = 0
    for msg in messages:
        # Message content
        content = msg.get("content", "")
        if content:
            total_chars += len(content)

        # Tool call arguments (assistant messages with tool_calls)
        for tc in msg.get("tool_calls", []):
            fn = tc.get("function", {})
            args = fn.get("arguments", {})
            if isinstance(args, dict):
                total_chars += len(json.dumps(args, default=str))
            elif isinstance(args, str):
                total_chars += len(args)
            # Tool name
            total_chars += len(fn.get("name", ""))

        # Thinking field (some models)
        thinking = msg.get("thinking", "")
        if thinking:
            total_chars += len(thinking)

        # Per-message framing overhead (~20 tokens for role, formatting)
        total_chars += 80

    return total_chars // 4


def prune_messages_for_context(
    messages: list[dict],
    num_ctx: int,
    threshold_pct: float = 0.80,
    preserve_recent_turns: int = 4,
) -> list[dict]:
    """Return a pruned copy of messages to fit within context budget.

    The original messages list is never modified (full history preserved for transcript).

    Algorithm (two phases, applied in order until under budget):
      Phase 1: Replace old tool message content with "[tool result pruned]"
      Phase 2: Drop oldest complete turn groups (assistant + tool results)

    Always preserves: system message (idx 0), initial user message (idx 1),
    and the last `preserve_recent_turns` turn groups.

    A "turn group" = one assistant message + its following tool result messages.
    """
    budget = int(num_ctx * threshold_pct)
    est = estimate_token_count(messages)

    if est <= budget:
        return messages  # No pruning needed, return original

    # Work on a deep copy to avoid mutating the original
    pruned = copy.deepcopy(messages)

    # Identify turn groups: each group starts with an assistant message
    # and includes any following tool messages until the next assistant/user message
    groups = []  # list of (start_idx, end_idx) inclusive
    i = 0
    while i < len(pruned):
        if pruned[i].get("role") == "assistant" and i >= 2:  # skip system[0], user[1]
            start = i
            j = i + 1
            while j < len(pruned) and pruned[j].get("role") == "tool":
                j += 1
            groups.append((start, j - 1))
            i = j
        else:
            i += 1

    if not groups:
        return pruned

    # Determine which groups are protected (recent ones)
    protected_start = max(0, len(groups) - preserve_recent_turns)

    # Phase 1: Prune tool results in old (non-protected) groups
    for gi in range(protected_start):
        start, end = groups[gi]
        for idx in range(start, end + 1):
            if pruned[idx].get("role") == "tool":
                pruned[idx]["content"] = "[tool result pruned]"

    est = estimate_token_count(pruned)
    if est <= budget:
        return pruned

    # Phase 2: Drop oldest complete turn groups (not protected)
    # Build list of indices to remove, starting from oldest
    for gi in range(protected_start):
        start, end = groups[gi]
        # Mark for removal by setting to None
        for idx in range(start, end + 1):
            pruned[idx] = None

        # Check if we're under budget after each group removal
        remaining = [m for m in pruned if m is not None]
        est = estimate_token_count(remaining)
        if est <= budget:
            return remaining

    # Return whatever we have left
    return [m for m in pruned if m is not None]


def run_chat_benchmark(
    model: str,
    system_msg: str,
    user_msg: str,
    tools: list[dict],
    num_ctx: int,
    num_predict: int,
    timeout_total: int,
    num_threads: int | None = None,
    context_management: str = "none",
    temperature: float | None = None,
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
        context_management: "none" (send full history) or "managed" (prune to fit context).
        temperature: Sampling temperature (None = Ollama default).

    Returns:
        Dict with messages, turn_metrics, tool_calls_log, total_turns,
        completed, final_response, context_management, temperature.
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
    empty_retries = 0
    spin_detected = None
    spin_warned = False       # Has Stage A intervention been issued?
    spin_warn_turn = -1       # Turn number when warning was issued
    start_time = time.time()

    options = {"num_ctx": num_ctx, "num_predict": num_predict}
    if num_threads is not None:
        options["num_thread"] = num_threads
    if temperature is not None:
        options["temperature"] = temperature

    for turn in range(max_turns):
        elapsed = time.time() - start_time
        if elapsed >= timeout_total:
            print(f"  Chat timeout after {elapsed:.0f}s ({turn} turns)")
            break

        remaining = timeout_total - elapsed
        turn_start = time.time()

        # Snapshot message size before the API call (proxy for prompt size)
        messages_json_bytes = len(json.dumps(messages, default=str).encode("utf-8"))

        # Apply context management if enabled
        if context_management == "managed":
            api_messages = prune_messages_for_context(messages, num_ctx)
            pruned = api_messages is not messages
            if pruned:
                est_before = estimate_token_count(messages)
                est_after = estimate_token_count(api_messages)
                print(f"  Turn {turn}: context management pruned {len(messages)} -> {len(api_messages)} messages "
                      f"(~{est_before} -> ~{est_after} est. tokens)")
        else:
            api_messages = messages

        try:
            resp = requests.post(
                OLLAMA_CHAT_URL,
                json={
                    "model": model,
                    "messages": api_messages,
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
        prompt_eval_count = data.get("prompt_eval_count", 0)
        eval_count = data.get("eval_count", 0)
        prompt_eval_ns = data.get("prompt_eval_duration", 0)
        eval_ns = data.get("eval_duration", 0)

        prompt_eval_s = prompt_eval_ns / 1e9
        eval_s = eval_ns / 1e9
        prompt_tps = round(prompt_eval_count / prompt_eval_s, 1) if prompt_eval_s > 0 else 0
        eval_tps = round(eval_count / eval_s, 1) if eval_s > 0 else 0
        context_pressure = round(prompt_eval_count / num_ctx * 100, 1) if num_ctx > 0 else 0

        tm = {
            "turn": turn,
            "duration_s": round(turn_duration, 2),
            "prompt_eval_count": prompt_eval_count,
            "eval_count": eval_count,
            "prompt_eval_duration_ns": prompt_eval_ns,
            "eval_duration_ns": eval_ns,
            "prompt_eval_tps": prompt_tps,
            "eval_tps": eval_tps,
            "num_ctx": num_ctx,
            "context_pressure_pct": context_pressure,
            "messages_json_bytes": messages_json_bytes,
            "had_tool_schema": True,
        }

        # Add context management metrics if pruning occurred
        if context_management == "managed":
            was_pruned = api_messages is not messages
            tm["context_management_active"] = True
            tm["messages_before_pruning"] = len(messages)
            tm["messages_after_pruning"] = len(api_messages)
            if was_pruned:
                tm["est_tokens_before"] = estimate_token_count(messages)
                tm["est_tokens_after"] = estimate_token_count(api_messages)

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

            pressure_warn = " \u26a0 NEAR LIMIT" if context_pressure > 90 else ""
            print(f"  Turn {turn}: {len(tool_calls)} tool call(s) in {turn_duration:.1f}s "
                  f"[prompt: {prompt_eval_count}/{num_ctx} tokens ({context_pressure:.1f}%){pressure_warn}, "
                  f"eval: {eval_count} tokens]")
            empty_retries = 0  # reset on successful tool-call turn

            # Spin detection: 2-stage escalation (warn → stop)
            spin = detect_spinning(tool_calls_log)
            if spin:
                if not spin_warned:
                    # Stage A: soft intervention — nudge the model
                    spin_warned = True
                    spin_warn_turn = turn
                    messages.append({
                        "role": "user",
                        "content": (
                            "You appear to be repeating the same tool calls. "
                            "If you've already fetched data for this portfolio, "
                            "proceed to the next step (risk check, report, or "
                            "next portfolio). Do not call the same tool with "
                            "the same arguments again."
                        ),
                    })
                    print(f"  SPIN WARNING: {spin['tool']}() repeated {spin['repeat_count']}x "
                          f"in last {spin['window']} calls — injecting correction")
                elif turn >= spin_warn_turn + 2:
                    # Stage B: hard stop — still spinning after intervention
                    spin["intervention_attempted"] = True
                    spin_detected = spin
                    print(f"  SPIN CONFIRMED: {spin['tool']}() still repeating after "
                          f"intervention — stopping")
                    break

        else:
            # No tool calls -- model is done (or stuck)
            tm["tool_calls"] = 0
            turn_metrics.append(tm)

            content = message.get("content", "")
            thinking = message.get("thinking", "")

            if content:
                messages.append({"role": "assistant", "content": content})
                final_response = content
                completed = True
                empty_retries = 0  # reset on success
                pressure_warn = " \u26a0 NEAR LIMIT" if context_pressure > 90 else ""
                print(f"  Turn {turn}: final response ({len(content)} chars) in {turn_duration:.1f}s "
                      f"[prompt: {prompt_eval_count}/{num_ctx} tokens ({context_pressure:.1f}%){pressure_warn}]")
                break
            elif thinking and empty_retries < 1:
                # Model is reasoning but didn't emit content or tool calls -- nudge it
                empty_retries += 1
                tm["thinking_only_retry"] = True
                messages.append(message)  # preserve the thinking-only message in history
                messages.append({
                    "role": "user",
                    "content": "Continue. You were thinking but didn't make a tool call or provide a response. Please proceed with the next step.",
                })
                print(f"  Turn {turn}: thinking-only response, retrying with nudge")
                continue  # don't break -- try again
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
        "context_management": context_management,
        "temperature": temperature,
        "spin_detected": spin_detected,
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
      - classification: one of success, partial_success, spinning, empty_response,
                        stalled_inference, text_narration, no_tool_support
      - description: human-readable explanation
    """
    tool_calls = chat_result.get("tool_calls_log", [])
    messages = chat_result.get("messages", [])
    completed = chat_result.get("completed", False)
    total_turns = chat_result.get("total_turns", 0)
    spin_detected = chat_result.get("spin_detected")

    num_tool_calls = len(tool_calls)
    tools_used = set(tc["tool"] for tc in tool_calls)

    # Spinning: model made tool calls but got stuck in a loop
    if spin_detected:
        intervened = spin_detected.get("intervention_attempted", False)
        suffix = " despite intervention" if intervened else ""
        desc = (f"Spun out{suffix} after {num_tool_calls} tool calls — "
                f"{spin_detected['tool']}() repeated {spin_detected['repeat_count']}x "
                f"in last {spin_detected['window']} calls")
        return {
            "classification": "spinning",
            "description": desc,
            "spin_details": spin_detected,
        }

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
    num_ctx: int = 0,
    num_predict: int = 0,
    tools: list[dict] | None = None,
    context_management: str = "none",
    temperature: float | None = None,
):
    """Save chat benchmark results to the standard results directory.

    Writes three files:
    - output.md: human-readable transcript
    - metrics.json: standard + chat-specific metrics
    - transcript.json: enriched object with metadata, turn_diagnostics, messages
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

    # 3. transcript.json -- enriched format with metadata, diagnostics, and messages
    tools_json = json.dumps(tools or [], default=str)
    tool_schema_bytes = len(tools_json.encode("utf-8"))
    # Rough token estimate: ~4 chars per token for JSON schema
    estimated_schema_tokens = tool_schema_bytes // 4

    turn_diagnostics = []
    for tm in chat_result.get("turn_metrics", []):
        td = {
            "turn": tm.get("turn"),
            "prompt_eval_count": tm.get("prompt_eval_count", 0),
            "eval_count": tm.get("eval_count", 0),
            "context_pressure_pct": tm.get("context_pressure_pct", 0),
            "messages_json_bytes": tm.get("messages_json_bytes", 0),
            "prompt_eval_tps": tm.get("prompt_eval_tps", 0),
            "eval_tps": tm.get("eval_tps", 0),
            "duration_s": tm.get("duration_s", 0),
            "tool_calls_made": tm.get("tool_calls", 0),
            "had_tool_schema": tm.get("had_tool_schema", True),
        }
        if "error" in tm:
            td["error"] = tm["error"]
        # Include context management fields if present
        if tm.get("context_management_active"):
            td["context_management_active"] = True
            td["messages_before_pruning"] = tm.get("messages_before_pruning", 0)
            td["messages_after_pruning"] = tm.get("messages_after_pruning", 0)
            if "est_tokens_before" in tm:
                td["est_tokens_before"] = tm["est_tokens_before"]
                td["est_tokens_after"] = tm["est_tokens_after"]
        turn_diagnostics.append(td)

    transcript_data = {
        "metadata": {
            "model": model,
            "num_ctx": num_ctx,
            "num_predict": num_predict,
            "temperature": temperature,
            "context_management": context_management,
            "tool_schema": {
                "num_tools": len(tools) if tools else 0,
                "schema_json_bytes": tool_schema_bytes,
                "estimated_tokens": estimated_schema_tokens,
            },
        },
        "turn_diagnostics": turn_diagnostics,
        "messages": chat_result["messages"],
    }

    transcript_path = os.path.join(results_dir, "transcript.json")
    with open(transcript_path, "w", encoding="utf-8") as f:
        json.dump(transcript_data, f, indent=2, default=str)

    print(f"  Saved chat results to {results_dir}")
