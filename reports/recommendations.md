# Model Recommendations for OpenClaw GPU Usage (RTX 4070 12GB)

Generated: 2026-02-19

Context: Recommendations for using local Ollama models via OpenClaw at 32K context
(OpenClaw's recommended default, warns below this), prioritizing agentic capabilities
with occasional coding subtasks.

> **Critical caveat: Structured tool calling is the gating factor, not text benchmarks.**
>
> The `agentic-chat` task tests structured tool calling via `/api/chat` -- the actual
> protocol OpenClaw uses. Of 19 local models tested (17 unique architectures + 2 quantization variants), **only 5
> model families can produce any structured tool calls at all**. The other 12 -- including models that score A on text-based agentic
> benchmarks -- fail silently: they return empty responses, stall, or describe tool calls
> in prose without producing the JSON wire format. A model that can't make structured
> tool_calls is useless for OpenClaw regardless of how well it writes code.
>
> **This document weights agentic-chat as the primary evaluation signal for OpenClaw
> suitability.** Agentic (text) and engine scores serve as secondary quality indicators
> for coding subtasks.

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

### Agentic-Chat Results (34 Evaluations, 4 Context Sizes)

The agentic-chat task runs multi-turn structured tool calling against 8 portfolio analysis
tools. Models were tested at ctx-8192, ctx-10240, ctx-16384, and ctx-32768 (where supported).
Two additional qwen3:8b quantization variants (Q6_K and Q8_0) were tested at ctx-10240/16384.

**Grade distribution:** 19 A, 2 B, 1 D, 12 F

**Outcome classification:**
- **Success** (structured tool calls, completed): 20 evaluations
- **Partial Success** (tool calls but incomplete): 2 evaluations
- **Text Narration** (described tools in prose, 0 structured calls): 6 evaluations
- **Empty Response** (no tokens, instant return): 4 evaluations
- **Stalled Inference** (loaded model, burned time, 0 tokens): 2 evaluations

**5 model families produced structured tool calls:**

| Model | ctx-8192 | ctx-10240 | ctx-16384 | ctx-32768 | Best |
|-------|----------|-----------|-----------|-----------|------|
| glm-4.7-flash:q4_K_M | A (10.0) | A (9.8) | A (10.0) | A (10.0) | 10.0 |
| qwen2.5:7b | - | - | A (10.0) | A (10.0) | 10.0 |
| qwen3:8b (Q4_K_M) | A (10.0) | A (9.0) | A (10.0) | A (10.0) | 10.0 |
| qwen3:8b Q6_K | - | A (10.0) | A (10.0) | - | 10.0 |
| qwen3:8b Q8_0 | - | A (10.0) | A (10.0) | - | 10.0 |
| qwen3:14b | A (9.8) | A (10.0) | A (10.0) | A (10.0) | 10.0 |
| llama3.2:latest | B (8.8) | A (9.1) | B (8.4) | D (6.9) | 9.1 |

**All 12 other models scored F (0 structured tool calls):**
- gpt-oss-20b Q4_K_M/Q5_K_M -- `stalled_inference` (loaded model, 0 tokens after 74-84s)
- qwen2.5-coder 7b/7b-instruct/14b-instruct -- `text_narration` (described tools in prose)
- phi4:14b-q4_K_M -- `empty_response`
- gemma2:9b-instruct, gemma3:12b-it -- `empty_response`
- deepseek-coder-v2:16b -- `empty_response`
- llama3.1:8b, llama3.1:8b-instruct -- `text_narration`
- mistral:7b-instruct-v0.3-q5_K_M -- `text_narration`

**Notable:** qwen2.5:7b (the base model) succeeds at tool calling while all three
qwen2.5-coder variants (7b, 7b-instruct, 14b-instruct) fail with `text_narration`.
The code-tuning appears to have degraded structured tool-calling ability in the coder
variants.

### GPU Mode -- Agentic (Text) and Engine (46 Evaluations Each)

**Agentic grade distribution:** 13 A, 25 B, 6 C, 1 D, 1 N/A (timeout)
**Engine grade distribution:** 18 A, 8 B, 4 D, 15 F

### CPU Mode (14 Local Models, Default Context)

**Agentic grade distribution:** 5 A, 5 B, 1 C, 3 D
**Engine grade distribution:** 6 A, 3 B, 3 C, 3 F

---

## Context Size Impact on Performance

### Speed Degradation at 16K Context

The 14B+ models show significant speed drops when going from 8K to 16K context.
The 7-8B models are largely unaffected.

| Model | Size | 8K tok/s | 16K tok/s | Speed Loss | Fits in VRAM? |
|-------|------|----------|-----------|------------|---------------|
| **7-8B Models** | | | | | |
| llama3.2:latest | 2.0 GB | 167 | 167 | ~0% | Yes (5.9 GB) |
| qwen2.5:7b | 4.7 GB | - | 89 | N/A (16K/32K only) | Yes (7.2 GB) |
| qwen2.5-coder:7b | 4.7 GB | 88 | 89 | ~0% | Yes (6.5 GB) |
| qwen2.5-coder:7b-instruct-q5_K_M | 5.4 GB | 79 | 78 | ~0% | Yes (8.0 GB) |
| qwen3:8b (Q4_K_M) | 5.2 GB | 72 | 71 | ~1% | Yes (9.0 GB) |
| qwen3:8b Q6_K | 6.6 GB | - | 59 | N/A | Marginal (10.5 GB) |
| qwen3:8b Q8_0 | 8.5 GB | - | 49 | N/A | Marginal (11.5 GB) |
| mistral:7b-instruct-v0.3-q5_K_M | 5.1 GB | 77 | 77 | ~0% | Yes (8.9 GB) |
| llama3.1:8b | 4.9 GB | 83 | 84 | ~0% | Yes (8.5 GB) |
| llama3.1:8b-instruct-q4_K_M | 4.9 GB | 83 | 84 | ~0% | Yes (8.0 GB) |
| gemma2:9b-instruct-q4_K_M | 5.8 GB | 60 | 60 | ~0% | Yes (10.6 GB) |
| gemma3:12b-it-q4_K_M | 8.1 GB | 51 | 50 | ~1% | Yes (11.4 GB) |
| **14B+ Models** | | | | | |
| phi4:14b-q4_K_M | 9.1 GB | 23 | **12** | **~49%** | Marginal (9.9 GB) |
| qwen3:14b | 9.3 GB | 44 | **23** | **~47%** | Marginal (11.6 GB) |
| qwen2.5-coder:14b-instruct-q4_K_M | 9.0 GB | 29 | **15** | **~47%** | Marginal (10.7 GB) |
| deepseek-coder-v2:16b | 10.0 GB | 25 | **11** | **~55%** | Marginal (11.7 GB) |
| **20B Models** | | | | | |
| gpt-oss-20b Q5_K_M | 11.7 GB | - | **28** | N/A (16K only) | Marginal (11.6 GB) |
| gpt-oss-20b Q4_K_M | 11.6 GB | - | **29** | N/A (16K only) | Marginal (11.7 GB) |
| glm-4.7-flash:q4_K_M | 19.0 GB | 9 | Timeout | **N/A** | **No** (11.7 GB) |

### Agentic-Chat Speed (Multi-Turn Tool Calling)

Agentic-chat speeds differ from text-generation speeds because they reflect multi-turn
conversations with tool dispatch overhead. These numbers represent the generation speed
during active inference.

| Model | Size | ctx-8192 | ctx-10240 | ctx-16384 | ctx-32768 | Notes |
|-------|------|----------|-----------|-----------|-----------|-------|
| llama3.2:latest | 2.0 GB | 172 | 173 | 177 | 179 | Fastest, but low quality |
| qwen2.5:7b | 4.7 GB | - | - | 89 | 91 | Fast, perfect quality, no speed loss at 32K |
| qwen3:8b (Q4_K_M) | 5.2 GB | 74 | 70 | 73 | 71 | Fast, perfect quality |
| qwen3:8b Q6_K | 6.6 GB | - | 60 | 59 | - | 17% slower than Q4, same quality |
| qwen3:8b Q8_0 | 8.5 GB | - | 49 | 49 | - | 32% slower than Q4, same quality |
| qwen3:14b | 9.3 GB | 42 | 29 | 23 | 11 | Slows significantly at 32K |
| glm-4.7-flash:q4_K_M | 19.0 GB | 15 | 14 | 13 | 9 | Slow (CPU spillover) but perfect quality |

### CPU Spillover Evidence

**Yes, larger models are clearly spilling to CPU at 16K context.** The evidence:

1. **VRAM stays capped around 11-11.7 GB** for all 14B+ models regardless of context
   size, while 7-8B models show VRAM increasing proportionally with context. This means
   the 14B+ models can't fit the full KV cache in VRAM and are offloading to system RAM.

2. **Speed halving** on 14B+ models (23 -> 12 tok/s for phi4, 44 -> 23 for qwen3:14b)
   is the classic symptom of partial CPU offload. The model weights may fit, but the
   growing KV cache at 16K pushes memory beyond VRAM capacity.

3. **7-8B models show no speed loss** at 16K because their smaller weights leave enough
   VRAM headroom for the larger KV cache.

4. **glm-4.7-flash (19GB)** doesn't fit in VRAM at all -- it runs almost entirely on CPU
   even in "GPU mode" (~9 tok/s on GPU vs ~9 tok/s on CPU, essentially the same). At
   16K context it flat-out times out (20-minute limit) on text tasks. However, in
   agentic-chat mode it completes successfully because tool-call turns are shorter
   individually (152-285s total across all turns).

5. **CPU baseline comparison:** On CPU, qwen3:14b runs at ~5.7 tok/s. On GPU at 16K it
   does ~23 tok/s. So it's still 4x faster than pure CPU, but is losing half its
   potential compared to 8K context. This partial-offload penalty is expected behavior
   for a 12GB card running 14B models at large contexts.

### Quantization Impact: qwen3:8b Variants (Q4_K_M vs Q6_K vs Q8_0)

Three quantization levels of qwen3:8b were tested on agentic-chat to determine whether
higher precision improves tool-calling quality. **It does not.**

| Variant | Size | ctx-10240 | ctx-16384 | tok/s (10K) | tok/s (16K) | VRAM (10K) | VRAM (16K) |
|---------|------|-----------|-----------|-------------|-------------|------------|------------|
| Q4_K_M (default) | 5.2 GB | A (9.0) | A (10.0) | 70 | 73 | 8.4 GB | 9.3 GB |
| Q6_K | 6.6 GB | A (10.0) | A (10.0) | 60 | 59 | 11.7 GB | 10.5 GB |
| Q8_0 | 8.5 GB | A (10.0) | A (10.0) | 49 | 49 | 11.3 GB | 11.5 GB |

**Key findings:**

1. **Quality is identical.** All three variants achieve perfect 10.0 on agentic-chat at
   ctx-16384, with 100% tool call success rates, correct ordering, and full portfolio
   coverage. The Q6_K at 16K even used 7/8 tools (including generate_report) -- but this
   is run-to-run variation, not a quantization effect.

2. **Higher quant = slower.** Q6_K is ~17% slower than Q4_K_M; Q8_0 is ~32% slower.
   The extra precision adds compute cost per token without improving output quality.

3. **Higher quant = more VRAM, killing 32K viability.** Q8_0 at ctx-16384 already uses
   11.5 GB -- at 32K it would blow past 12 GB and require heavy CPU spillover, negating
   the GPU advantage entirely. Q6_K is similarly constrained. Only the Q4_K_M (5.2 GB)
   leaves enough VRAM headroom for 32K context (11.6 GB at 32K, still fully in VRAM).

4. **Q4_K_M's ctx-10240 anomaly (9.0 vs 10.0) is not a quantization issue.** The Q4_K_M
   scored 9.0 at ctx-10240 due to a missing final text response (partial_success), while
   Q6_K and Q8_0 scored 10.0. But Q4_K_M scores 10.0 at three other context sizes. This
   is a one-off run variation, not evidence that higher quantization helps.

**Bottom line:** Stick with Q4_K_M. Higher quantization buys nothing for structured tool
calling while sacrificing speed and 32K context viability -- the two things that make
qwen3:8b the top recommendation in the first place.

---

## Recommended Models for OpenClaw

**OpenClaw requires structured tool calling.** Only 5 of 17 tested model families can
produce structured tool_calls via `/api/chat`. The recommendations below are filtered
to this viable set, then ranked by combined agentic-chat + engine + speed performance.

### Tier 1: Top Picks

#### qwen3:8b (Q4_K_M) - BEST OVERALL FOR OPENCLAW
- **Agentic-Chat:** A (10.0) at ctx-8192/16384/32768; A (9.0) at ctx-10240
- **Agentic (text):** A (9.7) at 10K; B (8.8) at 8K/16K
- **Engine:** A (9.9) at 10K/16K
- **Speed at 32K:** 71 tok/s chat (no degradation vs 16K -- the 5.2GB model still fits in VRAM)
- **VRAM at 32K:** 11.6 GB (tight but fits on RTX 4070 12GB)
- **Why:** Perfect structured tool calling at OpenClaw's recommended 32K context. The
  combination of perfect agentic-chat + strong engine + high speed makes this the best
  overall choice. 100% tool call success rate, 6/8 tools used, correct ordering across
  all portfolios. Per-token speed is essentially unchanged from 16K to 32K (71 vs 73
  tok/s) because the model weights are small enough that the larger KV cache still fits
  in VRAM. Total wall time increases slightly (109s vs 74s at 16K) due to more turns
  generated, not slower inference.
- **32K VRAM note:** At 32K context, VRAM usage jumps from 9.3 GB (16K) to 11.6 GB.
  This is close to the 12GB limit but still fits entirely in VRAM with no CPU spillover,
  which is why speed doesn't degrade.
- **Quantization tested:** Q6_K (6.6 GB) and Q8_0 (8.5 GB) variants scored identical
  10.0 on agentic-chat but are 17% and 32% slower respectively, and cannot fit 32K
  context in VRAM. Q4_K_M is the right quantization for this card. See "Quantization
  Impact" section above.
- **CPU agentic:** A (9.1)

#### qwen3:14b - HIGHEST QUALITY, TOO SLOW AT 32K
- **Agentic-Chat:** A (10.0) at ctx-10240/16384/32768; A (9.8) at ctx-8192 -- perfect at 3/4 sizes
- **Agentic (text):** A (10.0) at 16K -- perfect score, the only local model to achieve this
- **Engine:** A (9.8) at 16K
- **Speed at 16K:** 23 tok/s chat (tolerable -- 118s total for 24 tool calls in 3 turns)
- **Speed at 32K:** **10.5 tok/s** chat (52% slower than 16K -- heavy CPU spillover)
- **VRAM:** 11.3-11.5 GB (capped at all sizes above 8K -- KV cache spilling to system RAM)
- **Why:** The highest quality model that can do structured tool calling. Perfect 10.0 on
  agentic-chat at three context sizes, perfect 10.0 on text agentic, A (9.8) engine. At
  ctx-16384 it used all 8/8 tools across 24 tool calls with 96% success rate. At ctx-32768
  it used 7/8 tools across 28 calls in 15 turns. Dominant across every quality metric.
- **Problem at 32K:** The 9.3GB model weights plus the 32K KV cache exceed 12GB VRAM,
  causing heavy CPU spillover. The 32K agentic-chat run took **743 seconds (12.4 minutes)**
  at 10.5 tok/s. Quality is perfect but wall time is unacceptable for interactive use.
- **If using this model:** Override OpenClaw's 32K default to ctx-16384, where it scores
  A (10.0) on agentic-chat at a tolerable 23 tok/s (118s total). This is the sweet spot --
  close enough to OpenClaw's recommended context size while avoiding the 32K speed cliff.
- **CPU agentic:** A (9.5)

#### qwen2.5:7b - FASTEST PERFECT TOOL CALLER
- **Agentic-Chat:** A (10.0) at ctx-16384 and ctx-32768 -- perfect at both tested sizes
- **Agentic (text):** A (9.0) at 16K; B (8.8) at 32K
- **Engine:** B (8.7) -- correct logic, some worked example mismatches (share sign inversions)
- **Speed at 32K:** 91 tok/s chat (no degradation vs 16K -- the 4.7GB model has ample VRAM headroom)
- **VRAM at 32K:** 8.8 GB (very comfortable on RTX 4070 12GB)
- **Why:** The fastest model with perfect tool-calling scores. At 91 tok/s it's 28% faster
  than qwen3:8b (71 tok/s) at 32K, and uses 3 GB less VRAM (8.8 vs 11.6 GB). Perfect 10.0
  on agentic-chat at both contexts tested, with 27-30 tool calls, 7-8/8 tools used, and
  all 3 portfolios covered. The VRAM headroom means no risk of CPU spillover at 32K.
- **Tradeoff:** Engine score (B 8.7) is a step below qwen3:8b (A 9.9) -- the share sign
  convention was inverted in worked examples, and decimal formatting had minor issues.
  For pure tool-calling orchestration this doesn't matter, but for coding subtasks
  qwen3:8b produces more precise code.
- **Notable:** The base qwen2.5:7b succeeds at tool calling while all three qwen2.5-coder
  variants (7b, 7b-instruct, 14b-instruct) fail with `text_narration`. The code-tuning
  appears to have degraded the structured tool-calling ability.
- **Only tested at 16K/32K.** No 8K/10K data yet, but the 16K and 32K results are both
  perfect, suggesting this model handles tool calling robustly.

### Tier 2: Usable But Limited

#### glm-4.7-flash:q4_K_M - PERFECT TOOL CALLING, TOO SLOW FOR TEXT
- **Agentic-Chat:** A (10.0) at ctx-8192/16384/32768; A (9.8) at ctx-10240
- **Agentic (text):** A (9.2) at 10K; B (8.7) at 8K; timeout at 16K
- **Engine:** A (9.9) at 8K; A (9.4) at 16K; F at 10K
- **Speed at 32K:** 8.7 tok/s chat (31% slower than 16K's 12.8 -- already at CPU speed, further degradation)
- **VRAM:** 11.2-11.7 GB used (but model is 19GB, so heavily spilling to CPU at all sizes)
- **Why:** The most consistent tool caller tested -- perfect 10.0 at 3 of 4 context sizes.
  16 tool calls per run, 6/8 tools, 100% success rate, correct ordering. Its cloud sibling
  (glm-4.7) also scored top marks. The model clearly understands structured tool calling.
- **Tradeoff:** At 19GB it can't fit in VRAM and runs at CPU speed. Text-generation tasks
  time out at 16K+. Agentic-chat at 32K took 285s (~4.75 min) total. Only viable if
  response time is not critical and tool-calling reliability is paramount.

#### llama3.2:latest - FAST BUT LOW QUALITY, DEGRADES AT 32K
- **Agentic-Chat:** A (9.1) at ctx-10240; B (8.8) at ctx-8192; B (8.4) at ctx-16384; **D (6.9) at ctx-32768**
- **Agentic (text):** B (8.2-8.3) across contexts
- **Engine:** F across all GPU contexts (syntax errors, no output)
- **Speed at 32K:** 179 tok/s chat (fast, no speed degradation -- 2GB model easily fits)
- **VRAM at 32K:** 8.0 GB (comfortable)
- **Why:** The only other model that can make structured tool calls. Used all 8/8 tools
  (including generate_report and send_notification -- the only model to do so) at lower
  contexts.
- **Problem at 32K:** Quality degrades significantly -- D (6.9), only 2 tool calls made,
  only 2/8 tools used (vs 36-43 calls at smaller contexts). The 3B model appears to lose
  coherence at 32K context. Best scores are at ctx-8192/10240.
- **Tradeoff:** High argument error rate (37-57% of calls have bad args at ctx-8192/16384).
  Engine task is completely broken (F at all contexts). At 3B parameters it lacks the
  reasoning depth for complex tasks. Only useful as a very fast, low-accuracy fallback
  at reduced context sizes.

---

## Models to AVOID for OpenClaw

### Cannot Make Structured Tool Calls (Unusable for OpenClaw)

These models all scored **F on agentic-chat** despite many scoring well on text benchmarks.
They are fundamentally incompatible with OpenClaw's `/api/chat` tool-calling protocol.

| Model | Agentic (text) | Engine | Chat Failure | Why |
|-------|----------------|--------|--------------|-----|
| **gpt-oss-20b Q4_K_M** | A (9.1) | A (9.8) | `stalled_inference` | Loaded model, burned 84s, produced 0 tokens. Strong on text but cannot use `/api/chat` tools. |
| **gpt-oss-20b Q5_K_M** | A (9.8) | F (4.5) | `stalled_inference` | Same stall behavior (74s, 0 tokens). Near-perfect text agentic score is misleading for OpenClaw. |
| **phi4:14b-q4_K_M** | A (9.0) | A (9.9) | `empty_response` | Instant return, 0 tokens. One of the best text+engine models, completely broken for tool calling. |
| **qwen2.5-coder:14b** | B (8.7) | A (9.0-9.7) | `text_narration` | Described 6 tools in prose, made 0 structured calls. Strong coder that can't use the chat protocol. |
| **qwen2.5-coder:7b-instruct** | A (9.2) | B (8.8) | `text_narration` | Same narration failure. Understands tools conceptually, can't produce the wire format. |
| **qwen2.5-coder:7b** | B (8.3-8.7) | D-B | `text_narration` | Same narration failure. |
| **gemma3:12b-it** | A (9.2) at 16K | A (9.6) at 16K | `empty_response` | 0 tokens, instant return. Strong text model, no tool support. |
| **gemma2:9b-instruct** | B (8.2-8.5) | A (9.4) at 8K | `empty_response` | Same instant-return failure. |
| **deepseek-coder-v2:16b** | B (8.1) | A (9.1) at 16K | `empty_response` | 0 tokens. Also too slow (11 tok/s at 16K). |
| **llama3.1:8b** | D-B | F mostly | `text_narration` | Described 8 tools, 0 structured calls. Not instruction-tuned, also poor on text tasks. |
| **llama3.1:8b-instruct** | A (9.1) at 8K | F-A | `text_narration` | Described 8 tools, 0 structured calls. Instruction tuning didn't help with tool format. |
| **mistral:7b-instruct** | B (8.3-8.7) | B-F | `text_narration` | Described 8 tools, 0 structured calls. |

### Key Insight: Text Benchmarks Don't Predict Tool-Calling Ability

The correlation between agentic (text) scores and agentic-chat (tool calling) scores is
nearly zero across the tested models:

- **gpt-oss-20b Q5_K_M**: #2 on text agentic (9.8), F on tool calling (stalled)
- **phi4:14b**: A (9.0) on text, F on tool calling (empty response)
- **qwen2.5-coder:7b-instruct**: A (9.2) on text, F on tool calling (narration)
- **qwen2.5:7b** (base model): A (9.0) on text, **A (10.0) on tool calling** -- succeeds
  where all three qwen2.5-coder variants fail. Code-tuning broke tool calling.
- **llama3.2:latest**: B (8.3) on text, A (9.1) on tool calling -- the *weakest*
  text model among the 5 that passed is the only one besides qwen3/qwen2.5 to make all 8 tool calls

This is exactly why the agentic-chat task exists. Models that can write *about* tools
in generated code (the text agentic task) are not necessarily able to produce the structured
JSON tool_calls that `/api/chat` requires. For OpenClaw, only the latter matters. The
qwen2.5 vs qwen2.5-coder comparison is particularly striking: same base architecture,
but code fine-tuning destroyed the tool-calling capability.

---

## Final Recommendation Summary

### For OpenClaw -- Structured Tool Calling is Required

**Primary Model (Orchestrator/Planner):**
> **qwen3:8b @ 32K context** -- Perfect agentic-chat (10.0) at OpenClaw's recommended 32K
> context, excellent engine (9.9), and 71 tok/s with no speed degradation at 32K. The
> 5.2GB model still fits entirely in VRAM at 32K (11.6 GB used), avoiding the CPU spillover
> that cripples larger models at this context size. Best combination of tool-calling
> reliability, text quality, and speed.

**Quality-First Alternative (Reduced Context):**
> **qwen3:14b @ 16K context** -- Perfect agentic-chat (10.0) at 16K (confirmed on rerun:
> 24 tool calls, 8/8 tools, 96% success, 118s total), perfect text agentic (10.0), strong
> engine (9.8). **Must override OpenClaw's 32K default** -- at 32K context, speed drops to
> 10.5 tok/s (12+ minute response times due to CPU spillover). At ctx-16384 it runs at a
> tolerable 23 tok/s. Worth the config override if you need the quality edge over 8b.

**Speed-First Alternative (Perfect Quality, Maximum Throughput):**
> **qwen2.5:7b @ 32K context** -- Perfect agentic-chat (10.0) at 32K, 91 tok/s (28% faster
> than qwen3:8b), and only 8.8 GB VRAM. The fastest model with perfect tool-calling scores.
> Weaker on engine (B 8.7 vs A 9.9) so coding subtasks won't be as precise, but for pure
> tool-calling orchestration it's excellent. The base qwen2.5 model succeeds where all
> qwen2.5-coder variants fail.

**NOT Recommended Despite Strong Text Scores:**
> **gpt-oss-20b**, **phi4:14b**, **qwen2.5-coder** (all variants), **gemma2/3**,
> **deepseek-coder-v2**, **llama3.1**, **mistral** -- all score F on structured tool
> calling. These models cannot be used with OpenClaw for agentic workflows.

### Suggested OpenClaw Configuration

```
Primary Agent:    qwen3:8b       @ 32K context (OpenClaw default -- fast, reliable, fits in VRAM)
Speed Alt:        qwen2.5:7b     @ 32K context (28% faster, less VRAM, weaker engine)
Quality Backup:   qwen3:14b      @ 16K context (override default -- 32K is too slow for 14b)
```

**qwen3:8b remains the top overall recommendation** due to its combination of perfect
tool calling AND top-tier engine scores (A 9.9). qwen2.5:7b matches it on tool calling
and is significantly faster (91 vs 71 tok/s) with more VRAM headroom (8.8 vs 11.6 GB),
but its weaker engine score (B 8.7) means coding subtasks will be less precise. If
OpenClaw's workload is primarily tool orchestration with minimal code generation,
qwen2.5:7b is the faster choice. If coding quality matters, stick with qwen3:8b.

### What About Coding Subtasks?

If OpenClaw dispatches coding-only subtasks that use text generation (not tool calling),
models like phi4:14b or qwen2.5-coder could theoretically be used for those. However, the
operational complexity of running different models for different subtask types likely
outweighs the benefit. qwen3:8b scores A (9.9) on engine and B-A on text agentic, which
is strong enough for most coding work. qwen2.5:7b's engine score (B 8.7) is adequate but
not as precise. Stick with qwen3:8b for mixed workloads; consider qwen2.5:7b only if the
workload is predominantly tool orchestration.

### Does the 32K Context Actually Get Used?

Probably not for agentic-chat workloads. The multi-turn conversation (system message +
user message + ~15-30 tool call/response round trips) likely consumes 4-8K tokens. The
benchmark's qwen3:8b runs used 16 tool calls across 7-13 turns -- well within 8K context.
The 32K headroom is insurance for longer conversations, not a current requirement. This
is good news: it means the quality scores at 32K aren't being artificially degraded by
context pressure, and qwen3:8b's perfect 10.0 at 32K is genuine, not an artifact of
underutilizing the window.

---

*Analysis based on automated benchmark reports from cpu, gpu (ctx-8192/10240/16384/32768),
and cloud modes. 19 local models tested (17 unique architectures + 2 quantization variants).
Includes quantization comparison (Q4_K_M/Q6_K/Q8_0) for qwen3:8b. Agentic-chat evaluation
is 100% automated (structured calls are machine-checkable). Agentic (text) manual review
sections use placeholder 50% scores. Engine evaluation is fully automated.*
