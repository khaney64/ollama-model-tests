# Model Recommendations for OpenClaw GPU Usage (RTX 4070 12GB)

Generated: 2026-03-03

Context: Recommendations for using local Ollama models via OpenClaw at 32K context
(OpenClaw's recommended default, warns below this), prioritizing agentic capabilities
with occasional coding subtasks.

> **Critical caveat: Structured tool calling is the gating factor, not text benchmarks.**
>
> The `agentic-chat` task tests structured tool calling via `/api/chat` -- the actual
> protocol OpenClaw uses. Of 20 local models tested (including 3 qwen3:8b quantization
> variants), **only 7 model families can produce any structured tool calls at all**.
> The other 12 -- including models that score A on text-based agentic
> benchmarks -- fail silently: they return empty responses, stall, or describe tool calls
> in prose without producing the JSON wire format. A model that can't make structured
> tool_calls is useless for OpenClaw regardless of how well it writes code.
>
> **This document weights agentic-chat as the primary evaluation signal for OpenClaw
> suitability.** Agentic (text) and engine scores serve as secondary quality indicators
> for coding subtasks.

### Benchmark Methodology Update

The agentic-chat benchmark has been updated to more closely resemble how OpenClaw
operates:

- **Temperature settings**: Size-dependent (0.2 for 3B, 0.3 for 7-8B, 0.4 for 12B+)
  to balance creativity with structured output reliability
- **Spin/retry handling**: Models that stall or produce empty responses are nudged with
  retry prompts, matching OpenClaw's retry behavior
- **Improved tool instructions**: System message includes clearer guidance on structured
  tool_call format, reducing false negatives from prompt ambiguity
- **Context management**: Old conversation turns are pruned when context pressure exceeds
  thresholds, simulating how OpenClaw manages long conversations

These changes mean the benchmark results are a better predictor of real OpenClaw
performance than earlier runs. Models that still fail under these improved conditions
are genuinely incompatible with the protocol.

---

## Overall Results Summary

### Cloud Models (Baseline / Quality Ceiling)

All 5 cloud models scored A or B on the agentic task and A on engine:

| Model | Agentic Grade | Engine Grade | Agentic Time (s) | Engine Time (s) |
|-------|---------------|--------------|-------------------|-----------------|
| kimi-k2.5 | A (10.0) | A (9.6) | 83 | 93 |
| glm-4.7 | A (9.2) | A (10.0) | 115 | 56 |
| glm-5 | A (9.2) | A (9.7) | 68 | 107 |
| qwen3-coder-next | B (8.5) | A (9.7) | 49 | 45 |
| minimax-m2.5 | B (8.3) | A (10.0) | 88 | 104 |

Cloud models set the quality bar. The best local models approach but don't quite match
the top cloud scores, especially on agentic tasks.

### Agentic-Chat Results (36 Evaluations, 4 Context Sizes)

The agentic-chat task runs multi-turn structured tool calling against 8 portfolio analysis
tools. Models were tested at ctx-8192, ctx-10240, ctx-16384, and ctx-32768 (where
supported). Multiple qwen3:8b quantization variants (Q4_K_M, Q6_K, Q8_0) were tested.
qwen3.5:9b was added as a new model.

**Grade distribution:** 21 A, 2 B, 1 D, 12 F

**Outcome classification:**
- **Success** (structured tool calls, completed with final response): 22 evaluations
- **Partial Success** (tool calls made but no final text response): 2 evaluations
- **Text Narration** (described tools in prose, 0 structured calls): 6 evaluations
- **Empty Response** (no tokens, instant return): 4 evaluations
- **Stalled Inference** (loaded model, burned time, 0 tokens): 2 evaluations

**7 model families produced structured tool calls:**

| Model | ctx-8192 | ctx-10240 | ctx-16384 | ctx-32768 | Best |
|-------|----------|-----------|-----------|-----------|------|
| glm-4.7-flash:q4_K_M | A (10.0) | A (9.8) | A (10.0) | A (10.0) | 10.0 |
| qwen2.5:7b | - | - | A (10.0) | A (10.0) | 10.0 |
| qwen3:8b (Q4_K_M) | A (10.0) | A (9.0) | A (10.0) | A (10.0) | 10.0 |
| qwen3:8b Q6_K | - | A (10.0) | A (10.0) | *(not retested)* | 10.0 |
| qwen3:8b Q8_0 | - | A (10.0) | A (10.0) | *(not retested)* | 10.0 |
| qwen3:14b | A (9.8) | A (10.0) | A (10.0) | A (10.0) | 10.0 |
| qwen3.5:9b | - | - | A (10.0) | A (10.0) | 10.0 |
| llama3.2:latest | B (8.8) | A (9.1) | B (8.4) | D (6.9) | 9.1 |

**All 12 other models scored F (0 structured tool calls):**
- gpt-oss-20b Q4_K_M/Q5_K_M -- `stalled_inference` / `empty_response` at both 16K and 32K
- qwen2.5-coder 7b/7b-instruct/14b-instruct -- `text_narration` (described tools in prose)
- phi4:14b-q4_K_M -- `empty_response`
- gemma2:9b-instruct, gemma3:12b-it -- `empty_response`
- deepseek-coder-v2:16b -- `empty_response`
- llama3.1:8b, llama3.1:8b-instruct -- `text_narration`
- mistral:7b-instruct-v0.3-q5_K_M -- `text_narration`

**Notable findings:**
- qwen2.5:7b (the base model) succeeds at tool calling while all three
  qwen2.5-coder variants (7b, 7b-instruct, 14b-instruct) fail with `text_narration`.
  Code-tuning appears to have degraded structured tool-calling ability.
- qwen3.5:9b is a new 9B model that achieves perfect A (10.0) at both 16K and 32K context,
  with 68 tok/s at 32K and only 10.5 GB VRAM -- a strong new option between qwen3:8b and qwen3:14b.
- gpt-oss-20b now tested at 16K and 32K (was only 8K before) -- still completely fails.

---

## Context Size Impact on Performance

### Speed Degradation at Higher Context

The 14B+ models show significant speed drops at 16K+ context due to KV cache spilling
to system RAM. The 7-8B models are largely unaffected.

| Model | Size | 8K tok/s | 16K tok/s | 32K tok/s | Fits 32K in VRAM? |
|-------|------|----------|-----------|-----------|-------------------|
| **7-8B Models** | | | | | |
| llama3.2:latest | 2.0 GB | 172 | 177 | 179 | Yes (8.0 GB) |
| qwen2.5:7b | 4.7 GB | - | 89 | 91 | Yes (8.8 GB) |
| qwen3:8b (Q4_K_M) | 5.2 GB | 74 | 73 | 74 | Yes (10.7 GB) |
| qwen3.5:9b | 5.8 GB | - | 68 | 68 | Yes (10.5 GB) |
| qwen3:8b Q6_K | 6.6 GB | - | 60 | 27 | Marginal (11.4 GB) |
| qwen3:8b Q8_0 | 8.5 GB | - | 31 | 16 | No (11.6 GB) |
| **14B+ Models** | | | | | |
| qwen3:14b | 9.3 GB | 42 | 23 | **14** | No (11.5 GB) |
| glm-4.7-flash:q4_K_M | 19.0 GB | 15 | 13 | 9 | No (11.2 GB) |

### Agentic-Chat Wall Time (Total Conversation Duration)

Per-token speed doesn't tell the full story for multi-turn tool calling. Total wall time
depends on turn count, tool dispatch overhead, and retry handling. Models that complete
the task in fewer turns finish faster even if their per-token speed is lower.

| Model | ctx-16384 | ctx-32768 | Turns (32K) | Tool Calls (32K) |
|-------|-----------|-----------|-------------|------------------|
| qwen2.5:7b | 48s | **29s** | 2 | 27 |
| qwen3.5:9b | 67s | **78s** | 9 | 22 |
| qwen3:8b (Q4_K_M) | 74s | **109s** | 13 | 16 |
| llama3.2:latest | 16s | 9s | 2 | 2 (degraded) |
| glm-4.7-flash:q4_K_M | 190s | 285s | 5 | 16 |
| qwen3:14b | 118s | **743s** | 15 | 28 |
| qwen3:8b Q6_K | 69s | *(not retested)* | - | - |
| qwen3:8b Q8_0 | 88s | *(not retested)* | - | - |

**Key takeaway:** qwen2.5:7b completes the entire 27-tool-call conversation in just 29
seconds at 32K -- the fastest to complete. qwen3.5:9b follows in 78 seconds with 22 tool
calls across 9 turns. qwen3:8b finishes in 109 seconds with 16 tool calls across 13 turns.
All three are comfortably interactive. qwen3:14b at 743s (~12 min) is not suitable for
interactive 32K use -- use 16K instead (118s, 3 turns, 24 calls).

### CPU Spillover Evidence

**Yes, larger models are clearly spilling to CPU at 16K+ context.** The evidence:

1. **VRAM stays capped around 11-11.7 GB** for all 14B+ models regardless of context
   size, while 7-8B models show VRAM increasing proportionally with context.

2. **Speed halving** on 14B+ models (44 -> 23 -> 14 tok/s for qwen3:14b at 8K/16K/32K)
   is the classic symptom of partial CPU offload.

3. **7-8B models show no speed loss** at 16K-32K because their smaller weights leave
   enough VRAM headroom for the larger KV cache.

4. **qwen3:8b Q6_K and Q8_0 show spillover at 32K** -- Q6_K drops from 60 to 27
   tok/s (55% loss), Q8_0 from 31 to 16 tok/s (48% loss). Their larger weight files
   leave less room for the 32K KV cache. This confirms Q4_K_M is the right quantization
   for 32K context on a 12GB card. (Q6_K and Q8_0 not retested at 32K in current run
   due to diminishing returns.)

5. **qwen3.5:9b maintains speed at 32K** -- at 5.8 GB the weights leave ample VRAM for
   the KV cache, resulting in 68 tok/s at both 16K and 32K with only 10.5 GB VRAM used.

### Quantization Impact: qwen3:8b Variants (Q4_K_M vs Q6_K vs Q8_0)

Now tested at both 16K and 32K context. **Higher quantization still buys nothing for
tool-calling quality while destroying 32K viability.**

| Variant | Size | ctx-16384 | ctx-32768 | tok/s (16K) | tok/s (32K) | VRAM (32K) |
|---------|------|-----------|-----------|-------------|-------------|------------|
| Q4_K_M (default) | 5.2 GB | A (10.0) | A (10.0) | 73 | 74 | 10.7 GB |
| Q6_K | 6.6 GB | A (10.0) | A (10.0) | 60 | **27** | 11.4 GB |
| Q8_0 | 8.5 GB | A (10.0) | A (10.0) | 31 | **16** | 11.6 GB |

**Key findings:**

1. **Quality is identical at all contexts.** All three variants achieve perfect 10.0 at
   both 16K and 32K, with 100% tool call success rates and correct ordering.

2. **32K reveals the real cost of higher quant.** At 16K, Q6_K is 18% slower; at 32K it's
   **64% slower** (27 vs 74 tok/s) because the KV cache plus larger weights exceed VRAM
   capacity. Q8_0 at 32K is **78% slower** (16 tok/s).

**Total wall time diverges dramatically at 32K.** Q4_K_M completes in 109s; Q6_K and
Q8_0 were not retested at 32K in the current run (prior run: Q6_K ~147s, Q8_0 ~323s)
-- for identical quality output at 16K.

**Bottom line:** Stick with Q4_K_M. Higher quantization buys nothing for structured tool
calling while sacrificing speed and 32K context viability.

---

## Recommended Models for OpenClaw

**OpenClaw requires structured tool calling.** Only 6 of 17+ tested model families can
produce structured tool_calls via `/api/chat`. The recommendations below are filtered
to this viable set, then ranked by combined agentic-chat quality, speed, and wall time.

### Tier 1: Top Picks

#### qwen3:8b (Q4_K_M) -- BEST OVERALL FOR OPENCLAW
- **Agentic-Chat:** A (10.0) at all 4 contexts tested (8K/10K/16K/32K), except A (9.0) at 10K
- **Agentic (text):** A (9.7) at 10K; B (8.8) at 8K/16K
- **Engine:** A (9.9) at 10K/16K
- **Speed at 32K:** 74 tok/s chat (no degradation -- 5.2GB model still fits in VRAM)
- **Wall time at 32K:** 109 seconds for 16 tool calls in 13 turns
- **VRAM at 32K:** 10.7 GB (fits on RTX 4070 12GB)
- **Why:** Perfect structured tool calling at OpenClaw's recommended 32K context with
  strong overall wall time among quality models. Uses 6/8 tools at 32K with 16 tool calls
  across 13 turns -- reliable and consistent. Combined with A (9.9) engine scores for
  coding subtasks, this is the best all-rounder for mixed workloads.
- **Under improved test conditions:** With temperature 0.3 and enhanced tool instructions
  matching OpenClaw's setup, results are consistent and reproducible.
- **Quantization tested:** Q6_K and Q8_0 score identical quality but are 2-5x slower at
  32K due to VRAM spillover. Q4_K_M is the right quantization for this card.
- **CPU agentic:** A (9.1)

#### qwen2.5:7b -- FASTEST PERFECT TOOL CALLER
- **Agentic-Chat:** A (10.0) at both ctx-16384 and ctx-32768
- **Agentic (text):** A (9.0) at 16K; B (8.8) at 32K
- **Engine:** B (8.7) -- correct logic, some share sign inversions in worked examples
- **Speed at 32K:** 91 tok/s chat (no degradation -- 4.7GB model has ample VRAM headroom)
- **Wall time at 32K:** **29 seconds** for 27 tool calls in just 2 turns
- **VRAM at 32K:** 8.8 GB (very comfortable on RTX 4070 12GB)
- **Why:** The fastest model to complete the full tool-calling workflow. At 29 seconds
  total wall time, it's 3.8x faster than qwen3:8b and 26x faster than qwen3:14b (at 32K).
  Achieves this by batching all tool calls into just 2 turns. Uses 8/8 tools at 32K with
  27 calls and 89% success rate. The 8.8 GB VRAM footprint at 32K leaves 3+ GB headroom,
  ensuring zero risk of CPU spillover.
- **Tradeoff:** Engine score (B 8.7) is a step below qwen3:8b (A 9.9) -- for pure tool
  orchestration this doesn't matter, but coding subtasks will be less precise.
- **Notable:** The base qwen2.5:7b succeeds at tool calling while all three qwen2.5-coder
  variants fail with `text_narration`. Code-tuning broke tool calling.
- **Only tested at 16K/32K** -- but perfect at both, suggesting robust tool-calling support.

#### qwen3:14b -- HIGHEST QUALITY, REDUCED CONTEXT RECOMMENDED
- **Agentic-Chat:** A (10.0) at ctx-10240/16384/32768; A (9.8) at ctx-8192
- **Agentic (text):** A (10.0) at 16K -- perfect score, the only local model to achieve this
- **Engine:** A (9.8) at 16K
- **Speed at 16K:** 23 tok/s chat | **Speed at 32K:** 14 tok/s chat
- **Wall time at 16K:** 118s (~2 min) | **Wall time at 32K:** 743s (~12.4 min)
- **VRAM:** 11.3-11.6 GB (capped at all sizes -- KV cache spilling to system RAM)
- **Why:** The highest quality model that can do structured tool calling. Perfect 10.0 on
  agentic-chat at three context sizes, perfect 10.0 on text agentic, near-perfect engine.
  At 16K it completes in 118s with 24 tool calls across just 3 turns (8/8 tools, 96%
  success) -- efficient and well-structured. At 32K it scores 10.0 but takes 743s with
  28 tool calls across 15 turns.
- **Tradeoff:** At 14 tok/s (32K) or 23 tok/s (16K), it's noticeably slower than the 8B
  models. The 743s wall time at 32K makes it unsuitable for interactive use; use 16K
  instead. If OpenClaw sends concurrent requests, this model will bottleneck.
- **If using this model:** ctx-16384 is the practical sweet spot. At 16K, the benchmark
  scored perfect 10.0 with 24 tool calls across just 3 turns (8/8 tools), completing in
  just 118s (~2 min) at 23 tok/s. The quality edge over qwen3:8b (perfect text agentic
  10.0 vs 8.8) may justify the speed penalty for quality-critical workloads.
- **CPU agentic:** A (9.5)

#### qwen3.5:9b -- NEW: STRONG 32K OPTION, FAST AND EFFICIENT
- **Agentic-Chat:** A (10.0) at ctx-16384 and ctx-32768
- **Agentic (text):** Not yet evaluated
- **Engine:** Not yet evaluated
- **Speed at 32K:** 68 tok/s chat (no degradation -- 5.8GB model fits in VRAM at 32K)
- **Wall time at 32K:** 78 seconds for 22 tool calls in 9 turns
- **VRAM at 32K:** 10.5 GB (fits on RTX 4070 12GB)
- **Why:** New 9B model that achieves perfect A (10.0) at both 16K and 32K with 68 tok/s
  and 10.5 GB VRAM at 32K. Wall time of 78s at 32K places it between qwen2.5:7b (29s)
  and qwen3:8b (109s). Uses 6/8 tools with 100% success rate and context management
  active (37% peak pressure at 16K, 20% at 32K).
- **Tradeoff:** Agentic text and engine scores not yet evaluated -- quality on coding
  subtasks is unknown. The 5.8 GB model leaves less VRAM headroom than qwen2.5:7b (4.7 GB)
  but more than qwen3:8b (5.2 GB). Engine evaluation needed before recommending for
  coding-heavy workloads.
- **Verdict:** Promising fast option for pure tool orchestration at 32K; evaluate engine
  quality before using for coding subtasks.

### Tier 2: Usable But Limited

#### glm-4.7-flash:q4_K_M -- PERFECT TOOL CALLING, TOO SLOW
- **Agentic-Chat:** A (10.0) at ctx-8192/16384/32768; A (9.8) at ctx-10240
- **Agentic (text):** A (9.2) at 10K; B (8.7) at 8K; timeout at 16K
- **Engine:** A (9.9) at 8K; A (9.4) at 16K; F at 10K
- **Speed at 32K:** 8.7 tok/s chat | **Wall time at 32K:** 285s (~4.75 min)
- **VRAM:** 11.2-11.7 GB (model is 19GB, heavily spilling to CPU at all sizes)
- **Why:** The most consistent tool caller tested -- perfect 10.0 at 3 of 4 context sizes.
  16 tool calls per run, 6/8 tools, 100% success rate, correct ordering. Its cloud sibling
  (glm-4.7) also scored top marks.
- **Tradeoff:** At 19GB it can't fit in VRAM and runs at CPU speed. Text-generation tasks
  time out at 16K+. Only viable if response time is not critical and tool-calling
  reliability is paramount.

#### llama3.2:latest -- FAST BUT LOW QUALITY, DEGRADES AT 32K
- **Agentic-Chat:** A (9.1) at ctx-10240; B (8.8) at ctx-8192; B (8.4) at ctx-16384; **D (6.9) at ctx-32768**
- **Agentic (text):** B (8.2-8.3) across contexts
- **Engine:** F across all GPU contexts (syntax errors, no output)
- **Speed at 32K:** 179 tok/s chat (fast, but only 2 tool calls made)
- **Why:** Can make structured tool calls at lower contexts with all 8/8 tools used.
- **Problem at 32K:** Quality degrades to D (6.9) -- only 2 tool calls, 2/8 tools. The 3B
  model loses coherence at OpenClaw's recommended context size. At 16K, argument error
  rate is high and error recovery scored 3.0/10. Not reliable enough for production use.

---

## Models to AVOID for OpenClaw

### Cannot Make Structured Tool Calls (Unusable for OpenClaw)

These models all scored **F on agentic-chat** despite many scoring well on text benchmarks.
They are fundamentally incompatible with OpenClaw's `/api/chat` tool-calling protocol.

| Model | Agentic (text) | Engine | Chat Failure | Why |
|-------|----------------|--------|--------------|-----|
| **gpt-oss-20b Q4_K_M** | A (9.1) | A (9.8) | `stalled` 16K+32K | Loaded model, burned 300s, produced 0 tokens at both 16K and 32K. Strong on text but cannot use `/api/chat` tools. |
| **gpt-oss-20b Q5_K_M** | A (9.8) | F (4.5) | `empty`/`stalled` | Empty at 16K, stalled at 32K. Near-perfect text agentic score is misleading for OpenClaw. |
| **phi4:14b-q4_K_M** | A (9.0) | A (9.9) | `empty_response` | Instant return, 0 tokens. One of the best text+engine models, completely broken for tool calling. |
| **qwen2.5-coder:14b** | B (8.7) | A (9.0-9.7) | `text_narration` | Described 6 tools in prose, made 0 structured calls. |
| **qwen2.5-coder:7b-instruct** | A (9.2) | B (8.8) | `text_narration` | Same narration failure. Understands tools conceptually, can't produce the wire format. |
| **qwen2.5-coder:7b** | B (8.3-8.7) | D-B | `text_narration` | Same narration failure. |
| **gemma3:12b-it** | A (9.2) at 16K | A (9.6) at 16K | `empty_response` | 0 tokens, instant return. Strong text model, no tool support. |
| **gemma2:9b-instruct** | B (8.2-8.5) | A (9.4) at 8K | `empty_response` | Same instant-return failure. |
| **deepseek-coder-v2:16b** | B (8.1) | A (9.1) at 16K | `empty_response` | 0 tokens. Also too slow (11 tok/s at 16K). |
| **llama3.1:8b** | D-B | F mostly | `text_narration` | Described 8 tools, 0 structured calls. |
| **llama3.1:8b-instruct** | A (9.1) at 8K | F-A | `text_narration` | Described 8 tools, 0 structured calls. |
| **mistral:7b-instruct** | B (8.3-8.7) | B-F | `text_narration` | Described 8 tools, 0 structured calls. |

### Key Insight: Text Benchmarks Don't Predict Tool-Calling Ability

The correlation between agentic (text) scores and agentic-chat (tool calling) scores is
nearly zero across the tested models:

- **gpt-oss-20b Q5_K_M**: #2 on text agentic (9.8), F on tool calling (stalled at 16K+32K)
- **phi4:14b**: A (9.0) on text, F on tool calling (empty response)
- **qwen2.5-coder:7b-instruct**: A (9.2) on text, F on tool calling (narration)
- **qwen2.5:7b** (base model): A (9.0) on text, **A (10.0) on tool calling** -- succeeds
  where all three qwen2.5-coder variants fail. Code-tuning broke tool calling.
- **qwen3.5:9b**: New 9B model, **A (10.0) on tool calling** at 16K and 32K --
  joins the short list of models that reliably produce structured tool calls.

This is exactly why the agentic-chat task exists. Models that can write *about* tools
in generated code (the text agentic task) are not necessarily able to produce the structured
JSON tool_calls that `/api/chat` requires. For OpenClaw, only the latter matters.

---

## Final Recommendation Summary

### For OpenClaw -- Structured Tool Calling is Required

**Primary Model (Best All-Rounder):**
> **qwen3:8b @ 32K context** -- Perfect agentic-chat (10.0) at OpenClaw's recommended 32K
> context, excellent engine (9.9), 74 tok/s with no speed degradation, 109 second total
> wall time for 16 tool calls in 13 turns. The 5.2GB model fits entirely in VRAM
> at 32K (10.7 GB used). Best combination of tool-calling reliability, coding quality,
> and interactive speed.

**Speed-First Alternative (Fastest Completion):**
> **qwen2.5:7b @ 32K context** -- Perfect agentic-chat (10.0) at 32K, completes the full
> 27-tool-call workflow in just **29 seconds** (3.8x faster than qwen3:8b). Uses 91 tok/s
> with only 8.8 GB VRAM -- the most headroom of any recommended model. Weaker on engine
> (B 8.7 vs A 9.9) so coding subtasks won't be as precise, but for pure tool orchestration
> it's the fastest option available.

**Quality-First Alternative (Reduced Context):**
> **qwen3:14b @ 16K context** -- Perfect agentic-chat (10.0) at 16K, perfect text agentic
> (10.0), near-perfect engine (9.8). **Must reduce context from OpenClaw's 32K default**
> to 16K for usable speed (23 tok/s, 118s total). At 32K it still scores 10.0 but takes
> 743s (~12 min) at 14 tok/s -- unsuitable for interactive use. Worth the config override
> if coding quality matters more than speed.

**New Fast Option (Pending Engine Evaluation):**
> **qwen3.5:9b @ 32K context** -- Perfect agentic-chat (10.0) at 32K, 68 tok/s, 78s total
> wall time for 22 tool calls in 9 turns. Fits entirely in VRAM (10.5 GB). Engine/coding
> quality not yet evaluated -- promising for tool orchestration but needs engine benchmarking
> before recommending for coding-heavy workloads.

**NOT Recommended Despite Strong Text Scores:**
> **gpt-oss-20b**, **phi4:14b**, **qwen2.5-coder** (all variants), **gemma2/3**,
> **deepseek-coder-v2**, **llama3.1**, **mistral** -- all score F on structured tool
> calling. These models cannot be used with OpenClaw for agentic workflows.

**Not Ready for Production:**
> **llama3.2** -- can make structured tool calls but too inconsistent (argument errors,
> 32K quality degradation to D). Not reliable enough for production use.

**Pending Evaluation:**
> **qwen3.5:9b** -- tool-calling A (10.0) confirmed but engine/coding quality not yet
> evaluated. Run the engine task to determine suitability for coding-heavy workloads.

### Suggested OpenClaw Configuration

```
Primary Agent:    qwen3:8b       @ 32K context  (best all-rounder: quality + speed + reliability)
Speed Alt:        qwen2.5:7b     @ 32K context  (29s completion, fastest; weaker coding)
New Fast:         qwen3.5:9b     @ 32K context  (78s, 68 tok/s, pending engine eval)
Quality Alt:      qwen3:14b      @ 16K context  (override default -- 32K takes 12 min at 14 tok/s)
```

### Which Model for What Workload?

| Workload | Best Model | Why |
|----------|-----------|-----|
| **Mixed (tool calling + coding)** | qwen3:8b | A (9.9) engine + A (10.0) chat = best at both |
| **Pure tool orchestration** | qwen2.5:7b | 29s wall time, perfect chat, coding less important |
| **Fast + quality (unknown coding)** | qwen3.5:9b | 78s wall time, 68 tok/s, A chat -- pending engine eval |
| **Quality-critical coding** | qwen3:14b @ 16K | Perfect text agentic (10.0), best engine (9.8) |
| **Maximum throughput** | qwen2.5:7b | 91 tok/s, 8.8 GB VRAM, can handle concurrent requests |
| **Memory-constrained** | qwen2.5:7b | Only 8.8 GB at 32K, leaves room for other processes |

### Does the 32K Context Actually Get Used?

Probably not for agentic-chat workloads. The multi-turn conversation (system message +
user message + tool call/response round trips) typically consumes 4-8K tokens. The
benchmark's qwen3:8b runs used 16 tool calls across 13 turns at 32K with context pressure
well below the 32K limit. The 32K headroom is insurance for longer conversations, not a
current requirement. This is good news: quality scores at 32K are genuine, not artifacts
of context pressure, and the VRAM/speed tradeoffs are worth making for the safety margin.

---

*Analysis based on automated benchmark reports from cpu, gpu (ctx-8192/10240/16384/32768),
and cloud modes. 20 local models tested. Benchmark updated with temperature settings,
spin/retry nudge handling, improved tool instructions, and context management -- matching
OpenClaw's operational behavior. Agentic-chat evaluation is 100% automated (structured
calls are machine-checkable). Agentic (text) manual review sections use placeholder 50%
scores. Engine evaluation is fully automated.*
