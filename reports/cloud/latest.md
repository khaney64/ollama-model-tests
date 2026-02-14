# Ollama Model Benchmark Report (CLOUD Mode)

Generated: 2026-02-14 10:41:26

Execution mode: cloud
Models tested: 5
Tasks: greenfield, refactor, engine, api, agentic

---

## Warnings & Errors

| Model | Task | num_ctx | num_predict | num_threads | Severity | Detail |
|-------|------|---------|-------------|-------------|----------|--------|
| `kimi-k2.5:cloud` | greenfield | 32768 | 32768 | - | ERROR | 504 Server Error: Gateway Timeout for url: http://localhost:11434/api/generate |

## Generation Speed (tokens/sec)

| Model | agentic | api | engine | greenfield | refactor |
|-------|--------|--------|--------|--------|--------|
| `glm-4.7:cloud` | 0 | 0 | 0 | 0 | 0 |
| `glm-5:cloud` | 0 | 0 | 0 | - | 0 |
| `kimi-k2.5:cloud` | 0 | 0 | 0 | - | 0 |
| `minimax-m2.5:cloud` | 0 | 0 | 0 | - | 0 |
| `qwen3-coder-next:cloud` | 0 | 0 | 0 | - | 0 |

## Peak VRAM Usage (MB)

| Model | Size (GB) | agentic | api | engine | greenfield | refactor |
|-------|-----------|--------|--------|--------|--------|--------|
| `glm-4.7:cloud` | cloud | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| `glm-5:cloud` | cloud | 0.0 | 0.0 | 0.0 | - | 0.0 |
| `kimi-k2.5:cloud` | cloud | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| `minimax-m2.5:cloud` | cloud | 1228.0 | 1228.0 | 1232.0 | - | 1228.0 |
| `qwen3-coder-next:cloud` | cloud | 0.0 | 0.0 | 0.0 | - | 0.0 |

## Total Generation Time (seconds)

| Model | agentic | api | engine | greenfield | refactor |
|-------|--------|--------|--------|--------|--------|
| `glm-4.7:cloud` | 115.12 | 41.43 | 56.43 | 98.13 | 131.63 |
| `glm-5:cloud` | 67.79 | 59.61 | 107.39 | - | 92.34 |
| `kimi-k2.5:cloud` | 83.31 | 173.75 | 93.05 | 1200.03 | 211.94 |
| `minimax-m2.5:cloud` | 87.89 | 77.29 | 103.76 | - | 188.93 |
| `qwen3-coder-next:cloud` | 48.81 | 51.09 | 45.32 | - | 122.88 |

## Rankings by Generation Speed


## Quality Scores (Manual Evaluation)

*Score each criterion 1-10. Fill in after reviewing outputs.*

### Agentic

| Model | Completeness | Correctness | Code Quality | Overall |
|-------|-------------|-------------|--------------|---------|
| `glm-4.7:cloud` | /10 | /10 | /10 | /10 |
| `glm-5:cloud` | /10 | /10 | /10 | /10 |
| `kimi-k2.5:cloud` | /10 | /10 | /10 | /10 |
| `minimax-m2.5:cloud` | /10 | /10 | /10 | /10 |
| `qwen3-coder-next:cloud` | /10 | /10 | /10 | /10 |

### Api

| Model | Completeness | Correctness | Code Quality | Overall |
|-------|-------------|-------------|--------------|---------|
| `glm-4.7:cloud` | /10 | /10 | /10 | /10 |
| `glm-5:cloud` | /10 | /10 | /10 | /10 |
| `kimi-k2.5:cloud` | /10 | /10 | /10 | /10 |
| `minimax-m2.5:cloud` | /10 | /10 | /10 | /10 |
| `qwen3-coder-next:cloud` | /10 | /10 | /10 | /10 |

### Engine

| Model | Completeness | Correctness | Code Quality | Overall |
|-------|-------------|-------------|--------------|---------|
| `glm-4.7:cloud` | /10 | /10 | /10 | /10 |
| `glm-5:cloud` | /10 | /10 | /10 | /10 |
| `kimi-k2.5:cloud` | /10 | /10 | /10 | /10 |
| `minimax-m2.5:cloud` | /10 | /10 | /10 | /10 |
| `qwen3-coder-next:cloud` | /10 | /10 | /10 | /10 |

### Greenfield

| Model | Completeness | Correctness | Code Quality | Overall |
|-------|-------------|-------------|--------------|---------|
| `glm-4.7:cloud` | /10 | /10 | /10 | /10 |
| `kimi-k2.5:cloud` | /10 | /10 | /10 | /10 |

### Refactor

| Model | Completeness | Correctness | Code Quality | Overall |
|-------|-------------|-------------|--------------|---------|
| `glm-4.7:cloud` | /10 | /10 | /10 | /10 |
| `glm-5:cloud` | /10 | /10 | /10 | /10 |
| `kimi-k2.5:cloud` | /10 | /10 | /10 | /10 |
| `minimax-m2.5:cloud` | /10 | /10 | /10 | /10 |
| `qwen3-coder-next:cloud` | /10 | /10 | /10 | /10 |
