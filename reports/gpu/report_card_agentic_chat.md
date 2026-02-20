# Agentic Chat Task Report Card

Generated: 2026-02-19 19:03:28

This task tests models using Ollama's `/api/chat` endpoint with structured
tool calling (the same protocol used by OpenClaw and similar applications).

## Executive Summary

Evaluated **34** model(s) on the agentic-chat task.

**Grade Distribution:**
- A: 19 model(s)
- B: 2 model(s)
- D: 1 model(s)
- F: 12 model(s)

**Outcome Classification:**
- **Success (structured tool calls, completed)**: 20 model(s)
- **Partial Success (tool calls but incomplete)**: 2 model(s)
- **Text Narration (described tools in prose, 0 structured calls)**: 6 model(s)
- **Empty Response (no tokens, instant return -- model lacks tool-call support)**: 4 model(s)
- **Stalled Inference (loaded model, burned time, 0 tokens -- unparseable output)**: 2 model(s)

## Summary Rankings

| Rank | Model | Classification | Grade | Total | Valid Calls | Coverage | Ordering | Args | Portfolios | Response | Recovery | Pass |
|------|-------|----------------|-------|-------|-------------|----------|----------|------|------------|----------|----------|------|
| 1 | glm-4.7-flash(q4_K_M) (ctx-16384) | success | A | 10.0 | 10.0 | 10.0 | 10.0 | 10.0 | 10.0 | 10.0 | 10.0 | Y |
| 2 | glm-4.7-flash(q4_K_M) (ctx-32768) | success | A | 10.0 | 10.0 | 10.0 | 10.0 | 10.0 | 10.0 | 10.0 | 10.0 | Y |
| 3 | glm-4.7-flash(q4_K_M) (ctx-8192) | success | A | 10.0 | 10.0 | 10.0 | 10.0 | 10.0 | 10.0 | 10.0 | 10.0 | Y |
| 4 | hf.co__Qwen__Qwen3-8B-GGUF(Q6_K) (ctx-10240) | success | A | 10.0 | 10.0 | 10.0 | 10.0 | 10.0 | 10.0 | 10.0 | 10.0 | Y |
| 5 | hf.co__Qwen__Qwen3-8B-GGUF(Q6_K) (ctx-16384) | success | A | 10.0 | 10.0 | 10.0 | 10.0 | 10.0 | 10.0 | 10.0 | 10.0 | Y |
| 6 | hf.co__Qwen__Qwen3-8B-GGUF(Q8_0) (ctx-10240) | success | A | 10.0 | 10.0 | 10.0 | 10.0 | 10.0 | 10.0 | 10.0 | 10.0 | Y |
| 7 | hf.co__Qwen__Qwen3-8B-GGUF(Q8_0) (ctx-16384) | success | A | 10.0 | 10.0 | 10.0 | 10.0 | 10.0 | 10.0 | 10.0 | 10.0 | Y |
| 8 | qwen2.5(7b) (ctx-16384) | success | A | 10.0 | 10.0 | 10.0 | 10.0 | 10.0 | 10.0 | 10.0 | 10.0 | Y |
| 9 | qwen2.5(7b) (ctx-32768) | success | A | 10.0 | 10.0 | 10.0 | 10.0 | 10.0 | 10.0 | 10.0 | 10.0 | Y |
| 10 | qwen3(14b) (ctx-10240) | success | A | 10.0 | 10.0 | 10.0 | 10.0 | 10.0 | 10.0 | 10.0 | 10.0 | Y |
| 11 | qwen3(14b) (ctx-16384) | success | A | 10.0 | 10.0 | 10.0 | 10.0 | 10.0 | 10.0 | 10.0 | 10.0 | Y |
| 12 | qwen3(14b) (ctx-32768) | success | A | 10.0 | 10.0 | 10.0 | 10.0 | 10.0 | 10.0 | 10.0 | 10.0 | Y |
| 13 | qwen3(8b) (ctx-16384) | success | A | 10.0 | 10.0 | 10.0 | 10.0 | 10.0 | 10.0 | 10.0 | 10.0 | Y |
| 14 | qwen3(8b) (ctx-32768) | success | A | 10.0 | 10.0 | 10.0 | 10.0 | 10.0 | 10.0 | 10.0 | 10.0 | Y |
| 15 | qwen3(8b) (ctx-8192) | success | A | 10.0 | 10.0 | 10.0 | 10.0 | 10.0 | 10.0 | 10.0 | 10.0 | Y |
| 16 | glm-4.7-flash(q4_K_M) (ctx-10240) | success | A | 9.8 | 10.0 | 8.3 | 10.0 | 10.0 | 10.0 | 10.0 | 10.0 | Y |
| 17 | qwen3(14b) (ctx-8192) | success | A | 9.8 | 10.0 | 8.3 | 10.0 | 10.0 | 10.0 | 10.0 | 10.0 | Y |
| 18 | llama3.2(latest) (ctx-10240) | success | A | 9.1 | 10.0 | 10.0 | 10.0 | 4.0 | 10.0 | 10.0 | 10.0 | Y |
| 19 | qwen3(8b) (ctx-10240) | partial_success | A | 9.0 | 10.0 | 10.0 | 10.0 | 10.0 | 10.0 | 0.0 | 10.0 | Y |
| 20 | llama3.2(latest) (ctx-8192) | success | B | 8.8 | 10.0 | 10.0 | 10.0 | 2.0 | 10.0 | 10.0 | 10.0 | Y |
| 21 | llama3.2(latest) (ctx-16384) | success | B | 8.4 | 10.0 | 10.0 | 10.0 | 4.0 | 10.0 | 10.0 | 3.0 | Y |
| 22 | llama3.2(latest) (ctx-32768) | partial_success | D | 6.9 | 10.0 | 3.3 | 0.0 | 10.0 | 10.0 | 4.0 | 10.0 | N |
| 23 | llama3.1(8b) (ctx-32768) | text_narration | F | 3.5 | 0.0 | 0.0 | 0.0 | 0.0 | 10.0 | 10.0 | 10.0 | N |
| 24 | llama3.1(8b-instruct-q4_K_M) (ctx-32768) | text_narration | F | 3.5 | 0.0 | 0.0 | 0.0 | 0.0 | 10.0 | 10.0 | 10.0 | N |
| 25 | mistral(7b-instruct-v0.3-q5_K_M) (ctx-32768) | text_narration | F | 3.5 | 0.0 | 0.0 | 0.0 | 0.0 | 10.0 | 10.0 | 10.0 | N |
| 26 | qwen2.5-coder(14b-instruct-q4_K_M) (ctx-32768) | text_narration | F | 3.5 | 0.0 | 0.0 | 0.0 | 0.0 | 10.0 | 10.0 | 10.0 | N |
| 27 | qwen2.5-coder(7b) (ctx-32768) | text_narration | F | 3.5 | 0.0 | 0.0 | 0.0 | 0.0 | 10.0 | 10.0 | 10.0 | N |
| 28 | qwen2.5-coder(7b-instruct-q5_K_M) (ctx-32768) | text_narration | F | 3.5 | 0.0 | 0.0 | 0.0 | 0.0 | 10.0 | 10.0 | 10.0 | N |
| 29 | deepseek-coder-v2(16b) (ctx-32768) | empty_response | F | 2.5 | 0.0 | 0.0 | 0.0 | 0.0 | 10.0 | 0.0 | 10.0 | N |
| 30 | gemma2(9b-instruct-q4_K_M) (ctx-32768) | empty_response | F | 2.5 | 0.0 | 0.0 | 0.0 | 0.0 | 10.0 | 0.0 | 10.0 | N |
| 31 | gemma3(12b-it-q4_K_M) (ctx-32768) | empty_response | F | 2.5 | 0.0 | 0.0 | 0.0 | 0.0 | 10.0 | 0.0 | 10.0 | N |
| 32 | hf.co__unsloth__gpt-oss-20b-GGUF(Q4_K_M) (ctx-32768) | stalled_inference | F | 2.5 | 0.0 | 0.0 | 0.0 | 0.0 | 10.0 | 0.0 | 10.0 | N |
| 33 | hf.co__unsloth__gpt-oss-20b-GGUF(Q5_K_M) (ctx-32768) | stalled_inference | F | 2.5 | 0.0 | 0.0 | 0.0 | 0.0 | 10.0 | 0.0 | 10.0 | N |
| 34 | phi4(14b-q4_K_M) (ctx-32768) | empty_response | F | 2.5 | 0.0 | 0.0 | 0.0 | 0.0 | 10.0 | 0.0 | 10.0 | N |

