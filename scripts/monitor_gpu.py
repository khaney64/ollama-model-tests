"""GPU monitoring via nvidia-smi polling."""

import subprocess
import threading
import time
from dataclasses import dataclass, field


@dataclass
class GPUSnapshot:
    """Single GPU measurement."""
    timestamp: float
    vram_used_mb: float
    gpu_utilization_pct: float
    temperature_c: float


@dataclass
class GPUSummary:
    """Aggregated GPU metrics from a monitoring session."""
    peak_vram_mb: float = 0.0
    avg_vram_mb: float = 0.0
    avg_gpu_utilization_pct: float = 0.0
    max_gpu_utilization_pct: float = 0.0
    max_temperature_c: float = 0.0
    sample_count: int = 0

    def to_dict(self) -> dict:
        return {
            "peak_vram_mb": round(self.peak_vram_mb, 1),
            "avg_vram_mb": round(self.avg_vram_mb, 1),
            "avg_gpu_utilization_pct": round(self.avg_gpu_utilization_pct, 1),
            "max_gpu_utilization_pct": round(self.max_gpu_utilization_pct, 1),
            "max_temperature_c": round(self.max_temperature_c, 1),
            "sample_count": self.sample_count,
        }


class GPUMonitor:
    """Polls nvidia-smi in a background thread to capture GPU metrics."""

    def __init__(self, poll_interval: float = 1.0):
        self.poll_interval = poll_interval
        self._snapshots: list[GPUSnapshot] = []
        self._running = False
        self._thread: threading.Thread | None = None

    def start(self):
        """Start background GPU monitoring."""
        self._snapshots = []
        self._running = True
        self._thread = threading.Thread(target=self._poll_loop, daemon=True)
        self._thread.start()

    def stop(self) -> GPUSummary:
        """Stop monitoring and return aggregated summary."""
        self._running = False
        if self._thread:
            self._thread.join(timeout=5)
            self._thread = None
        return self._compute_summary()

    def _poll_loop(self):
        """Continuously poll nvidia-smi until stopped."""
        while self._running:
            snapshot = self._query_gpu()
            if snapshot:
                self._snapshots.append(snapshot)
            time.sleep(self.poll_interval)

    @staticmethod
    def get_gpu_info() -> dict:
        """Query GPU name and total VRAM. Returns empty dict if nvidia-smi unavailable."""
        try:
            result = subprocess.run(
                ["nvidia-smi", "--query-gpu=name,memory.total", "--format=csv,noheader,nounits"],
                capture_output=True, text=True, timeout=5
            )
            if result.returncode == 0:
                parts = [p.strip() for p in result.stdout.strip().split(",")]
                return {"gpu_name": parts[0], "gpu_vram_total_mb": float(parts[1])}
        except (subprocess.TimeoutExpired, FileNotFoundError):
            pass
        return {}

    def _query_gpu(self) -> GPUSnapshot | None:
        """Query nvidia-smi for current GPU metrics."""
        try:
            result = subprocess.run(
                [
                    "nvidia-smi",
                    "--query-gpu=memory.used,utilization.gpu,temperature.gpu",
                    "--format=csv,noheader,nounits",
                ],
                capture_output=True,
                text=True,
                timeout=5,
            )
            if result.returncode != 0:
                return None

            line = result.stdout.strip().split("\n")[0]
            parts = [p.strip() for p in line.split(",")]
            if len(parts) != 3:
                return None

            return GPUSnapshot(
                timestamp=time.time(),
                vram_used_mb=float(parts[0]),
                gpu_utilization_pct=float(parts[1]),
                temperature_c=float(parts[2]),
            )
        except (subprocess.TimeoutExpired, FileNotFoundError, ValueError):
            return None

    def _compute_summary(self) -> GPUSummary:
        """Compute aggregate statistics from collected snapshots."""
        if not self._snapshots:
            return GPUSummary()

        vram_values = [s.vram_used_mb for s in self._snapshots]
        util_values = [s.gpu_utilization_pct for s in self._snapshots]
        temp_values = [s.temperature_c for s in self._snapshots]

        return GPUSummary(
            peak_vram_mb=max(vram_values),
            avg_vram_mb=sum(vram_values) / len(vram_values),
            avg_gpu_utilization_pct=sum(util_values) / len(util_values),
            max_gpu_utilization_pct=max(util_values),
            max_temperature_c=max(temp_values),
            sample_count=len(self._snapshots),
        )


if __name__ == "__main__":
    print("Starting GPU monitor for 10 seconds...")
    monitor = GPUMonitor(poll_interval=1.0)
    monitor.start()
    time.sleep(10)
    summary = monitor.stop()
    print(f"Peak VRAM: {summary.peak_vram_mb} MB")
    print(f"Avg VRAM: {summary.avg_vram_mb} MB")
    print(f"Avg GPU Util: {summary.avg_gpu_utilization_pct}%")
    print(f"Max Temp: {summary.max_temperature_c}°C")
    print(f"Samples: {summary.sample_count}")
