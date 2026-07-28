# Technograd — Agent Guide

## What this is

Multi-agent AI weather briefing system. Given a city name, it produces a 24-hour weather risk brief using Google Gemini and various data tools.

## Entrypoints

- **CLI:** `python agents/run.py --city "Mumbai"`  
  Optional: `--start ISO_TIMESTAMP --end ISO_TIMESTAMP` (defaults to next 24h)
- **Streamlit UI:** `streamlit run streamlit_app.py`

## Pipeline (orchestrated in `agents/orchestrator.py`)

```
PlannerAgent → ExecutorAgent → VerifierAgent → SummarizerAgent
```

All agents use `agno` framework + `Gemini` model (`gemini-3.1-flash-lite-preview`).

## Key files

| File | Purpose |
|---|---|
| `agents/run.py` | CLI entrypoint with argparse |
| `agents/orchestrator.py` | `WeatherBriefOrchestrator` — coordinates pipeline |
| `agents/PlannerAgent.py` | Generates workflow plan |
| `agents/ExecutorAgent.py` | Gathers data (OpenWeather, Wikipedia, HackerNews tools) |
| `agents/VerifierAgent.py` | Validates consistency, deduplication, completeness |
| `agents/SummarizerAgent.py` | Writes `output/brief.md` + `output/brief.json` |
| `agents/city_guardrail.py` | Input validation — rejects URLs, digits, request words, >4 tokens |
| `agents/execution_logger.py` | Logs tool calls to `output/ExecutionLog.csv` |
| `.env` | Required: `GOOGLE_API_KEY`, `OPENWEATHER_API_KEY` |

## Outputs (all to `output/`)

- `brief.md` — human-readable weather brief
- `brief.json` — machine-readable risk data
- `ExecutionLog.csv` — per-tool-call log
- `execution_log.json` — agent step log

## Framework & dependencies

- Framework: **agno** (not LangChain, not CrewAI)
- Model: `gemini-3.1-flash-lite-preview` via `agno.models.google.Gemini`
- Tools: `agno.tools.openweather.OpenWeatherTools`, `WikipediaTools`, `HackerNewsTools`
- Env: `python-dotenv` — call `load_dotenv()` before agent init

## Gotchas

- Virtual env at `myenv/` is **broken** (wrong Python path). Install deps fresh: `pip install agno python-dotenv google-genai firecrawl-py`
- No `requirements.txt`, `pyproject.toml`, or `setup.py` — deps are ad-hoc
- No tests, no formatter, no linter configured
- `dontuseit/` directory is abandoned code, ignore it
- City names are strictly validated: max 80 chars, max 4 tokens, no digits/URLs/request words
