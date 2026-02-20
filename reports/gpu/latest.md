# Ollama Model Benchmark Report (GPU Mode)

Generated: 2026-02-19 19:04:05

Execution mode: gpu
Models tested: 19
Tasks: greenfield, refactor, engine, api, agentic, agentic-chat

---

## Warnings & Errors

| Model | Task | num_ctx | num_predict | num_threads | Severity | Detail |
|-------|------|---------|-------------|-------------|----------|--------|
| `phi4:14b-q4_K_M` | refactor (ctx-8192) | 8192 | 8192 | 18 | WARNING | Hit context limit (8192). Output likely truncated. |
| `phi4:14b-q4_K_M` | agentic-chat (ctx-32768) | 32768 | 32768 | 18 | WARNING | Chat did not complete with a final text response |
| `gemma3:12b-it-q4_K_M` | refactor (ctx-10240) | 10240 | 10240 | 18 | WARNING | Hit context limit (10240). Output likely truncated. |
| `gemma3:12b-it-q4_K_M` | refactor (ctx-8192) | 8192 | 8192 | 18 | WARNING | Hit context limit (8192). Output likely truncated. |
| `gemma3:12b-it-q4_K_M` | agentic-chat (ctx-32768) | 32768 | 32768 | 18 | WARNING | Chat did not complete with a final text response |
| `gemma2:9b-instruct-q4_K_M` | agentic-chat (ctx-32768) | 32768 | 32768 | 18 | WARNING | Chat did not complete with a final text response |
| `qwen2.5-coder:7b-instruct-q5_K_M` | refactor (ctx-10240) | 10240 | 10240 | 18 | WARNING | Used 92% of context. Output may be truncated. |
| `qwen3:8b` | refactor (ctx-8192) | 8192 | 8192 | 18 | WARNING | Hit context limit (8192). Output likely truncated. |
| `qwen3:8b` | engine (ctx-10240) | 10240 | 10240 | 18 | WARNING | Hit context limit (10240). Output likely truncated. |
| `qwen3:8b` | engine (ctx-10240) | 10240 | 10240 | 18 | WARNING | Hit num_predict limit (10240). Output likely truncated — consider increasing --num-predict. |
| `qwen3:8b` | engine (ctx-8192) | 8192 | 8192 | 18 | WARNING | Hit context limit (8192). Output likely truncated. |
| `qwen3:8b` | engine (ctx-8192) | 8192 | 8192 | 18 | WARNING | Hit num_predict limit (8192). Output likely truncated — consider increasing --num-predict. |
| `qwen3:8b` | api (ctx-10240) | 10240 | 10240 | 18 | WARNING | Hit context limit (10240). Output likely truncated. |
| `qwen3:8b` | api (ctx-10240) | 10240 | 10240 | 18 | WARNING | Hit num_predict limit (10240). Output likely truncated — consider increasing --num-predict. |
| `qwen3:8b` | api (ctx-8192) | 8192 | 8192 | 18 | WARNING | Hit context limit (8192). Output likely truncated. |
| `qwen3:8b` | api (ctx-8192) | 8192 | 8192 | 18 | WARNING | Hit num_predict limit (8192). Output likely truncated — consider increasing --num-predict. |
| `qwen3:8b` | agentic-chat (ctx-10240) | 10240 | 10240 | 18 | WARNING | Chat did not complete with a final text response |
| `mistral:7b-instruct-v0.3-q5_K_M` | refactor (ctx-8192) | 8192 | 8192 | 18 | WARNING | Used 93% of context. Output may be truncated. |
| `llama3.1:8b` | refactor (ctx-8192) | 8192 | 8192 | 18 | WARNING | Used 96% of context. Output may be truncated. |
| `llama3.1:8b-instruct-q4_K_M` | refactor (ctx-8192) | 8192 | 8192 | 18 | WARNING | Hit context limit (8192). Output likely truncated. |
| `llama3.2:latest` | refactor (ctx-8192) | 8192 | 8192 | 18 | WARNING | Used 99% of context. Output may be truncated. |
| `deepseek-coder-v2:16b` | refactor (ctx-10240) | 10240 | 10240 | 18 | WARNING | Used 91% of context. Output may be truncated. |
| `deepseek-coder-v2:16b` | refactor (ctx-8192) | 8192 | 8192 | 18 | WARNING | Hit context limit (8192). Output likely truncated. |
| `deepseek-coder-v2:16b` | agentic-chat (ctx-32768) | 32768 | 32768 | 18 | WARNING | Chat did not complete with a final text response |
| `qwen3:14b` | refactor (ctx-8192) | 8192 | 8192 | 18 | WARNING | Hit context limit (8192). Output likely truncated. |
| `qwen3:14b` | engine (ctx-10240) | 10240 | 10240 | 18 | WARNING | Used 95% of context. Output may be truncated. |
| `qwen3:14b` | engine (ctx-8192) | 8192 | 8192 | 18 | WARNING | Hit context limit (8192). Output likely truncated. |
| `qwen3:14b` | api (ctx-10240) | 10240 | 10240 | 18 | WARNING | Hit context limit (10240). Output likely truncated. |
| `qwen3:14b` | api (ctx-10240) | 10240 | 10240 | 18 | WARNING | Hit num_predict limit (10240). Output likely truncated — consider increasing --num-predict. |
| `qwen3:14b` | api (ctx-8192) | 8192 | 8192 | 18 | WARNING | Hit context limit (8192). Output likely truncated. |
| `qwen3:14b` | api (ctx-8192) | 8192 | 8192 | 18 | WARNING | Hit num_predict limit (8192). Output likely truncated — consider increasing --num-predict. |
| `qwen2.5-coder:14b-instruct-q4_K_M` | refactor (ctx-10240) | 10240 | 10240 | 18 | WARNING | Used 90% of context. Output may be truncated. |
| `qwen2.5-coder:14b-instruct-q4_K_M` | refactor (ctx-8192) | 8192 | 8192 | 18 | WARNING | Hit context limit (8192). Output likely truncated. |
| `glm-4.7-flash:q4_K_M` | refactor (ctx-10240) | 10240 | 10240 | 18 | ERROR | HTTPConnectionPool(host='localhost', port=11434): Read timed out. (read timeout=1200) |
| `glm-4.7-flash:q4_K_M` | refactor (ctx-16384) | 16384 | 16384 | 18 | ERROR | HTTPConnectionPool(host='localhost', port=11434): Read timed out. (read timeout=1200) |
| `glm-4.7-flash:q4_K_M` | refactor (ctx-8192) | 8192 | 8192 | 18 | WARNING | Hit context limit (8192). Output likely truncated. |
| `glm-4.7-flash:q4_K_M` | api (ctx-8192) | 8192 | 8192 | 18 | WARNING | Hit context limit (8192). Output likely truncated. |
| `glm-4.7-flash:q4_K_M` | api (ctx-8192) | 8192 | 8192 | 18 | WARNING | Hit num_predict limit (8192). Output likely truncated — consider increasing --num-predict. |
| `glm-4.7-flash:q4_K_M` | agentic (ctx-16384) | 16384 | 16384 | 18 | ERROR | HTTPConnectionPool(host='localhost', port=11434): Read timed out. (read timeout=1200) |
| `hf.co/unsloth/gpt-oss-20b-GGUF:Q4_K_M` | refactor (ctx-16384) | 16384 | 16384 | - | WARNING | Used 93% of context. Output may be truncated. |
| `hf.co/unsloth/gpt-oss-20b-GGUF:Q4_K_M` | agentic-chat (ctx-32768) | 32768 | 32768 | 18 | WARNING | Chat did not complete with a final text response |
| `hf.co/unsloth/gpt-oss-20b-GGUF:Q5_K_M` | refactor (ctx-16384) | 16384 | 16384 | - | WARNING | Used 95% of context. Output may be truncated. |
| `hf.co/unsloth/gpt-oss-20b-GGUF:Q5_K_M` | agentic-chat (ctx-32768) | 32768 | 32768 | 18 | WARNING | Chat did not complete with a final text response |

