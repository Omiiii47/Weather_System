import csv
import hashlib
from pathlib import Path
from datetime import datetime
from typing import Any, Dict


class ExecutionLogger:
    def __init__(self, output_dir: Path = Path("output")):
        self.output_dir = output_dir
        self.output_dir.mkdir(exist_ok=True)
        self.log_file = self.output_dir / "ExecutionLog.csv"
        self._initialize_csv()

    def _initialize_csv(self):
        """Create CSV with headers if it doesn't exist"""
        if not self.log_file.exists():
            with open(self.log_file, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow([
                    'timestamp',
                    'tool',
                    'params_hash',
                    'status_code',
                    'retry_after_s',
                    'attempt',
                    'latency_ms',
                    'cache_hit',
                    'circuit_state',
                    'outcome_hash'
                ])

    def log_tool_call(
            self,
            tool: str,
            params: Dict[str, Any],
            status_code: int,
            latency_ms: float,
            retry_after_s: float = 0,
            attempt: int = 1,
            cache_hit: bool = False,
            circuit_state: str = "closed",
            outcome: Any = None
    ):
        """Log a single tool call"""
        timestamp = datetime.utcnow().isoformat() + "Z"
        params_hash = hashlib.md5(str(params).encode()).hexdigest()[:8]
        outcome_hash = hashlib.md5(str(outcome).encode()).hexdigest()[:8] if outcome else ""

        with open(self.log_file, 'a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow([
                timestamp,
                tool,
                params_hash,
                status_code,
                retry_after_s,
                attempt,
                latency_ms,
                cache_hit,
                circuit_state,
                outcome_hash
            ])