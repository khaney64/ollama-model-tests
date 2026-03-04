"""Shared configuration for the Ollama model testing framework."""

import os
import re

# Paths
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REQUIREMENTS_DIR = os.path.join(PROJECT_ROOT, "requirements")
REFACTOR_SOURCE_DIR = os.path.join(PROJECT_ROOT, "refactor-source")
MODELS_DIR = os.path.join(PROJECT_ROOT, "models")
REPORTS_DIR = os.path.join(PROJECT_ROOT, "reports")

# Ollama API
OLLAMA_BASE_URL = "http://localhost:11434"
OLLAMA_GENERATE_URL = f"{OLLAMA_BASE_URL}/api/generate"
OLLAMA_CHAT_URL = f"{OLLAMA_BASE_URL}/api/chat"
OLLAMA_PULL_URL = f"{OLLAMA_BASE_URL}/api/pull"
OLLAMA_LIST_URL = f"{OLLAMA_BASE_URL}/api/tags"

# Tasks
TASKS = ["greenfield", "refactor", "engine", "api", "agentic", "agentic-chat"]

# Execution modes
EXECUTION_MODES = ["cloud", "cpu", "gpu"]

# Agentic task tools reference
AGENTIC_TOOLS_DIR = os.path.join(REQUIREMENTS_DIR, "tools_reference.py")

# Engine task historical data
HISTORICAL_CSV_PATH = os.path.join(REQUIREMENTS_DIR, "historical.csv")

# All models to benchmark
MODELS = [
    # Tier 1: Small (<=6GB) — very comfortable on 3090
    "qwen3:8b",
    "qwen3.5:9b",
    "qwen2.5:7b",
    "qwen2.5-coder:7b-instruct-q5_K_M",
    "phi4:14b-q4_K_M",
    "hf.co/Qwen/Qwen3-8B-GGUF:Q6_K",
    "hf.co/Qwen/Qwen3-8B-GGUF:Q8_0",
    "hf.co/DevQuasar/Nanbeige.Nanbeige4.1-3B-GGUF:q4_K_M",
    "hf.co/DevQuasar/Nanbeige.Nanbeige4.1-3B-GGUF:q5_K_M",
    "hf.co/DevQuasar/Nanbeige.Nanbeige4.1-3B-GGUF:q6_K",
    "hf.co/DevQuasar/Nanbeige.Nanbeige4.1-3B-GGUF:q8_0",
    # Tier 2: Mid (7-15GB) — comfortable on 3090, larger context available
    "qwen3:14b",
    "qwen2.5-coder:14b-instruct-q4_K_M",
    # Tier 3: Large (16-21GB) — comfortable on 3090, was partial offload on 4070
    "glm-4.7-flash:q4_K_M",
    "qwen3:32b",
    "qwen3.5:27b",
    "qwen3.5:35b-a3b",
    "qwen3-coder:30b",
    "qwen2.5-coder:32b-instruct-q4_K_M",
    "hf.co/unsloth/gpt-oss-20b-GGUF:Q4_K_M",
    "hf.co/unsloth/gpt-oss-20b-GGUF:Q5_K_M",
    # Tier 4: Cloud models
    "kimi-k2.5:cloud",
    "glm-4.7:cloud",
    "glm-5:cloud",
    "minimax-m2.5:cloud",
    "qwen3-coder-next:cloud",
]

# Models to pull (not already installed)
MODELS_TO_PULL = [
    # Small
    "qwen3:8b",
    "qwen2.5:7b",
    "qwen2.5-coder:7b-instruct-q5_K_M",
    "phi4:14b-q4_K_M",
    "hf.co/Qwen/Qwen3-8B-GGUF:Q6_K",
    "hf.co/Qwen/Qwen3-8B-GGUF:Q8_0",
    # Mid
    "qwen3:14b",
    "qwen2.5-coder:14b-instruct-q4_K_M",
    # Large (new for 3090)
    "qwen3:32b",
    "qwen3.5:27b",
    "qwen3.5:35b-a3b",
    "qwen3-coder:30b",
    "qwen2.5-coder:32b-instruct-q4_K_M",
    "glm-4.7-flash:q4_K_M",
]

