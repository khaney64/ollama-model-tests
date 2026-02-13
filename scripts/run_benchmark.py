"""Main orchestrator for running Ollama model benchmarks."""

import argparse
import json
import os
import subprocess
import sys
import time

# Allow running from any directory
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import requests

from config import (
    MODELS,
    MODELS_DIR,
    OLLAMA_BASE_URL,
    OLLAMA_GENERATE_URL,
    OLLAMA_LIST_URL,
    REFACTOR_SOURCE_DIR,
    REQUIREMENTS_DIR,
    TASKS,
    GPU_POLL_INTERVAL,
    get_model_results_dir,
    get_num_ctx,
    get_num_predict,
    model_to_dirname,
    is_cloud_model,
)
from monitor_gpu import GPUMonitor
from datetime import datetime


def check_ollama_running() -> bool:
    """Verify Ollama server is accessible."""
    try:
        resp = requests.get(OLLAMA_BASE_URL, timeout=5)
        return resp.status_code == 200
    except requests.RequestException:
        return False


def is_gpu_available() -> bool:
    """Check if a GPU is available on the system."""
    gpu_info = GPUMonitor.get_gpu_info()
    return gpu_info.get("gpu_name") is not None and gpu_info.get("gpu_name") != "Unknown"


def get_installed_models() -> set[str]:
    """Get set of installed model names."""
    try:
        resp = requests.get(OLLAMA_LIST_URL, timeout=10)
        resp.raise_for_status()
        return {m["name"] for m in resp.json().get("models", [])}
    except requests.RequestException:
        return set()


def pull_model(model: str) -> bool:
    """Pull a model if not already installed."""
    print(f"  Pulling {model}...")
    try:
        resp = requests.post(
            f"{OLLAMA_BASE_URL}/api/pull",
            json={"name": model, "stream": False},
            timeout=3600,
        )
        resp.raise_for_status()
        print(f"  Pulled {model}")
        return True
    except requests.RequestException as e:
        print(f"  FAILED to pull {model}: {e}")
        return False


def unload_model(model: str):
    """Unload a model from VRAM by setting keep_alive to 0."""
    try:
        requests.post(
            OLLAMA_GENERATE_URL,
            json={"model": model, "prompt": "", "keep_alive": 0},
            timeout=30,
        )
    except requests.RequestException:
        pass


def parse_num_threads(value: str | None) -> int | None:
    """Parse num_threads argument (e.g., '16' or '75%') into an integer.

    Caps at 75% of available cores to leave headroom for the system.
    """
    if value is None:
        return None
    available = os.cpu_count() or 1
    max_allowed = int(available * 0.75)

    if value.endswith('%'):
        pct = int(value[:-1])
        requested = max(1, int(available * pct / 100))
    else:
        requested = int(value)

    return min(requested, max_allowed)


def load_prompt(task: str) -> str:
    """Load the prompt for a task, inlining source files for refactor."""
    prompt_path = os.path.join(REQUIREMENTS_DIR, f"{task}.md")
    if not os.path.exists(prompt_path):
        raise FileNotFoundError(f"Prompt file not found: {prompt_path}")

    with open(prompt_path, "r", encoding="utf-8") as f:
        prompt = f.read()

    # For refactor task, inline the C# source files
    if task == "refactor":
        source_files = {
            "{{ORDER_PROCESSOR_SOURCE}}": "OrderProcessor.cs",
            "{{REPORT_GENERATOR_SOURCE}}": "ReportGenerator.cs",
            "{{DATA_HELPER_SOURCE}}": "DataHelper.cs",
        }
        for placeholder, filename in source_files.items():
            filepath = os.path.join(REFACTOR_SOURCE_DIR, filename)
            if os.path.exists(filepath):
                with open(filepath, "r", encoding="utf-8") as f:
                    source = f.read()
                prompt = prompt.replace(placeholder, source)
            else:
                print(f"  Warning: Source file not found: {filepath}")

    return prompt


def run_generation(model: str, prompt: str, num_ctx: int, num_predict: int = 4096, timeout: int = 600, num_threads: int | None = None) -> dict:
    """Call Ollama generate API and return the response with timing data."""
    try:
        options = {
            "num_predict": num_predict,
            "num_ctx": num_ctx,
        }
        if num_threads is not None:
            options["num_thread"] = num_threads

        resp = requests.post(
            OLLAMA_GENERATE_URL,
            json={
                "model": model,
                "prompt": prompt,
                "stream": False,
                "options": options,
            },
            timeout=timeout,
        )
        resp.raise_for_status()
        return resp.json()
    except requests.RequestException as e:
        return {"error": str(e)}


