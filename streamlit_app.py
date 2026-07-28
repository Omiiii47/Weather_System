import streamlit as st
import sys
import io
import json
from pathlib import Path
from contextlib import redirect_stdout

sys.path.insert(0, str(Path(__file__).parent / "agents"))
from orchestrator import WeatherBriefOrchestrator
from city_guardrail import CityNameValidationError, validate_city_name

st.set_page_config(
    page_title="Weather Risk Brief",
    page_icon="🌤️",
    layout="wide",
)

st.title("🌤️ 24-Hour Weather Risk Brief Generator")
st.markdown("Enter a city name to generate a comprehensive weather risk brief.")

with st.sidebar:
    st.header("Settings")
    city = st.text_input(
        "City Name",
        placeholder="e.g. Mumbai, New York, Tokyo",
        value="Mumbai",
    )

    generate = st.button("🚀 Generate Brief", type="primary", use_container_width=True)

if generate:
    if not city.strip():
        st.error("Please enter a city name.")
        st.stop()

    try:
        city = validate_city_name(city)
    except CityNameValidationError as exc:
        st.error(f"Invalid city name: {exc}")
        st.stop()

    log_placeholder = st.empty()
    tab_md, tab_json, tab_log = st.tabs(["📄 Brief (Markdown)", "📊 Brief (JSON)", "📋 Execution Log"])

    logs = []

    with st.spinner(f"Generating weather brief for {city}..."):
        buf = io.StringIO()
        try:
            with redirect_stdout(buf):
                orchestrator = WeatherBriefOrchestrator()
                result = orchestrator.run_briefing(city=city)

            output = buf.getvalue()
            logs.append(output)

            with log_placeholder.container():
                st.text_area("Pipeline Log", output, height=200)

            output_dir = Path("output")

            brief_md_path = output_dir / "brief.md"
            brief_json_path = output_dir / "brief.json"
            exec_log_path = output_dir / "execution_log.json"
            csv_log_path = output_dir / "ExecutionLog.csv"

            with tab_md:
                if brief_md_path.exists():
                    st.markdown(brief_md_path.read_text(encoding="utf-8"))
                else:
                    st.warning("brief.md not yet generated. The agent may still be processing.")

            with tab_json:
                if brief_json_path.exists():
                    data = json.loads(brief_json_path.read_text(encoding="utf-8"))
                    st.json(data)
                else:
                    st.warning("brief.json not yet generated.")

            with tab_log:
                if exec_log_path.exists():
                    log_data = json.loads(exec_log_path.read_text(encoding="utf-8"))
                    st.json(log_data)
                else:
                    st.warning("execution_log.json not available.")

                if csv_log_path.exists():
                    with open(csv_log_path, encoding="utf-8") as f:
                        st.download_button(
                            label="📥 Download ExecutionLog.csv",
                            data=f,
                            file_name="ExecutionLog.csv",
                            mime="text/csv",
                        )

            st.success(f"✅ Weather brief for {city} generated successfully!")

        except Exception as e:
            output = buf.getvalue()
            st.error(f"❌ Failed to generate brief: {e}")
            with st.expander("Error Details & Logs"):
                st.code(output)
else:
    st.info("👈 Enter a city name and click **Generate Brief** to get started.")

    st.markdown("""
    ### How it works

    This system uses a multi-agent AI pipeline to produce a 24-hour weather risk brief:

    1. **PlannerAgent** — Designs the data-gathering workflow
    2. **ExecutorAgent** — Fetches weather, Wikipedia context, and news via tools
    3. **VerifierAgent** — Validates consistency, deduplication, and completeness
    4. **SummarizerAgent** — Writes the final brief.md and brief.json

    All agents run on **Google Gemini** via the **agno** framework.
    """)
