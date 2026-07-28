from agno.agent import Agent
from agno.models.google import Gemini
from textwrap import dedent
from planner_prompt import planner_instructions

planner_agent = Agent(
    name="PlannerAgent",
    role="Plans multi-agent workflow for generating a 24-hour weather risk brief.",
    model=Gemini(id="gemini-3.1-flash-lite-preview"),
    add_name_to_context=True,
    markdown=True,
    instructions=planner_instructions
)


def create_plan(city: str, window_start: str, window_end: str) -> dict:
    """
    Generate execution plan for weather brief

    Args:
        city: Target city name
        window_start: ISO timestamp for start of 24h window
        window_end: ISO timestamp for end of 24h window

    Returns:
        Dictionary containing workflow plan
    """
    prompt = f"""
    Create a detailed execution plan for generating a 24-hour weather risk brief.

    Target City: {city}
    Time Window: {window_start} to {window_end}

    Provide a JSON workflow with steps for ExecutorAgent, VerifierAgent, and SummarizerAgent.
    """

    response = planner_agent.run(prompt)
    return {
        "city": city,
        "window_start": window_start,
        "window_end": window_end,
        "plan": response.content
    }


if __name__ == "__main__":
    plan = create_plan(
        city="Mumbai",
        window_start="2025-11-01T00:00:00Z",
        window_end="2025-11-02T00:00:00Z"
    )
    print(plan)