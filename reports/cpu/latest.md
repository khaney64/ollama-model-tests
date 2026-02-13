# Ollama Model Benchmark Report (CPU Mode)

Generated: 2026-02-13 12:22:26

Execution mode: cpu
Models tested: 16
Tasks: greenfield, refactor, engine, api, agentic

---

## Warnings & Errors

| Model | Task | num_ctx | num_predict | num_threads | Severity | Detail |
|-------|------|---------|-------------|-------------|----------|--------|
| `qwen3:8b` | api | 32768 | 32768 | 18 | ERROR | HTTPConnectionPool(host='localhost', port=11434): Read timed out. (read timeout=1800) |
| `qwen3:14b` | engine | 32768 | 32768 | 18 | ERROR | HTTPConnectionPool(host='localhost', port=11434): Read timed out. (read timeout=1800) |
| `qwen3:14b` | api | 32768 | 32768 | 18 | ERROR | HTTPConnectionPool(host='localhost', port=11434): Read timed out. (read timeout=1800) |

## Generation Speed (tokens/sec)

| Model | agentic | api | engine | refactor |
|-------|--------|--------|--------|--------|
| `phi4:14b-q4_K_M` | 5.96 | 6.56 | 6.47 | 4.7 |
| `gemma3:12b-it-q4_K_M` | 6.75 | 6.98 | 7.0 | 6.47 |
| `gemma2:9b-instruct-q4_K_M` | 7.08 | 8.59 | 7.85 | 6.57 |
| `qwen2.5-coder:7b-instruct-q5_K_M` | 9.46 | 10.49 | 10.17 | 8.32 |
| `qwen3:8b` | 8.31 | - | 7.6 | 6.7 |
| `mistral:7b-instruct-v0.3-q5_K_M` | 8.93 | 9.96 | 9.89 | 7.9 |
| `llama3.1:8b` | 9.97 | 11.24 | 10.86 | 8.79 |
| `llama3.1:8b-instruct-q4_K_M` | 10.03 | 11.16 | 10.98 | 8.62 |
| `qwen2.5-coder:7b` | 10.85 | 11.96 | 11.44 | 9.74 |
| `llama3.2:latest` | 19.59 | 22.89 | 21.81 | 14.03 |
| `deepseek-coder-v2:16b` | 16.69 | 22.13 | 20.68 | 11.35 |
| `qwen3:14b` | 5.71 | - | - | 4.46 |
| `qwen2.5-coder:14b-instruct-q4_K_M` | 5.84 | 6.58 | 6.37 | 4.42 |
| `glm-4.7-flash:q4_K_M` | 8.63 | 10.17 | 10.11 | 6.02 |
| `glm-4.7:cloud` | - | - | 0 | - |
| `kimi-k2.5:cloud` | - | - | 0 | - |

## Peak VRAM Usage (MB)

| Model | Size (GB) | agentic | api | engine | refactor |
|-------|-----------|--------|--------|--------|--------|
| `phi4:14b-q4_K_M` | 9.1 | 0.0 | 0.0 | 0.0 | 0.0 |
| `gemma3:12b-it-q4_K_M` | 8.1 | 0.0 | 0.0 | 0.0 | 0.0 |
| `gemma2:9b-instruct-q4_K_M` | 5.8 | 0.0 | 0.0 | 0.0 | 0.0 |
| `qwen2.5-coder:7b-instruct-q5_K_M` | 5.4 | 0.0 | 0.0 | 0.0 | 0.0 |
| `qwen3:8b` | 5.2 | 0.0 | 0.0 | 0.0 | 0.0 |
| `mistral:7b-instruct-v0.3-q5_K_M` | 5.1 | 0.0 | 0.0 | 0.0 | 0.0 |
| `llama3.1:8b` | 4.9 | 0.0 | 0.0 | 0.0 | 0.0 |
| `llama3.1:8b-instruct-q4_K_M` | 4.9 | 0.0 | 0.0 | 0.0 | 0.0 |
| `qwen2.5-coder:7b` | 4.7 | 0.0 | 0.0 | 0.0 | 0.0 |
| `llama3.2:latest` | 2.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| `deepseek-coder-v2:16b` | 10.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| `qwen3:14b` | 9.3 | 0.0 | 0.0 | 0.0 | 0.0 |
| `qwen2.5-coder:14b-instruct-q4_K_M` | 9.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| `glm-4.7-flash:q4_K_M` | 19.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| `glm-4.7:cloud` | cloud | - | - | 0.0 | - |
| `kimi-k2.5:cloud` | cloud | - | - | 0.0 | - |

