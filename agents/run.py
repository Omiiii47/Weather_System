"""
Main entry point for weather briefing system
Usage: python run.py --city "Mumbai" [--start ISO_TIMESTAMP] [--end ISO_TIMESTAMP]
"""
import argparse
from orchestrator import WeatherBriefOrchestrator
from datetime import datetime, timedelta, timezone
from city_guardrail import CityNameValidationError, validate_city_name


def main():
    parser = argparse.ArgumentParser(description='Generate 24-hour weather risk brief')
    parser.add_argument('--city', type=str, required=True, help='Target city name')
    parser.add_argument('--start', type=str, help='Start time (ISO format)')
    parser.add_argument('--end', type=str, help='End time (ISO format)')

    args = parser.parse_args()

    try:
        args.city = validate_city_name(args.city)
    except CityNameValidationError as exc:
        print(f"Invalid city name: {exc}")
        raise SystemExit(1)

    # Default to next 24 hours if times not specified
    if not args.start:
        now = datetime.now(timezone.utc)
        args.start = now.isoformat().replace('+00:00', 'Z')
        args.end = (now + timedelta(hours=24)).isoformat().replace('+00:00', 'Z')

    # Run the orchestrator
    orchestrator = WeatherBriefOrchestrator()
    orchestrator.run_briefing(
        city=args.city,
        window_start=args.start,
        window_end=args.end
    )


if __name__ == "__main__":
    main()