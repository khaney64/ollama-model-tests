# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What This Is

A benchmarking framework for evaluating local LLMs via Ollama against real coding tasks. Measures generation speed, VRAM usage, GPU utilization, and output quality. Target hardware: RTX 4070 12GB, but hardware-agnostic.

## Commands

All commands run from project root. `--mode` (cpu/gpu/cloud) is **required** for every script.

```bash
# Install
pip install -r scripts/requirements.txt

# Run benchmarks
python scripts/run_benchmark.py --mode gpu --models qwen3:8b --tasks agentic --num-ctx 8192 --skip-pull
python scripts/run_benchmark.py --mode cpu --timeout 30 --num-threads "75%" --skip-pull

# Generate reports
python scripts/generate_report.py --mode gpu

# Evaluate results
python scripts/evaluate_agentic_code.py --mode gpu --ctx-size 8192
python scripts/evaluate_agentic_chat.py --mode gpu --ctx-size 8192

# Pull models
python scripts/pull_models.py
```

Key flags for `run_benchmark.py`: `--models` (comma-sep), `--tasks` (comma-sep), `--skip-pull`, `--num-ctx`, `--num-predict`, `--timeout` (minutes, default 10), `--num-threads` (count or percentage like "75%").

## Architecture

**Data flow:** benchmark run → `models/{dirname}/results/{task}/{mode}/` → evaluation scripts → `reports/{mode}/latest.md`

**Config source of truth:** `scripts/config.py` — all model lists, context sizes, tiers, and metadata live here. To add a model, edit 4 places: `MODELS`, `MODELS_TO_PULL`, `MODEL_NUM_CTX`, `MODEL_META`.

**Two benchmark paths** routed by `run_benchmark.py`:
- `run_single_benchmark()` → `/api/generate` for tasks: greenfield, refactor, engine, api, agentic
- `run_single_chat_benchmark()` → `/api/chat` for task: agentic-chat (multi-turn structured tool calling)

**Results layout:**
- CPU/cloud: `models/{dirname}/results/{task}/{mode}/` → output.md, metrics.json
- GPU: `models/{dirname}/results/{task}/gpu/ctx-{size}/` (context-size subfolders)
- agentic-chat adds: transcript.json (raw messages for evaluation)
- engine task adds: trading_engine.py, output.csv, or failure.md

**Model tiers** control mode validation and report sorting:
- Tier 1-3 (local): only run in cpu/gpu mode
- Tier 4 (cloud): only run in cloud mode

**Prompt loading:** `load_prompt(task)` prefers `{task}.md.local` over `{task}.md`. `.local` files are gitignored for proprietary specs (engine task).

**Refactor task** inlines C# source from `refactor-source/` via `{{PLACEHOLDER}}` replacement.

**Engine task** auto-extracts Python code from output.md, copies historical.csv, executes with 30s timeout, creates failure.md on error.

## Key Conventions

- `model_to_dirname()` converts `model:tag` → `model(tag)` and `/` → `__` (Windows can't use colons in paths)
- `num_predict` defaults to `num_ctx` (no artificial output cap)
- Reports sorted by tier ascending, size descending within tier
- `collect_results()` skips model dirs with no metrics.json
- Scripts use `sys.path.insert(0, ...)` for cross-directory imports — always run from project root
- GPU mode analyzes CPU results to suggest context sizes before running

## Platform Gotchas (Windows)

- Parentheses in directory names cause shell expansion issues — use quotes
- In `.bat` files, escape `%` as `%%` (e.g., `"75%%"`)
- Renaming dirs with parens may get "Access denied" — delete and recreate instead
- After installing GPU: set `OLLAMA_USE_GPU=false` and restart Ollama for true CPU-only benchmarks
- Benchmark warns on mode/hardware mismatch (CPU mode with GPU detected, or GPU mode without GPU)

## Adding a New Task

1. Create `requirements/{task}.md` with the prompt
2. Add task name to `TASKS` list in `config.py`
3. If it uses `/api/chat`, add routing in `run_benchmark.py` (see agentic-chat pattern)
4. Create evaluation script in `scripts/evaluate_{task}.py` if needed