def extract_metrics(response: dict, gpu_summary) -> dict:
    """Extract and compute metrics from the Ollama response and GPU data."""
    if "error" in response:
        return {
            "error": response["error"],
            "gpu": gpu_summary.to_dict(),
        }

    total_duration_ns = response.get("total_duration", 0)
    load_duration_ns = response.get("load_duration", 0)
    prompt_eval_duration_ns = response.get("prompt_eval_duration", 0)
    eval_duration_ns = response.get("eval_duration", 0)
    prompt_eval_count = response.get("prompt_eval_count", 0)
    eval_count = response.get("eval_count", 0)

    # Convert nanoseconds to seconds
    total_duration_s = total_duration_ns / 1e9
    load_duration_s = load_duration_ns / 1e9
    prompt_eval_duration_s = prompt_eval_duration_ns / 1e9
    eval_duration_s = eval_duration_ns / 1e9

    # Tokens per second
    prompt_eval_tps = (prompt_eval_count / prompt_eval_duration_s) if prompt_eval_duration_s > 0 else 0
    eval_tps = (eval_count / eval_duration_s) if eval_duration_s > 0 else 0

    return {
        "model": response.get("model", ""),
        "timing": {
            "total_duration_s": round(total_duration_s, 2),
            "load_duration_s": round(load_duration_s, 2),
            "prompt_eval_duration_s": round(prompt_eval_duration_s, 2),
            "eval_duration_s": round(eval_duration_s, 2),
        },
        "tokens": {
            "prompt_eval_count": prompt_eval_count,
            "eval_count": eval_count,
            "prompt_eval_tokens_per_sec": round(prompt_eval_tps, 2),
            "eval_tokens_per_sec": round(eval_tps, 2),
        },
        "gpu": gpu_summary.to_dict(),
    }


def save_results(model: str, task: str, output_text: str, metrics: dict, mode: str, ctx_size: int = None):
    """Save output and metrics to mode-specific directory."""
    results_dir = get_model_results_dir(model, task, mode=mode, ctx_size=ctx_size)
    os.makedirs(results_dir, exist_ok=True)

    output_path = os.path.join(results_dir, "output.md")
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(output_text)

    metrics_path = os.path.join(results_dir, "metrics.json")
    with open(metrics_path, "w", encoding="utf-8") as f:
        json.dump(metrics, f, indent=2)

    print(f"  Saved results to {results_dir}")


def extract_code_from_markdown(text: str) -> str | None:
    """Extract Python code from markdown code blocks.

    Tries ```python first, then ``` without language specifier.
    Returns the longest code block found, or None.
    """
    import re

    # Try with python specifier first
    pattern = r'```python\n(.*?)```'
    matches = re.findall(pattern, text, re.DOTALL)

    # Fallback to any code block
    if not matches:
        pattern = r'```\n(.*?)```'
        matches = re.findall(pattern, text, re.DOTALL)

    if not matches:
        return None

    # Return the longest block (most likely to be the complete implementation)
    return max(matches, key=len).strip()