## Generation Speed (tokens/sec)

| Model | agentic-chat (ctx-10240) | agentic-chat (ctx-16384) | agentic-chat (ctx-32768) | agentic-chat (ctx-8192) | agentic (ctx-10240) | agentic (ctx-16384) | agentic (ctx-32768) | agentic (ctx-8192) | api (ctx-10240) | api (ctx-16384) | api (ctx-32768) | api (ctx-8192) | engine (ctx-10240) | engine (ctx-16384) | engine (ctx-32768) | engine (ctx-8192) | refactor (ctx-10240) | refactor (ctx-16384) | refactor (ctx-32768) | refactor (ctx-8192) |
|-------|--------|--------|--------|--------|--------|--------|--------|--------|--------|--------|--------|--------|--------|--------|--------|--------|--------|--------|--------|--------|
| `phi4:14b-q4_K_M` | - | - | 0 | - | 19.06 | 11.88 | - | 23.42 | 20.12 | 13.02 | - | 24.39 | 20.39 | 12.97 | - | 24.25 | 17.85 | 9.95 | - | 21.96 |
| `hf.co/Qwen/Qwen3-8B-GGUF:Q8_0` | 49.1 | 49.42 | - | - | - | - | - | - | - | - | - | - | - | - | - | - | - | - | - | - |
| `gemma3:12b-it-q4_K_M` | - | - | 0 | - | 50.58 | 50.26 | - | 50.69 | 51.77 | 51.97 | - | 51.71 | 51.38 | 51.48 | - | 51.43 | 49.05 | 49.93 | - | 48.24 |
| `hf.co/Qwen/Qwen3-8B-GGUF:Q6_K` | 60.12 | 58.59 | - | - | - | - | - | - | - | - | - | - | - | - | - | - | - | - | - | - |
| `gemma2:9b-instruct-q4_K_M` | - | - | 0 | - | 59.93 | 60.04 | - | 60.0 | 66.33 | 66.7 | - | 65.87 | 64.95 | 65.07 | - | 64.63 | 55.96 | 55.61 | - | 55.39 |
| `qwen2.5-coder:7b-instruct-q5_K_M` | - | - | 82.41 | - | 78.73 | 78.35 | - | 78.67 | 81.15 | 82.35 | - | 81.87 | 81.37 | 81.49 | - | 81.08 | 73.68 | 76.05 | - | 75.7 |
| `qwen3:8b` | 69.86 | 73.32 | 70.74 | 73.75 | 71.79 | 71.09 | - | 72.13 | 69.38 | 70.79 | - | 71.16 | 68.04 | 70.03 | - | 69.84 | 68.85 | 66.42 | - | 66.68 |
| `mistral:7b-instruct-v0.3-q5_K_M` | - | - | 33.58 | - | 77.2 | 77.41 | - | 76.87 | 80.06 | 81.3 | - | 81.65 | 80.81 | 81.49 | - | 81.38 | 73.1 | 72.29 | - | 72.29 |
| `llama3.1:8b` | - | - | 36.81 | - | 83.5 | 83.81 | - | 83.25 | 86.65 | 87.07 | - | 86.98 | 87.4 | 87.68 | - | 87.42 | 77.38 | 78.63 | - | 77.09 |
| `llama3.1:8b-instruct-q4_K_M` | - | - | 36.16 | - | 83.47 | 84.19 | - | 83.48 | 87.21 | 86.75 | - | 86.24 | 87.1 | 87.73 | - | 87.25 | 79.24 | 78.25 | - | 76.2 |
| `qwen2.5:7b` | - | 88.75 | 90.97 | - | - | 87.92 | 88.36 | - | - | 92.11 | 91.67 | - | - | 91.94 | 91.43 | - | - | 83.4 | 84.28 | - |
| `qwen2.5-coder:7b` | - | - | 93.76 | - | 88.58 | 88.73 | - | 88.12 | 92.09 | 92.64 | - | 92.92 | 91.98 | 92.49 | - | 91.75 | 83.69 | 83.1 | - | 84.75 |
| `llama3.2:latest` | 172.71 | 177.38 | 178.76 | 171.54 | 165.51 | 167.34 | - | 166.64 | 176.23 | 174.72 | - | 173.75 | 173.23 | 176.31 | - | 173.97 | 154.79 | 150.17 | - | 146.03 |
| `deepseek-coder-v2:16b` | - | - | 0 | - | 17.76 | 11.48 | - | 25.19 | 31.81 | 23.35 | - | 38.83 | 26.26 | 17.94 | - | 37.08 | 9.85 | 5.63 | - | 16.92 |
| `qwen3:14b` | 29.09 | 23.29 | 10.55 | 42.45 | 42.06 | 23.34 | - | 43.68 | 41.7 | 23.02 | - | 42.67 | 42.26 | 22.41 | - | 42.2 | 41.35 | 22.44 | - | 40.64 |
| `qwen2.5-coder:14b-instruct-q4_K_M` | - | - | 8.65 | - | 22.1 | 15.48 | - | 28.66 | 22.94 | 16.49 | - | 29.49 | 22.99 | 16.32 | - | 29.55 | 20.29 | 11.45 | - | 27.23 |
| `glm-4.7-flash:q4_K_M` | 13.78 | 12.82 | 8.68 | 14.76 | 8.57 | - | - | 8.94 | 11.08 | 10.23 | - | 9.09 | 10.95 | 10.61 | - | 11.08 | - | - | - | 6.95 |
| `hf.co/unsloth/gpt-oss-20b-GGUF:Q4_K_M` | - | - | 0 | - | - | 28.78 | - | - | - | 28.67 | - | - | - | 29.33 | - | - | - | 26.25 | - | - |
| `hf.co/unsloth/gpt-oss-20b-GGUF:Q5_K_M` | - | - | 0 | - | - | 28.05 | - | - | - | 27.82 | - | - | - | 28.46 | - | - | - | 26.38 | - | - |

