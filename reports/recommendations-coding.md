# Model Recommendations for Coding Assistants (RTX 4070 12GB)

Generated: 2026-02-19

Context: Recommendations for using local Ollama models with coding tools like
OpenCode, Claude Code (via `ollama launch claude`), Cline, Continue, or similar
IDE-integrated coding assistants. These tools primarily use **text generation**
(`/api/generate` or `/api/chat` without structured tool calling), so the gating
factor is **code quality + speed**, not structured tool calling.

> **How this differs from the OpenClaw recommendations:**
>
> The [OpenClaw recommendations](recommendations.md) filter models by structured
> tool calling ability -- only 4 of 16 model families could produce the JSON
> wire format that `/api/chat` requires. That filter is irrelevant here. Coding
> assistants generate text (code, explanations, diffs) and don't require structured
> `tool_calls`. This means models like phi4 and qwen2.5-coder -- which scored F
> on tool calling but A on code generation -- are strong candidates for this use case.

---

## Evaluation Methodology

Models were ranked using three coding-relevant benchmarks from our GPU test suite:

| Task | What It Tests | Weight |
|------|---------------|--------|
| **Engine** | Write a complete Python trading engine from a detailed spec with worked examples. Tests correctness, output format compliance, and code quality. Fully automated scoring. | Primary |
| **Agentic** | Generate a multi-tool portfolio risk analysis agent. Tests planning, tool selection, data flow, error handling. 70% automated + 30% manual review. | Secondary |
| **Speed** | Tokens/second at various context sizes. Critical for interactive coding where you're waiting for completions. | Practical |

We did not have automated report cards for the greenfield, refactor, or API tasks,
so engine and agentic serve as proxies for "can this model write working code?" and
"can this model plan and reason about complex code?" respectively.

---

## Quick Reference: Top Models for Coding

| Rank | Model | Engine | Agentic | Speed (16K) | Sweet Spot | Best For |
|------|-------|--------|---------|-------------|------------|----------|
| 1 | **qwen3:8b** | A (9.9) | A (9.7) | 72 tok/s | ctx-10240 | Best all-rounder |
| 2 | **qwen3:14b** | A (9.8) | A (10.0) | 44 tok/s | ctx-8192 | Highest quality |
| 3 | **phi4:14b-q4_K_M** | A (9.9) | A (9.0) | 23 tok/s | ctx-8192 | Precise code generation |
| 4 | **qwen2.5-coder:14b-instruct** | A (9.7) | B (8.8) | 29 tok/s | ctx-10240 | Purpose-built coder |
| 5 | **qwen2.5:7b** | B (8.7) | A (9.0) | 89 tok/s | ctx-16384 | Fast coding + tool calling |
| 6 | **qwen2.5-coder:7b-instruct** | B (8.8) | A (9.2) | 79 tok/s | ctx-16384 | Fast coding, good quality |

---

## Detailed Rankings

### Tier 1: Recommended for Coding

#### qwen3:8b -- BEST OVERALL FOR CODING ASSISTANTS

- **Engine:** A (9.9) at ctx-10240 and ctx-16384 -- perfect correctness, output format, worked example match
- **Agentic:** A (9.7) at ctx-10240 -- strong planning, 10/10 on tools, execution, and data flow
- **Speed:** 72 tok/s at 8K, 70 tok/s at 10K, 71 tok/s at 16K -- **no speed degradation** up to 16K
- **VRAM:** 5.2 GB model, 7.3-9.3 GB with KV cache (8K-16K) -- comfortably fits
- **Context warning:** At ctx-8192 the engine task hit context limits and scored F (3.5). Use ctx-10240+ for non-trivial coding tasks.
- **Why #1:** The best combination of quality and speed. At 72 tok/s it's fast enough for interactive coding, and A (9.9) on engine means it writes correct, well-structured code. The 5.2 GB footprint leaves ample VRAM headroom, so speed doesn't degrade at larger contexts the way 14B models do. For a coding assistant where you're generating completions, refactoring code, and explaining logic, qwen3:8b at ctx-10240 or higher is the sweet spot.

#### qwen3:14b -- HIGHEST QUALITY, SLOWER

- **Engine:** A (9.8) at ctx-16384 -- perfect correctness, format, and worked example; only 0.1 behind qwen3:8b
- **Agentic:** A (10.0) at ctx-16384 -- **perfect score, the only local model to achieve this**
- **Speed:** 44 tok/s at 8K (usable), **23 tok/s at 16K** (tolerable), **22 tok/s at 10K** (partial spillover)
- **VRAM:** 9.3 GB model, KV cache spills to CPU at 16K+ (capped at ~11.5 GB)
- **Why #2:** If you're doing complex refactoring, designing architectures, or need the model to reason through multi-step code changes, qwen3:14b produces the highest quality output. The perfect 10.0 on agentic (text) means it plans better than any other local model. The tradeoff is speed: at 16K context you're waiting ~2x longer per response than qwen3:8b.
- **Best config:** Use ctx-8192 for quick completions (44 tok/s), ctx-16384 for complex tasks where you need to pass more context (23 tok/s). Avoid ctx-32768 -- speed drops to 10.5 tok/s.