def post_process_engine_task(model: str, task: str, mode: str, ctx_size: int | None, results_dir: str):
    """Post-process engine task: extract code, copy historical.csv, execute."""
    print("  Post-processing engine task...")

    # Read output.md
    output_path = os.path.join(results_dir, "output.md")
    if not os.path.exists(output_path):
        print("  Warning: output.md not found, skipping post-processing")
        return

    with open(output_path, "r", encoding="utf-8") as f:
        output_text = f.read()

    # Extract Python code
    code = extract_code_from_markdown(output_text)
    if not code:
        failure_path = os.path.join(results_dir, "failure.md")
        with open(failure_path, "w", encoding="utf-8") as f:
            f.write("# Engine Task Failure\n\n")
            f.write("**Reason:** No Python code block found in output.md\n\n")
            f.write("The model's response did not contain a ```python code block.\n")
        print("  Warning: No code block found in output.md")
        return

    # Save trading_engine.py
    engine_path = os.path.join(results_dir, "trading_engine.py")
    with open(engine_path, "w", encoding="utf-8") as f:
        f.write(code)
    print(f"  Extracted {len(code)} bytes to trading_engine.py")

    # Copy historical.csv
    from config import HISTORICAL_CSV_PATH
    historical_dest = os.path.join(results_dir, "historical.csv")
    if os.path.exists(HISTORICAL_CSV_PATH):
        import shutil
        shutil.copy2(HISTORICAL_CSV_PATH, historical_dest)
        print("  Copied historical.csv")
    else:
        print(f"  Warning: {HISTORICAL_CSV_PATH} not found")
        return

    # Execute trading_engine.py
    print("  Executing trading_engine.py...")
    try:
        result = subprocess.run(
            [sys.executable, "trading_engine.py"],
            cwd=results_dir,
            capture_output=True,
            text=True,
            timeout=30
        )

        if result.returncode != 0:
            # Execution failed
            failure_path = os.path.join(results_dir, "failure.md")
            with open(failure_path, "w", encoding="utf-8") as f:
                f.write("# Engine Task Execution Failure\n\n")
                f.write(f"**Exit Code:** {result.returncode}\n\n")
                f.write("## stderr:\n```\n")
                f.write(result.stderr)
                f.write("\n```\n")
            print(f"  Execution failed with exit code {result.returncode}")
            return

        # Check if output.csv was created
        output_csv_path = os.path.join(results_dir, "output.csv")
        if os.path.exists(output_csv_path):
            print("  Successfully generated output.csv")
        else:
            print("  Warning: output.csv was not created")

    except subprocess.TimeoutExpired:
        failure_path = os.path.join(results_dir, "failure.md")
        with open(failure_path, "w", encoding="utf-8") as f:
            f.write("# Engine Task Execution Failure\n\n")
            f.write("**Reason:** Execution timed out after 30 seconds\n")
        print("  Execution timed out")
    except Exception as e:
        failure_path = os.path.join(results_dir, "failure.md")
        with open(failure_path, "w", encoding="utf-8") as f:
            f.write("# Engine Task Execution Failure\n\n")
            f.write(f"**Error:** {str(e)}\n")
        print(f"  Execution error: {e}")


def run_single_benchmark(model: str, task: str, mode: str, num_ctx_override: int | None = None, num_predict_override: int | None = None, timeout: int = 600, num_threads: int | None = None):
    """Run a single model against a single task."""
    print(f"\n{'='*60}")
    print(f"Model: {model}")
    print(f"Task:  {task}")
    print(f"Mode:  {mode}")
    print(f"{'='*60}")

    # Load prompt
    print("  Loading prompt...")
    prompt = load_prompt(task)
    print(f"  Prompt length: {len(prompt)} chars")

    # Start GPU monitoring
    gpu_monitor = GPUMonitor(poll_interval=GPU_POLL_INTERVAL)
    gpu_monitor.start()

    # Run generation
    num_ctx = num_ctx_override if num_ctx_override is not None else get_num_ctx(model)
    num_predict = num_predict_override if num_predict_override is not None else get_num_predict(model)
    print(f"  Context size: {num_ctx} tokens{' (override)' if num_ctx_override else ''}")
    print(f"  Max output tokens: {num_predict}{' (override)' if num_predict_override else ''}")
    if num_threads is not None:
        print(f"  CPU threads: {num_threads}")
    else:
        print(f"  CPU threads: Ollama default (physical cores)")
    print("  Generating response (this may take several minutes)...")
    start_time = time.time()
    response = run_generation(model, prompt, num_ctx, num_predict, timeout=timeout, num_threads=num_threads)
    elapsed = time.time() - start_time
    print(f"  Generation completed in {elapsed:.1f}s")

    # Stop GPU monitoring
    gpu_summary = gpu_monitor.stop()

    # Extract output text
    output_text = response.get("response", response.get("error", "No response"))

    # Compute metrics
    metrics = extract_metrics(response, gpu_summary)
    metrics["task"] = task
    metrics["wall_clock_s"] = round(elapsed, 2)
    metrics["num_ctx"] = num_ctx
    metrics["num_predict"] = num_predict
    if num_threads is not None:
        metrics["num_threads"] = num_threads

    # Add execution metadata
    metrics["execution_mode"] = mode
    metrics["run_timestamp"] = datetime.now().isoformat()

    # Add hardware metadata
    import platform
    hw_info = {"cpu_logical_cores": os.cpu_count()}
    if mode == "gpu":
        hw_info.update(GPUMonitor.get_gpu_info())
    metrics["hardware"] = hw_info

    # Print summary
    if "error" not in metrics:
        tokens = metrics["tokens"]
        timing = metrics["timing"]
        gpu = metrics["gpu"]
        prompt_tokens = tokens["prompt_eval_count"]
        gen_tokens = tokens["eval_count"]
        total_tokens = prompt_tokens + gen_tokens
        print(f"  Prompt tokens: {prompt_tokens}")
        print(f"  Tokens generated: {gen_tokens}")
        print(f"  Context usage: {total_tokens}/{num_ctx} ({100 * total_tokens / num_ctx:.0f}%)")
        print(f"  Generation speed: {tokens['eval_tokens_per_sec']} tok/s")
        print(f"  Peak VRAM: {gpu['peak_vram_mb']} MB")
        print(f"  Avg GPU Util: {gpu['avg_gpu_utilization_pct']}%")

        # Check for warnings
        warnings = []
        if total_tokens >= num_ctx - 10:
            warnings.append(f"Hit context limit ({num_ctx}). Output likely truncated.")
        elif total_tokens >= num_ctx * 0.9:
            warnings.append(f"Used {100 * total_tokens / num_ctx:.0f}% of context. Output may be truncated.")
        if gen_tokens >= num_predict - 10:
            warnings.append(f"Hit num_predict limit ({num_predict}). Output likely truncated — consider increasing --num-predict.")

        for w in warnings:
            print(f"  *** WARNING: {w}")

        if warnings:
            metrics["warnings"] = warnings
    else:
        print(f"  ERROR: {metrics['error']}")

    # Save results
    ctx_size = num_ctx if mode == "gpu" else None
    save_results(model, task, output_text, metrics, mode=mode, ctx_size=ctx_size)

    # Task-specific post-processing
    if task == "engine":
        results_dir = get_model_results_dir(model, task, mode=mode, ctx_size=ctx_size)
        post_process_engine_task(model, task, mode, ctx_size, results_dir)

    # Unload model to free VRAM
    print("  Unloading model...")
    unload_model(model)
    time.sleep(2)  # Brief pause to let VRAM clear