## Peak VRAM Usage (MB)

| Model | Size (GB) | agentic-chat (ctx-10240) | agentic-chat (ctx-16384) | agentic-chat (ctx-32768) | agentic-chat (ctx-8192) | agentic (ctx-10240) | agentic (ctx-16384) | agentic (ctx-32768) | agentic (ctx-8192) | api (ctx-10240) | api (ctx-16384) | api (ctx-32768) | api (ctx-8192) | engine (ctx-10240) | engine (ctx-16384) | engine (ctx-32768) | engine (ctx-8192) | refactor (ctx-10240) | refactor (ctx-16384) | refactor (ctx-32768) | refactor (ctx-8192) |
|-------|-----------|--------|--------|--------|--------|--------|--------|--------|--------|--------|--------|--------|--------|--------|--------|--------|--------|--------|--------|--------|--------|
| `phi4:14b-q4_K_M` | 9.1 | - | - | 1962.0 | - | 10576.0 | 9907.0 | - | 11040.0 | 10576.0 | 9907.0 | - | 11040.0 | 10574.0 | 9905.0 | - | 11038.0 | 10576.0 | 9907.0 | - | 11040.0 |
| `hf.co/Qwen/Qwen3-8B-GGUF:Q8_0` | 8.5 | 11343.0 | 11535.0 | - | - | - | - | - | - | - | - | - | - | - | - | - | - | - | - | - | - |
| `gemma3:12b-it-q4_K_M` | 8.1 | - | - | 1964.0 | - | 11071.0 | 11391.0 | - | 10984.0 | 11071.0 | 11391.0 | - | 10983.0 | 11071.0 | 11380.0 | - | 10983.0 | 11073.0 | 11382.0 | - | 10985.0 |
| `hf.co/Qwen/Qwen3-8B-GGUF:Q6_K` | 6.6 | 11650.0 | 10495.0 | - | - | - | - | - | - | - | - | - | - | - | - | - | - | - | - | - | - |
| `gemma2:9b-instruct-q4_K_M` | 5.8 | - | - | 1964.0 | - | 10717.0 | 10641.0 | - | 10763.0 | 10717.0 | 10639.0 | - | 10761.0 | 10717.0 | 10641.0 | - | 10761.0 | 10717.0 | 10639.0 | - | 10762.0 |
| `qwen2.5-coder:7b-instruct-q5_K_M` | 5.4 | - | - | 9179.0 | - | 7705.0 | 7319.0 | - | 7637.0 | 7705.0 | 8005.0 | - | 7637.0 | 7705.0 | 7307.0 | - | 7637.0 | 7705.0 | 8005.0 | - | 7637.0 |
| `qwen3:8b` | 5.2 | 8377.0 | 9283.0 | 11605.0 | 8098.0 | 8216.0 | 9011.0 | - | 7272.0 | 8216.0 | 9011.0 | - | 7959.0 | 8216.0 | 9011.0 | - | 7280.0 | 8205.0 | 8322.0 | - | 7957.0 |
| `mistral:7b-instruct-v0.3-q5_K_M` | 5.1 | - | - | 9420.0 | - | 8219.0 | 8918.0 | - | 8000.0 | 8219.0 | 8918.0 | - | 8000.0 | 8219.0 | 8918.0 | - | 8000.0 | 8219.0 | 8918.0 | - | 8000.0 |
| `llama3.1:8b` | 4.9 | - | - | 9714.0 | - | 7881.0 | 8541.0 | - | 7704.0 | 7881.0 | 8541.0 | - | 7704.0 | 7881.0 | 8539.0 | - | 7693.0 | 7879.0 | 8541.0 | - | 7704.0 |
| `llama3.1:8b-instruct-q4_K_M` | 4.9 | - | - | 9718.0 | - | 7281.0 | 7991.0 | - | 7050.0 | 7968.0 | 8678.0 | - | 7737.0 | 7270.0 | 7991.0 | - | 7050.0 | 7972.0 | 8678.0 | - | 7737.0 |
| `qwen2.5:7b` | 4.7 | - | 7155.0 | 8750.0 | - | - | 7152.0 | 8750.0 | - | - | 7159.0 | 8750.0 | - | - | 7155.0 | 8750.0 | - | - | 7153.0 | 8749.0 | - |
| `qwen2.5-coder:7b` | 4.7 | - | - | 8513.0 | - | 6283.0 | 6510.0 | - | 6246.0 | 6969.0 | 7197.0 | - | 6933.0 | 6271.0 | 6499.0 | - | 6246.0 | 6969.0 | 7197.0 | - | 6933.0 |
| `llama3.2:latest` | 2.0 | 5477.0 | 6169.0 | 7987.0 | 5273.0 | 5322.0 | 5886.0 | - | 5127.0 | 5322.0 | 5886.0 | - | 5127.0 | 5322.0 | 5886.0 | - | 5127.0 | 5322.0 | 5886.0 | - | 5127.0 |
| `deepseek-coder-v2:16b` | 10.0 | - | - | 1975.0 | - | 11512.0 | 11652.0 | - | 11678.0 | 11512.0 | 11652.0 | - | 11678.0 | 11512.0 | 11699.0 | - | 11678.0 | 11512.0 | 11649.0 | - | 11678.0 |
| `qwen3:14b` | 9.3 | 11075.0 | 11563.0 | 11496.0 | 11361.0 | 11494.0 | 11565.0 | - | 11210.0 | 11496.0 | 11560.0 | - | 11208.0 | 11505.0 | 11553.0 | - | 11208.0 | 11497.0 | 11553.0 | - | 11215.0 |
| `qwen2.5-coder:14b-instruct-q4_K_M` | 9.0 | - | - | 9664.0 | - | 11282.0 | 10721.0 | - | 11357.0 | 11282.0 | 10720.0 | - | 11357.0 | 11282.0 | 10721.0 | - | 11357.0 | 11282.0 | 10720.0 | - | 11357.0 |
| `glm-4.7-flash:q4_K_M` | 19.0 | 11424.0 | 11298.0 | 11183.0 | 11719.0 | 11558.0 | 11725.0 | - | 11541.0 | 11558.0 | 11303.0 | - | 11540.0 | 11556.0 | 11717.0 | - | 11528.0 | 11563.0 | 11731.0 | - | 11540.0 |
| `hf.co/unsloth/gpt-oss-20b-GGUF:Q4_K_M` | cloud | - | - | 11420.0 | - | - | 11720.0 | - | - | - | 11536.0 | - | - | - | 11666.0 | - | - | - | 11573.0 | - | - |
| `hf.co/unsloth/gpt-oss-20b-GGUF:Q5_K_M` | cloud | - | - | 11474.0 | - | - | 11636.0 | - | - | - | 11625.0 | - | - | - | 11629.0 | - | - | - | 11698.0 | - | - |

