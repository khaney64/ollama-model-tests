"""Pull recommended models from Ollama."""

import os
import sys

# Allow running from any directory
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import requests
from config import OLLAMA_PULL_URL, OLLAMA_LIST_URL, MODELS_TO_PULL


def get_installed_models() -> set[str]:
    """Get set of already-installed model tags."""
    try:
        resp = requests.get(OLLAMA_LIST_URL, timeout=10)
        resp.raise_for_status()
        data = resp.json()
        return {m["name"] for m in data.get("models", [])}
    except requests.RequestException as e:
        print(f"Warning: Could not query Ollama for installed models: {e}")
        return set()


def pull_model(model: str) -> bool:
    """Pull a single model from Ollama. Returns True on success."""
    print(f"\n{'='*60}")
    print(f"Pulling: {model}")
    print(f"{'='*60}")

    try:
        resp = requests.post(
            OLLAMA_PULL_URL,
            json={"name": model, "stream": True},
            stream=True,
            timeout=3600,
        )
        resp.raise_for_status()

        for line in resp.iter_lines():
            if line:
                import json
                data = json.loads(line)
                status = data.get("status", "")
                if "completed" in data and "total" in data:
                    total = data["total"]
                    completed = data["completed"]
                    pct = (completed / total * 100) if total > 0 else 0
                    print(f"\r  {status}: {pct:.1f}% ({completed}/{total})", end="", flush=True)
                else:
                    print(f"\r  {status}", end="", flush=True)

        print(f"\n  Done: {model}")
        return True

    except requests.RequestException as e:
        print(f"\n  FAILED: {model} - {e}")
        return False


def main():
    print("Ollama Model Puller")
    print("=" * 60)

    installed = get_installed_models()
    if installed:
        print(f"Already installed: {len(installed)} models")
        for m in sorted(installed):
            print(f"  - {m}")

    to_pull = []
    for model in MODELS_TO_PULL:
        if model in installed:
            print(f"  Skipping (already installed): {model}")
        else:
            to_pull.append(model)

    if not to_pull:
        print("\nAll recommended models are already installed!")
        return

    print(f"\nModels to pull: {len(to_pull)}")
    for m in to_pull:
        print(f"  - {m}")

    print(f"\nStarting downloads...")
    success = 0
    failed = 0
    for model in to_pull:
        if pull_model(model):
            success += 1
        else:
            failed += 1

    print(f"\n{'='*60}")
    print(f"Results: {success} succeeded, {failed} failed out of {len(to_pull)}")
    if failed > 0:
        sys.exit(1)


if __name__ == "__main__":
    main()
