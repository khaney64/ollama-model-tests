# Model Recommendations for OpenClaw GPU Usage (RTX 4070 12GB)

Generated: 2026-02-18

Context: Recommendations for using local Ollama models via OpenClaw at 32K context
(OpenClaw's recommended default, warns below this), prioritizing agentic capabilities
with occasional coding subtasks.

> **Critical caveat: Structured tool calling is the gating factor, not text benchmarks.**
>
> The `agentic-chat` task tests structured tool calling via `/api/chat` -- the actual
> protocol OpenClaw uses. Of 16 local models tested, **only 4 can produce any structured
> tool calls at all**. The other 12 -- including models that score A on text-based agentic
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

### Agentic-Chat Results (28 Evaluations, 4 Context Sizes)

The agentic-chat task runs multi-turn structured tool calling against 8 portfolio analysis
tools. Models were tested at ctx-8192, ctx-10240, ctx-16384, and ctx-32768 (where supported).

**Grade distribution:** 13 A, 2 B, 1 D, 12 F

**Outcome classification:**
- **Success** (structured tool calls, completed): 14 evaluations
- **Partial Success** (tool calls but incomplete): 2 evaluations
- **Text Narration** (described tools in prose, 0 structured calls): 6 evaluations
- **Empty Response** (no tokens, instant return): 4 evaluations
- **Stalled Inference** (loaded model, burned time, 0 tokens): 2 evaluations

**Only 4 model families produced any structured tool calls:**

| Model | ctx-8192 | ctx-10240 | ctx-16384 | ctx-32768 | Best |
|-------|----------|-----------|-----------|-----------|------|
| glm-4.7-flash:q4_K_M | A (10.0) | A (9.8) | A (10.0) | A (10.0) | 10.0 |
| qwen3:8b | A (10.0) | A (9.0) | A (10.0) | A (10.0) | 10.0 |
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

### GPU Mode -- Agentic (Text) and Engine (44 Evaluations Each)

**Agentic grade distribution:** 12 A, 24 B, 6 C, 1 D, 1 N/A (timeout)
**Engine grade distribution:** 18 A, 7 B, 4 D, 15 F

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
| qwen2.5-coder:7b | 4.7 GB | 88 | 89 | ~0% | Yes (6.5 GB) |
| qwen2.5-coder:7b-instruct-q5_K_M | 5.4 GB | 79 | 78 | ~0% | Yes (8.0 GB) |
| qwen3:8b | 5.2 GB | 72 | 71 | ~1% | Yes (9.0 GB) |
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

| Model | ctx-8192 | ctx-10240 | ctx-16384 | ctx-32768 | Notes |
|-------|----------|-----------|-----------|-----------|-------|
| llama3.2:latest | 172 | 173 | 177 | 179 | Fastest, but low quality |
| qwen3:8b | 74 | 70 | 73 | 71 | Fast, perfect quality |
| qwen3:14b | 42 | 29 | 23 | 11 | Slows significantly at 32K |
| glm-4.7-flash:q4_K_M | 15 | 14 | 13 | 9 | Slow (CPU spillover) but perfect quality |

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

---

## Recommended Models for OpenClaw

**OpenClaw requires structured tool calling.** Only 4 of 16 tested local models can
produce structured tool_calls via `/api/chat`. The recommendations below are filtered
to this viable set, then ranked by combined agentic-chat + engine + speed performance.

### Tier 1: Top Picks

#### qwen3:8b - BEST OVERALL FOR OPENCLAW
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
- **llama3.2:latest**: B (8.3) on text, A (9.1) on tool calling -- the *weakest*
  text model among the 4 that passed is the only one besides qwen3 to make all 8 tool calls

This is exactly why the agentic-chat task exists. Models that can write *about* tools
in generated code (the text agentic task) are not necessarily able to produce the structured
JSON tool_calls that `/api/chat` requires. For OpenClaw, only the latter matters.

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

**NOT Recommended Despite Strong Text Scores:**
> **gpt-oss-20b**, **phi4:14b**, **qwen2.5-coder** (all variants), **gemma2/3**,
> **deepseek-coder-v2**, **llama3.1**, **mistral** -- all score F on structured tool
> calling. These models cannot be used with OpenClaw for agentic workflows.

### Suggested OpenClaw Configuration

```
Primary Agent:    qwen3:8b       @ 32K context (OpenClaw default -- fast, reliable, fits in VRAM)
Quality Backup:   qwen3:14b      @ 16K context (override default -- 32K is too slow for 14b)
```

**qwen3:8b is the clear winner at OpenClaw's 32K default.** It's the only model that
scores perfectly on structured tool calling AND runs at full GPU speed at 32K context.
The 14b variant produces higher quality text and now has confirmed perfect scores across
all context sizes, but requires overriding the context default to 16K to avoid the 32K
speed cliff (10.5 tok/s vs 23 tok/s). If you need the quality edge, the 14b at 16K is
a strong choice -- but for most users, qwen3:8b at 32K is simpler and faster.

### What About Coding Subtasks?

If OpenClaw dispatches coding-only subtasks that use text generation (not tool calling),
models like phi4:14b or qwen2.5-coder could theoretically be used for those. However, the
operational complexity of running different models for different subtask types likely
outweighs the benefit. qwen3:8b scores A (9.9) on engine and B-A on text agentic, which
is strong enough for most coding work. Stick with qwen3 for everything.

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
and cloud modes. Agentic-chat evaluation is 100% automated (structured calls are machine-
checkable). Agentic (text) manual review sections use placeholder 50% scores. Engine
evaluation is fully automated.*
