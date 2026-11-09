from agno.agent import Agent
from agno.models.google import Gemini
from textwrap import dedent
import json
from pathlib import Path

summarizer_agent = Agent(
    name="SummarizerAgent",
    role="Produces clear, actionable resident-facing brief and structured machine-readable report",
    model=Gemini(id="gemini-3.5-flash-lite"),
    add_name_to_context=True,
    markdown=True,
    instructions=dedent("""
    You are the SummarizerAgent - create the final weather risk brief.

    ### Output Requirements:

    1. **brief.md** (Human-Readable)
       - 1-2 screen summary for residents
       - Structure: What → When → Where → How to Prepare
       - Include 2-3 corroborating news mentions
       - Clear risk levels (High/Moderate/Low)

    2. **brief.json** (Machine-Readable)
       Required fields:
       - city, window_start_iso, window_end_iso
       - headline_risks: [{risk_type, level, start_iso, end_iso, rationale}]
       - alerts: [{title, severity, effective_iso, expires_iso, regions, uri}]
       - forecast_highlights: [{time_iso, precip_prob, rain_rate_mmph, wind_gust_kmph, temp_c, tags}]
       - corroborating_news: [{title, url, source, published_iso}]
       - notes: [{kind, text}]

    ### Risk Levels:
    - High: precip_prob > 70% AND rain_rate > 10mm/h, OR wind > 60km/h
    - Moderate: precip_prob 50-70% OR rain_rate 5-10mm/h, OR wind 40-60km/h
    - Low: below moderate thresholds
    """),
)


def create_brief(verified_data: dict) -> dict:
    """
    Create final weather brief in markdown and JSON formats

    Args:
        verified_data: Validated data from VerifierAgent

    Returns:
        Dictionary with brief.md and brief.json content
    """
    prompt = f"""
    Create a comprehensive 24-hour weather risk brief from this verified data:

    {json.dumps(verified_data, indent=2)}

    Generate TWO outputs:

    1. **brief.md** - Markdown format for residents:
       # 24-Hour Weather Risk Brief: [City]
       ## Key Risks
       [List risks with timing and severity]
       ## Recent Updates
       [2-3 news items]
       ## How to Prepare
       [Actionable advice]

    2. **brief.json** - Complete JSON with all required fields:
       {{
         "city": "...",
         "window_start_iso": "...",
         "window_end_iso": "...",
         "headline_risks": [...],
         "alerts": [...],
         "forecast_highlights": [...],
         "corroborating_news": [...],
         "notes": [...]
       }}

    Ensure all timestamps are ISO format and risk levels are justified.
    """

    response = summarizer_agent.run(prompt)

    # Save outputs
    output_dir = Path("output")
    output_dir.mkdir(exist_ok=True)

    # Extract and save brief.md
    brief_md = response.content
    (output_dir / "brief.md").write_text(brief_md, encoding='utf-8')

    # Create brief.json structure
    brief_json = {
        "generated_at": verified_data.get("verification_timestamp", ""),
        "content": response.content
    }
    (output_dir / "brief.json").write_text(json.dumps(brief_json, indent=2), encoding='utf-8')

    return {
        "brief_md": brief_md,
        "brief_json": brief_json,
        "status": "completed"
    }


if __name__ == "__main__":
    test_data = {
        "city": "Mumbai",
        "weather_forecast": [{"precip_prob": 85, "rain_rate_mmph": 12}]
    }
    result = create_brief(test_data)
    print("Brief created successfully!")