## Total Generation Time (seconds)

| Model | agentic-chat (ctx-10240) | agentic-chat (ctx-16384) | agentic-chat (ctx-32768) | agentic-chat (ctx-8192) | agentic (ctx-10240) | agentic (ctx-16384) | agentic (ctx-32768) | agentic (ctx-8192) | api (ctx-10240) | api (ctx-16384) | api (ctx-32768) | api (ctx-8192) | engine (ctx-10240) | engine (ctx-16384) | engine (ctx-32768) | engine (ctx-8192) | refactor (ctx-10240) | refactor (ctx-16384) | refactor (ctx-32768) | refactor (ctx-8192) |
|-------|--------|--------|--------|--------|--------|--------|--------|--------|--------|--------|--------|--------|--------|--------|--------|--------|--------|--------|--------|--------|
| `phi4:14b-q4_K_M` | - | - | 0.06 | - | 94.54 | 130.99 | - | 74.44 | 120.32 | 166.91 | - | 88.22 | 62.26 | 86.59 | - | 50.55 | 195.09 | 233.02 | - | 200.4 |
| `hf.co/Qwen/Qwen3-8B-GGUF:Q8_0` | 111.13 | 87.42 | - | - | - | - | - | - | - | - | - | - | - | - | - | - | - | - | - | - |
| `gemma3:12b-it-q4_K_M` | - | - | 0.18 | - | 83.24 | 128.74 | - | 71.33 | 50.87 | 49.08 | - | 53.81 | 23.99 | 19.93 | - | 20.03 | 114.65 | 85.21 | - | 90.12 |
| `hf.co/Qwen/Qwen3-8B-GGUF:Q6_K` | 68.62 | 103.41 | - | - | - | - | - | - | - | - | - | - | - | - | - | - | - | - | - | - |
| `gemma2:9b-instruct-q4_K_M` | - | - | 0.1 | - | 29.06 | 30.98 | - | 28.96 | 25.41 | 25.78 | - | 29.68 | 21.93 | 22.21 | - | 24.78 | 10.33 | 15.79 | - | 15.07 |
| `qwen2.5-coder:7b-instruct-q5_K_M` | - | - | 13.05 | - | 22.26 | 34.51 | - | 23.85 | 30.59 | 20.34 | - | 21.48 | 15.81 | 15.04 | - | 14.95 | 69.12 | 30.45 | - | 27.83 |
| `qwen3:8b` | 125.9 | 73.96 | 108.64 | 66.64 | 59.0 | 73.16 | - | 56.51 | 150.15 | 131.42 | - | 117.59 | 153.57 | 127.46 | - | 120.67 | 56.27 | 104.53 | - | 85.17 |
| `mistral:7b-instruct-v0.3-q5_K_M` | - | - | 25.81 | - | 17.73 | 18.23 | - | 20.24 | 42.03 | 31.15 | - | 26.36 | 17.2 | 14.74 | - | 12.92 | 13.74 | 32.03 | - | 23.91 |
| `llama3.1:8b` | - | - | 34.41 | - | 15.52 | 14.04 | - | 15.82 | 25.99 | 24.11 | - | 19.92 | 12.3 | 11.64 | - | 11.81 | 43.93 | 29.03 | - | 46.08 |
| `llama3.1:8b-instruct-q4_K_M` | - | - | 52.01 | - | 14.87 | 10.89 | - | 14.25 | 21.12 | 25.79 | - | 27.64 | 11.63 | 11.19 | - | 12.31 | 15.46 | 34.45 | - | 60.27 |
| `qwen2.5:7b` | - | 47.91 | 29.1 | - | - | 22.11 | 20.96 | - | - | 22.22 | 21.7 | - | - | 12.07 | 13.08 | - | - | 49.93 | 34.36 | - |
| `qwen2.5-coder:7b` | - | - | 10.65 | - | 21.77 | 19.45 | - | 22.3 | 26.63 | 22.2 | - | 18.14 | 14.75 | 10.53 | - | 14.24 | 51.17 | 56.61 | - | 27.73 |
| `llama3.2:latest` | 15.47 | 16.26 | 8.7 | 17.34 | 8.23 | 7.08 | - | 5.98 | 10.43 | 16.08 | - | 14.32 | 8.06 | 7.21 | - | 7.53 | 4.94 | 18.87 | - | 27.19 |
| `deepseek-coder-v2:16b` | - | - | 0.07 | - | 100.14 | 134.03 | - | 81.4 | 52.18 | 64.74 | - | 54.4 | 49.29 | 71.14 | - | 33.58 | 367.48 | 724.8 | - | 183.83 |
| `qwen3:14b` | 159.14 | 117.51 | 742.95 | 180.28 | 143.06 | 134.38 | - | 59.73 | 249.68 | 371.68 | - | 196.12 | 197.01 | 437.03 | - | 192.77 | 98.35 | 175.31 | - | 125.55 |
| `qwen2.5-coder:14b-instruct-q4_K_M` | - | - | 42.75 | - | 69.96 | 95.67 | - | 52.87 | 76.58 | 102.17 | - | 64.83 | 33.63 | 49.12 | - | 32.32 | 228.32 | 416.46 | - | 149.02 |
| `glm-4.7-flash:q4_K_M` | 182.08 | 190.16 | 285.28 | 152.39 | 517.04 | 1200.03 | - | 487.62 | 491.02 | 533.63 | - | 909.54 | 440.8 | 475.74 | - | 439.63 | 1200.02 | 1200.02 | - | 824.96 |
| `hf.co/unsloth/gpt-oss-20b-GGUF:Q4_K_M` | - | - | 84.3 | - | - | 279.3 | - | - | - | 275.33 | - | - | - | 176.73 | - | - | - | 582.08 | - | - |
| `hf.co/unsloth/gpt-oss-20b-GGUF:Q5_K_M` | - | - | 74.0 | - | - | 205.43 | - | - | - | 386.36 | - | - | - | 167.56 | - | - | - | 594.68 | - | - |

