"""
Orchestrator for multi-agent weather briefing system
Coordinates: PlannerAgent → ExecutorAgent → VerifierAgent → SummarizerAgent
"""

from PlannerAgent import create_plan
from ExecutorAgent import execute_data_gathering
from VerifierAgent import verify_data
from SummarizerAgent import create_brief
from execution_logger import ExecutionLogger
from city_guardrail import CityNameValidationError, validate_city_name
import json
from pathlib import Path
from datetime import datetime, timedelta


class WeatherBriefOrchestrator:
    def __init__(self):
        self.execution_log = []
        self.tool_logger = ExecutionLogger()

    def log_step(self, agent: str, status: str, details: dict):
        """Log each agent execution step"""
        log_entry = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "agent": agent,
            "status": status,
            "details": details
        }
        self.execution_log.append(log_entry)
        print(f"\n{'=' * 60}")
        print(f"[{agent}] {status}")
        print(f"{'=' * 60}")

    def run_briefing(self, city: str, window_start: str = None, window_end: str = None):
        """
        Execute complete weather briefing workflow

        Args:
            city: Target city name
            window_start: ISO timestamp (default: now)
            window_end: ISO timestamp (default: now + 24h)
        """
        try:
            city = validate_city_name(city)
        except CityNameValidationError as exc:
            self.log_step("InputValidation", "FAILED", {"city": city, "error": str(exc)})
            self._save_execution_log()
            raise

        # Set default time window if not provided
        if not window_start:
            now = datetime.utcnow()
            window_start = now.isoformat() + "Z"
            window_end = (now + timedelta(hours=24)).isoformat() + "Z"

        print(f"\n🌤️  Starting Weather Brief Generation")
        print(f"City: {city}")
        print(f"Window: {window_start} to {window_end}\n")

        try:
            # Step 1: PlannerAgent
            self.log_step("PlannerAgent", "STARTED", {"city": city})
            plan = create_plan(city, window_start, window_end)
            self.log_step("PlannerAgent", "COMPLETED", {"plan": "Workflow created"})

            # Step 2: ExecutorAgent (with tool logging)
            self.log_step("ExecutorAgent", "STARTED", {"task": "Data gathering"})
            executor_output = execute_data_gathering(city, window_start, window_end, self.tool_logger)
            self.log_step("ExecutorAgent", "COMPLETED", {"data_collected": True})

            # Step 3: VerifierAgent
            self.log_step("VerifierAgent", "STARTED", {"task": "Data verification"})
            verified_data = verify_data(executor_output)
            self.log_step("VerifierAgent", "COMPLETED", {"verification": "passed"})

            # Step 4: SummarizerAgent
            self.log_step("SummarizerAgent", "STARTED", {"task": "Brief generation"})
            final_brief = create_brief(verified_data)
            self.log_step("SummarizerAgent", "COMPLETED", {"output": "brief.md & brief.json"})

            # Save execution log
            self._save_execution_log()

            print("\n✅ Weather Brief Generation COMPLETE")
            print(f"📄 Outputs saved in ./output/")
            print(f"   - brief.md")
            print(f"   - brief.json")
            print(f"   - ExecutionLog.csv")
            print(f"   - execution_log.json")

            return final_brief

        except Exception as e:
            self.log_step("ERROR", "FAILED", {"error": str(e)})
            self._save_execution_log()
            raise

    def _save_execution_log(self):
        """Save execution log to file"""
        output_dir = Path("output")
        output_dir.mkdir(exist_ok=True)

        log_file = output_dir / "execution_log.json"
        log_file.write_text(json.dumps(self.execution_log, indent=2), encoding='utf-8')


if __name__ == "__main__":
    orchestrator = WeatherBriefOrchestrator()
    orchestrator.run_briefing(
        city="Mumbai",
        window_start="2025-11-01T00:00:00Z",
        window_end="2025-11-02T00:00:00Z"
    )