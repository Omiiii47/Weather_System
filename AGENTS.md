# Technograd — Agent Guide

## What this is

Multi-agent AI weather briefing system. Given a city name, it produces a 24-hour weather risk brief using Google Gemini and various data tools.

## Commands

- Setup: `pip install -r requirements.txt`, then create `.env` with `GOOGLE_API_KEY` and `OPENWEATHER_API_KEY`
- CLI: `python agents/run.py --city "Mumbai"` — optional `--start` / `--end` ISO timestamps (default: next 24h)
- Streamlit UI: `streamlit run streamlit_app.py`
- **Run from the repo root.** All outputs go to `output/` relative to the CWD; running inside `agents/` silently creates `agents/output/`.
- There are no tests, linter, formatter, or CI configs — don't hunt for one; verify changes by running the CLI or UI.

## Pipeline (orchestrated in `agents/orchestrator.py`)

```
PlannerAgent → ExecutorAgent → VerifierAgent → SummarizerAgent
```

All agents use **agno** (not LangChain/CrewAI) + `agno.models.google.Gemini` with id `gemini-3.1-flash-lite-preview`. Executor tools: `OpenWeatherTools`, `WikipediaTools`, `HackerNewsTools`.

## Import convention

Modules inside `agents/` use **flat imports** (`from orchestrator import ...`), not package-relative ones. The CLI works because Python puts the script's directory on `sys.path`; `streamlit_app.py` manually inserts `agents/` into `sys.path`. Keep new modules flat.

## Key files

| File | Purpose |
|---|---|
| `agents/run.py` | CLI entrypoint with argparse |
| `agents/orchestrator.py` | `WeatherBriefOrchestrator` — coordinates pipeline |
| `agents/PlannerAgent.py` + `planner_prompt.py` | Generates workflow plan (instructions live in `planner_prompt.py`) |
| `agents/ExecutorAgent.py` | Gathers data via OpenWeather/Wikipedia/HackerNews tools |
| `agents/VerifierAgent.py` | Validates consistency, deduplication, completeness |
| `agents/SummarizerAgent.py` | Writes `output/brief.md` + `output/brief.json` |
| `agents/city_guardrail.py` | Input validation (see below) |
| `agents/execution_logger.py` | Appends rows to `output/ExecutionLog.csv` |

## Outputs (all written to `output/`, tracked in git)

- `brief.md` — human-readable weather brief
- `brief.json` — **not** the structured schema the prompts describe: the SummarizerAgent writes `{"generated_at", "content"}` where `content` is the raw markdown string. Don't assume `headline_risks`/`alerts` fields exist here.
- `ExecutionLog.csv` — tool-call log, but rows are **simulated**: `ExecutorAgent` hardcodes `status_code=200` and splits latency by 3. Not real telemetry.
- `execution_log.json` — per-step agent log; written even when the pipeline fails

## City input guardrail (`agents/city_guardrail.py`)

`validate_city_name()` runs in CLI, orchestrator, and Streamlit. Rejects: >80 chars, >4 tokens, digits, URLs/emails (`http`, `www.`, `@`, `/`), and a fixed word list including `weather`, `forecast`, `city`, `today`, `report`. `New York` passes; `weather in Mumbai` fails.

## Env loading

- CLI path: each agent module calls `load_dotenv()` at import time.
- Streamlit (`streamlit_app.py`): loads `.env` first, then overrides with `st.secrets` values when they exist and don't start with `your-`. If `GOOGLE_API_KEY`/`OPENWEATHER_API_KEY` is still missing, a preflight check shows `st.error` and stops **before** importing the orchestrator (tools are constructed at import time and crash otherwise).
- `.streamlit/secrets.toml` is untracked (gitignored) — real keys go in local `.env` or the Streamlit Cloud **App settings → Secrets** console, never in the repo.