# Context sizes per model (num_ctx for Ollama API) — tuned for RTX 3090 24GB
# Tier 1 small (<=9GB): 32768 — ~15-19GB free, ample KV cache headroom
# Tier 2 mid (9-15GB): 32768 — ~15GB free, still comfortable
# Tier 3 large (16-21GB): 16384 — 3-8GB free, safe for 24GB; 32K would risk OOM on 20-21GB models
MODEL_NUM_CTX = {
    # Tier 1: Small (<=9GB)
    "qwen3:8b": 32768,
    "qwen3.5:9b": 32768,
    "qwen2.5:7b": 32768,
    "qwen2.5-coder:7b-instruct-q5_K_M": 32768,
    "phi4:14b-q4_K_M": 32768,
    "hf.co/Qwen/Qwen3-8B-GGUF:Q6_K": 32768,
    "hf.co/Qwen/Qwen3-8B-GGUF:Q8_0": 32768,
    "hf.co/DevQuasar/Nanbeige.Nanbeige4.1-3B-GGUF:q4_K_M": 32768,
    "hf.co/DevQuasar/Nanbeige.Nanbeige4.1-3B-GGUF:q5_K_M": 32768,
    "hf.co/DevQuasar/Nanbeige.Nanbeige4.1-3B-GGUF:q6_K": 32768,
    "hf.co/DevQuasar/Nanbeige.Nanbeige4.1-3B-GGUF:q8_0": 32768,
    # Tier 2: Mid (9-15GB)
    "qwen3:14b": 32768,
    "qwen2.5-coder:14b-instruct-q4_K_M": 32768,
    # Tier 3: Large (16-21GB) — fully resident in 3090 VRAM
    "glm-4.7-flash:q4_K_M": 16384,
    "qwen3:32b": 16384,
    "qwen3.5:27b": 16384,
    "qwen3.5:35b-a3b": 16384,
    "qwen3-coder:30b": 16384,
    "qwen2.5-coder:32b-instruct-q4_K_M": 16384,
    "hf.co/unsloth/gpt-oss-20b-GGUF:Q4_K_M": 16384,
    "hf.co/unsloth/gpt-oss-20b-GGUF:Q5_K_M": 16384,
    # Cloud models (no VRAM constraint)
    "kimi-k2.5:cloud": 32768,
    "glm-4.7:cloud": 32768,
    "glm-5:cloud": 32768,
    "minimax-m2.5:cloud": 32768,
    "qwen3-coder-next:cloud": 32768,
}

DEFAULT_NUM_CTX = 4096


def get_num_ctx(model: str) -> int:
    """Get the context size for a model, falling back to DEFAULT_NUM_CTX."""
    return MODEL_NUM_CTX.get(model, DEFAULT_NUM_CTX)


# Max output tokens per model (num_predict for Ollama API)
# Default: match num_ctx so the context window is the only limit.
# No reason to cap output below the context size — truncation loses data.
MODEL_NUM_PREDICT = {}

DEFAULT_NUM_PREDICT = None  # None means use num_ctx


def get_num_predict(model: str) -> int:
    """Get the max output tokens for a model. Defaults to num_ctx (no artificial cap)."""
    override = MODEL_NUM_PREDICT.get(model)
    if override is not None:
        return override
    return get_num_ctx(model)


