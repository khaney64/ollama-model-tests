# Execution Mode Support

This framework now supports three execution modes to organize benchmark results by execution environment:

## Modes

- **`cpu`**: Local models running on CPU-only (existing CPU baseline results)
- **`gpu`**: Local models running with GPU acceleration
- **`cloud`**: Cloud API models (e.g., glm-4.7:cloud, kimi-k2.5:cloud)

## Directory Structure

Results are now organized by mode:

```
models/{model}/results/{task}/{mode}/
```

For GPU mode with multiple context sizes:

```
models/{model}/results/{task}/gpu/ctx-{size}/
```

### Examples

```
models/qwen3(8b)/results/agentic/cpu/metrics.json
models/qwen3(8b)/results/agentic/gpu/ctx-8192/metrics.json
models/qwen3(8b)/results/agentic/gpu/ctx-16384/metrics.json
models/glm-4.7(cloud)/results/agentic/cloud/metrics.json
```

## Running Benchmarks

The `--mode` flag is now **required**:

```bash
# CPU mode (existing baseline)
python scripts/run_benchmark.py --mode cpu --models qwen3:8b --tasks agentic

# GPU mode (multiple contexts)
python scripts/run_benchmark.py --mode gpu --models qwen3:8b --tasks agentic --num-ctx 8192
python scripts/run_benchmark.py --mode gpu --models qwen3:8b --tasks agentic --num-ctx 16384

# Cloud mode
python scripts/run_benchmark.py --mode cloud --models glm-4.7:cloud --tasks agentic
```

### Model-Mode Validation

The framework validates that models are run in the correct mode:

- Cloud models (tier 4) **only** in `--mode cloud`
- Local models (tier 1-3) **only** in `--mode cpu` or `--mode gpu`

Attempting to run a model in the wrong mode will produce an error.

## GPU Context Size Suggestions

When running `--mode gpu`, the framework analyzes existing CPU results and suggests appropriate context sizes:

```
Analyzing CPU results for context size recommendations...
  qwen3:8b agentic: used 15234 tokens on CPU, suggest ctx >= 16384
```

This helps optimize GPU VRAM usage by setting context sizes based on actual token usage.

## Generating Reports

Reports are generated per-mode and saved to `reports/{mode}/`:

```bash
# CPU mode report
python scripts/generate_report.py --mode cpu
# Output: reports/cpu/latest.md

# GPU mode report (shows all context sizes as separate columns)
python scripts/generate_report.py --mode gpu
# Output: reports/gpu/latest.md

# Cloud mode report
python scripts/generate_report.py --mode cloud
# Output: reports/cloud/latest.md
```

GPU reports display context sizes as separate columns for easy comparison:

```
| Model | agentic (ctx-8192) | agentic (ctx-16384) | agentic (ctx-32768) |
```

## Evaluating Results

Evaluation scripts also require `--mode`:

```bash
# Evaluate CPU results
python scripts/evaluate_engine_code.py --mode cpu
python scripts/evaluate_agentic_code.py --mode cpu

# Evaluate GPU results for specific context size
python scripts/evaluate_engine_code.py --mode gpu --ctx-size 8192
python scripts/evaluate_agentic_code.py --mode gpu --ctx-size 16384

# Evaluate cloud results
python scripts/evaluate_engine_code.py --mode cloud
python scripts/evaluate_agentic_code.py --mode cloud
```

## Batch Files

Updated batch files now use the `--mode` flag:

- `cloud.bat`: Runs cloud models with `--mode cloud`
- `rerun.bat`: Runs local models with `--mode cpu`
- `gpu-test.bat`: Example GPU benchmark with multiple context sizes

## Migration

Existing results were automatically migrated to mode-specific subdirectories:

- Local model results → `{task}/cpu/`
- Cloud model results → `{task}/cloud/`

The migration preserved all metrics and added `execution_mode` and `run_timestamp` fields retroactively.

## New Metrics Fields

All metrics.json files now include:

```json
{
  "execution_mode": "gpu",
  "run_timestamp": "2026-02-12T14:30:00",
  "hardware": {
    "gpu_name": "NVIDIA GeForce RTX 4070",
    "gpu_vram_total_mb": 12288,
    "cpu_logical_cores": 24
  }
}
```

Hardware metadata is captured for GPU mode runs (when GPU is available).

## Controlling GPU Usage

### Running CPU-Only Benchmarks After Installing a GPU

Once you install a GPU, Ollama will automatically detect and use it. To run true CPU-only benchmarks for comparison, you must disable GPU usage in Ollama using environment variables.

**IMPORTANT:** You must restart the Ollama service after setting these variables for them to take effect.

### Method 1: OLLAMA_USE_GPU (Recommended)

Set the `OLLAMA_USE_GPU` environment variable to `false` before starting Ollama:

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

### Method 2: CUDA_VISIBLE_DEVICES (NVIDIA Alternative)

For NVIDIA GPUs, you can hide the GPU from CUDA applications:

**Windows PowerShell:**
```powershell
$env:CUDA_VISIBLE_DEVICES="-1"
ollama serve
```

**Windows Command Prompt:**
```cmd
set CUDA_VISIBLE_DEVICES=-1
ollama serve
```

**Note:** Some users report issues with this method where Ollama still tries to access GPU libraries. The `OLLAMA_USE_GPU=false` method is more reliable.

### Verification

The benchmark script will detect if a GPU is available and warn you if there's a mismatch:

- **`--mode cpu` with GPU detected**: Warns you to disable GPU in Ollama with `OLLAMA_USE_GPU=false`
- **`--mode gpu` with no GPU detected**: Warns that GPU mode results will actually be CPU results

This ensures your CPU and GPU benchmarks are truly measuring different execution environments.

## Benefits

1. **Non-destructive**: GPU runs don't overwrite CPU baseline data
2. **Context experimentation**: Test multiple GPU context sizes side-by-side
3. **Clear separation**: CPU, GPU, and cloud results are clearly distinguished
4. **Informed decisions**: CPU token counts guide GPU context size selection
5. **Traceable**: Execution environment and timestamp recorded for every run
6. **Mode validation**: Warnings prevent accidentally mixing CPU and GPU results
