# Ollama Model Benchmark Suite

Systematic benchmarking of local LLMs via [Ollama](https://ollama.com) against real coding tasks. Measures generation speed, VRAM usage, GPU utilization, and output quality across multiple models and tasks.

Originally built around an **RTX 4070 12GB**, but the framework is hardware-agnostic: it runs on CPU-only machines, any NVIDIA GPU, or cloud model endpoints. The default model list and context sizes are tuned for 12GB VRAM — see [Customizing Models](#customizing-models) to adapt them for your hardware.

> **TL;DR** — Already ran the benchmarks? See [Model Recommendations](reports/recommendations.md) for the final picks (spoiler: qwen3 family dominates).

## Quick Start

```bash
# Install dependencies
pip install -r scripts/requirements.txt

# Pull recommended models
python scripts/pull_models.py

# Run CPU benchmarks (--mode is REQUIRED)
python scripts/run_benchmark.py --mode cpu --models qwen3:8b --tasks agentic --skip-pull

# Run GPU benchmarks (when GPU is available)
python scripts/run_benchmark.py --mode gpu --models qwen3:8b --tasks agentic --num-ctx 16384

# Run cloud model benchmarks
python scripts/run_benchmark.py --mode cloud --models glm-4.7:cloud --tasks api --skip-pull

# CPU-only? Increase the timeout (default: 10 minutes)
python scripts/run_benchmark.py --mode cpu --timeout 30 --skip-pull

# Control CPU thread usage (default: Ollama decides)
python scripts/run_benchmark.py --mode cpu --num-threads 75% --skip-pull

# Generate comparison report (specify mode)
python scripts/generate_report.py --mode cpu
python scripts/generate_report.py --mode gpu
python scripts/generate_report.py --mode cloud
```

## Tasks

Each task is a self-contained coding prompt designed to test different aspects of model capability.

| Task | Prompt | Description |
|------|--------|-------------|
| greenfield | [greenfield.md](requirements/greenfield.md) | Full-stack TaskFlow app (React + C# API) |
| refactor | [refactor.md](requirements/refactor.md) | Refactor 3 C# files with code smells |
| engine | [engine.md](requirements/engine.md) | Business logic implementation from specification (internal task) |
| api | [api.md](requirements/api.md) | Weather Station API with FastAPI + pytest tests |
| agentic | [agentic.md](requirements/agentic.md) | Portfolio risk analysis agent with tool orchestration |

Tasks range from ~1,000 to ~19,000 output tokens, testing whether models can produce complete answers within their context limits.

## Models

20 models across 4 tiers (15 local + 5 cloud), categorized by VRAM fit on a 12GB GPU. The source of truth for all model configuration is [`scripts/config.py`](scripts/config.py). See [Customizing Models](#customizing-models) to add your own.

| Tier | VRAM Fit | Models |
|------|----------|--------|
| 1 | Comfortable (<10 GB) | qwen3:8b, qwen2.5-coder:7b-instruct-q5_K_M, gemma2:9b-instruct-q4_K_M, gemma3:12b-it-q4_K_M, mistral:7b-instruct-v0.3-q5_K_M, phi4:14b-q4_K_M, llama3.1:8b-instruct-q4_K_M, llama3.2:latest |
| 2 | Tight (9-11 GB) | qwen3:14b, qwen2.5-coder:14b-instruct-q4_K_M, deepseek-coder-v2:16b |
| 3 | Partial offload (>12 GB) | glm-4.7-flash:q4_K_M, hf.co/unsloth/gpt-oss-20b-GGUF:Q4_K_M, hf.co/unsloth/gpt-oss-20b-GGUF:Q5_K_M |
| 4 | Cloud API | kimi-k2.5:cloud, glm-4.7:cloud, glm-5:cloud, minimax-m2.5:cloud, qwen3-coder-next:cloud |

## Project Structure

```
scripts/
  run_benchmark.py         # Main orchestrator
  generate_report.py       # Build comparison tables from results
  evaluate_engine_code.py  # Evaluate engine task implementations
  evaluate_agentic_code.py # Evaluate agentic task implementations
  config.py                # Models, tasks, context sizes, model metadata
  monitor_gpu.py           # GPU/VRAM monitoring during generation
  pull_models.py           # Pull models from Ollama registry
requirements/              # Task prompt files (.md)
refactor-source/           # C# source files inlined into refactor task
models/                    # Results per model per task per mode
  {model}/results/{task}/{mode}/
    metrics.json           # Timing, tokens, GPU stats
    output.md              # Model's generated response
  {model}/results/{task}/gpu/ctx-{size}/  # GPU mode: multiple context sizes
reports/                   # Generated comparison reports
  cpu/                     # CPU mode reports
  gpu/                     # GPU mode reports
  cloud/                   # Cloud mode reports
```

## CLI Options

### run_benchmark.py

| Flag | Description |
|------|-------------|
| `--mode` | **REQUIRED**: `cpu`, `gpu`, or `cloud` — execution mode |
| `--models` | Comma-separated list of models (default: all in config) |
| `--tasks` | Comma-separated list of tasks (default: all) |
| `--skip-pull` | Skip pulling models before benchmarking |
| `--num-ctx` | Override context window size for all models |
| `--num-predict` | Override max output tokens (default: matches num_ctx) |
| `--timeout` | Timeout per generation in minutes (default: 10) |
| `--num-threads` | CPU threads: number (e.g., `16`) or percentage (e.g., `75%`) of logical cores (capped at 75%). Use `%%` in batch files. |

**Mode Validation**: Cloud models (tier 4) only run in `--mode cloud`. Local models (tier 1-3) only run in `--mode cpu` or `--mode gpu`.

### generate_report.py

| Flag | Description |
|------|-------------|
| `--mode` | **REQUIRED**: `cpu`, `gpu`, or `cloud` — which results to report on |

### Evaluation scripts

Both `evaluate_engine_code.py` and `evaluate_agentic_code.py`:

| Flag | Description |
|------|-------------|
| `--mode` | **REQUIRED**: `cpu`, `gpu`, or `cloud` |
| `--ctx-size` | Optional: For GPU mode, specify context size (e.g., `8192`) |

## Customizing Models

All model configuration lives in [`scripts/config.py`](scripts/config.py). To add a new model, edit these four places:

### 1. `MODELS` list (~line 32)

Add the Ollama model tag string:

```python
MODELS = [
    # ...existing models...
    "your-model:7b-q4_K_M",
]
```

### 2. `MODELS_TO_PULL` list (~line 60)

If the model needs to be downloaded from the Ollama registry, add it here too. Skip this for models you've already pulled or for cloud models.

### 3. `MODEL_NUM_CTX` dict (~line 75)

Set the context window size. Use the tier guidelines based on your GPU's VRAM:

| Tier | VRAM Fit | Suggested num_ctx |
|------|----------|-------------------|
| 1 | Comfortable (<10 GB) | 8192 |
| 2 | Tight (9-11 GB) | 4096 |
| 3 | Partial offload (>12 GB) | 4096 |
| 4 | Cloud API | 32768 |

### 4. `MODEL_META` dict (~line 129)

Set the `(tier, size_gb)` tuple so reports sort correctly:

```python
MODEL_META = {
    # ...existing models...
    "your-model:7b-q4_K_M": (1, 4.5),
}
```

### Adjusting for Different Hardware

- **More VRAM** (e.g., 24 GB): Use lower quantization tiers and/or higher `num_ctx` values. Tier 2-3 models become comfortable fits.
- **Less VRAM** (e.g., 8 GB): Stick to Tier 1 models with smaller quantizations, or reduce `num_ctx`.
- **CPU-only**: All local models work. Increase `--timeout` for 14B+ models (they run at ~6 tok/s on CPU and can exceed the 10-minute default).

## Results

Each benchmark run produces mode-specific results:

```
models/{model}/results/{task}/{mode}/
  output.md       # Model's generated response
  metrics.json    # Timing, tokens/sec, VRAM, GPU stats, warnings
```

For GPU mode, results are organized by context size:
```
models/{model}/results/{task}/gpu/ctx-8192/
models/{model}/results/{task}/gpu/ctx-16384/
```

Run `python scripts/generate_report.py --mode cpu` to build a comparison report with speed, VRAM, timing tables, and a warnings/errors summary. Reports are saved to `reports/{mode}/`.

## Execution Modes

The framework supports three execution modes to organize results by environment:

- **`cpu`**: Local models running CPU-only (baseline results)
- **`gpu`**: Local models with GPU acceleration (with context size experimentation)
- **`cloud`**: Cloud API models

GPU mode **automatically suggests context sizes** based on CPU baseline token usage.

### Running CPU-Only Mode With a GPU Installed

After installing a GPU, Ollama will automatically use it. To get true CPU-only benchmarks, disable GPU usage before starting Ollama:

**Windows PowerShell:**
```powershell
$env:OLLAMA_USE_GPU="false"
ollama serve
```

**Windows Command Prompt:**
```cmd
set OLLAMA_USE_GPU=false
ollama serve
```

The benchmark script will warn you if a GPU is detected while running `--mode cpu`, or if no GPU is detected while running `--mode gpu`.

See [EXECUTION_MODES.md](EXECUTION_MODES.md) for detailed guide on controlling GPU usage and mode validation.

## Documentation

- [EXECUTION_MODES.md](EXECUTION_MODES.md) — Execution mode guide: CPU/GPU/cloud workflows