**Passing Score:** 7.0/10.0

## Scoring Weights

| Criterion | Weight | What it checks |
|-----------|--------|----------------|
| Valid Tool Calls | 20% | Model produced structured tool_calls with valid JSON |
| Tool Coverage | 15% | At least 6 of 8 tools used |
| Call Ordering | 15% | Data-dependent calls in correct order per portfolio |
| Argument Correctness | 15% | Valid portfolio IDs, symbol lists, risk config |
| Portfolio Coverage | 15% | All 3 portfolios processed |
| Final Response | 10% | Useful text summary at the end |
| Error Recovery | 10% | Continued after tool errors |

## Detailed Results

### glm-4.7-flash(q4_K_M) (ctx-16384)

**Grade: A (10.0/10.0)** | **Classification: success**

> Made 16 tool calls using 6 tools

| Criterion | Score |
|-----------|-------|
| Valid Tool Calls | 10.0/10 |
| Tool Coverage | 10.0/10 |
| Call Ordering | 10.0/10 |
| Argument Correctness | 10.0/10 |
| Portfolio Coverage | 10.0/10 |
| Final Response | 10.0/10 |
| Error Recovery | 10.0/10 |

**Tools used (6/8):** calculate_portfolio_value, calculate_volatility_score, check_risk_threshold, get_portfolio_holdings, get_stock_prices, log_operation

**Missing:** generate_report, send_notification

**Portfolios:** PORT-001, PORT-002, PORT-003

**Turns:** 5 | **Tool calls:** 16 | **Success rate:** 100%

### glm-4.7-flash(q4_K_M) (ctx-32768)

**Grade: A (10.0/10.0)** | **Classification: success**

> Made 16 tool calls using 6 tools