## Total Generation Time (seconds)

| Model | agentic | api | engine | refactor |
|-------|--------|--------|--------|--------|
| `phi4:14b-q4_K_M` | 398.13 | 376.64 | 237.19 | 1165.93 |
| `gemma3:12b-it-q4_K_M` | 677.21 | 468.61 | 173.58 | 1061.07 |
| `gemma2:9b-instruct-q4_K_M` | 292.83 | 127.79 | 171.89 | 254.03 |
| `qwen2.5-coder:7b-instruct-q5_K_M` | 272.85 | 215.46 | 141.18 | 510.76 |
| `qwen3:8b` | 569.78 | 1800.0 | 1198.86 | 1231.34 |
| `mistral:7b-instruct-v0.3-q5_K_M` | 252.42 | 285.8 | 138.46 | 289.81 |
| `llama3.1:8b` | 160.61 | 144.41 | 118.88 | 320.24 |
| `llama3.1:8b-instruct-q4_K_M` | 157.79 | 156.76 | 91.96 | 379.02 |
| `qwen2.5-coder:7b` | 174.59 | 158.76 | 112.26 | 301.86 |
| `llama3.2:latest` | 67.36 | 75.01 | 54.87 | 355.14 |
| `deepseek-coder-v2:16b` | 115.77 | 92.61 | 67.76 | 413.6 |
| `qwen3:14b` | 632.82 | 1800.03 | 1800.01 | 1679.91 |
| `qwen2.5-coder:14b-instruct-q4_K_M` | 369.48 | 308.19 | 221.95 | 1306.25 |
| `glm-4.7-flash:q4_K_M` | 550.91 | 544.38 | 423.56 | 1477.09 |
| `glm-4.7:cloud` | - | - | 55.71 | - |
| `kimi-k2.5:cloud` | - | - | 369.52 | - |

## Rankings by Generation Speed

### Agentic

1. `llama3.2:latest` - 19.59 tok/s
2. `deepseek-coder-v2:16b` - 16.69 tok/s
3. `qwen2.5-coder:7b` - 10.85 tok/s
4. `llama3.1:8b-instruct-q4_K_M` - 10.03 tok/s
5. `llama3.1:8b` - 9.97 tok/s
6. `qwen2.5-coder:7b-instruct-q5_K_M` - 9.46 tok/s
7. `mistral:7b-instruct-v0.3-q5_K_M` - 8.93 tok/s
8. `glm-4.7-flash:q4_K_M` - 8.63 tok/s
9. `qwen3:8b` - 8.31 tok/s
10. `gemma2:9b-instruct-q4_K_M` - 7.08 tok/s
11. `gemma3:12b-it-q4_K_M` - 6.75 tok/s
12. `phi4:14b-q4_K_M` - 5.96 tok/s
13. `qwen2.5-coder:14b-instruct-q4_K_M` - 5.84 tok/s
14. `qwen3:14b` - 5.71 tok/s

### Api

1. `llama3.2:latest` - 22.89 tok/s
2. `deepseek-coder-v2:16b` - 22.13 tok/s
3. `qwen2.5-coder:7b` - 11.96 tok/s
4. `llama3.1:8b` - 11.24 tok/s
5. `llama3.1:8b-instruct-q4_K_M` - 11.16 tok/s
6. `qwen2.5-coder:7b-instruct-q5_K_M` - 10.49 tok/s
7. `glm-4.7-flash:q4_K_M` - 10.17 tok/s
8. `mistral:7b-instruct-v0.3-q5_K_M` - 9.96 tok/s
9. `gemma2:9b-instruct-q4_K_M` - 8.59 tok/s
10. `gemma3:12b-it-q4_K_M` - 6.98 tok/s
11. `qwen2.5-coder:14b-instruct-q4_K_M` - 6.58 tok/s
12. `phi4:14b-q4_K_M` - 6.56 tok/s

