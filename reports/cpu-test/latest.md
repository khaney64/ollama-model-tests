# Ollama Model Benchmark Report

Generated: 2026-02-09 23:28:42

Models tested: 16
Tasks: greenfield, refactor, engine, api, agentic

---

## Warnings & Errors

| Model | Task | num_ctx | num_predict | num_threads | Severity | Detail |
|-------|------|---------|-------------|-------------|----------|--------|
| `qwen3:8b` | engine | 32768 | 32768 | 18 | ERROR | HTTPConnectionPool(host='localhost', port=11434): Read timed out. (read timeout=1800) |
| `qwen3:8b` | api | 32768 | 32768 | 18 | ERROR | HTTPConnectionPool(host='localhost', port=11434): Read timed out. (read timeout=1800) |
| `qwen3:14b` | api | 32768 | 32768 | 18 | ERROR | HTTPConnectionPool(host='localhost', port=11434): Read timed out. (read timeout=1800) |
| `kimi-k2.5:cloud` | greenfield | 32768 | 32768 | - | ERROR | 504 Server Error: Gateway Timeout for url: http://localhost:11434/api/generate |

## Generation Speed (tokens/sec)

| Model | greenfield | refactor | engine | api | agentic |
|-------|--------|--------|--------|--------|--------|
| `phi4:14b-q4_K_M` | - | 4.98 | 6.14 | 6.25 | 5.89 |
| `gemma3:12b-it-q4_K_M` | - | 6.53 | 7.34 | 7.29 | 6.83 |
| `gemma2:9b-instruct-q4_K_M` | - | 5.89 | 7.78 | 8.63 | 7.07 |
| `qwen2.5-coder:7b-instruct-q5_K_M` | - | 9.0 | 10.69 | 10.93 | 9.47 |
| `qwen3:8b` | - | 7.1 | - | - | 8.78 |
| `mistral:7b-instruct-v0.3-q5_K_M` | - | 7.91 | 9.94 | 10.17 | 9.32 |
| `llama3.1:8b` | - | 8.24 | 11.31 | 11.68 | 10.67 |
| `llama3.1:8b-instruct-q4_K_M` | - | 7.76 | 11.18 | 11.6 | 10.59 |
| `qwen2.5-coder:7b` | - | 9.1 | 12.11 | 12.88 | 10.32 |
| `llama3.2:latest` | - | 14.12 | 21.55 | 23.41 | 18.07 |
| `deepseek-coder-v2:16b` | - | 11.77 | 21.83 | 23.51 | 16.18 |
| `qwen3:14b` | - | 4.86 | 5.33 | - | 4.95 |
| `qwen2.5-coder:14b-instruct-q4_K_M` | - | 4.33 | 5.96 | 6.27 | 5.84 |
| `glm-4.7-flash:q4_K_M` | - | 6.36 | 10.39 | 8.66 | 8.41 |
| `glm-4.7:cloud` | 0 | 0 | 0 | 0 | 0 |
| `kimi-k2.5:cloud` | - | 0 | 0 | 0 | 0 |

## Peak VRAM Usage (MB)