| Criterion | Score |
|-----------|-------|
| Valid Tool Calls | 10.0/10 |
| Tool Coverage | 10.0/10 |
| Call Ordering | 10.0/10 |
| Argument Correctness | 10.0/10 |
| Portfolio Coverage | 10.0/10 |
| Final Response | 10.0/10 |
| Error Recovery | 10.0/10 |

**Tools used (6/8):** calculate_portfolio_value, calculate_volatility_score, check_risk_threshold, get_portfolio_holdings, get_stock_prices, log_operation

**Missing:** generate_report, send_notification

**Portfolios:** PORT-001, PORT-002, PORT-003

**Turns:** 5 | **Tool calls:** 16 | **Success rate:** 100%

### glm-4.7-flash(q4_K_M) (ctx-8192)

**Grade: A (10.0/10.0)** | **Classification: success**

> Made 16 tool calls using 6 tools

| Criterion | Score |
|-----------|-------|
| Valid Tool Calls | 10.0/10 |
| Tool Coverage | 10.0/10 |
| Call Ordering | 10.0/10 |
| Argument Correctness | 10.0/10 |
| Portfolio Coverage | 10.0/10 |
| Final Response | 10.0/10 |
| Error Recovery | 10.0/10 |

**Tools used (6/8):** calculate_portfolio_value, calculate_volatility_score, check_risk_threshold, get_portfolio_holdings, get_stock_prices, log_operation

**Missing:** generate_report, send_notification

**Portfolios:** PORT-001, PORT-002, PORT-003

**Turns:** 7 | **Tool calls:** 16 | **Success rate:** 100%

### hf.co__Qwen__Qwen3-8B-GGUF(Q6_K) (ctx-10240)

**Grade: A (10.0/10.0)** | **Classification: success**

> Made 18 tool calls using 6 tools, completed with final response

| Criterion | Score |
|-----------|-------|
| Valid Tool Calls | 10.0/10 |
| Tool Coverage | 10.0/10 |
| Call Ordering | 10.0/10 |
| Argument Correctness | 10.0/10 |
| Portfolio Coverage | 10.0/10 |
| Final Response | 10.0/10 |
| Error Recovery | 10.0/10 |

**Tools used (6/8):** calculate_portfolio_value, calculate_volatility_score, check_risk_threshold, get_portfolio_holdings, get_stock_prices, log_operation

**Missing:** generate_report, send_notification

**Portfolios:** PORT-001, PORT-002, PORT-003

**Turns:** 7 | **Tool calls:** 18 | **Success rate:** 100%

### hf.co__Qwen__Qwen3-8B-GGUF(Q6_K) (ctx-16384)

**Grade: A (10.0/10.0)** | **Classification: success**

> Made 20 tool calls using 7 tools, completed with final response

| Criterion | Score |
|-----------|-------|
| Valid Tool Calls | 10.0/10 |
| Tool Coverage | 10.0/10 |
| Call Ordering | 10.0/10 |
| Argument Correctness | 10.0/10 |
| Portfolio Coverage | 10.0/10 |
| Final Response | 10.0/10 |
| Error Recovery | 10.0/10 |

**Tools used (7/8):** calculate_portfolio_value, calculate_volatility_score, check_risk_threshold, generate_report, get_portfolio_holdings, get_stock_prices, log_operation

**Missing:** send_notification

**Portfolios:** PORT-001, PORT-002, PORT-003

**Turns:** 8 | **Tool calls:** 20 | **Success rate:** 95%

### hf.co__Qwen__Qwen3-8B-GGUF(Q8_0) (ctx-10240)

**Grade: A (10.0/10.0)** | **Classification: success**

> Made 18 tool calls using 6 tools, completed with final response

| Criterion | Score |
|-----------|-------|
| Valid Tool Calls | 10.0/10 |
| Tool Coverage | 10.0/10 |
| Call Ordering | 10.0/10 |
| Argument Correctness | 10.0/10 |
| Portfolio Coverage | 10.0/10 |
| Final Response | 10.0/10 |
| Error Recovery | 10.0/10 |

**Tools used (6/8):** calculate_portfolio_value, calculate_volatility_score, check_risk_threshold, get_portfolio_holdings, get_stock_prices, log_operation

**Missing:** generate_report, send_notification

**Portfolios:** PORT-001, PORT-002, PORT-003

**Turns:** 5 | **Tool calls:** 18 | **Success rate:** 100%

### hf.co__Qwen__Qwen3-8B-GGUF(Q8_0) (ctx-16384)

**Grade: A (10.0/10.0)** | **Classification: success**

> Made 18 tool calls using 6 tools, completed with final response

| Criterion | Score |
|-----------|-------|
| Valid Tool Calls | 10.0/10 |
| Tool Coverage | 10.0/10 |
| Call Ordering | 10.0/10 |
| Argument Correctness | 10.0/10 |
| Portfolio Coverage | 10.0/10 |
| Final Response | 10.0/10 |
| Error Recovery | 10.0/10 |

**Tools used (6/8):** calculate_portfolio_value, calculate_volatility_score, check_risk_threshold, get_portfolio_holdings, get_stock_prices, log_operation

**Missing:** generate_report, send_notification

**Portfolios:** PORT-001, PORT-002, PORT-003

