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
    # Tier 1: Comfortable fit (<10GB)
    "qwen3:8b",
    "qwen2.5:7b",
    "qwen2.5-coder:7b-instruct-q5_K_M",
    "gemma2:9b-instruct-q4_K_M",
    "gemma3:12b-it-q4_K_M",
    "mistral:7b-instruct-v0.3-q5_K_M",
    "phi4:14b-q4_K_M",
    "llama3.1:8b-instruct-q4_K_M",
    "llama3.2:latest",
    "hf.co/Qwen/Qwen3-8B-GGUF:Q6_K",
    "hf.co/Qwen/Qwen3-8B-GGUF:Q8_0",
    # Tier 2: Tight fit (9-11GB)
    "qwen3:14b",
    "qwen2.5-coder:14b-instruct-q4_K_M",
    "deepseek-coder-v2:16b",
    # Tier 3: Partial offload
    "glm-4.7-flash:q4_K_M",
    # Tier 4: Cloud models
    "kimi-k2.5:cloud",
    "glm-4.7:cloud",
    "glm-5:cloud",
    "minimax-m2.5:cloud",
    "qwen3-coder-next:cloud",
    # Other installed
    "qwen2.5-coder:7b",
    "llama3.1:8b",
]

# Models to pull (not already installed)
MODELS_TO_PULL = [
    "qwen3:8b",
    "qwen3:14b",
    "qwen2.5:7b",
    "qwen2.5-coder:7b-instruct-q5_K_M",
    "qwen2.5-coder:14b-instruct-q4_K_M",
    "phi4:14b-q4_K_M",
    "gemma3:12b-it-q4_K_M",
    "gemma2:9b-instruct-q4_K_M",
    "mistral:7b-instruct-v0.3-q5_K_M",
    "hf.co/Qwen/Qwen3-8B-GGUF:Q6_K",
    "hf.co/Qwen/Qwen3-8B-GGUF:Q8_0",
]

# Context sizes per model (num_ctx for Ollama API)
# Tier 1 (<10GB): 8192 — comfortable fit, plenty of room for KV cache
# Tier 2 (9-11GB): 4096 — tight fit, keep context small
# Tier 3 (>12GB): 4096 — partial offload to RAM, minimize VRAM pressure
MODEL_NUM_CTX = {
    # Tier 1: Comfortable fit
    "qwen3:8b": 8192,
    "qwen2.5:7b": 8192,
    "qwen2.5-coder:7b-instruct-q5_K_M": 8192,
    "gemma2:9b-instruct-q4_K_M": 8192,
    "gemma3:12b-it-q4_K_M": 8192,
    "mistral:7b-instruct-v0.3-q5_K_M": 8192,
    "phi4:14b-q4_K_M": 8192,
    "llama3.1:8b-instruct-q4_K_M": 8192,
    "llama3.2:latest": 8192,
    "hf.co/Qwen/Qwen3-8B-GGUF:Q6_K": 8192,
    "hf.co/Qwen/Qwen3-8B-GGUF:Q8_0": 8192,
    # Tier 2: Tight fit
    "qwen3:14b": 4096,
    "qwen2.5-coder:14b-instruct-q4_K_M": 4096,
    "deepseek-coder-v2:16b": 4096,
    # Tier 3: Partial offload
    "glm-4.7-flash:q4_K_M": 4096,
    # Cloud models (no VRAM constraint)
    "kimi-k2.5:cloud": 32768,
    "glm-4.7:cloud": 32768,
    "glm-5:cloud": 32768,
    "minimax-m2.5:cloud": 32768,
    "qwen3-coder-next:cloud": 32768,
    # Other installed
    "qwen2.5-coder:7b": 8192,
    "llama3.1:8b": 8192,
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
# Tier 1: Comfortable fit (<10GB), Tier 2: Tight fit (9-11GB),
# Tier 3: Partial offload (>12GB), Tier 4: Cloud
MODEL_META = {
    # Tier 1: Comfortable fit
    "qwen3:8b": (1, 5.2),
    "qwen2.5:7b": (1, 4.7),
    "qwen2.5-coder:7b-instruct-q5_K_M": (1, 5.4),
    "gemma2:9b-instruct-q4_K_M": (1, 5.8),
    "gemma3:12b-it-q4_K_M": (1, 8.1),
    "mistral:7b-instruct-v0.3-q5_K_M": (1, 5.1),
    "phi4:14b-q4_K_M": (1, 9.1),
    "llama3.1:8b-instruct-q4_K_M": (1, 4.9),
    "llama3.2:latest": (1, 2.0),
    "hf.co/Qwen/Qwen3-8B-GGUF:Q6_K": (1, 6.6),
    "hf.co/Qwen/Qwen3-8B-GGUF:Q8_0": (1, 8.5),
    # Tier 2: Tight fit
    "qwen3:14b": (2, 9.3),
    "qwen2.5-coder:14b-instruct-q4_K_M": (2, 9.0),
    "deepseek-coder-v2:16b": (2, 10.0),
    # Tier 3: Partial offload
    "glm-4.7-flash:q4_K_M": (3, 19.0),
    # Tier 4: Cloud
    "kimi-k2.5:cloud": (4, 0),
    "glm-4.7:cloud": (4, 0),
    "glm-5:cloud": (4, 0),
    "minimax-m2.5:cloud": (4, 0),
    "qwen3-coder-next:cloud": (4, 0),
    # Other installed
    "qwen2.5-coder:7b": (1, 4.7),
    "llama3.1:8b": (1, 4.9),
}

DEFAULT_MODEL_META = (99, 0)  # Unknown models sort last


def get_model_meta(model: str) -> tuple:
    """Get (tier, size_gb) for a model, falling back to DEFAULT_MODEL_META."""
    return MODEL_META.get(model, DEFAULT_MODEL_META)


def is_cloud_model(model: str) -> bool:
    """Return True if model is a cloud/API model (tier 4)."""
    tier, _ = get_model_meta(model)
    return tier == 4


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
