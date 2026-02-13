"""Generate comparison report from benchmark results."""

import argparse
import json
import os
import sys
from datetime import datetime

# Allow running from any directory
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from config import MODELS_DIR, REPORTS_DIR, TASKS, model_to_dirname, dirname_to_model, get_model_meta


TIER_LABELS = {1: "Tier 1", 2: "Tier 2", 3: "Tier 3", 4: "Cloud", 99: "Unknown"}


def sort_models(models: list) -> list:
    """Sort models by tier ascending, then size descending within each tier."""
    return sorted(models, key=lambda m: (get_model_meta(m)[0], -get_model_meta(m)[1]))


def collect_results(mode: str) -> dict:
    """Scan models directory and collect metrics for specified mode."""
    results = {}  # {model: {task|ctx-size: metrics}}

    if not os.path.exists(MODELS_DIR):
        return results

    for model_dir in os.listdir(MODELS_DIR):
        model_path = os.path.join(MODELS_DIR, model_dir)
        if not os.path.isdir(model_path):
            continue

        model_name = dirname_to_model(model_dir)
        task_results = {}

        for task in TASKS:
            if mode == "gpu":
                # For GPU, collect all ctx-* subfolders
                gpu_dir = os.path.join(model_path, "results", task, "gpu")
                if os.path.isdir(gpu_dir):
                    ctx_dirs = sorted([d for d in os.listdir(gpu_dir) if d.startswith("ctx-")])
                    for ctx_dir in ctx_dirs:
                        metrics_path = os.path.join(gpu_dir, ctx_dir, "metrics.json")
                        if os.path.exists(metrics_path):
                            with open(metrics_path, "r", encoding="utf-8") as f:
                                # Use composite key: "task|ctx-size"
                                task_results[f"{task}|{ctx_dir}"] = json.load(f)
            else:
                # CPU and cloud modes: flat structure
                metrics_path = os.path.join(model_path, "results", task, mode, "metrics.json")
                if os.path.exists(metrics_path):
                    with open(metrics_path, "r", encoding="utf-8") as f:
                        task_results[task] = json.load(f)

        # Only include models that have at least one result
        if task_results:
            results[model_name] = task_results

    return results


def build_speed_table(results: dict, mode: str) -> str:
    """Build a markdown table of generation speed (tokens/sec) per model per task."""
    lines = ["## Generation Speed (tokens/sec)", ""]

    # Collect all task keys (may include ctx-size for GPU mode)
    task_keys = set()
    for model_data in results.values():
        task_keys.update(model_data.keys())
    task_keys = sorted(task_keys)

    # Build header
    header = "| Model |"
    separator = "|-------|"
    for task_key in task_keys:
        # Format column header
        if "|" in task_key:
            task, ctx = task_key.split("|")
            col_name = f"{task} ({ctx})"
        else:
            col_name = task_key
        header += f" {col_name} |"
        separator += "--------|"
    lines.append(header)
    lines.append(separator)

    for model in sort_models(results.keys()):
        row = f"| `{model}` |"
        for task_key in task_keys:
            metrics = results[model].get(task_key)
            if metrics and "tokens" in metrics:
                tps = metrics["tokens"].get("eval_tokens_per_sec", "-")
                row += f" {tps} |"
            else:
                row += " - |"
        lines.append(row)

    return "\n".join(lines)


def build_vram_table(results: dict, mode: str) -> str:
    """Build a markdown table of peak VRAM usage per model per task, with model size."""
    lines = ["## Peak VRAM Usage (MB)", ""]

    # Collect all task keys
    task_keys = set()
    for model_data in results.values():
        task_keys.update(model_data.keys())
    task_keys = sorted(task_keys)

    header = "| Model | Size (GB) |"
    separator = "|-------|-----------|"
    for task_key in task_keys:
        if "|" in task_key:
            task, ctx = task_key.split("|")
            col_name = f"{task} ({ctx})"
        else:
            col_name = task_key
        header += f" {col_name} |"
        separator += "--------|"
    lines.append(header)
    lines.append(separator)

    for model in sort_models(results.keys()):
        tier, size_gb = get_model_meta(model)
        size_str = f"{size_gb}" if size_gb > 0 else "cloud"
        row = f"| `{model}` | {size_str} |"
        for task_key in task_keys:
            metrics = results[model].get(task_key)
            if metrics and "gpu" in metrics:
                vram = metrics["gpu"].get("peak_vram_mb", "-")
                row += f" {vram} |"
            else:
                row += " - |"
        lines.append(row)

    return "\n".join(lines)


def build_timing_table(results: dict, mode: str) -> str:
    """Build a markdown table of total generation time per model per task."""
    lines = ["## Total Generation Time (seconds)", ""]

    # Collect all task keys
    task_keys = set()
    for model_data in results.values():
        task_keys.update(model_data.keys())
    task_keys = sorted(task_keys)

    header = "| Model |"
    separator = "|-------|"
    for task_key in task_keys:
        if "|" in task_key:
            task, ctx = task_key.split("|")
            col_name = f"{task} ({ctx})"
        else:
            col_name = task_key
        header += f" {col_name} |"
        separator += "--------|"
    lines.append(header)
    lines.append(separator)

    for model in sort_models(results.keys()):
        row = f"| `{model}` |"
        for task_key in task_keys:
            metrics = results[model].get(task_key)
            if metrics and "timing" in metrics:
                total = metrics["timing"].get("total_duration_s", "-")
                row += f" {total} |"
            elif metrics and "wall_clock_s" in metrics:
                row += f" {metrics['wall_clock_s']} |"
            else:
                row += " - |"
        lines.append(row)

    return "\n".join(lines)