**Turns:** 7 | **Tool calls:** 18 | **Success rate:** 100%

### qwen2.5(7b) (ctx-16384)

**Grade: A (10.0/10.0)** | **Classification: success**

> Made 30 tool calls using 7 tools, completed with final response

| Criterion | Score |
|-----------|-------|
| Valid Tool Calls | 10.0/10 |
| Tool Coverage | 10.0/10 |
| Call Ordering | 10.0/10 |
| Argument Correctness | 10.0/10 |
| Portfolio Coverage | 10.0/10 |
| Final Response | 10.0/10 |
| Error Recovery | 10.0/10 |

**Tools used (7/8):** calculate_portfolio_value, calculate_volatility_score, check_risk_threshold, generate_report, get_portfolio_holdings, log_operation, send_notification

**Missing:** get_stock_prices

**Portfolios:** PORT-001, PORT-002, PORT-003

**Turns:** 3 | **Tool calls:** 30 | **Success rate:** 90%

### qwen2.5(7b) (ctx-32768)

**Grade: A (10.0/10.0)** | **Classification: success**

> Made 27 tool calls using 8 tools, completed with final response

| Criterion | Score |
|-----------|-------|
| Valid Tool Calls | 10.0/10 |
| Tool Coverage | 10.0/10 |
| Call Ordering | 10.0/10 |
| Argument Correctness | 10.0/10 |
| Portfolio Coverage | 10.0/10 |
| Final Response | 10.0/10 |
| Error Recovery | 10.0/10 |

**Tools used (8/8):** calculate_portfolio_value, calculate_volatility_score, check_risk_threshold, generate_report, get_portfolio_holdings, get_stock_prices, log_operation, send_notification

**Portfolios:** PORT-001, PORT-002, PORT-003

**Turns:** 2 | **Tool calls:** 27 | **Success rate:** 89%

### qwen3(14b) (ctx-10240)

**Grade: A (10.0/10.0)** | **Classification: success**

> Made 18 tool calls using 6 tools

| Criterion | Score |
|-----------|-------|
| Valid Tool Calls | 10.0/10 |
| Tool Coverage | 10.0/10 |
| Call Ordering | 10.0/10 |
| Argument Correctness | 10.0/10 |
| Portfolio Coverage | 10.0/10 |
| Final Response | 10.0/10 |
| Error Recovery | 10.0/10 |

**Tools used (6/8):** calculate_portfolio_value, calculate_volatility_score, check_risk_threshold, get_portfolio_holdings, get_stock_prices, log_operation

**Missing:** generate_report, send_notification

**Portfolios:** PORT-001, PORT-002, PORT-003

**Turns:** 7 | **Tool calls:** 18 | **Success rate:** 100%

### qwen3(14b) (ctx-16384)

**Grade: A (10.0/10.0)** | **Classification: success**

> Made 24 tool calls using 8 tools, completed with final response

| Criterion | Score |
|-----------|-------|
| Valid Tool Calls | 10.0/10 |
| Tool Coverage | 10.0/10 |
| Call Ordering | 10.0/10 |
| Argument Correctness | 10.0/10 |
| Portfolio Coverage | 10.0/10 |
| Final Response | 10.0/10 |
| Error Recovery | 10.0/10 |

**Tools used (8/8):** calculate_portfolio_value, calculate_volatility_score, check_risk_threshold, generate_report, get_portfolio_holdings, get_stock_prices, log_operation, send_notification

**Portfolios:** PORT-001, PORT-002, PORT-003

**Turns:** 3 | **Tool calls:** 24 | **Success rate:** 96%

### qwen3(14b) (ctx-32768)

**Grade: A (10.0/10.0)** | **Classification: success**

> Made 28 tool calls using 7 tools

| Criterion | Score |
|-----------|-------|
| Valid Tool Calls | 10.0/10 |
| Tool Coverage | 10.0/10 |
| Call Ordering | 10.0/10 |
| Argument Correctness | 10.0/10 |
| Portfolio Coverage | 10.0/10 |
| Final Response | 10.0/10 |
| Error Recovery | 10.0/10 |

**Tools used (7/8):** calculate_portfolio_value, calculate_volatility_score, check_risk_threshold, generate_report, get_portfolio_holdings, get_stock_prices, log_operation

**Missing:** send_notification

**Portfolios:** PORT-001, PORT-002, PORT-003

**Turns:** 15 | **Tool calls:** 28 | **Success rate:** 100%

### qwen3(8b) (ctx-16384)

**Grade: A (10.0/10.0)** | **Classification: success**

> Made 16 tool calls using 6 tools

| Criterion | Score |
|-----------|-------|
| Valid Tool Calls | 10.0/10 |
| Tool Coverage | 10.0/10 |
| Call Ordering | 10.0/10 |
| Argument Correctness | 10.0/10 |
| Portfolio Coverage | 10.0/10 |
| Final Response | 10.0/10 |
| Error Recovery | 10.0/10 |

**Tools used (6/8):** calculate_portfolio_value, calculate_volatility_score, check_risk_threshold, get_portfolio_holdings, get_stock_prices, log_operation

**Missing:** generate_report, send_notification

**Portfolios:** PORT-001, PORT-002, PORT-003