## Rankings by Generation Speed

### Agentic-Chat (ctx-10240)

1. `llama3.2:latest` - 172.71 tok/s
2. `qwen3:8b` - 69.86 tok/s
3. `hf.co/Qwen/Qwen3-8B-GGUF:Q6_K` - 60.12 tok/s
4. `hf.co/Qwen/Qwen3-8B-GGUF:Q8_0` - 49.1 tok/s
5. `qwen3:14b` - 29.09 tok/s
6. `glm-4.7-flash:q4_K_M` - 13.78 tok/s

### Agentic-Chat (ctx-16384)

1. `llama3.2:latest` - 177.38 tok/s
2. `qwen2.5:7b` - 88.75 tok/s
3. `qwen3:8b` - 73.32 tok/s
4. `hf.co/Qwen/Qwen3-8B-GGUF:Q6_K` - 58.59 tok/s
5. `hf.co/Qwen/Qwen3-8B-GGUF:Q8_0` - 49.42 tok/s
6. `qwen3:14b` - 23.29 tok/s
7. `glm-4.7-flash:q4_K_M` - 12.82 tok/s

### Agentic-Chat (ctx-32768)

1. `llama3.2:latest` - 178.76 tok/s
2. `qwen2.5-coder:7b` - 93.76 tok/s
3. `qwen2.5:7b` - 90.97 tok/s
4. `qwen2.5-coder:7b-instruct-q5_K_M` - 82.41 tok/s
5. `qwen3:8b` - 70.74 tok/s
6. `llama3.1:8b` - 36.81 tok/s
7. `llama3.1:8b-instruct-q4_K_M` - 36.16 tok/s
8. `mistral:7b-instruct-v0.3-q5_K_M` - 33.58 tok/s
9. `qwen3:14b` - 10.55 tok/s
10. `glm-4.7-flash:q4_K_M` - 8.68 tok/s
11. `qwen2.5-coder:14b-instruct-q4_K_M` - 8.65 tok/s

### Agentic-Chat (ctx-8192)

1. `llama3.2:latest` - 171.54 tok/s
2. `qwen3:8b` - 73.75 tok/s
3. `qwen3:14b` - 42.45 tok/s
4. `glm-4.7-flash:q4_K_M` - 14.76 tok/s

### Agentic (ctx-10240)

1. `llama3.2:latest` - 165.51 tok/s
2. `qwen2.5-coder:7b` - 88.58 tok/s
3. `llama3.1:8b` - 83.5 tok/s
4. `llama3.1:8b-instruct-q4_K_M` - 83.47 tok/s
5. `qwen2.5-coder:7b-instruct-q5_K_M` - 78.73 tok/s
6. `mistral:7b-instruct-v0.3-q5_K_M` - 77.2 tok/s
7. `qwen3:8b` - 71.79 tok/s
8. `gemma2:9b-instruct-q4_K_M` - 59.93 tok/s
9. `gemma3:12b-it-q4_K_M` - 50.58 tok/s
10. `qwen3:14b` - 42.06 tok/s
11. `qwen2.5-coder:14b-instruct-q4_K_M` - 22.1 tok/s
12. `phi4:14b-q4_K_M` - 19.06 tok/s
13. `deepseek-coder-v2:16b` - 17.76 tok/s
14. `glm-4.7-flash:q4_K_M` - 8.57 tok/s

### Agentic (ctx-16384)

1. `llama3.2:latest` - 167.34 tok/s
2. `qwen2.5-coder:7b` - 88.73 tok/s
3. `qwen2.5:7b` - 87.92 tok/s
4. `llama3.1:8b-instruct-q4_K_M` - 84.19 tok/s
5. `llama3.1:8b` - 83.81 tok/s
6. `qwen2.5-coder:7b-instruct-q5_K_M` - 78.35 tok/s
7. `mistral:7b-instruct-v0.3-q5_K_M` - 77.41 tok/s
8. `qwen3:8b` - 71.09 tok/s
9. `gemma2:9b-instruct-q4_K_M` - 60.04 tok/s
10. `gemma3:12b-it-q4_K_M` - 50.26 tok/s
11. `hf.co/unsloth/gpt-oss-20b-GGUF:Q4_K_M` - 28.78 tok/s
12. `hf.co/unsloth/gpt-oss-20b-GGUF:Q5_K_M` - 28.05 tok/s
13. `qwen3:14b` - 23.34 tok/s
14. `qwen2.5-coder:14b-instruct-q4_K_M` - 15.48 tok/s
15. `phi4:14b-q4_K_M` - 11.88 tok/s
16. `deepseek-coder-v2:16b` - 11.48 tok/s

### Agentic (ctx-32768)

1. `qwen2.5:7b` - 88.36 tok/s

### Agentic (ctx-8192)

