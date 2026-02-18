#!/usr/bin/env python3
"""
Agentic Chat Task Evaluation Script

Evaluates model performance on the agentic-chat task by analyzing
transcript.json (structured tool-calling conversation) and metrics.json.

100% automated -- no manual review needed because tool calls are structured.

Scoring Criteria:
- Valid Tool Calls (20%): Did model produce structured tool_calls with correct JSON?
- Tool Coverage (15%): How many of 8 tools were called? (threshold: 6)
- Call Ordering (15%): Data-dependent calls in correct order per portfolio?
- Argument Correctness (15%): Valid portfolio IDs, symbol lists, risk config values?
- Portfolio Coverage (15%): All 3 portfolios processed?
- Final Response (10%): Useful text summary at the end?
- Error Recovery (10%): Continued processing after any tool errors?

Usage:
    python scripts/evaluate_agentic_chat.py --mode gpu --ctx-size 16384
    python scripts/evaluate_agentic_chat.py --mode cpu
"""

import json
import os
import re
import sys
from datetime import datetime
from pathlib import Path
from typing import Any

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from config import MODELS_DIR, REPORTS_DIR, TASKS, dirname_to_model, get_model_meta

ALL_TOOLS = {
    "get_stock_prices",
    "get_portfolio_holdings",
    "calculate_portfolio_value",
    "calculate_volatility_score",
    "check_risk_threshold",
    "generate_report",
    "send_notification",
    "log_operation",
}

REQUIRED_PORTFOLIOS = {"PORT-001", "PORT-002", "PORT-003"}

# Expected call ordering per portfolio (data dependencies):
# get_portfolio_holdings -> get_stock_prices -> calculate_portfolio_value
# get_portfolio_holdings -> calculate_volatility_score
# calculate_portfolio_value + calculate_volatility_score -> check_risk_threshold
# check_risk_threshold -> generate_report (if high risk)
# generate_report -> send_notification (if high risk)
ORDERING_RULES = [
    ("get_portfolio_holdings", "get_stock_prices"),
    ("get_portfolio_holdings", "calculate_volatility_score"),
    ("get_stock_prices", "calculate_portfolio_value"),
    ("calculate_portfolio_value", "check_risk_threshold"),
    ("calculate_volatility_score", "check_risk_threshold"),
]


