# Model Recommendations for OpenClaw GPU Usage (RTX 4070 12GB)

Generated: 2026-02-14

Context: Recommendations for using local Ollama models via OpenClaw at 16K+ context,
prioritizing agentic capabilities with occasional coding subtasks.

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

### GPU Mode (14 Local Models, 3 Context Sizes)

42 agentic evaluations, 42 engine evaluations across ctx-8192, ctx-10240, ctx-16384.

**Agentic grade distribution:** 10 A, 24 B, 6 C, 1 D, 1 N/A (timeout)
**Engine grade distribution:** 17 A, 7 B, 4 D, 14 F

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
| glm-4.7-flash:q4_K_M | 19.0 GB | 9 | Timeout | **N/A** | **No** (11.7 GB) |

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

4. **glm-4.7-flash (19GB)** doesn't fit in VRAM at all - it runs almost entirely on CPU
   even in "GPU mode" (~9 tok/s on GPU vs ~9 tok/s on CPU, essentially the same). At
   16K context it flat-out times out (20-minute limit) on multiple tasks.

5. **CPU baseline comparison:** On CPU, qwen3:14b runs at ~5.7 tok/s. On GPU at 16K it
   does ~23 tok/s. So it's still 4x faster than pure CPU, but is losing half its
   potential compared to 8K context. This partial-offload penalty is expected behavior
   for a 12GB card running 14B models at large contexts.

---

## Recommended Models for OpenClaw at 16K Context

### Tier 1: Top Picks (Best Quality + Speed Balance)

#### qwen3:14b - BEST AGENTIC MODEL
- **Agentic:** A (10.0) at 16K -- **perfect score**, the only local model to achieve this
- **Engine:** A (9.8) at 16K
- **Speed at 16K:** 23 tok/s (tolerable, ~2-4 min for complex tasks)
- **VRAM:** 11.6 GB (tight but works)
- **Why:** Dominant agentic performance across all context sizes. Perfect format, tools,
  execution, data flow, error handling, and logging at 16K. On CPU (default context) it
  also scored A (9.5). Consistently the best agentic model in the entire local lineup.
- **Tradeoff:** Half the speed of 7B models at 16K due to VRAM pressure. Worth it for
  the quality gap, especially for agentic primary use.
- **CPU agentic:** A (9.5) -- proves the model quality, not just a context size fluke

#### qwen3:8b - BEST SPEED/QUALITY RATIO
- **Agentic:** A (9.7) at 10K; B (8.8) at 16K and 8K
- **Engine:** A (9.9) at 10K and 16K
- **Speed at 16K:** 71 tok/s (fast, no degradation)
- **VRAM:** 9.0 GB (comfortable)
- **Why:** Excellent engine scores, strong agentic performance, and blazing fast at 16K.
  Best choice when response time matters. Engine results are consistently top-tier.
  The slight agentic dip at 16K (B vs A at 10K) may be noise in the evaluation.
- **CPU agentic:** A (9.1) -- strong baseline quality

#### phi4:14b-q4_K_M - STRONG ALL-ROUNDER
- **Agentic:** A (9.0) at 16K and 8K; B (8.7) at 10K
- **Engine:** A (9.9) at 16K and 8K
- **Speed at 16K:** 12 tok/s (slow but usable)
- **VRAM:** 9.9 GB (fits)
- **Why:** Consistently strong across both tasks and all context sizes. The most reliable
  14B model -- never drops below B on agentic, never below A on engine at any context.
- **Tradeoff:** Slowest 14B model at 16K. For subtask agent use, the 3-5 min response
  times may be acceptable if quality matters more than speed.
- **CPU agentic:** A (9.2) -- confirmed quality

### Tier 2: Good Alternatives

#### qwen2.5-coder:7b-instruct-q5_K_M - FAST CODING SPECIALIST
- **Agentic:** A (9.2) at 16K; B (8.8) at 8K; B (8.4) at 10K
- **Engine:** B (8.8) at 16K; B (8.1) at 10K and 8K
- **Speed at 16K:** 78 tok/s (very fast)
- **VRAM:** 8.0 GB (comfortable)
- **Why:** Great for coding subtasks due to coder specialization. Fast and reliable.
  Agentic A at 16K suggests the extra context helps it plan better.
- **CPU agentic:** B (8.7)

#### qwen2.5-coder:14b-instruct-q4_K_M - QUALITY CODING MODEL
- **Agentic:** B (8.7-8.8) across all context sizes
- **Engine:** A (9.0-9.7) across all context sizes
- **Speed at 16K:** 15 tok/s (slow)
- **VRAM:** 10.7 GB (tight)
- **Why:** Very strong engine scores. Reliable agentic B. Good choice for coding-heavy
  workloads where you need higher quality than the 7B coder variant.
- **CPU agentic:** A (9.3) -- actually scores better on CPU (more tokens generated)