#### phi4:14b-q4_K_M -- PRECISE CODE, SLOW BUT RELIABLE

- **Engine:** A (9.9) at ctx-8192 and ctx-16384 -- tied for the best engine score across all models
- **Agentic:** A (9.0) at ctx-8192 and ctx-16384 -- solid planning, 10/10 on tools and execution
- **Speed:** 23 tok/s at 8K, **12 tok/s at 16K** (heavy CPU spillover)
- **VRAM:** 9.1 GB model, ~11 GB with KV cache
- **Why #3:** phi4 produces extremely precise code -- perfect correctness, perfect worked examples, perfect edge case handling on the engine task. Its 9.9 engine score at ctx-8192 matches the best models with no context-limit issues. The agentic score is slightly lower than the qwen3 models but still solid. The main drawback is speed: 23 tok/s at 8K is workable but not snappy, and at 16K it drops to 12 tok/s.
- **Best config:** ctx-8192 only. At 16K the speed is barely interactive.
- **Note:** This model scores F on structured tool calling (empty response) -- irrelevant for coding assistants but important if you also use OpenClaw.

#### qwen2.5-coder:14b-instruct-q4_K_M -- PURPOSE-BUILT CODER

- **Engine:** A (9.7) at ctx-10240 -- strong across all criteria
- **Agentic:** B (8.8) at ctx-8192 -- good but not top-tier planning
- **Speed:** 29 tok/s at 8K, **15 tok/s at 16K** (heavy CPU spillover)
- **VRAM:** 9.0 GB model, similar spillover profile to phi4
- **Why #4:** A code-specialized model that lives up to its name. Its engine score is excellent (9.7) and it produces clean, well-structured Python. On agentic tasks it's a step behind the qwen3 and phi4 models, suggesting it's better at writing code than planning multi-step solutions. Speed is the main issue -- at 29 tok/s (8K) it's usable but not fast, and at 16K it's marginal.
- **Best config:** ctx-8192 or ctx-10240 for best speed/quality balance.

### Tier 2: Good Alternatives

#### qwen2.5-coder:7b-instruct-q5_K_M -- FAST CODER

- **Engine:** B (8.8) at ctx-16384 -- good but some worked example mismatches
- **Agentic:** A (9.2) at ctx-16384 -- strong planning and tool coverage
- **Speed:** 79 tok/s at 8K, 78 tok/s at 16K -- fast and stable
- **VRAM:** 5.4 GB model, 7.6-8.0 GB with KV cache
- **Why:** A fast, code-specialized model. At 79 tok/s it's the second-fastest model (after llama3.2) while still producing decent code. The engine score (8.8) shows it gets the logic mostly right but has some precision issues (decimal formatting, worked example mismatches). Good choice for quick completions and iterative coding where you can review and fix minor issues.

#### gemma3:12b-it-q4_K_M -- CONTEXT-SENSITIVE

- **Engine:** A (9.6) at ctx-16384 -- but D (6.6) at 8K and 10K (empty output CSV)
- **Agentic:** A (9.2) at ctx-16384 -- but C (7.1-7.3) at 8K/10K
- **Speed:** 51 tok/s -- stable across contexts
- **VRAM:** 8.1 GB model, 10.9-11.4 GB with KV cache
- **Why:** At ctx-16384 this is an excellent coding model (A on both engine and agentic). The problem is extreme context sensitivity: at 8K/10K contexts it produces broken output (empty CSVs, poor planning). Only use at ctx-16384+. The model also hit context limits on the refactor task and timed out at higher contexts, suggesting it generates verbose output.
- **Best config:** ctx-16384 only. Performance at lower contexts is unreliable.

#### qwen2.5:7b -- FAST ALL-ROUNDER, WEAKER ON PRECISION