1. `llama3.2:latest` - 166.64 tok/s
2. `qwen2.5-coder:7b` - 88.12 tok/s
3. `llama3.1:8b-instruct-q4_K_M` - 83.48 tok/s
4. `llama3.1:8b` - 83.25 tok/s
5. `qwen2.5-coder:7b-instruct-q5_K_M` - 78.67 tok/s
6. `mistral:7b-instruct-v0.3-q5_K_M` - 76.87 tok/s
7. `qwen3:8b` - 72.13 tok/s
8. `gemma2:9b-instruct-q4_K_M` - 60.0 tok/s
9. `gemma3:12b-it-q4_K_M` - 50.69 tok/s
10. `qwen3:14b` - 43.68 tok/s
11. `qwen2.5-coder:14b-instruct-q4_K_M` - 28.66 tok/s
12. `deepseek-coder-v2:16b` - 25.19 tok/s
13. `phi4:14b-q4_K_M` - 23.42 tok/s
14. `glm-4.7-flash:q4_K_M` - 8.94 tok/s

### Api (ctx-10240)

1. `llama3.2:latest` - 176.23 tok/s
2. `qwen2.5-coder:7b` - 92.09 tok/s
3. `llama3.1:8b-instruct-q4_K_M` - 87.21 tok/s
4. `llama3.1:8b` - 86.65 tok/s
5. `qwen2.5-coder:7b-instruct-q5_K_M` - 81.15 tok/s
6. `mistral:7b-instruct-v0.3-q5_K_M` - 80.06 tok/s
7. `qwen3:8b` - 69.38 tok/s
8. `gemma2:9b-instruct-q4_K_M` - 66.33 tok/s
9. `gemma3:12b-it-q4_K_M` - 51.77 tok/s
10. `qwen3:14b` - 41.7 tok/s
11. `deepseek-coder-v2:16b` - 31.81 tok/s
12. `qwen2.5-coder:14b-instruct-q4_K_M` - 22.94 tok/s
13. `phi4:14b-q4_K_M` - 20.12 tok/s
14. `glm-4.7-flash:q4_K_M` - 11.08 tok/s

### Api (ctx-16384)

1. `llama3.2:latest` - 174.72 tok/s
2. `qwen2.5-coder:7b` - 92.64 tok/s
3. `qwen2.5:7b` - 92.11 tok/s
4. `llama3.1:8b` - 87.07 tok/s
5. `llama3.1:8b-instruct-q4_K_M` - 86.75 tok/s
6. `qwen2.5-coder:7b-instruct-q5_K_M` - 82.35 tok/s
7. `mistral:7b-instruct-v0.3-q5_K_M` - 81.3 tok/s
8. `qwen3:8b` - 70.79 tok/s
9. `gemma2:9b-instruct-q4_K_M` - 66.7 tok/s
10. `gemma3:12b-it-q4_K_M` - 51.97 tok/s
11. `hf.co/unsloth/gpt-oss-20b-GGUF:Q4_K_M` - 28.67 tok/s
12. `hf.co/unsloth/gpt-oss-20b-GGUF:Q5_K_M` - 27.82 tok/s
13. `deepseek-coder-v2:16b` - 23.35 tok/s
14. `qwen3:14b` - 23.02 tok/s
15. `qwen2.5-coder:14b-instruct-q4_K_M` - 16.49 tok/s
16. `phi4:14b-q4_K_M` - 13.02 tok/s
17. `glm-4.7-flash:q4_K_M` - 10.23 tok/s

### Api (ctx-32768)

1. `qwen2.5:7b` - 91.67 tok/s

### Api (ctx-8192)

1. `llama3.2:latest` - 173.75 tok/s
2. `qwen2.5-coder:7b` - 92.92 tok/s
3. `llama3.1:8b` - 86.98 tok/s
4. `llama3.1:8b-instruct-q4_K_M` - 86.24 tok/s
5. `qwen2.5-coder:7b-instruct-q5_K_M` - 81.87 tok/s
6. `mistral:7b-instruct-v0.3-q5_K_M` - 81.65 tok/s
7. `qwen3:8b` - 71.16 tok/s
8. `gemma2:9b-instruct-q4_K_M` - 65.87 tok/s
9. `gemma3:12b-it-q4_K_M` - 51.71 tok/s
10. `qwen3:14b` - 42.67 tok/s
11. `deepseek-coder-v2:16b` - 38.83 tok/s
12. `qwen2.5-coder:14b-instruct-q4_K_M` - 29.49 tok/s
13. `phi4:14b-q4_K_M` - 24.39 tok/s
14. `glm-4.7-flash:q4_K_M` - 9.09 tok/s

### Engine (ctx-10240)

1. `llama3.2:latest` - 173.23 tok/s
2. `qwen2.5-coder:7b` - 91.98 tok/s
3. `llama3.1:8b` - 87.4 tok/s
4. `llama3.1:8b-instruct-q4_K_M` - 87.1 tok/s
5. `qwen2.5-coder:7b-instruct-q5_K_M` - 81.37 tok/s
6. `mistral:7b-instruct-v0.3-q5_K_M` - 80.81 tok/s
7. `qwen3:8b` - 68.04 tok/s
8. `gemma2:9b-instruct-q4_K_M` - 64.95 tok/s
9. `gemma3:12b-it-q4_K_M` - 51.38 tok/s
10. `qwen3:14b` - 42.26 tok/s
11. `deepseek-coder-v2:16b` - 26.26 tok/s
12. `qwen2.5-coder:14b-instruct-q4_K_M` - 22.99 tok/s
13. `phi4:14b-q4_K_M` - 20.39 tok/s
14. `glm-4.7-flash:q4_K_M` - 10.95 tok/s

### Engine (ctx-16384)

1. `llama3.2:latest` - 176.31 tok/s
2. `qwen2.5-coder:7b` - 92.49 tok/s
3. `qwen2.5:7b` - 91.94 tok/s
4. `llama3.1:8b-instruct-q4_K_M` - 87.73 tok/s
5. `llama3.1:8b` - 87.68 tok/s
6. `mistral:7b-instruct-v0.3-q5_K_M` - 81.49 tok/s
7. `qwen2.5-coder:7b-instruct-q5_K_M` - 81.49 tok/s
8. `qwen3:8b` - 70.03 tok/s
9. `gemma2:9b-instruct-q4_K_M` - 65.07 tok/s
10. `gemma3:12b-it-q4_K_M` - 51.48 tok/s
11. `hf.co/unsloth/gpt-oss-20b-GGUF:Q4_K_M` - 29.33 tok/s
12. `hf.co/unsloth/gpt-oss-20b-GGUF:Q5_K_M` - 28.46 tok/s
13. `qwen3:14b` - 22.41 tok/s
14. `deepseek-coder-v2:16b` - 17.94 tok/s
15. `qwen2.5-coder:14b-instruct-q4_K_M` - 16.32 tok/s
16. `phi4:14b-q4_K_M` - 12.97 tok/s
17. `glm-4.7-flash:q4_K_M` - 10.61 tok/s