#### gemma3:12b-it-q4_K_M - STRONG AT 16K
- **Agentic:** A (9.2) at 16K; C (7.3/7.1) at 10K/8K
- **Engine:** A (9.6) at 16K; D (6.6) at 10K/8K
- **Speed at 16K:** 50 tok/s (good, no degradation)
- **VRAM:** 11.4 GB (usable)
- **Why:** Dramatic quality improvement at 16K vs smaller contexts. If you're committed
  to 16K context (which OpenClaw recommends), gemma3 becomes a viable option. The quality
  cliff at lower contexts means 16K is essentially mandatory for this model.
- **Caution:** Inconsistent -- great at 16K, poor at 8K/10K

### Tier 3: Situationally Useful

#### llama3.1:8b-instruct-q4_K_M
- **Agentic:** A (9.1) at 8K; B (8.3) at 16K; C (7.8) at 10K
- **Engine:** A (9.3) at 10K; F (5.6) at 8K and 16K
- **Speed at 16K:** 84 tok/s (very fast)
- **Why:** Inconsistent quality across contexts. Fast but unreliable for engine tasks.
  May work as a quick-response subtask agent where speed trumps accuracy.

#### gemma2:9b-instruct-q4_K_M
- **Agentic:** B (8.2-8.5) across all contexts
- **Engine:** A (9.4) at 8K; F (5.3) at 10K; B (8.5) at 16K
- **Speed at 16K:** 60 tok/s (good)
- **Why:** Decent agentic baseline, but engine quality is inconsistent. Older
  architecture superseded by gemma3.

---

## Models to AVOID

### Definitely Not Useful

| Model | Reason |
|-------|--------|
| **glm-4.7-flash:q4_K_M** (19GB) | **Does not fit in 12GB VRAM.** Runs at CPU speed (~9 tok/s) even in GPU mode. Times out at 16K context on refactor and agentic tasks. Effectively unusable on RTX 4070. |
| **llama3.2:latest** (2.0GB) | Fastest model (167 tok/s) but **worst quality**. Engine: F across all GPU contexts (syntax errors, no output). Agentic: B-C range but low automated scores. The 3B parameter count is simply too small for complex tasks. Only useful for trivial text generation. |
| **llama3.1:8b** (base, not instruct) | **Not instruction-tuned.** Agentic: D (6.3) on CPU, D-B on GPU. Engine: F on GPU at all contexts (no output file generated). The instruct variant is strictly better. |
| **deepseek-coder-v2:16b** | At 16K: 11 tok/s (very slow due to VRAM spillover). Agentic: B (8.1) at best. Engine: inconsistent (A at 16K, F at 10K). Too slow and too inconsistent for the 10GB model size. |

### Marginal / Not Recommended

| Model | Reason |
|-------|--------|
| **mistral:7b-instruct-v0.3-q5_K_M** | Agentic: B (8.3-8.7), Engine: B (8.0) at best, F at multiple contexts. Execution failures on CPU agentic. Superseded by qwen models at similar size. |
| **qwen2.5-coder:7b** (base) | Agentic: B (8.3-8.7), Engine: inconsistent (D at 8K/10K). The instruct variant (q5_K_M) is more reliable. |

---

## Final Recommendation Summary

### For OpenClaw at 16K Context, Agentic Primary

**Primary Model (Orchestrator/Planner):**
> **qwen3:14b** -- Perfect agentic score at 16K. Accept the ~23 tok/s speed for the
> quality gain. Best for complex planning, tool orchestration, and multi-step reasoning.

**Fast Subtask Agent (Coding):**
> **qwen3:8b** or **qwen2.5-coder:7b-instruct-q5_K_M** -- Both run at 70-78 tok/s
> at 16K with strong engine/coding scores. Use qwen3:8b for general subtasks,
> qwen2.5-coder for code-specific work.

**Alternative Primary (If Speed Matters More):**
> **qwen3:8b** -- Nearly as good on agentic (A at 10K, B at 16K) at 3x the speed of
> qwen3:14b. Best compromise if 23 tok/s feels too slow for interactive use.

### Suggested OpenClaw Configuration

```
Primary Agent:    qwen3:14b      @ 16K context (quality-first orchestration)
Coding Subtask:   qwen2.5-coder:7b-instruct-q5_K_M @ 16K context (fast, code-focused)
General Subtask:  qwen3:8b       @ 16K context (fast, versatile)
```

### Key Insight

The qwen3 family dominates both agentic and engine tasks across all modes. The 14B
variant is the clear agentic champion, while the 8B variant offers the best
speed-to-quality ratio. The qwen2.5-coder models fill the coding niche well.
All other model families tested (llama, gemma, mistral, deepseek, glm) are either
too slow, too inconsistent, or too low quality at 16K context to recommend for
OpenClaw use on the RTX 4070 12GB.

---

*Analysis based on automated benchmark reports from cpu, gpu (ctx-8192/10240/16384),
and cloud modes. GPU quality scores (manual review sections) are not yet filled in;
recommendations are based on automated evaluation scores only.*