**Turns:** 9 | **Tool calls:** 16 | **Success rate:** 100%

### qwen3(8b) (ctx-32768)

**Grade: A (10.0/10.0)** | **Classification: success**

> Made 16 tool calls using 6 tools

| Criterion | Score |
|-----------|-------|
| Valid Tool Calls | 10.0/10 |
| Tool Coverage | 10.0/10 |
| Call Ordering | 10.0/10 |
| Argument Correctness | 10.0/10 |
| Portfolio Coverage | 10.0/10 |
| Final Response | 10.0/10 |
| Error Recovery | 10.0/10 |

**Tools used (6/8):** calculate_portfolio_value, calculate_volatility_score, check_risk_threshold, get_portfolio_holdings, get_stock_prices, log_operation

**Missing:** generate_report, send_notification

**Portfolios:** PORT-001, PORT-002, PORT-003

**Turns:** 13 | **Tool calls:** 16 | **Success rate:** 100%

### qwen3(8b) (ctx-8192)

**Grade: A (10.0/10.0)** | **Classification: success**

> Made 16 tool calls using 6 tools

| Criterion | Score |
|-----------|-------|
| Valid Tool Calls | 10.0/10 |
| Tool Coverage | 10.0/10 |
| Call Ordering | 10.0/10 |
| Argument Correctness | 10.0/10 |
| Portfolio Coverage | 10.0/10 |
| Final Response | 10.0/10 |
| Error Recovery | 10.0/10 |

**Tools used (6/8):** calculate_portfolio_value, calculate_volatility_score, check_risk_threshold, get_portfolio_holdings, get_stock_prices, log_operation

**Missing:** generate_report, send_notification

**Portfolios:** PORT-001, PORT-002, PORT-003

**Turns:** 7 | **Tool calls:** 16 | **Success rate:** 100%

### glm-4.7-flash(q4_K_M) (ctx-10240)

**Grade: A (9.8/10.0)** | **Classification: success**

> Made 14 tool calls using 5 tools

| Criterion | Score |
|-----------|-------|
| Valid Tool Calls | 10.0/10 |
| Tool Coverage | 8.3/10 |
| Call Ordering | 10.0/10 |
| Argument Correctness | 10.0/10 |
| Portfolio Coverage | 10.0/10 |
| Final Response | 10.0/10 |
| Error Recovery | 10.0/10 |

**Tools used (5/8):** calculate_portfolio_value, calculate_volatility_score, get_portfolio_holdings, get_stock_prices, log_operation

**Missing:** check_risk_threshold, generate_report, send_notification

**Portfolios:** PORT-001, PORT-002, PORT-003

**Turns:** 5 | **Tool calls:** 14 | **Success rate:** 100%

**Issues:**
- Only 5/8 tools used (need 6 for full score)

### qwen3(14b) (ctx-8192)

**Grade: A (9.8/10.0)** | **Classification: success**

> Made 15 tool calls using 5 tools

| Criterion | Score |
|-----------|-------|
| Valid Tool Calls | 10.0/10 |
| Tool Coverage | 8.3/10 |
| Call Ordering | 10.0/10 |
| Argument Correctness | 10.0/10 |
| Portfolio Coverage | 10.0/10 |
| Final Response | 10.0/10 |
| Error Recovery | 10.0/10 |

**Tools used (5/8):** calculate_portfolio_value, calculate_volatility_score, check_risk_threshold, get_portfolio_holdings, get_stock_prices

**Missing:** generate_report, log_operation, send_notification

**Portfolios:** PORT-001, PORT-002, PORT-003

**Turns:** 14 | **Tool calls:** 15 | **Success rate:** 100%

**Issues:**
- Only 5/8 tools used (need 6 for full score)

### llama3.2(latest) (ctx-10240)

**Grade: A (9.1/10.0)** | **Classification: success**

> Made 36 tool calls using 8 tools

| Criterion | Score |
|-----------|-------|
| Valid Tool Calls | 10.0/10 |
| Tool Coverage | 10.0/10 |
| Call Ordering | 10.0/10 |
| Argument Correctness | 4.0/10 |
| Portfolio Coverage | 10.0/10 |
| Final Response | 10.0/10 |
| Error Recovery | 10.0/10 |

**Tools used (8/8):** calculate_portfolio_value, calculate_volatility_score, check_risk_threshold, generate_report, get_portfolio_holdings, get_stock_prices, log_operation, send_notification

**Portfolios:** PORT-001, PORT-002, PORT-003

**Turns:** 2 | **Tool calls:** 36 | **Success rate:** 50%

**Issues:**
- 9 argument issue(s)

### qwen3(8b) (ctx-10240)

**Grade: A (9.0/10.0)** | **Classification: partial_success**

> Made 13 tool calls but incomplete

| Criterion | Score |
|-----------|-------|
| Valid Tool Calls | 10.0/10 |
| Tool Coverage | 10.0/10 |
| Call Ordering | 10.0/10 |
| Argument Correctness | 10.0/10 |
| Portfolio Coverage | 10.0/10 |
| Final Response | 0.0/10 |
| Error Recovery | 10.0/10 |

**Tools used (6/8):** calculate_portfolio_value, calculate_volatility_score, check_risk_threshold, get_portfolio_holdings, get_stock_prices, log_operation