### Engine (ctx-32768)

1. `qwen2.5:7b` - 91.43 tok/s

### Engine (ctx-8192)

1. `llama3.2:latest` - 173.97 tok/s
2. `qwen2.5-coder:7b` - 91.75 tok/s
3. `llama3.1:8b` - 87.42 tok/s
4. `llama3.1:8b-instruct-q4_K_M` - 87.25 tok/s
5. `mistral:7b-instruct-v0.3-q5_K_M` - 81.38 tok/s
6. `qwen2.5-coder:7b-instruct-q5_K_M` - 81.08 tok/s
7. `qwen3:8b` - 69.84 tok/s
8. `gemma2:9b-instruct-q4_K_M` - 64.63 tok/s
9. `gemma3:12b-it-q4_K_M` - 51.43 tok/s
10. `qwen3:14b` - 42.2 tok/s
11. `deepseek-coder-v2:16b` - 37.08 tok/s
12. `qwen2.5-coder:14b-instruct-q4_K_M` - 29.55 tok/s
13. `phi4:14b-q4_K_M` - 24.25 tok/s
14. `glm-4.7-flash:q4_K_M` - 11.08 tok/s

### Refactor (ctx-10240)

1. `llama3.2:latest` - 154.79 tok/s
2. `qwen2.5-coder:7b` - 83.69 tok/s
3. `llama3.1:8b-instruct-q4_K_M` - 79.24 tok/s
4. `llama3.1:8b` - 77.38 tok/s
5. `qwen2.5-coder:7b-instruct-q5_K_M` - 73.68 tok/s
6. `mistral:7b-instruct-v0.3-q5_K_M` - 73.1 tok/s
7. `qwen3:8b` - 68.85 tok/s
8. `gemma2:9b-instruct-q4_K_M` - 55.96 tok/s
9. `gemma3:12b-it-q4_K_M` - 49.05 tok/s
10. `qwen3:14b` - 41.35 tok/s
11. `qwen2.5-coder:14b-instruct-q4_K_M` - 20.29 tok/s
12. `phi4:14b-q4_K_M` - 17.85 tok/s
13. `deepseek-coder-v2:16b` - 9.85 tok/s

### Refactor (ctx-16384)

1. `llama3.2:latest` - 150.17 tok/s
2. `qwen2.5:7b` - 83.4 tok/s
3. `qwen2.5-coder:7b` - 83.1 tok/s
4. `llama3.1:8b` - 78.63 tok/s
5. `llama3.1:8b-instruct-q4_K_M` - 78.25 tok/s
6. `qwen2.5-coder:7b-instruct-q5_K_M` - 76.05 tok/s
7. `mistral:7b-instruct-v0.3-q5_K_M` - 72.29 tok/s
8. `qwen3:8b` - 66.42 tok/s
9. `gemma2:9b-instruct-q4_K_M` - 55.61 tok/s
10. `gemma3:12b-it-q4_K_M` - 49.93 tok/s
11. `hf.co/unsloth/gpt-oss-20b-GGUF:Q5_K_M` - 26.38 tok/s
12. `hf.co/unsloth/gpt-oss-20b-GGUF:Q4_K_M` - 26.25 tok/s
13. `qwen3:14b` - 22.44 tok/s
14. `qwen2.5-coder:14b-instruct-q4_K_M` - 11.45 tok/s
15. `phi4:14b-q4_K_M` - 9.95 tok/s
16. `deepseek-coder-v2:16b` - 5.63 tok/s

### Refactor (ctx-32768)

1. `qwen2.5:7b` - 84.28 tok/s

### Refactor (ctx-8192)

1. `llama3.2:latest` - 146.03 tok/s
2. `qwen2.5-coder:7b` - 84.75 tok/s
3. `llama3.1:8b` - 77.09 tok/s
4. `llama3.1:8b-instruct-q4_K_M` - 76.2 tok/s
5. `qwen2.5-coder:7b-instruct-q5_K_M` - 75.7 tok/s
6. `mistral:7b-instruct-v0.3-q5_K_M` - 72.29 tok/s
7. `qwen3:8b` - 66.68 tok/s
8. `gemma2:9b-instruct-q4_K_M` - 55.39 tok/s
9. `gemma3:12b-it-q4_K_M` - 48.24 tok/s
10. `qwen3:14b` - 40.64 tok/s
11. `qwen2.5-coder:14b-instruct-q4_K_M` - 27.23 tok/s
12. `phi4:14b-q4_K_M` - 21.96 tok/s
13. `deepseek-coder-v2:16b` - 16.92 tok/s
14. `glm-4.7-flash:q4_K_M` - 6.95 tok/s


## Quality Scores (Manual Evaluation)

*Score each criterion 1-10. Fill in after reviewing outputs.*

### Agentic-Chat (ctx-10240)

| Model | Completeness | Correctness | Code Quality | Overall |
|-------|-------------|-------------|--------------|---------|
| `hf.co/Qwen/Qwen3-8B-GGUF:Q8_0` | /10 | /10 | /10 | /10 |
| `hf.co/Qwen/Qwen3-8B-GGUF:Q6_K` | /10 | /10 | /10 | /10 |
| `qwen3:8b` | /10 | /10 | /10 | /10 |
| `llama3.2:latest` | /10 | /10 | /10 | /10 |
| `qwen3:14b` | /10 | /10 | /10 | /10 |
| `glm-4.7-flash:q4_K_M` | /10 | /10 | /10 | /10 |

### Agentic-Chat (ctx-16384)

| Model | Completeness | Correctness | Code Quality | Overall |
|-------|-------------|-------------|--------------|---------|
| `hf.co/Qwen/Qwen3-8B-GGUF:Q8_0` | /10 | /10 | /10 | /10 |
| `hf.co/Qwen/Qwen3-8B-GGUF:Q6_K` | /10 | /10 | /10 | /10 |
| `qwen3:8b` | /10 | /10 | /10 | /10 |
| `qwen2.5:7b` | /10 | /10 | /10 | /10 |
| `llama3.2:latest` | /10 | /10 | /10 | /10 |
| `qwen3:14b` | /10 | /10 | /10 | /10 |
| `glm-4.7-flash:q4_K_M` | /10 | /10 | /10 | /10 |

