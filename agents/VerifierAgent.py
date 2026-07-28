from agno.agent import Agent
from agno.models.google import Gemini
from textwrap import dedent
import json

verifier_agent = Agent(
    name="VerifierAgent",
    role="Validates consistency, alignment, and deduplication across all data sources",
    model=Gemini(id="gemini-3.1-flash-lite-preview"),
    add_name_to_context=True,
    markdown=True,
    instructions=dedent("""
    You are the VerifierAgent - responsible for ensuring data quality and consistency.

    ### Verification Rules:

    1. **Forecast-Alert Alignment**
       - If heavy rain risk flagged (precip_prob > 70% OR rain_rate > 5mm/h):
         Must have corroborating news or context

    2. **News Alignment**
       - News items must relate to the target city
       - Published dates should be recent (within 7 days)
       - Remove duplicates by URL and source

    3. **Data Completeness**
       - Verify all required fields present
       - Validate ISO timestamp formats
       - Flag missing or invalid data

    4. **Output Format**
       Return JSON with:
       - verification_passed: boolean
       - verification_results: {alignment_status, deduplication_summary, completeness_check}
       - validated_data: {cleaned and verified data}
       - recommendations: [list of suggestions]
    """),
)


def verify_data(executor_output: dict) -> dict:
    """
    Verify and validate data from ExecutorAgent

    Args:
        executor_output: Raw data from ExecutorAgent

    Returns:
        Dictionary with verification results and validated data
    """
    prompt = f"""
    Verify the following weather data for consistency and quality:

    {json.dumps(executor_output, indent=2)}

    Check:
    1. Forecast-news alignment (do weather conditions match news mentions?)
    2. News relevance (is news about the correct city and timeframe?)
    3. Deduplication (remove duplicate URLs and sources)
    4. Data completeness (all required fields present?)
    5. Timestamp validation (correct ISO format?)

    Return verification results in JSON format with:
    - verification_passed (true/false)
    - verification_results (detailed checks)
    - validated_data (cleaned data)
    - recommendations (improvements needed)
    """

    response = verifier_agent.run(prompt)

    return {
        "verification_timestamp": json.dumps(executor_output),
        "verification_response": response.content,
        "status": "verified"
    }


if __name__ == "__main__":
    # Test data
    test_data = {
        "city": "Mumbai",
        "weather_forecast": [{"precip_prob": 85, "rain_rate_mmph": 12}],
        "news_items": [{"title": "Mumbai rain alert", "url": "http://example.com"}]
    }
    result = verify_data(test_data)
    print(json.dumps(result, indent=2))