### Engine

1. `llama3.2:latest` - 21.81 tok/s
2. `deepseek-coder-v2:16b` - 20.68 tok/s
3. `qwen2.5-coder:7b` - 11.44 tok/s
4. `llama3.1:8b-instruct-q4_K_M` - 10.98 tok/s
5. `llama3.1:8b` - 10.86 tok/s
6. `qwen2.5-coder:7b-instruct-q5_K_M` - 10.17 tok/s
7. `glm-4.7-flash:q4_K_M` - 10.11 tok/s
8. `mistral:7b-instruct-v0.3-q5_K_M` - 9.89 tok/s
9. `gemma2:9b-instruct-q4_K_M` - 7.85 tok/s
10. `qwen3:8b` - 7.6 tok/s
11. `gemma3:12b-it-q4_K_M` - 7.0 tok/s
12. `phi4:14b-q4_K_M` - 6.47 tok/s
13. `qwen2.5-coder:14b-instruct-q4_K_M` - 6.37 tok/s

### Refactor

1. `llama3.2:latest` - 14.03 tok/s
2. `deepseek-coder-v2:16b` - 11.35 tok/s
3. `qwen2.5-coder:7b` - 9.74 tok/s
4. `llama3.1:8b` - 8.79 tok/s
5. `llama3.1:8b-instruct-q4_K_M` - 8.62 tok/s
6. `qwen2.5-coder:7b-instruct-q5_K_M` - 8.32 tok/s
7. `mistral:7b-instruct-v0.3-q5_K_M` - 7.9 tok/s
8. `qwen3:8b` - 6.7 tok/s
9. `gemma2:9b-instruct-q4_K_M` - 6.57 tok/s
10. `gemma3:12b-it-q4_K_M` - 6.47 tok/s
11. `glm-4.7-flash:q4_K_M` - 6.02 tok/s
12. `phi4:14b-q4_K_M` - 4.7 tok/s
13. `qwen3:14b` - 4.46 tok/s
14. `qwen2.5-coder:14b-instruct-q4_K_M` - 4.42 tok/s


## Quality Scores (Manual Evaluation)

*Score each criterion 1-10. Fill in after reviewing outputs.*

### Agentic

| Model | Completeness | Correctness | Code Quality | Overall |
|-------|-------------|-------------|--------------|---------|
| `phi4:14b-q4_K_M` | /10 | /10 | /10 | /10 |
| `gemma3:12b-it-q4_K_M` | /10 | /10 | /10 | /10 |
| `gemma2:9b-instruct-q4_K_M` | /10 | /10 | /10 | /10 |
| `qwen2.5-coder:7b-instruct-q5_K_M` | /10 | /10 | /10 | /10 |
| `qwen3:8b` | /10 | /10 | /10 | /10 |
| `mistral:7b-instruct-v0.3-q5_K_M` | /10 | /10 | /10 | /10 |
| `llama3.1:8b` | /10 | /10 | /10 | /10 |
| `llama3.1:8b-instruct-q4_K_M` | /10 | /10 | /10 | /10 |
| `qwen2.5-coder:7b` | /10 | /10 | /10 | /10 |
| `llama3.2:latest` | /10 | /10 | /10 | /10 |
| `deepseek-coder-v2:16b` | /10 | /10 | /10 | /10 |
| `qwen3:14b` | /10 | /10 | /10 | /10 |
| `qwen2.5-coder:14b-instruct-q4_K_M` | /10 | /10 | /10 | /10 |
| `glm-4.7-flash:q4_K_M` | /10 | /10 | /10 | /10 |

### Api