**Missing:** generate_report, send_notification

**Portfolios:** PORT-001, PORT-002, PORT-003

**Turns:** 10 | **Tool calls:** 13 | **Success rate:** 100%

**Issues:**
- No final text response from model

### llama3.2(latest) (ctx-8192)

**Grade: B (8.8/10.0)** | **Classification: success**

> Made 43 tool calls using 8 tools

| Criterion | Score |
|-----------|-------|
| Valid Tool Calls | 10.0/10 |
| Tool Coverage | 10.0/10 |
| Call Ordering | 10.0/10 |
| Argument Correctness | 2.0/10 |
| Portfolio Coverage | 10.0/10 |
| Final Response | 10.0/10 |
| Error Recovery | 10.0/10 |

**Tools used (8/8):** calculate_portfolio_value, calculate_volatility_score, check_risk_threshold, generate_report, get_portfolio_holdings, get_stock_prices, log_operation, send_notification

**Portfolios:** PORT-001, PORT-002, PORT-003

**Turns:** 2 | **Tool calls:** 43 | **Success rate:** 37%

**Issues:**
- 12 argument issue(s)

### llama3.2(latest) (ctx-16384)

**Grade: B (8.4/10.0)** | **Classification: success**

> Made 7 tool calls using 7 tools

| Criterion | Score |
|-----------|-------|
| Valid Tool Calls | 10.0/10 |
| Tool Coverage | 10.0/10 |
| Call Ordering | 10.0/10 |
| Argument Correctness | 4.0/10 |
| Portfolio Coverage | 10.0/10 |
| Final Response | 10.0/10 |
| Error Recovery | 3.0/10 |

**Tools used (7/8):** calculate_portfolio_value, calculate_volatility_score, check_risk_threshold, generate_report, get_portfolio_holdings, get_stock_prices, log_operation

**Missing:** send_notification

**Portfolios:** PORT-001, PORT-002, PORT-003

**Turns:** 2 | **Tool calls:** 7 | **Success rate:** 57%

**Issues:**
- 3 argument issue(s)
- Model stopped making tool calls after encountering errors

### llama3.2(latest) (ctx-32768)

**Grade: D (6.9/10.0)** | **Classification: partial_success**

> Made 2 tool calls but incomplete

| Criterion | Score |
|-----------|-------|
| Valid Tool Calls | 10.0/10 |
| Tool Coverage | 3.3/10 |
| Call Ordering | 0.0/10 |
| Argument Correctness | 10.0/10 |
| Portfolio Coverage | 10.0/10 |
| Final Response | 4.0/10 |
| Error Recovery | 10.0/10 |

**Tools used (2/8):** get_portfolio_holdings, log_operation

**Missing:** calculate_portfolio_value, calculate_volatility_score, check_risk_threshold, generate_report, get_stock_prices, send_notification

**Portfolios:** PORT-001, PORT-002, PORT-003

**Turns:** 2 | **Tool calls:** 2 | **Success rate:** 50%

**Issues:**
- Only 2/8 tools used (need 6 for full score)
- No ordering rules could be checked (too few tool calls)

### llama3.1(8b) (ctx-32768)

**Grade: F (3.5/10.0)** | **Classification: text_narration**

> Described 8 tools in text but made 0 structured calls

| Criterion | Score |
|-----------|-------|
| Valid Tool Calls | 0.0/10 |
| Tool Coverage | 0.0/10 |
| Call Ordering | 0.0/10 |
| Argument Correctness | 0.0/10 |
| Portfolio Coverage | 10.0/10 |
| Final Response | 10.0/10 |
| Error Recovery | 10.0/10 |

**Tools used (0/8):** none

**Missing:** calculate_portfolio_value, calculate_volatility_score, check_risk_threshold, generate_report, get_portfolio_holdings, get_stock_prices, log_operation, send_notification

**Portfolios:** PORT-001, PORT-002, PORT-003

**Turns:** 1 | **Tool calls:** 0 | **Success rate:** 0%

**Issues:**
- Model referenced 8 tool(s) in text but made 0 structured tool_calls
- Only 0/8 tools used (need 6 for full score)

### llama3.1(8b-instruct-q4_K_M) (ctx-32768)

**Grade: F (3.5/10.0)** | **Classification: text_narration**

> Described 8 tools in text but made 0 structured calls

| Criterion | Score |
|-----------|-------|
| Valid Tool Calls | 0.0/10 |
| Tool Coverage | 0.0/10 |
| Call Ordering | 0.0/10 |
| Argument Correctness | 0.0/10 |
| Portfolio Coverage | 10.0/10 |
| Final Response | 10.0/10 |
| Error Recovery | 10.0/10 |

**Tools used (0/8):** none

**Missing:** calculate_portfolio_value, calculate_volatility_score, check_risk_threshold, generate_report, get_portfolio_holdings, get_stock_prices, log_operation, send_notification

**Portfolios:** PORT-001, PORT-002, PORT-003

**Turns:** 1 | **Tool calls:** 0 | **Success rate:** 0%

**Issues:**
- Model referenced 8 tool(s) in text but made 0 structured tool_calls
- Only 0/8 tools used (need 6 for full score)