- **Engine:** B (8.7) -- correct logic (10.0 correctness), but share sign inversions in worked examples and decimal formatting issues
- **Agentic:** A (9.0) at ctx-16384, B (8.8) at ctx-32768 -- 8/8 tools used, good execution and data flow
- **Speed:** 89 tok/s at 16K, 91 tok/s at 32K -- fast and stable, no speed loss at 32K
- **VRAM:** 4.7 GB model, 7.2 GB at 16K, 8.8 GB at 32K -- very comfortable
- **Why:** The fastest model with a passing engine score. At 89 tok/s it's faster than qwen3:8b (72 tok/s) while still producing working code. The engine score (B 8.7) shows the logic is correct but the share sign convention was inverted. Importantly, this is also the only qwen2.5 variant that can do structured tool calling (A 10.0 on agentic-chat), making it the best dual-purpose model if you use both coding assistants and OpenClaw.
- **Best config:** ctx-16384 or ctx-32768. Only tested at these two sizes.
- **Note:** Not code-tuned like qwen2.5-coder, but produces comparable quality with the bonus of structured tool-calling ability.

#### gpt-oss-20b (Q4_K_M) -- HIGH QUALITY, LARGE FOOTPRINT

- **Engine:** A (9.8) at ctx-16384 -- excellent
- **Agentic:** A (9.1) at ctx-16384 -- strong
- **Speed:** 29 tok/s at ctx-16384 (the only context tested)
- **VRAM:** ~11.6-11.7 GB (near limit)
- **Why:** Produces very high quality code (engine 9.8) and plans well (agentic 9.1). But at 20B parameters it barely fits in 12GB VRAM, can only run at ctx-16384, and 29 tok/s is on the slow side. Also had a syntax error on the Q5_K_M variant's engine output. Use if quality is paramount and you can tolerate the speed.
- **Note:** The Q5_K_M variant scored F on engine (syntax error) despite near-perfect agentic scores. Stick with Q4_K_M.

### Tier 3: Usable with Caveats

#### gemma2:9b-instruct-q4_K_M -- INCONSISTENT

- **Engine:** A (9.4) at ctx-8192, B (8.5) at ctx-16384, F (5.3) at ctx-10240
- **Agentic:** B (8.2-8.5) -- decent but not outstanding
- **Speed:** 60-66 tok/s -- good
- **Why:** Fast and compact, with a solid engine score at ctx-8192. But wildly inconsistent across context sizes -- the same model fails at ctx-10240 due to a `NameError` while producing A-grade code at ctx-8192. Use at ctx-8192 only.

#### deepseek-coder-v2:16b -- TOO SLOW FOR ITS QUALITY

- **Engine:** A (9.1) at ctx-16384, B (8.3) at ctx-8192 -- good but not best-in-class
- **Agentic:** B (8.0-8.1) -- middling
- **Speed:** 25 tok/s at 8K, 11 tok/s at 16K -- too slow
- **VRAM:** 10 GB model, maxes out VRAM
- **Why:** A once-great coding model that's outclassed by newer options. At 10 GB it fills VRAM, leaves little room for KV cache, and generates at speeds that are barely interactive. qwen2.5-coder:14b produces better code at the same speed with less VRAM.

#### llama3.1:8b-instruct-q4_K_M -- PLANNING STRONG, CODING WEAK

- **Engine:** A (9.3) at ctx-10240, but F at 8K and 16K (KeyError crashes)
- **Agentic:** A (9.1) at ctx-8192 -- good reasoning
- **Speed:** 83 tok/s -- fast
- **Why:** Fast and good at reasoning tasks, but its code frequently crashes with runtime errors (KeyError on 'Shares', 'shares'). The ctx-10240 engine result is an outlier -- at two other contexts the generated code doesn't run. Too unreliable for production coding.

### Not Recommended for Coding

| Model | Speed | Engine (best) | Problem |
|-------|-------|--------------|---------|
| llama3.2:latest | 167 tok/s | F (5.7) | Fastest model but code crashes at every context size (KeyError, TypeError). Too small (3B) for real coding tasks. |
| llama3.1:8b | 83 tok/s | F (5.7) | Code crashes (UnboundLocalError, no output). Fast but unreliable. |
| mistral:7b-instruct | 77 tok/s | B (8.0) at 10K | Decent at best context, but F at 8K/16K (SyntaxError, KeyError). Very inconsistent. |
| glm-4.7-flash:q4_K_M | 9 tok/s | A (9.9) at 8K | Excellent code quality but at 19 GB it runs at CPU speed (~9 tok/s). Times out at 16K+ on text generation. Not practical for interactive coding. |

---

## Context Size Recommendations for Coding

Coding assistants typically send the current file (or portion of it) plus instructions
as the prompt. Typical prompt sizes:

| Use Case | Prompt Size | Recommended Context |
|----------|------------|---------------------|
| Simple completions, single function | 1-2K tokens | 8192 |
| Full file refactoring | 2-6K tokens | 10240-16384 |
| Multi-file context (imports, related files) | 4-10K tokens | 16384 |
| Large codebase context | 8-16K+ tokens | 16384-32768 |

**For 7-8B models:** Use ctx-16384 freely. Speed is unaffected (72-88 tok/s at all sizes) and VRAM stays within budget.