# Model metadata: (tier, approximate size in GB)
# Tier 1: Small (<=6GB), Tier 2: Mid (7-15GB),
# Tier 3: Large (16-21GB, fully resident on 3090), Tier 4: Cloud
MODEL_META = {
    # Tier 1: Small (<=6GB)
    "qwen3:8b": (1, 5.2),
    "qwen3.5:9b": (1, 5.8),
    "qwen2.5:7b": (1, 4.7),
    "qwen2.5-coder:7b-instruct-q5_K_M": (1, 5.4),
    "hf.co/Qwen/Qwen3-8B-GGUF:Q6_K": (1, 6.6),
    "hf.co/Qwen/Qwen3-8B-GGUF:Q8_0": (1, 8.5),
    "hf.co/DevQuasar/Nanbeige.Nanbeige4.1-3B-GGUF:q4_K_M": (1, 2.44),
    "hf.co/DevQuasar/Nanbeige.Nanbeige4.1-3B-GGUF:q5_K_M": (1, 2.83),
    "hf.co/DevQuasar/Nanbeige.Nanbeige4.1-3B-GGUF:q6_K": (1, 3.28),
    "hf.co/DevQuasar/Nanbeige.Nanbeige4.1-3B-GGUF:q8_0": (1, 4.18),
    # Tier 2: Mid (7-15GB)
    "phi4:14b-q4_K_M": (2, 9.1),
    "qwen3:14b": (2, 9.3),
    "qwen2.5-coder:14b-instruct-q4_K_M": (2, 9.0),
    # Tier 3: Large (16-21GB) — fully resident in 3090 VRAM
    "glm-4.7-flash:q4_K_M": (3, 19.0),
    "qwen3:32b": (3, 20.0),
    "qwen3.5:27b": (3, 16.0),
    "qwen3.5:35b-a3b": (3, 21.0),
    "qwen3-coder:30b": (3, 19.0),
    "qwen2.5-coder:32b-instruct-q4_K_M": (3, 19.0),
    "hf.co/unsloth/gpt-oss-20b-GGUF:Q4_K_M": (3, 12.5),
    "hf.co/unsloth/gpt-oss-20b-GGUF:Q5_K_M": (3, 14.5),
    # Tier 4: Cloud
    "kimi-k2.5:cloud": (4, 0),
    "glm-4.7:cloud": (4, 0),
    "glm-5:cloud": (4, 0),
    "minimax-m2.5:cloud": (4, 0),
    "qwen3-coder-next:cloud": (4, 0),
}

DEFAULT_MODEL_META = (99, 0)  # Unknown models sort last


def get_model_meta(model: str) -> tuple:
    """Get (tier, size_gb) for a model, falling back to DEFAULT_MODEL_META."""
    return MODEL_META.get(model, DEFAULT_MODEL_META)


def is_cloud_model(model: str) -> bool:
    """Return True if model is a cloud/API model (tier 4)."""
    tier, _ = get_model_meta(model)
    return tier == 4


def get_chat_temperature(model: str) -> float:
    """Get recommended temperature for chat/tool-calling mode.

    Smaller models need lower temperature for reliable structured output.
    """
    _, size_gb = get_model_meta(model)
    if size_gb <= 4.0:   # 3B models
        return 0.2
    elif size_gb <= 8.0:  # 7-8B models
        return 0.3
    else:                 # 12B+ models
        return 0.4


# GPU monitoring interval in seconds
GPU_POLL_INTERVAL = 1.0


def model_to_dirname(model: str) -> str:
    """Convert an Ollama model tag to a Windows-safe directory name.

    Replaces '/' with '__' and ':' with '(' and appends ')'.
    Examples:
        llama3.1:8b -> llama3.1(8b)
        qwen2.5-coder:7b-instruct-q5_K_M -> qwen2.5-coder(7b-instruct-q5_K_M)
        llama3.2:latest -> llama3.2(latest)
        hf.co/unsloth/gpt-oss-20b-GGUF:Q4_K_M -> hf.co__unsloth__gpt-oss-20b-GGUF(Q4_K_M)
    """
    safe = model.replace("/", "__")
    if ":" in safe:
        name, tag = safe.split(":", 1)
        return f"{name}({tag})"
    return safe


def dirname_to_model(dirname: str) -> str:
    """Convert a directory name back to an Ollama model tag.

    Examples:
        llama3.1(8b) -> llama3.1:8b
        qwen2.5-coder(7b-instruct-q5_K_M) -> qwen2.5-coder:7b-instruct-q5_K_M
        hf.co__unsloth__gpt-oss-20b-GGUF(Q4_K_M) -> hf.co/unsloth/gpt-oss-20b-GGUF:Q4_K_M
    """
    match = re.match(r"^(.+)\((.+)\)$", dirname)
    if match:
        name = match.group(1).replace("__", "/")
        return f"{name}:{match.group(2)}"
    return dirname.replace("__", "/")


def get_model_results_dir(model: str, task: str, mode: str = None, ctx_size: int = None) -> str:
    """Get results directory path. For GPU mode, optionally include ctx-size subfolder."""
    dirname = model_to_dirname(model)
    path = os.path.join(MODELS_DIR, dirname, "results", task)
    if mode:
        path = os.path.join(path, mode)
        if mode == "gpu" and ctx_size is not None:
            path = os.path.join(path, f"ctx-{ctx_size}")
    return path