### mistral(7b-instruct-v0.3-q5_K_M) (ctx-32768)

**Grade: F (3.5/10.0)** | **Classification: text_narration**

> Described 8 tools in text but made 0 structured calls

| Criterion | Score |
|-----------|-------|
| Valid Tool Calls | 0.0/10 |
| Tool Coverage | 0.0/10 |
| Call Ordering | 0.0/10 |
| Argument Correctness | 0.0/10 |
| Portfolio Coverage | 10.0/10 |
| Final Response | 10.0/10 |
| Error Recovery | 10.0/10 |

**Tools used (0/8):** none

**Missing:** calculate_portfolio_value, calculate_volatility_score, check_risk_threshold, generate_report, get_portfolio_holdings, get_stock_prices, log_operation, send_notification

**Portfolios:** PORT-001, PORT-002, PORT-003

**Turns:** 1 | **Tool calls:** 0 | **Success rate:** 0%

**Issues:**
- Model referenced 8 tool(s) in text but made 0 structured tool_calls
- Only 0/8 tools used (need 6 for full score)

### qwen2.5-coder(14b-instruct-q4_K_M) (ctx-32768)

**Grade: F (3.5/10.0)** | **Classification: text_narration**

> Described 6 tools in text but made 0 structured calls

| Criterion | Score |
|-----------|-------|
| Valid Tool Calls | 0.0/10 |
| Tool Coverage | 0.0/10 |
| Call Ordering | 0.0/10 |
| Argument Correctness | 0.0/10 |
| Portfolio Coverage | 10.0/10 |
| Final Response | 10.0/10 |
| Error Recovery | 10.0/10 |

**Tools used (0/8):** none

**Missing:** calculate_portfolio_value, calculate_volatility_score, check_risk_threshold, generate_report, get_portfolio_holdings, get_stock_prices, log_operation, send_notification

**Portfolios:** PORT-001, PORT-002, PORT-003

**Turns:** 1 | **Tool calls:** 0 | **Success rate:** 0%

**Issues:**
- Model referenced 6 tool(s) in text but made 0 structured tool_calls
- Only 0/8 tools used (need 6 for full score)

### qwen2.5-coder(7b) (ctx-32768)

**Grade: F (3.5/10.0)** | **Classification: text_narration**

> Described 8 tools in text but made 0 structured calls

| Criterion | Score |
|-----------|-------|
| Valid Tool Calls | 0.0/10 |
| Tool Coverage | 0.0/10 |
| Call Ordering | 0.0/10 |
| Argument Correctness | 0.0/10 |
| Portfolio Coverage | 10.0/10 |
| Final Response | 10.0/10 |
| Error Recovery | 10.0/10 |

**Tools used (0/8):** none

**Missing:** calculate_portfolio_value, calculate_volatility_score, check_risk_threshold, generate_report, get_portfolio_holdings, get_stock_prices, log_operation, send_notification

**Portfolios:** PORT-001, PORT-002, PORT-003

**Turns:** 1 | **Tool calls:** 0 | **Success rate:** 0%

**Issues:**
- Model referenced 8 tool(s) in text but made 0 structured tool_calls
- Only 0/8 tools used (need 6 for full score)

### qwen2.5-coder(7b-instruct-q5_K_M) (ctx-32768)

**Grade: F (3.5/10.0)** | **Classification: text_narration**

> Described 8 tools in text but made 0 structured calls

| Criterion | Score |
|-----------|-------|
| Valid Tool Calls | 0.0/10 |
| Tool Coverage | 0.0/10 |
| Call Ordering | 0.0/10 |
| Argument Correctness | 0.0/10 |
| Portfolio Coverage | 10.0/10 |
| Final Response | 10.0/10 |
| Error Recovery | 10.0/10 |

**Tools used (0/8):** none

**Missing:** calculate_portfolio_value, calculate_volatility_score, check_risk_threshold, generate_report, get_portfolio_holdings, get_stock_prices, log_operation, send_notification

**Portfolios:** PORT-001, PORT-002, PORT-003

**Turns:** 1 | **Tool calls:** 0 | **Success rate:** 0%

**Issues:**
- Model referenced 8 tool(s) in text but made 0 structured tool_calls
- Only 0/8 tools used (need 6 for full score)

### deepseek-coder-v2(16b) (ctx-32768)

**Grade: F (2.5/10.0)** | **Classification: empty_response**

> No tokens generated, instant return

| Criterion | Score |
|-----------|-------|
| Valid Tool Calls | 0.0/10 |
| Tool Coverage | 0.0/10 |
| Call Ordering | 0.0/10 |
| Argument Correctness | 0.0/10 |
| Portfolio Coverage | 10.0/10 |
| Final Response | 0.0/10 |
| Error Recovery | 10.0/10 |

**Tools used (0/8):** none

**Missing:** calculate_portfolio_value, calculate_volatility_score, check_risk_threshold, generate_report, get_portfolio_holdings, get_stock_prices, log_operation, send_notification

**Portfolios:** PORT-001, PORT-002, PORT-003

**Turns:** 1 | **Tool calls:** 0 | **Success rate:** 0%

**Issues:**
- No tool calls made at all
- Only 0/8 tools used (need 6 for full score)
- No final text response from model