| Model | Completeness | Correctness | Code Quality | Overall |
|-------|-------------|-------------|--------------|---------|
| `phi4:14b-q4_K_M` | /10 | /10 | /10 | /10 |
| `gemma3:12b-it-q4_K_M` | /10 | /10 | /10 | /10 |
| `gemma2:9b-instruct-q4_K_M` | /10 | /10 | /10 | /10 |
| `qwen2.5-coder:7b-instruct-q5_K_M` | /10 | /10 | /10 | /10 |
| `qwen3:8b` | /10 | /10 | /10 | /10 |
| `mistral:7b-instruct-v0.3-q5_K_M` | /10 | /10 | /10 | /10 |
| `llama3.1:8b` | /10 | /10 | /10 | /10 |
| `llama3.1:8b-instruct-q4_K_M` | /10 | /10 | /10 | /10 |
| `qwen2.5-coder:7b` | /10 | /10 | /10 | /10 |
| `llama3.2:latest` | /10 | /10 | /10 | /10 |
| `deepseek-coder-v2:16b` | /10 | /10 | /10 | /10 |
| `qwen3:14b` | /10 | /10 | /10 | /10 |
| `qwen2.5-coder:14b-instruct-q4_K_M` | /10 | /10 | /10 | /10 |
| `glm-4.7-flash:q4_K_M` | /10 | /10 | /10 | /10 |

### Engine

| Model | Completeness | Correctness | Code Quality | Overall |
|-------|-------------|-------------|--------------|---------|
| `phi4:14b-q4_K_M` | /10 | /10 | /10 | /10 |
| `gemma3:12b-it-q4_K_M` | /10 | /10 | /10 | /10 |
| `gemma2:9b-instruct-q4_K_M` | /10 | /10 | /10 | /10 |
| `qwen2.5-coder:7b-instruct-q5_K_M` | /10 | /10 | /10 | /10 |
| `qwen3:8b` | /10 | /10 | /10 | /10 |
| `mistral:7b-instruct-v0.3-q5_K_M` | /10 | /10 | /10 | /10 |
| `llama3.1:8b` | /10 | /10 | /10 | /10 |
| `llama3.1:8b-instruct-q4_K_M` | /10 | /10 | /10 | /10 |
| `qwen2.5-coder:7b` | /10 | /10 | /10 | /10 |
| `llama3.2:latest` | /10 | /10 | /10 | /10 |
| `deepseek-coder-v2:16b` | /10 | /10 | /10 | /10 |
| `qwen3:14b` | /10 | /10 | /10 | /10 |
| `qwen2.5-coder:14b-instruct-q4_K_M` | /10 | /10 | /10 | /10 |
| `glm-4.7-flash:q4_K_M` | /10 | /10 | /10 | /10 |
| `glm-4.7:cloud` | /10 | /10 | /10 | /10 |
| `kimi-k2.5:cloud` | /10 | /10 | /10 | /10 |

### Refactor

| Model | Completeness | Correctness | Code Quality | Overall |
|-------|-------------|-------------|--------------|---------|
| `phi4:14b-q4_K_M` | /10 | /10 | /10 | /10 |
| `gemma3:12b-it-q4_K_M` | /10 | /10 | /10 | /10 |
| `gemma2:9b-instruct-q4_K_M` | /10 | /10 | /10 | /10 |
| `qwen2.5-coder:7b-instruct-q5_K_M` | /10 | /10 | /10 | /10 |
| `qwen3:8b` | /10 | /10 | /10 | /10 |
| `mistral:7b-instruct-v0.3-q5_K_M` | /10 | /10 | /10 | /10 |
| `llama3.1:8b` | /10 | /10 | /10 | /10 |
| `llama3.1:8b-instruct-q4_K_M` | /10 | /10 | /10 | /10 |
| `qwen2.5-coder:7b` | /10 | /10 | /10 | /10 |
| `llama3.2:latest` | /10 | /10 | /10 | /10 |
| `deepseek-coder-v2:16b` | /10 | /10 | /10 | /10 |
| `qwen3:14b` | /10 | /10 | /10 | /10 |
| `qwen2.5-coder:14b-instruct-q4_K_M` | /10 | /10 | /10 | /10 |
| `glm-4.7-flash:q4_K_M` | /10 | /10 | /10 | /10 |