def build_quality_table(results: dict, mode: str) -> str:
    """Build a placeholder quality scoring table for manual evaluation."""
    lines = ["## Quality Scores (Manual Evaluation)", ""]
    lines.append("*Score each criterion 1-10. Fill in after reviewing outputs.*")
    lines.append("")

    # Collect all task keys
    task_keys = set()
    for model_data in results.values():
        task_keys.update(model_data.keys())
    task_keys = sorted(task_keys)

    for task_key in task_keys:
        if "|" in task_key:
            task, ctx = task_key.split("|")
            title = f"{task.title()} ({ctx})"
        else:
            title = task_key.title()
        lines.append(f"### {title}")
        lines.append("")
        lines.append("| Model | Completeness | Correctness | Code Quality | Overall |")
        lines.append("|-------|-------------|-------------|--------------|---------|")
        for model in sort_models(results.keys()):
            if task_key in results[model]:
                lines.append(f"| `{model}` | /10 | /10 | /10 | /10 |")
        lines.append("")

    return "\n".join(lines)


def build_warnings_table(results: dict, mode: str) -> str:
    """Build a markdown table of warnings and errors per model per task."""
    # Collect all entries that have warnings or errors
    entries = []
    for model in sort_models(results.keys()):
        for task_key, metrics in results[model].items():
            if not metrics:
                continue
            # Extract task name from composite key
            if "|" in task_key:
                task, ctx = task_key.split("|")
                task_display = f"{task} ({ctx})"
            else:
                task_display = task_key
            num_ctx = metrics.get("num_ctx", "-")
            num_predict = metrics.get("num_predict", "-")
            num_threads = metrics.get("num_threads", "-")
            error = metrics.get("error")
            warnings = metrics.get("warnings", [])
            if error:
                entries.append((model, task_display, num_ctx, num_predict, num_threads, "ERROR", error))
            for w in warnings:
                entries.append((model, task_display, num_ctx, num_predict, num_threads, "WARNING", w))

    if not entries:
        return ""

    lines = ["## Warnings & Errors", ""]
    lines.append("| Model | Task | num_ctx | num_predict | num_threads | Severity | Detail |")
    lines.append("|-------|------|---------|-------------|-------------|----------|--------|")
    for model, task, num_ctx, num_predict, num_threads, severity, detail in entries:
        lines.append(f"| `{model}` | {task} | {num_ctx} | {num_predict} | {num_threads} | {severity} | {detail} |")

    return "\n".join(lines)


def build_rankings(results: dict, mode: str) -> str:
    """Build rankings by generation speed across all tasks."""
    lines = ["## Rankings by Generation Speed", ""]

    # Collect all task keys
    task_keys = set()
    for model_data in results.values():
        task_keys.update(model_data.keys())
    task_keys = sorted(task_keys)

    for task_key in task_keys:
        speeds = []
        for model, tasks_data in results.items():
            if task_key in tasks_data:
                metrics = tasks_data[task_key]
                if "tokens" in metrics:
                    tps = metrics["tokens"].get("eval_tokens_per_sec", 0)
                    if tps > 0:
                        speeds.append((model, tps))

        if speeds:
            speeds.sort(key=lambda x: x[1], reverse=True)
            if "|" in task_key:
                task, ctx = task_key.split("|")
                title = f"{task.title()} ({ctx})"
            else:
                title = task_key.title()
            lines.append(f"### {title}")
            lines.append("")
            for rank, (model, tps) in enumerate(speeds, 1):
                lines.append(f"{rank}. `{model}` - {tps} tok/s")
            lines.append("")

    return "\n".join(lines)


def generate_report(mode: str):
    """Generate the full comparison report for specified mode."""
    results = collect_results(mode)

    if not results:
        print(f"No results found for mode '{mode}'. Run benchmarks first.")
        return

    models_with_data = sum(1 for m in results if results[m])
    print(f"Found results for {models_with_data} models in '{mode}' mode")

    # Build report sections
    report_parts = [
        f"# Ollama Model Benchmark Report ({mode.upper()} Mode)",
        f"",
        f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        f"",
        f"Execution mode: {mode}",
        f"Models tested: {models_with_data}",
        f"Tasks: {', '.join(TASKS)}",
        f"",
        f"---",
        f"",
        build_warnings_table(results, mode),
        "",
        build_speed_table(results, mode),
        "",
        build_vram_table(results, mode),
        "",
        build_timing_table(results, mode),
        "",
        build_rankings(results, mode),
        "",
        build_quality_table(results, mode),
    ]

    report = "\n".join(report_parts)

    # Save report
    report_dir = os.path.join(REPORTS_DIR, mode)
    os.makedirs(report_dir, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    timestamped_path = os.path.join(report_dir, f"comparison_{timestamp}.md")

    with open(timestamped_path, "w", encoding="utf-8") as f:
        f.write(report)

    # Also save as latest
    latest_path = os.path.join(report_dir, "latest.md")
    with open(latest_path, "w", encoding="utf-8") as f:
        f.write(report)

    print(f"Report saved to: {timestamped_path}")
    print(f"Latest report:   {latest_path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate benchmark comparison report")
    parser.add_argument("--mode", type=str, required=True, choices=["cloud", "cpu", "gpu"],
                       help="Execution mode to generate report for")
    args = parser.parse_args()
    generate_report(args.mode)