| Model | Size (GB) | greenfield | refactor | engine | api | agentic |
|-------|-----------|--------|--------|--------|--------|--------|
| `phi4:14b-q4_K_M` | 9.1 | - | 0.0 | 0.0 | 0.0 | 0.0 |
| `gemma3:12b-it-q4_K_M` | 8.1 | - | 0.0 | 0.0 | 0.0 | 0.0 |
| `gemma2:9b-instruct-q4_K_M` | 5.8 | - | 0.0 | 0.0 | 0.0 | 0.0 |
| `qwen2.5-coder:7b-instruct-q5_K_M` | 5.4 | - | 0.0 | 0.0 | 0.0 | 0.0 |
| `qwen3:8b` | 5.2 | - | 0.0 | 0.0 | 0.0 | 0.0 |
| `mistral:7b-instruct-v0.3-q5_K_M` | 5.1 | - | 0.0 | 0.0 | 0.0 | 0.0 |
| `llama3.1:8b` | 4.9 | - | 0.0 | 0.0 | 0.0 | 0.0 |
| `llama3.1:8b-instruct-q4_K_M` | 4.9 | - | 0.0 | 0.0 | 0.0 | 0.0 |
| `qwen2.5-coder:7b` | 4.7 | - | 0.0 | 0.0 | 0.0 | 0.0 |
| `llama3.2:latest` | 2.0 | - | 0.0 | 0.0 | 0.0 | 0.0 |
| `deepseek-coder-v2:16b` | 10.0 | - | 0.0 | 0.0 | 0.0 | 0.0 |
| `qwen3:14b` | 9.3 | - | 0.0 | 0.0 | 0.0 | 0.0 |
| `qwen2.5-coder:14b-instruct-q4_K_M` | 9.0 | - | 0.0 | 0.0 | 0.0 | 0.0 |
| `glm-4.7-flash:q4_K_M` | 19.0 | - | 0.0 | 0.0 | 0.0 | 0.0 |
| `glm-4.7:cloud` | cloud | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| `kimi-k2.5:cloud` | cloud | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |

## Total Generation Time (seconds)

| Model | greenfield | refactor | engine | api | agentic |
|-------|--------|--------|--------|--------|--------|
| `phi4:14b-q4_K_M` | - | 971.55 | 259.83 | 380.43 | 421.09 |
| `gemma3:12b-it-q4_K_M` | - | 1051.4 | 177.01 | 438.62 | 398.23 |
| `gemma2:9b-instruct-q4_K_M` | - | 417.29 | 190.39 | 163.39 | 281.54 |
| `qwen2.5-coder:7b-instruct-q5_K_M` | - | 342.9 | 174.47 | 186.85 | 211.22 |
| `qwen3:8b` | - | 964.48 | 1800.03 | 1800.0 | 474.02 |
| `mistral:7b-instruct-v0.3-q5_K_M` | - | 304.14 | 176.23 | 264.28 | 230.51 |
| `llama3.1:8b` | - | 288.12 | 100.76 | 150.23 | 137.49 |
| `llama3.1:8b-instruct-q4_K_M` | - | 387.6 | 125.72 | 155.55 | 153.6 |
| `qwen2.5-coder:7b` | - | 550.6 | 142.74 | 136.27 | 221.63 |
| `llama3.2:latest` | - | 209.3 | 81.77 | 77.5 | 118.67 |
| `deepseek-coder-v2:16b` | - | 353.58 | 58.76 | 97.44 | 141.9 |
| `qwen3:14b` | - | 1005.04 | 1313.99 | 1800.01 | 1415.54 |
| `qwen2.5-coder:14b-instruct-q4_K_M` | - | 1540.78 | 256.51 | 326.05 | 379.02 |
| `glm-4.7-flash:q4_K_M` | - | 1205.28 | 372.57 | 945.38 | 602.55 |
| `glm-4.7:cloud` | 98.13 | 287.52 | 55.71 | 177.96 | 160.69 |
| `kimi-k2.5:cloud` | 1200.03 | 967.08 | 369.52 | 597.92 | 226.7 |

## Rankings by Generation Speed

### Refactor

1. `llama3.2:latest` - 14.12 tok/s
2. `deepseek-coder-v2:16b` - 11.77 tok/s
3. `qwen2.5-coder:7b` - 9.1 tok/s
4. `qwen2.5-coder:7b-instruct-q5_K_M` - 9.0 tok/s
5. `llama3.1:8b` - 8.24 tok/s
6. `mistral:7b-instruct-v0.3-q5_K_M` - 7.91 tok/s
7. `llama3.1:8b-instruct-q4_K_M` - 7.76 tok/s
8. `qwen3:8b` - 7.1 tok/s
9. `gemma3:12b-it-q4_K_M` - 6.53 tok/s
10. `glm-4.7-flash:q4_K_M` - 6.36 tok/s
11. `gemma2:9b-instruct-q4_K_M` - 5.89 tok/s
12. `phi4:14b-q4_K_M` - 4.98 tok/s
13. `qwen3:14b` - 4.86 tok/s
14. `qwen2.5-coder:14b-instruct-q4_K_M` - 4.33 tok/s