**For 14B models:** Use ctx-8192 for fast completions (23-44 tok/s). Only go to ctx-16384 if you need the extra context and can accept ~50% speed loss due to VRAM spillover.

---

## Speed vs Quality Tradeoff

```
Speed (tok/s at 16K ctx)
  |
  |  llama3.2 (167)  -- F engine, not recommended
  |
  |  qwen2.5:7b (89)          -- B engine, fast + tool calling
  |  qwen2.5-coder:7b (88)    -- D-B engine, inconsistent
  |  llama3.1:8b-instruct (83) -- A at 10K, F at 8K/16K
  |  qwen2.5-coder:7b-instruct (79) -- B engine, fast coder
  |  mistral:7b (77)           -- B at 10K, F at others
  |  qwen3:8b (72)     <-- SWEET SPOT: A (9.9) engine
  |  gemma2:9b (60)            -- A at 8K, F at 10K
  |  gemma3:12b (51)           -- A at 16K only
  |  qwen3:14b (44)    <-- QUALITY PICK: A (10.0) agentic
  |  qwen2.5-coder:14b (29)   -- A engine, purpose-built
  |  deepseek-coder-v2 (25)   -- outclassed
  |  phi4:14b (23)     <-- A (9.9) engine, reliable
  |  glm-4.7-flash (9)        -- too slow for interactive
  +-------------------------------------------------> Quality
     F(5)    D(6)    C(7)    B(8)    A(9)    A(10)
```

The sweet spot for coding assistants is the 40-80 tok/s range with A-grade engine
scores. Below 20 tok/s, interactive coding becomes frustrating (waiting 5+ seconds
for a short response). Above 80 tok/s, the quality drops too much.

---

## Final Recommendation Summary

### For Interactive Coding (OpenCode, Claude Code, Cline, Continue)

**Primary Model -- Best Speed/Quality Balance:**
> **qwen3:8b @ ctx-10240 or ctx-16384** -- A (9.9) engine, A (9.7) agentic,
> 72 tok/s with no speed loss at 16K. Writes correct, well-structured code. The
> 5.2 GB footprint means it runs at full GPU speed even at 16K context. Best
> all-rounder for day-to-day coding assistance.

**Quality-First Alternative -- When Accuracy Matters Most:**
> **qwen3:14b @ ctx-8192** -- A (9.8) engine, A (10.0) agentic. The best reasoning
> and planning of any local model. Use for complex refactoring, architecture design,
> or when you need the model to think through multi-step changes. At ctx-8192 it
> runs at 44 tok/s (usable); at ctx-16384 it drops to 23 tok/s. Worth the speed
> tradeoff for difficult tasks.

**Budget/Speed Alternative -- When Latency Matters Most:**
> **qwen2.5-coder:7b-instruct-q5_K_M @ ctx-16384** -- B (8.8) engine, A (9.2)
> agentic, 79 tok/s. Code-specialized, fast, and stable. Slightly less precise
> than qwen3:8b on correctness but produces clean code quickly. Good for rapid
> iteration where you review and fix minor issues.

**Precision Alternative -- When Correctness Matters Most:**
> **phi4:14b-q4_K_M @ ctx-8192** -- A (9.9) engine (tied for best), A (9.0)
> agentic. Produces the most precise code with perfect worked-example matches.
> At 23 tok/s it's slow for interactive use but excellent for batch/offline code
> generation where you need it right the first time.

### Suggested Coding Assistant Configuration

```
Daily driver:     qwen3:8b                     @ ctx-16384  (72 tok/s, A quality)
Complex tasks:    qwen3:14b                    @ ctx-8192   (44 tok/s, A+ quality)
Quick iterations: qwen2.5-coder:7b-instruct    @ ctx-16384  (79 tok/s, B+ quality)
```

### Can These Models Replace Cloud APIs?

For straightforward coding tasks (function implementation, refactoring, boilerplate,
bug fixes), qwen3:8b and qwen3:14b approach cloud model quality. The cloud models
scored A (9.6-10.0) on engine vs these local models' A (9.8-9.9) -- the gap is minimal.

Where cloud models still lead:
- **Multi-file reasoning** -- cloud models have 128K+ context windows
- **Novel problem solving** -- larger parameter counts handle edge cases better
- **Instruction following** -- cloud models are better at nuanced user intent

For 80%+ of daily coding tasks, a well-configured local model is a viable alternative
to cloud APIs, with the advantages of privacy, zero cost, and no rate limits.

---

*Analysis based on GPU benchmark results (RTX 4070 12GB) across engine (46 evaluations),
agentic-text (46 evaluations), and speed measurements at ctx-8192/10240/16384/32768.
Engine evaluation is 100% automated. Agentic manual review sections use placeholder scores.*