class AgenticChatEvaluator:
    def __init__(self, mode: str, ctx_size: int | None = None):
        self.base_dir = Path(__file__).parent.parent
        self.models_dir = self.base_dir / "models"
        self.mode = mode
        self.ctx_size = ctx_size

    def evaluate_model(self, model_dir_name: str, ctx: int | None = None) -> dict:
        """Evaluate a single model's agentic-chat transcript."""
        print(f"\nEvaluating {model_dir_name}...")

        # Build path to results
        result_path = self.models_dir / model_dir_name / "results" / "agentic-chat"
        if self.mode == "gpu" and ctx:
            result_path = result_path / "gpu" / f"ctx-{ctx}"
        else:
            result_path = result_path / self.mode

        transcript_file = result_path / "transcript.json"
        metrics_file = result_path / "metrics.json"

        result = {
            "model": model_dir_name,
            "status": "evaluated",
            "scores": {},
            "issues": [],
            "details": {},
        }

        if not transcript_file.exists():
            result["status"] = "No transcript.json found"
            result["scores"]["total"] = 0
            return result

        try:
            with open(transcript_file, "r", encoding="utf-8") as f:
                messages = json.load(f)
        except (json.JSONDecodeError, OSError) as e:
            result["status"] = f"Failed to read transcript: {e}"
            result["scores"]["total"] = 0
            return result

        metrics = {}
        if metrics_file.exists():
            try:
                with open(metrics_file, "r", encoding="utf-8") as f:
                    metrics = json.load(f)
            except (json.JSONDecodeError, OSError):
                pass

        # Extract tool calls from messages
        tool_calls = self._extract_tool_calls(messages)

        # Classify outcome (prefer saved classification, fallback to recompute)
        classification = self._get_classification(metrics, messages, tool_calls)
        result["classification"] = classification

        # Score each criterion
        result["scores"]["valid_tool_calls"] = self._score_valid_tool_calls(tool_calls, messages, result)
        result["scores"]["tool_coverage"] = self._score_tool_coverage(tool_calls, result)
        result["scores"]["call_ordering"] = self._score_call_ordering(tool_calls, result)
        result["scores"]["argument_correctness"] = self._score_argument_correctness(tool_calls, result)
        result["scores"]["portfolio_coverage"] = self._score_portfolio_coverage(tool_calls, messages, result)
        result["scores"]["final_response"] = self._score_final_response(messages, result)
        result["scores"]["error_recovery"] = self._score_error_recovery(tool_calls, messages, result)

        # Weighted total
        weights = {
            "valid_tool_calls": 0.20,
            "tool_coverage": 0.15,
            "call_ordering": 0.15,
            "argument_correctness": 0.15,
            "portfolio_coverage": 0.15,
            "final_response": 0.10,
            "error_recovery": 0.10,
        }

        total = sum(
            result["scores"][k] * weights[k]
            for k in weights
        )
        result["scores"]["total"] = round(total, 2)
        result["scores"]["letter_grade"] = self._get_letter_grade(total)

        # Include chat metrics summary if available
        if "chat" in metrics:
            result["details"]["chat_metrics"] = metrics["chat"]

        return result

    def _extract_tool_calls(self, messages: list[dict]) -> list[dict]:
        """Extract ordered list of tool calls from the conversation.

        Returns list of {index, name, arguments, result} dicts.
        """
        calls = []
        idx = 0

        for i, msg in enumerate(messages):
            if msg.get("role") == "assistant" and "tool_calls" in msg:
                for tc in msg["tool_calls"]:
                    fn = tc.get("function", {})
                    name = fn.get("name", "")
                    arguments = fn.get("arguments", {})

                    # Find the corresponding tool result
                    # Tool results follow the assistant message, one per tool call
                    result_content = None
                    result_idx = i + 1 + len([c for c in calls if c.get("_msg_idx") == i])
                    for j in range(i + 1, min(i + 20, len(messages))):
                        if messages[j].get("role") == "tool":
                            if result_idx == j:
                                result_content = messages[j].get("content", "")
                                break
                            # If we've gone past tool results, stop
                        elif messages[j].get("role") in ("assistant", "user"):
                            break

                    calls.append({
                        "index": idx,
                        "name": name,
                        "arguments": arguments,
                        "result": result_content,
                        "_msg_idx": i,
                    })
                    idx += 1

        return calls

    def _score_valid_tool_calls(self, tool_calls: list[dict], messages: list[dict], result: dict) -> float:
        """Score: Did the model produce structured tool_calls? (20%, 0-10 scale)"""
        if not tool_calls:
            # Check if the model tried to call tools via text instead of structured calls
            text_tool_refs = 0
            for msg in messages:
                if msg.get("role") == "assistant":
                    content = msg.get("content", "")
                    for tool in ALL_TOOLS:
                        if tool in content:
                            text_tool_refs += 1
            if text_tool_refs > 0:
                result["issues"].append(
                    f"Model referenced {text_tool_refs} tool(s) in text but made 0 structured tool_calls"
                )
            else:
                result["issues"].append("No tool calls made at all")
            return 0.0

        # Check JSON structure validity
        valid_calls = 0
        for tc in tool_calls:
            if tc["name"] and isinstance(tc["arguments"], (dict, str)):
                valid_calls += 1

        score = min(10.0, (valid_calls / max(len(tool_calls), 1)) * 10.0)

        result["details"]["valid_tool_calls"] = {
            "total_calls": len(tool_calls),
            "valid_calls": valid_calls,
        }

        if valid_calls < len(tool_calls):
            result["issues"].append(
                f"{len(tool_calls) - valid_calls} tool calls had invalid structure"
            )

        return round(score, 2)

    def _score_tool_coverage(self, tool_calls: list[dict], result: dict) -> float:
        """Score: How many of 8 tools were called? (15%, 0-10 scale, threshold: 6)"""
        tools_used = set(tc["name"] for tc in tool_calls if tc["name"])
        coverage = len(tools_used & ALL_TOOLS)

        if coverage >= 6:
            score = 10.0
        else:
            score = round(coverage * (10.0 / 6.0), 2)

        result["details"]["tool_coverage"] = {
            "tools_used": sorted(tools_used & ALL_TOOLS),
            "tools_missing": sorted(ALL_TOOLS - tools_used),
            "count": coverage,
        }

        if coverage < 6:
            result["issues"].append(
                f"Only {coverage}/8 tools used (need 6 for full score)"
            )

        return score

    def _score_call_ordering(self, tool_calls: list[dict], result: dict) -> float:
        """Score: Were data-dependent calls in correct order? (15%, 0-10 scale)"""
        if not tool_calls:
            return 0.0

        # Build per-portfolio call sequences
        portfolio_sequences = self._group_calls_by_portfolio(tool_calls)

        violations = []
        total_rules_checked = 0

        for port_id, calls in portfolio_sequences.items():
            call_names = [c["name"] for c in calls]

            for before, after in ORDERING_RULES:
                if before in call_names and after in call_names:
                    total_rules_checked += 1
                    before_idx = call_names.index(before)
                    after_idx = call_names.index(after)
                    if before_idx > after_idx:
                        violations.append(
                            f"{port_id}: {before} called after {after}"
                        )

        if total_rules_checked == 0:
            result["issues"].append("No ordering rules could be checked (too few tool calls)")
            return 0.0

        correct = total_rules_checked - len(violations)
        score = round((correct / total_rules_checked) * 10.0, 2)

        result["details"]["call_ordering"] = {
            "rules_checked": total_rules_checked,
            "violations": violations,
        }

        if violations:
            result["issues"].append(
                f"{len(violations)} ordering violation(s): {'; '.join(violations[:3])}"
            )

        return score

    def _score_argument_correctness(self, tool_calls: list[dict], result: dict) -> float:
        """Score: Were arguments correct? (15%, 0-10 scale)"""
        if not tool_calls:
            return 0.0

        checks = 0
        correct = 0
        issues = []

        for tc in tool_calls:
            name = tc["name"]
            args = tc["arguments"]
            if isinstance(args, str):
                try:
                    args = json.loads(args)
                except json.JSONDecodeError:
                    issues.append(f"{name}: arguments not valid JSON")
                    checks += 1
                    continue

            if name == "get_portfolio_holdings":
                checks += 1
                pid = args.get("portfolio_id", "")
                if pid in REQUIRED_PORTFOLIOS:
                    correct += 1
                else:
                    issues.append(f"get_portfolio_holdings: invalid portfolio_id '{pid}'")

            elif name == "get_stock_prices":
                checks += 1
                symbols = args.get("symbols", [])
                if isinstance(symbols, list) and len(symbols) > 0:
                    correct += 1
                else:
                    issues.append(f"get_stock_prices: invalid symbols {symbols}")

            elif name == "check_risk_threshold":
                checks += 1
                rc = args.get("risk_config", {})
                # Check that risk config has the expected keys
                if isinstance(rc, dict) and "max_volatility" in rc:
                    correct += 1
                else:
                    issues.append(f"check_risk_threshold: missing/invalid risk_config")

            elif name == "calculate_volatility_score":
                checks += 1
                symbols = args.get("symbols", [])
                if isinstance(symbols, list) and len(symbols) > 0:
                    correct += 1
                else:
                    issues.append(f"calculate_volatility_score: invalid symbols")

            elif name == "calculate_portfolio_value":
                checks += 1
                holdings = args.get("holdings", [])
                prices = args.get("current_prices", {})
                if (isinstance(holdings, list) and len(holdings) > 0 and
                        isinstance(prices, dict) and len(prices) > 0):
                    correct += 1
                else:
                    issues.append(f"calculate_portfolio_value: missing holdings or prices")

        if checks == 0:
            return 0.0

        score = round((correct / checks) * 10.0, 2)

        result["details"]["argument_correctness"] = {
            "checks": checks,
            "correct": correct,
            "issues": issues[:5],
        }

        if issues:
            result["issues"].append(f"{len(issues)} argument issue(s)")

        return score

    def _score_portfolio_coverage(self, tool_calls: list[dict], messages: list[dict], result: dict) -> float:
        """Score: Were all 3 portfolios processed? (15%, 0-10 scale)"""
        portfolios_seen = set()

        for tc in tool_calls:
            args = tc["arguments"]
            if isinstance(args, str):
                try:
                    args = json.loads(args)
                except json.JSONDecodeError:
                    continue

            # Check arguments for portfolio IDs
            pid = args.get("portfolio_id", "")
            if pid in REQUIRED_PORTFOLIOS:
                portfolios_seen.add(pid)

            # Also check nested data for portfolio references
            for val in args.values():
                if isinstance(val, str) and val in REQUIRED_PORTFOLIOS:
                    portfolios_seen.add(val)
                elif isinstance(val, dict):
                    for v2 in val.values():
                        if isinstance(v2, str) and v2 in REQUIRED_PORTFOLIOS:
                            portfolios_seen.add(v2)

        # Also scan tool results and assistant text for portfolio IDs
        for msg in messages:
            content = msg.get("content", "")
            if isinstance(content, str):
                for pid in REQUIRED_PORTFOLIOS:
                    if pid in content:
                        portfolios_seen.add(pid)

        coverage = len(portfolios_seen & REQUIRED_PORTFOLIOS)
        score = round((coverage / 3) * 10.0, 2)

        result["details"]["portfolio_coverage"] = {
            "portfolios_processed": sorted(portfolios_seen & REQUIRED_PORTFOLIOS),
            "missing": sorted(REQUIRED_PORTFOLIOS - portfolios_seen),
        }

        if coverage < 3:
            result["issues"].append(
                f"Only {coverage}/3 portfolios processed"
            )

        return score

    def _score_final_response(self, messages: list[dict], result: dict) -> float:
        """Score: Did model produce a useful final text summary? (10%, 0-10 scale)"""
        # Find the last assistant message that has content (not just tool_calls)
        final_text = ""
        for msg in reversed(messages):
            if msg.get("role") == "assistant":
                content = msg.get("content", "")
                if content and "tool_calls" not in msg:
                    final_text = content
                    break

        if not final_text:
            result["issues"].append("No final text response from model")
            return 0.0

        score = 0.0

        # Length check: at least 100 chars for a useful summary
        if len(final_text) >= 100:
            score += 4.0
        elif len(final_text) >= 50:
            score += 2.0

        # Content quality: mentions portfolios or risk
        mentions_portfolios = sum(1 for pid in REQUIRED_PORTFOLIOS if pid in final_text)
        if mentions_portfolios >= 2:
            score += 3.0
        elif mentions_portfolios >= 1:
            score += 1.5

        # Mentions risk-related terms
        risk_terms = ["risk", "volatil", "threshold", "high", "low", "medium", "alert"]
        risk_mentions = sum(1 for term in risk_terms if term.lower() in final_text.lower())
        if risk_mentions >= 3:
            score += 3.0
        elif risk_mentions >= 1:
            score += 1.5

        score = min(10.0, score)

        result["details"]["final_response"] = {
            "length": len(final_text),
            "mentions_portfolios": mentions_portfolios,
            "risk_terms_found": risk_mentions,
        }

        return round(score, 2)

    def _score_error_recovery(self, tool_calls: list[dict], messages: list[dict], result: dict) -> float:
        """Score: Did model continue processing after tool errors? (10%, 0-10 scale)

        If there were no errors, full score (nothing to recover from).
        If there were errors, check that model continued making tool calls after.
        """
        # Find tool calls that returned errors
        error_indices = []
        for tc in tool_calls:
            if tc.get("result"):
                try:
                    r = json.loads(tc["result"]) if isinstance(tc["result"], str) else tc["result"]
                    if isinstance(r, dict) and "error" in r:
                        error_indices.append(tc["index"])
                except (json.JSONDecodeError, TypeError):
                    pass

        if not error_indices:
            # No errors occurred -- full marks (nothing to recover from)
            result["details"]["error_recovery"] = {
                "errors_encountered": 0,
                "note": "No errors to recover from",
            }
            return 10.0

        # Check if model continued after errors
        max_error_idx = max(error_indices)
        calls_after_error = [tc for tc in tool_calls if tc["index"] > max_error_idx]

        if calls_after_error:
            score = 10.0
        else:
            score = 3.0  # Partial credit: at least it didn't crash
            result["issues"].append("Model stopped making tool calls after encountering errors")

        result["details"]["error_recovery"] = {
            "errors_encountered": len(error_indices),
            "calls_after_last_error": len(calls_after_error),
        }

        return score

    def _get_classification(self, metrics: dict, messages: list[dict], tool_calls: list[dict]) -> dict:
        """Get failure classification from metrics.json or recompute from transcript.

        Returns dict with 'classification' and 'description' keys.
        """
        # Prefer saved classification from benchmark run
        saved = metrics.get("chat", {}).get("failure_classification")
        if saved and isinstance(saved, dict) and "classification" in saved:
            return saved

        # Fallback: recompute from available data
        wall_clock = metrics.get("wall_clock_s", 0)
        eval_count = metrics.get("tokens", {}).get("eval_count", 0)
        num_tool_calls = len(tool_calls)

        # Check assistant text for tool name references
        assistant_text = ""
        for msg in messages:
            if msg.get("role") == "assistant":
                content = msg.get("content", "")
                if content:
                    assistant_text += content + "\n"

        has_final_response = bool(assistant_text.strip())
        tool_refs_in_text = sum(1 for t in ALL_TOOLS if t in assistant_text)

        if num_tool_calls > 0:
            tools_used = set(tc["name"] for tc in tool_calls if tc["name"])
            if has_final_response and len(tools_used) >= 4:
                return {"classification": "success",
                        "description": f"Made {num_tool_calls} tool calls using {len(tools_used)} tools"}
            else:
                return {"classification": "partial_success",
                        "description": f"Made {num_tool_calls} tool calls but incomplete"}

        if eval_count == 0:
            if wall_clock < 1.0:
                return {"classification": "empty_response",
                        "description": "No tokens generated, instant return"}
            else:
                return {"classification": "stalled_inference",
                        "description": f"No tokens generated after {wall_clock:.0f}s"}

        if tool_refs_in_text >= 2:
            return {"classification": "text_narration",
                    "description": f"Described {tool_refs_in_text} tools in text but made 0 structured calls"}

        return {"classification": "no_tool_support",
                "description": f"Generated text with no tool references"}

    def _group_calls_by_portfolio(self, tool_calls: list[dict]) -> dict[str, list[dict]]:
        """Group tool calls by portfolio ID for ordering analysis.

        Uses a heuristic: when get_portfolio_holdings is called with a new
        portfolio ID, subsequent calls belong to that portfolio until the next
        get_portfolio_holdings call.
        """
        groups: dict[str, list[dict]] = {}
        current_portfolio = None

        for tc in tool_calls:
            args = tc["arguments"]
            if isinstance(args, str):
                try:
                    args = json.loads(args)
                except json.JSONDecodeError:
                    args = {}

            name = tc["name"]

            # Detect portfolio switches
            if name == "get_portfolio_holdings":
                pid = args.get("portfolio_id", "")
                if pid:
                    current_portfolio = pid

            if current_portfolio:
                if current_portfolio not in groups:
                    groups[current_portfolio] = []
                groups[current_portfolio].append(tc)

        return groups

    def _get_letter_grade(self, score: float) -> str:
        if score >= 9.0:
            return "A"
        elif score >= 8.0:
            return "B"
        elif score >= 7.0:
            return "C"
        elif score >= 6.0:
            return "D"
        return "F"

    def evaluate_all_models(self):
        """Evaluate all models and generate report."""
        print("Evaluating agentic-chat task implementations...")

        # Find models with transcript.json
        model_entries = []  # (dir_name, ctx_or_None)
        for model_dir in sorted(self.models_dir.iterdir()):
            if not model_dir.is_dir():
                continue

            if self.mode == "gpu" and self.ctx_size:
                f = model_dir / "results" / "agentic-chat" / "gpu" / f"ctx-{self.ctx_size}" / "transcript.json"
                if f.exists():
                    model_entries.append((model_dir.name, self.ctx_size))
            elif self.mode == "gpu" and not self.ctx_size:
                gpu_dir = model_dir / "results" / "agentic-chat" / "gpu"
                if gpu_dir.is_dir():
                    for ctx_dir in sorted(gpu_dir.iterdir()):
                        if ctx_dir.is_dir() and ctx_dir.name.startswith("ctx-"):
                            if (ctx_dir / "transcript.json").exists():
                                ctx = ctx_dir.name.replace("ctx-", "")
                                model_entries.append((model_dir.name, ctx))
            else:
                f = model_dir / "results" / "agentic-chat" / self.mode / "transcript.json"
                if f.exists():
                    model_entries.append((model_dir.name, None))

        print(f"Found {len(model_entries)} model(s) to evaluate:")
        for name, ctx in model_entries:
            label = f"{name} (ctx-{ctx})" if ctx else name
            print(f"  - {label}")

        if not model_entries:
            print("No agentic-chat results found. Run benchmarks first.")
            return

        all_results = []
        for dir_name, ctx in model_entries:
            r = self.evaluate_model(dir_name, ctx=ctx)
            if ctx and not self.ctx_size:
                r["model"] = f"{dir_name} (ctx-{ctx})"
            all_results.append(r)

        report_path = self._generate_report(all_results)
        print(f"\nEvaluation complete! Report: {report_path}")

    def _generate_report(self, results: list[dict]) -> Path:
        """Generate the evaluation report card."""
        report_dir = self.base_dir / "reports" / self.mode
        report_dir.mkdir(parents=True, exist_ok=True)
        report_path = report_dir / "report_card_agentic_chat.md"

        results.sort(key=lambda x: x["scores"].get("total", 0), reverse=True)

        with open(report_path, "w", encoding="utf-8") as f:
            f.write("# Agentic Chat Task Report Card\n\n")
            f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            f.write("This task tests models using Ollama's `/api/chat` endpoint with structured\n")
            f.write("tool calling (the same protocol used by OpenClaw and similar applications).\n\n")

            # Grade distribution
            grade_dist: dict[str, int] = {}
            for r in results:
                g = r["scores"].get("letter_grade", "N/A")
                grade_dist[g] = grade_dist.get(g, 0) + 1

            f.write("## Executive Summary\n\n")
            f.write(f"Evaluated **{len(results)}** model(s) on the agentic-chat task.\n\n")
            f.write("**Grade Distribution:**\n")
            for g in ["A", "B", "C", "D", "F", "N/A"]:
                if g in grade_dist:
                    f.write(f"- {g}: {grade_dist[g]} model(s)\n")
            f.write("\n")

            # Failure classification breakdown
            cls_dist: dict[str, list[str]] = {}
            for r in results:
                cls = r.get("classification", {}).get("classification", "unknown")
                if cls not in cls_dist:
                    cls_dist[cls] = []
                cls_dist[cls].append(r["model"])

            cls_labels = {
                "success": "Success (structured tool calls, completed)",
                "partial_success": "Partial Success (tool calls but incomplete)",
                "empty_response": "Empty Response (no tokens, instant return -- model lacks tool-call support)",
                "stalled_inference": "Stalled Inference (loaded model, burned time, 0 tokens -- unparseable output)",
                "text_narration": "Text Narration (described tools in prose, 0 structured calls)",
                "no_tool_support": "No Tool Support (plain text, no tool references)",
                "unknown": "Unknown",
            }

            f.write("**Outcome Classification:**\n")
            for cls_key in ["success", "partial_success", "text_narration",
                            "empty_response", "stalled_inference", "no_tool_support", "unknown"]:
                if cls_key in cls_dist:
                    label = cls_labels.get(cls_key, cls_key)
                    count = len(cls_dist[cls_key])
                    f.write(f"- **{label}**: {count} model(s)\n")
            f.write("\n")

            # Summary table
            f.write("## Summary Rankings\n\n")
            f.write("| Rank | Model | Classification | Grade | Total | Valid Calls | Coverage | Ordering | Args | Portfolios | Response | Recovery | Pass |\n")
            f.write("|------|-------|----------------|-------|-------|-------------|----------|----------|------|------------|----------|----------|------|\n")

            for i, r in enumerate(results, 1):
                s = r["scores"]
                cls = r.get("classification", {}).get("classification", "?")
                passed = "Y" if s.get("total", 0) >= 7.0 else "N"
                f.write(
                    f"| {i} | {r['model']} | {cls} | {s.get('letter_grade', 'N/A')} | "
                    f"{s.get('total', 0):.1f} | "
                    f"{s.get('valid_tool_calls', 0):.1f} | "
                    f"{s.get('tool_coverage', 0):.1f} | "
                    f"{s.get('call_ordering', 0):.1f} | "
                    f"{s.get('argument_correctness', 0):.1f} | "
                    f"{s.get('portfolio_coverage', 0):.1f} | "
                    f"{s.get('final_response', 0):.1f} | "
                    f"{s.get('error_recovery', 0):.1f} | "
                    f"{passed} |\n"
                )

            f.write("\n**Passing Score:** 7.0/10.0\n\n")

            # Scoring weights
            f.write("## Scoring Weights\n\n")
            f.write("| Criterion | Weight | What it checks |\n")
            f.write("|-----------|--------|----------------|\n")
            f.write("| Valid Tool Calls | 20% | Model produced structured tool_calls with valid JSON |\n")
            f.write("| Tool Coverage | 15% | At least 6 of 8 tools used |\n")
            f.write("| Call Ordering | 15% | Data-dependent calls in correct order per portfolio |\n")
            f.write("| Argument Correctness | 15% | Valid portfolio IDs, symbol lists, risk config |\n")
            f.write("| Portfolio Coverage | 15% | All 3 portfolios processed |\n")
            f.write("| Final Response | 10% | Useful text summary at the end |\n")
            f.write("| Error Recovery | 10% | Continued after tool errors |\n\n")

            # Detailed results
            f.write("## Detailed Results\n\n")

            for r in results:
                f.write(f"### {r['model']}\n\n")
                s = r["scores"]
                cls_info = r.get("classification", {})
                cls_name = cls_info.get("classification", "?")
                cls_desc = cls_info.get("description", "")
                f.write(f"**Grade: {s.get('letter_grade', 'N/A')} ({s.get('total', 0):.1f}/10.0)** | **Classification: {cls_name}**\n\n")
                if cls_desc:
                    f.write(f"> {cls_desc}\n\n")

                if r["status"] != "evaluated":
                    f.write(f"**Status:** {r['status']}\n\n")
                    continue

                f.write("| Criterion | Score |\n")
                f.write("|-----------|-------|\n")
                for criterion in ["valid_tool_calls", "tool_coverage", "call_ordering",
                                  "argument_correctness", "portfolio_coverage",
                                  "final_response", "error_recovery"]:
                    label = criterion.replace("_", " ").title()
                    f.write(f"| {label} | {s.get(criterion, 0):.1f}/10 |\n")
                f.write("\n")

                # Details
                details = r.get("details", {})

                if "tool_coverage" in details:
                    tc = details["tool_coverage"]
                    f.write(f"**Tools used ({tc['count']}/8):** {', '.join(tc['tools_used']) or 'none'}\n\n")
                    if tc["tools_missing"]:
                        f.write(f"**Missing:** {', '.join(tc['tools_missing'])}\n\n")

                if "portfolio_coverage" in details:
                    pc = details["portfolio_coverage"]
                    f.write(f"**Portfolios:** {', '.join(pc['portfolios_processed']) or 'none'}\n\n")

                if "call_ordering" in details:
                    co = details["call_ordering"]
                    if co["violations"]:
                        f.write(f"**Ordering violations:** {'; '.join(co['violations'])}\n\n")

                if "chat_metrics" in details:
                    cm = details["chat_metrics"]
                    f.write(f"**Turns:** {cm.get('total_turns', '?')} | "
                            f"**Tool calls:** {cm.get('total_tool_calls', '?')} | "
                            f"**Success rate:** {cm.get('tool_call_success_rate', 0)*100:.0f}%\n\n")

                if r["issues"]:
                    f.write("**Issues:**\n")
                    for issue in r["issues"]:
                        f.write(f"- {issue}\n")
                    f.write("\n")

            f.write("---\n\n")
            f.write("*Report generated by evaluate_agentic_chat.py*\n")

        return report_path


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Evaluate agentic-chat task implementations")
    parser.add_argument("--mode", type=str, required=True, choices=["cloud", "cpu", "gpu"],
                        help="Execution mode")
    parser.add_argument("--ctx-size", type=int, default=None,
                        help="Context size for GPU mode (e.g., 16384)")

    args = parser.parse_args()
    evaluator = AgenticChatEvaluator(mode=args.mode, ctx_size=args.ctx_size)
    evaluator.evaluate_all_models()