def main():
    parser = argparse.ArgumentParser(description="Run Ollama model benchmarks")
    parser.add_argument(
        "--models",
        type=str,
        default=None,
        help="Comma-separated list of models to test (default: all)",
    )
    parser.add_argument(
        "--tasks",
        type=str,
        default=None,
        help="Comma-separated list of tasks to run (default: all)",
    )
    parser.add_argument(
        "--skip-pull",
        action="store_true",
        help="Skip pulling models before benchmarking",
    )
    parser.add_argument(
        "--num-ctx",
        type=int,
        default=None,
        help="Override context size (num_ctx) for all models in this run",
    )
    parser.add_argument(
        "--num-predict",
        type=int,
        default=None,
        help="Override max output tokens (num_predict) for all models (default: 4096)",
    )
    parser.add_argument(
        "--timeout",
        type=int,
        default=10,
        help="Timeout in minutes for generation requests (default: 10)",
    )
    parser.add_argument(
        "--num-threads",
        type=str,
        default=None,
        help="CPU threads: absolute number (e.g., '16') or percentage (e.g., '75%%') of logical cores. Capped at 75%% of available. In batch files, use '75%%%%' to escape the percent sign.",
    )
    parser.add_argument(
        "--mode",
        type=str,
        required=True,
        choices=["cloud", "cpu", "gpu"],
        help="Execution mode: cloud (API models), cpu (local CPU-only), gpu (local GPU-accelerated)"
    )
    args = parser.parse_args()

    timeout_seconds = args.timeout * 60
    num_threads = parse_num_threads(args.num_threads)

    # Parse model and task lists
    models = args.models.split(",") if args.models else MODELS
    tasks = args.tasks.split(",") if args.tasks else TASKS

    # Validate tasks
    for task in tasks:
        if task not in TASKS:
            print(f"Error: Unknown task '{task}'. Valid tasks: {TASKS}")
            sys.exit(1)

    # Filter models based on mode (auto-exclude incompatible models)
    original_count = len(models)
    if args.mode == "cloud":
        models = [m for m in models if is_cloud_model(m)]
        excluded = [m for m in MODELS if not is_cloud_model(m)] if not args.models else []
    else:  # cpu or gpu mode
        models = [m for m in models if not is_cloud_model(m)]
        excluded = [m for m in MODELS if is_cloud_model(m)] if not args.models else []

    if len(models) == 0:
        print(f"\nError: No models available for --mode {args.mode}")
        if args.mode == "cloud":
            print("Cloud models must have ':cloud' suffix in their tag.")
            print("Available cloud models: kimi-k2.5:cloud, glm-4.7:cloud, glm-5:cloud, minimax-m2.5:cloud, qwen3-coder-next:cloud")
        else:
            print("Local models cannot have ':cloud' suffix.")
            print(f"Specify models with --models, e.g.: --models qwen3:8b,phi4:14b-q4_K_M")
        sys.exit(1)

    # Report filtered models if auto-filtering occurred
    if not args.models and original_count != len(models):
        filtered_count = original_count - len(models)
        print(f"Auto-filtered {filtered_count} incompatible model(s) for --mode {args.mode}")

    print("Ollama Model Benchmark")
    print("=" * 60)
    print(f"Models: {len(models)}")
    print(f"Tasks:  {len(tasks)}")
    print(f"Total runs: {len(models) * len(tasks)}")

    # Show CPU thread info
    available_threads = os.cpu_count() or 1
    if num_threads is not None:
        if args.num_threads.endswith('%'):
            print(f"CPU threads: {num_threads} ({args.num_threads} of {available_threads} logical cores)")
        else:
            print(f"CPU threads: {num_threads}")
    else:
        print(f"CPU threads: Ollama default ({available_threads} logical cores available)")

    # Check Ollama is running
    if not check_ollama_running():
        print("\nError: Ollama is not running. Start it with 'ollama serve'")
        sys.exit(1)
    print("Ollama server: OK")

    # Check GPU availability and warn about mode mismatches
    gpu_available = is_gpu_available()
    if args.mode == "cpu" and gpu_available:
        print("\n" + "="*60)
        print("WARNING: GPU detected but running in CPU mode")
        print("="*60)
        print("A GPU was detected on this system, but you're running with --mode cpu.")
        print("If you want CPU-only results (ignoring the GPU), make sure Ollama")
        print("was started with GPU disabled:")
        print("")
        print("  Windows (PowerShell):")
        print("    $env:OLLAMA_USE_GPU=\"false\"")
        print("    ollama serve")
        print("")
        print("  Windows (Command Prompt):")
        print("    set OLLAMA_USE_GPU=false")
        print("    ollama serve")
        print("")
        print("If Ollama is using the GPU, your CPU results will actually be GPU results!")
        print("Restart Ollama with OLLAMA_USE_GPU=false to get true CPU-only benchmarks.")
        print("="*60)
        print("")
        response = input("Continue anyway? (y/N): ").strip().lower()
        if response != 'y':
            print("Aborted. Restart Ollama with GPU disabled and try again.")
            sys.exit(0)
    elif args.mode == "gpu" and not gpu_available:
        print("\n" + "="*60)
        print("WARNING: No GPU detected but running in GPU mode")
        print("="*60)
        print("You're running with --mode gpu, but no GPU was detected.")
        print("Your results will be saved to the gpu/ directory but will actually")
        print("be CPU results. Consider using --mode cpu instead for clarity.")
        print("="*60)
        print("")
        response = input("Continue anyway? (y/N): ").strip().lower()
        if response != 'y':
            print("Aborted.")
            sys.exit(0)

    # For GPU mode, suggest context sizes based on CPU results
    if args.mode == "gpu":
        print("\nAnalyzing CPU results for context size recommendations...")
        for model in models:
            for task in tasks:
                cpu_metrics_path = os.path.join(get_model_results_dir(model, task, mode="cpu"), "metrics.json")
                if os.path.exists(cpu_metrics_path):
                    with open(cpu_metrics_path, "r") as f:
                        data = json.load(f)
                        if "tokens" in data:
                            total_tokens = data["tokens"]["prompt_eval_count"] + data["tokens"]["eval_count"]
                            suggested_ctx = max(8192, 2 ** (total_tokens.bit_length()))  # Round up to power of 2
                            print(f"  {model} {task}: used {total_tokens} tokens on CPU, suggest ctx >= {suggested_ctx}")

    # Pull models if needed
    if not args.skip_pull:
        installed = get_installed_models()
        for model in models:
            if model not in installed:
                pull_model(model)

    # Run benchmarks
    total = len(models) * len(tasks)
    current = 0
    for model in models:
        for task in tasks:
            current += 1
            print(f"\n[{current}/{total}]")
            run_single_benchmark(
                model, task, mode=args.mode,
                num_ctx_override=args.num_ctx,
                num_predict_override=args.num_predict,
                timeout=timeout_seconds,
                num_threads=num_threads
            )

    print(f"\n{'='*60}")
    print("All benchmarks complete!")
    print(f"Results saved to: {MODELS_DIR}")
    print("Run 'python scripts/generate_report.py' to build comparison report.")


if __name__ == "__main__":
    main()