### gemma2(9b-instruct-q4_K_M) (ctx-32768)

**Grade: F (2.5/10.0)** | **Classification: empty_response**

> No tokens generated, instant return

| Criterion | Score |
|-----------|-------|
| Valid Tool Calls | 0.0/10 |
| Tool Coverage | 0.0/10 |
| Call Ordering | 0.0/10 |
| Argument Correctness | 0.0/10 |
| Portfolio Coverage | 10.0/10 |
| Final Response | 0.0/10 |
| Error Recovery | 10.0/10 |

**Tools used (0/8):** none

**Missing:** calculate_portfolio_value, calculate_volatility_score, check_risk_threshold, generate_report, get_portfolio_holdings, get_stock_prices, log_operation, send_notification

**Portfolios:** PORT-001, PORT-002, PORT-003

**Turns:** 1 | **Tool calls:** 0 | **Success rate:** 0%

**Issues:**
- No tool calls made at all
- Only 0/8 tools used (need 6 for full score)
- No final text response from model

### gemma3(12b-it-q4_K_M) (ctx-32768)

**Grade: F (2.5/10.0)** | **Classification: empty_response**

> No tokens generated, instant return

| Criterion | Score |
|-----------|-------|
| Valid Tool Calls | 0.0/10 |
| Tool Coverage | 0.0/10 |
| Call Ordering | 0.0/10 |
| Argument Correctness | 0.0/10 |
| Portfolio Coverage | 10.0/10 |
| Final Response | 0.0/10 |
| Error Recovery | 10.0/10 |

**Tools used (0/8):** none

**Missing:** calculate_portfolio_value, calculate_volatility_score, check_risk_threshold, generate_report, get_portfolio_holdings, get_stock_prices, log_operation, send_notification

**Portfolios:** PORT-001, PORT-002, PORT-003

**Turns:** 1 | **Tool calls:** 0 | **Success rate:** 0%

**Issues:**
- No tool calls made at all
- Only 0/8 tools used (need 6 for full score)
- No final text response from model

### hf.co__unsloth__gpt-oss-20b-GGUF(Q4_K_M) (ctx-32768)

**Grade: F (2.5/10.0)** | **Classification: stalled_inference**

> No tokens generated after 84s

| Criterion | Score |
|-----------|-------|
| Valid Tool Calls | 0.0/10 |
| Tool Coverage | 0.0/10 |
| Call Ordering | 0.0/10 |
| Argument Correctness | 0.0/10 |
| Portfolio Coverage | 10.0/10 |
| Final Response | 0.0/10 |
| Error Recovery | 10.0/10 |

**Tools used (0/8):** none

**Missing:** calculate_portfolio_value, calculate_volatility_score, check_risk_threshold, generate_report, get_portfolio_holdings, get_stock_prices, log_operation, send_notification

**Portfolios:** PORT-001, PORT-002, PORT-003

**Turns:** 1 | **Tool calls:** 0 | **Success rate:** 0%

**Issues:**
- No tool calls made at all
- Only 0/8 tools used (need 6 for full score)
- No final text response from model

### hf.co__unsloth__gpt-oss-20b-GGUF(Q5_K_M) (ctx-32768)

**Grade: F (2.5/10.0)** | **Classification: stalled_inference**

> No tokens generated after 74s

| Criterion | Score |
|-----------|-------|
| Valid Tool Calls | 0.0/10 |
| Tool Coverage | 0.0/10 |
| Call Ordering | 0.0/10 |
| Argument Correctness | 0.0/10 |
| Portfolio Coverage | 10.0/10 |
| Final Response | 0.0/10 |
| Error Recovery | 10.0/10 |

**Tools used (0/8):** none

**Missing:** calculate_portfolio_value, calculate_volatility_score, check_risk_threshold, generate_report, get_portfolio_holdings, get_stock_prices, log_operation, send_notification

**Portfolios:** PORT-001, PORT-002, PORT-003

**Turns:** 1 | **Tool calls:** 0 | **Success rate:** 0%

**Issues:**
- No tool calls made at all
- Only 0/8 tools used (need 6 for full score)
- No final text response from model

### phi4(14b-q4_K_M) (ctx-32768)

**Grade: F (2.5/10.0)** | **Classification: empty_response**

> No tokens generated, instant return

| Criterion | Score |
|-----------|-------|
| Valid Tool Calls | 0.0/10 |
| Tool Coverage | 0.0/10 |
| Call Ordering | 0.0/10 |
| Argument Correctness | 0.0/10 |
| Portfolio Coverage | 10.0/10 |
| Final Response | 0.0/10 |
| Error Recovery | 10.0/10 |

**Tools used (0/8):** none

**Missing:** calculate_portfolio_value, calculate_volatility_score, check_risk_threshold, generate_report, get_portfolio_holdings, get_stock_prices, log_operation, send_notification

**Portfolios:** PORT-001, PORT-002, PORT-003

**Turns:** 1 | **Tool calls:** 0 | **Success rate:** 0%

**Issues:**
- No tool calls made at all
- Only 0/8 tools used (need 6 for full score)
- No final text response from model

---

*Report generated by evaluate_agentic_chat.py*
