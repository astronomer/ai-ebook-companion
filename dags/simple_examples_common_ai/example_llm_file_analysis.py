from airflow.sdk import dag, task, Param
from pathlib import Path

REPORT_DIR = Path("/usr/local/airflow/include/ship_reports")
REPORT_FILE = REPORT_DIR / "anomaly_report.log"

SAMPLE_REPORT = """\
Mission log: Stardate 47634.4
- Coolant pressure dropped to 42% at 03:21. Manual reset required.
- Sensor array B reported intermittent ghost contacts near sector 9.
- Galley replicator produced Earl Grey at 31C instead of 80C.
- Warp coil 2 temperature spiked twice during burn; within tolerance.
"""


@dag(
    params={
        "instruction": Param(
            type="string",
            default=(
                "Read the mission log and list every "
                "distinct anomaly with a short note "
                "describing it."
            ),
        ),
    },
    tags=["Common AI Syntax Example"],
)
def example_llm_file_analysis():

    @task
    def upstream_task(**context) -> str:
        REPORT_DIR.mkdir(parents=True, exist_ok=True)
        for stale in REPORT_DIR.iterdir():
            stale.unlink()
        REPORT_FILE.write_text(SAMPLE_REPORT)
        print(f"Staged report at {REPORT_FILE}")
        return context["params"]["instruction"]

    @task.llm_file_analysis(
        llm_conn_id="pydanticai_default",
        file_path=f"file://{REPORT_DIR}/",
        max_files=10,
        max_file_size_bytes=1024 * 1024,
        max_text_chars=50000,
        output_type=str,
    )
    def analyze_file(instruction: str) -> str:
        return instruction

    @task
    def downstream_task(report: str):
        print("Analysis report:")
        print(report)
        return {
            "report": report,
            "character_count": len(report),
        }

    _upstream_task = upstream_task()
    _analysis = analyze_file(_upstream_task)
    downstream_task(_analysis)


example_llm_file_analysis()