### Agentic-Chat (ctx-32768)

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
| `qwen2.5:7b` | /10 | /10 | /10 | /10 |
| `qwen2.5-coder:7b` | /10 | /10 | /10 | /10 |
| `llama3.2:latest` | /10 | /10 | /10 | /10 |
| `deepseek-coder-v2:16b` | /10 | /10 | /10 | /10 |
| `qwen3:14b` | /10 | /10 | /10 | /10 |
| `qwen2.5-coder:14b-instruct-q4_K_M` | /10 | /10 | /10 | /10 |
| `glm-4.7-flash:q4_K_M` | /10 | /10 | /10 | /10 |
| `hf.co/unsloth/gpt-oss-20b-GGUF:Q4_K_M` | /10 | /10 | /10 | /10 |
| `hf.co/unsloth/gpt-oss-20b-GGUF:Q5_K_M` | /10 | /10 | /10 | /10 |

### Agentic-Chat (ctx-8192)

| Model | Completeness | Correctness | Code Quality | Overall |
|-------|-------------|-------------|--------------|---------|
| `qwen3:8b` | /10 | /10 | /10 | /10 |
| `llama3.2:latest` | /10 | /10 | /10 | /10 |
| `qwen3:14b` | /10 | /10 | /10 | /10 |
| `glm-4.7-flash:q4_K_M` | /10 | /10 | /10 | /10 |

### Agentic (ctx-10240)

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

### Agentic (ctx-16384)

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
| `qwen2.5:7b` | /10 | /10 | /10 | /10 |
| `qwen2.5-coder:7b` | /10 | /10 | /10 | /10 |
| `llama3.2:latest` | /10 | /10 | /10 | /10 |
| `deepseek-coder-v2:16b` | /10 | /10 | /10 | /10 |
| `qwen3:14b` | /10 | /10 | /10 | /10 |
| `qwen2.5-coder:14b-instruct-q4_K_M` | /10 | /10 | /10 | /10 |
| `glm-4.7-flash:q4_K_M` | /10 | /10 | /10 | /10 |
| `hf.co/unsloth/gpt-oss-20b-GGUF:Q4_K_M` | /10 | /10 | /10 | /10 |
| `hf.co/unsloth/gpt-oss-20b-GGUF:Q5_K_M` | /10 | /10 | /10 | /10 |

### Agentic (ctx-32768)

| Model | Completeness | Correctness | Code Quality | Overall |
|-------|-------------|-------------|--------------|---------|
| `qwen2.5:7b` | /10 | /10 | /10 | /10 |

### Agentic (ctx-8192)

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

### Api (ctx-10240)

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

### Api (ctx-16384)

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
| `qwen2.5:7b` | /10 | /10 | /10 | /10 |
| `qwen2.5-coder:7b` | /10 | /10 | /10 | /10 |
| `llama3.2:latest` | /10 | /10 | /10 | /10 |
| `deepseek-coder-v2:16b` | /10 | /10 | /10 | /10 |
| `qwen3:14b` | /10 | /10 | /10 | /10 |
| `qwen2.5-coder:14b-instruct-q4_K_M` | /10 | /10 | /10 | /10 |
| `glm-4.7-flash:q4_K_M` | /10 | /10 | /10 | /10 |
| `hf.co/unsloth/gpt-oss-20b-GGUF:Q4_K_M` | /10 | /10 | /10 | /10 |
| `hf.co/unsloth/gpt-oss-20b-GGUF:Q5_K_M` | /10 | /10 | /10 | /10 |

### Api (ctx-32768)

| Model | Completeness | Correctness | Code Quality | Overall |
|-------|-------------|-------------|--------------|---------|
| `qwen2.5:7b` | /10 | /10 | /10 | /10 |

### Api (ctx-8192)

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

### Engine (ctx-10240)

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

### Engine (ctx-16384)

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
| `qwen2.5:7b` | /10 | /10 | /10 | /10 |
| `qwen2.5-coder:7b` | /10 | /10 | /10 | /10 |
| `llama3.2:latest` | /10 | /10 | /10 | /10 |
| `deepseek-coder-v2:16b` | /10 | /10 | /10 | /10 |
| `qwen3:14b` | /10 | /10 | /10 | /10 |
| `qwen2.5-coder:14b-instruct-q4_K_M` | /10 | /10 | /10 | /10 |
| `glm-4.7-flash:q4_K_M` | /10 | /10 | /10 | /10 |
| `hf.co/unsloth/gpt-oss-20b-GGUF:Q4_K_M` | /10 | /10 | /10 | /10 |
| `hf.co/unsloth/gpt-oss-20b-GGUF:Q5_K_M` | /10 | /10 | /10 | /10 |

### Engine (ctx-32768)

| Model | Completeness | Correctness | Code Quality | Overall |
|-------|-------------|-------------|--------------|---------|
| `qwen2.5:7b` | /10 | /10 | /10 | /10 |

### Engine (ctx-8192)

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

### Refactor (ctx-10240)

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

### Refactor (ctx-16384)

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
| `qwen2.5:7b` | /10 | /10 | /10 | /10 |
| `qwen2.5-coder:7b` | /10 | /10 | /10 | /10 |
| `llama3.2:latest` | /10 | /10 | /10 | /10 |
| `deepseek-coder-v2:16b` | /10 | /10 | /10 | /10 |
| `qwen3:14b` | /10 | /10 | /10 | /10 |
| `qwen2.5-coder:14b-instruct-q4_K_M` | /10 | /10 | /10 | /10 |
| `glm-4.7-flash:q4_K_M` | /10 | /10 | /10 | /10 |
| `hf.co/unsloth/gpt-oss-20b-GGUF:Q4_K_M` | /10 | /10 | /10 | /10 |
| `hf.co/unsloth/gpt-oss-20b-GGUF:Q5_K_M` | /10 | /10 | /10 | /10 |

### Refactor (ctx-32768)

| Model | Completeness | Correctness | Code Quality | Overall |
|-------|-------------|-------------|--------------|---------|
| `qwen2.5:7b` | /10 | /10 | /10 | /10 |

### Refactor (ctx-8192)

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