### Engine

1. `deepseek-coder-v2:16b` - 21.83 tok/s
2. `llama3.2:latest` - 21.55 tok/s
3. `qwen2.5-coder:7b` - 12.11 tok/s
4. `llama3.1:8b` - 11.31 tok/s
5. `llama3.1:8b-instruct-q4_K_M` - 11.18 tok/s
6. `qwen2.5-coder:7b-instruct-q5_K_M` - 10.69 tok/s
7. `glm-4.7-flash:q4_K_M` - 10.39 tok/s
8. `mistral:7b-instruct-v0.3-q5_K_M` - 9.94 tok/s
9. `gemma2:9b-instruct-q4_K_M` - 7.78 tok/s
10. `gemma3:12b-it-q4_K_M` - 7.34 tok/s
11. `phi4:14b-q4_K_M` - 6.14 tok/s
12. `qwen2.5-coder:14b-instruct-q4_K_M` - 5.96 tok/s
13. `qwen3:14b` - 5.33 tok/s

### Api

1. `deepseek-coder-v2:16b` - 23.51 tok/s
2. `llama3.2:latest` - 23.41 tok/s
3. `qwen2.5-coder:7b` - 12.88 tok/s
4. `llama3.1:8b` - 11.68 tok/s
5. `llama3.1:8b-instruct-q4_K_M` - 11.6 tok/s
6. `qwen2.5-coder:7b-instruct-q5_K_M` - 10.93 tok/s
7. `mistral:7b-instruct-v0.3-q5_K_M` - 10.17 tok/s
8. `glm-4.7-flash:q4_K_M` - 8.66 tok/s
9. `gemma2:9b-instruct-q4_K_M` - 8.63 tok/s
10. `gemma3:12b-it-q4_K_M` - 7.29 tok/s
11. `qwen2.5-coder:14b-instruct-q4_K_M` - 6.27 tok/s
12. `phi4:14b-q4_K_M` - 6.25 tok/s

### Agentic

1. `llama3.2:latest` - 18.07 tok/s
2. `deepseek-coder-v2:16b` - 16.18 tok/s
3. `llama3.1:8b` - 10.67 tok/s
4. `llama3.1:8b-instruct-q4_K_M` - 10.59 tok/s
5. `qwen2.5-coder:7b` - 10.32 tok/s
6. `qwen2.5-coder:7b-instruct-q5_K_M` - 9.47 tok/s
7. `mistral:7b-instruct-v0.3-q5_K_M` - 9.32 tok/s
8. `qwen3:8b` - 8.78 tok/s
9. `glm-4.7-flash:q4_K_M` - 8.41 tok/s
10. `gemma2:9b-instruct-q4_K_M` - 7.07 tok/s
11. `gemma3:12b-it-q4_K_M` - 6.83 tok/s
12. `phi4:14b-q4_K_M` - 5.89 tok/s
13. `qwen2.5-coder:14b-instruct-q4_K_M` - 5.84 tok/s
14. `qwen3:14b` - 4.95 tok/s


## Quality Scores (Manual Evaluation)

*Score each criterion 1-10. Fill in after reviewing outputs.*

### Greenfield

| Model | Completeness | Correctness | Code Quality | Overall |
|-------|-------------|-------------|--------------|---------|
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
| `glm-4.7:cloud` | /10 | /10 | /10 | /10 |
| `kimi-k2.5:cloud` | /10 | /10 | /10 | /10 |

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
| `glm-4.7:cloud` | /10 | /10 | /10 | /10 |
| `kimi-k2.5:cloud` | /10 | /10 | /10 | /10 |

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
| `glm-4.7:cloud` | /10 | /10 | /10 | /10 |
| `kimi-k2.5:cloud` | /10 | /10 | /10 | /10 |
