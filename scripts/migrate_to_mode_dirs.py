"""One-time migration: move existing results into cpu/ or cloud/ subdirectories."""

import os
import json
import shutil
import sys

# Allow running from any directory
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from config import MODELS_DIR, TASKS, model_to_dirname, dirname_to_model, is_cloud_model

def migrate():
    """Move all existing top-level results into mode subdirectories."""
    moved_count = 0

    for model_dir_name in os.listdir(MODELS_DIR):
        model_path = os.path.join(MODELS_DIR, model_dir_name)
        if not os.path.isdir(model_path):
            continue

        model_name = dirname_to_model(model_dir_name)
        mode = "cloud" if is_cloud_model(model_name) else "cpu"

        for task in TASKS:
            task_dir = os.path.join(model_path, "results", task)
            if not os.path.isdir(task_dir):
                continue

            # Check for top-level metrics.json (unmigrated)
            metrics_file = os.path.join(task_dir, "metrics.json")
            output_file = os.path.join(task_dir, "output.md")

            if os.path.exists(metrics_file):
                # Create mode subdirectory
                mode_dir = os.path.join(task_dir, mode)
                os.makedirs(mode_dir, exist_ok=True)

                # Move files
                shutil.move(metrics_file, os.path.join(mode_dir, "metrics.json"))
                if os.path.exists(output_file):
                    shutil.move(output_file, os.path.join(mode_dir, "output.md"))

                # Move task-specific files (engine)
                if task == "engine":
                    for extra_file in ["trading_engine.py", "output.csv", "historical.csv", "failure.md"]:
                        extra_path = os.path.join(task_dir, extra_file)
                        if os.path.exists(extra_path):
                            shutil.move(extra_path, os.path.join(mode_dir, extra_file))

                # Add execution_mode to metrics retroactively
                migrated_metrics_path = os.path.join(mode_dir, "metrics.json")
                with open(migrated_metrics_path, "r") as f:
                    metrics = json.load(f)
                metrics["execution_mode"] = mode
                metrics["run_timestamp"] = "2026-02-09T00:00:00"  # Placeholder
                with open(migrated_metrics_path, "w") as f:
                    json.dump(metrics, f, indent=2)

                moved_count += 1
                print(f"Migrated {model_name}/{task} -> {mode}/")

            # Handle existing cpu-test/ subfolders (engine task)
            if task == "engine":
                cpu_test_dir = os.path.join(task_dir, "cpu-test")
                if os.path.isdir(cpu_test_dir):
                    # Move cpu-test contents into cpu/ (they're the same thing)
                    cpu_dir = os.path.join(task_dir, "cpu")
                    if not os.path.isdir(cpu_dir):
                        shutil.move(cpu_test_dir, cpu_dir)
                        print(f"Renamed {model_name}/engine/cpu-test -> cpu/")
                    else:
                        print(f"Warning: {model_name}/engine has both cpu/ and cpu-test/. Manual merge needed.")

    print(f"\nMigration complete. Moved {moved_count} result sets.")

if __name__ == "__main__":
    migrate()
