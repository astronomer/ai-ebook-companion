from airflow.sdk import dag, task, Param
import sqlite3
from pathlib import Path

PRIMARY_DB = "/tmp/space_logistics_primary.db"
ALT_DB = "/tmp/space_logistics_alt.db"


def seed_primary():
    Path(PRIMARY_DB).unlink(missing_ok=True)
    with sqlite3.connect(PRIMARY_DB) as conn:
        conn.executescript(
            """
            CREATE TABLE spacecraft (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                capacity_tonnes REAL,
                current_status TEXT
            );
            """
        )


def seed_alt_with_drift():
    Path(ALT_DB).unlink(missing_ok=True)
    with sqlite3.connect(ALT_DB) as conn:
        conn.executescript(
            """
            CREATE TABLE spacecraft (
                id INTEGER PRIMARY KEY,
                ship_name TEXT NOT NULL,
                capacity_kg INTEGER,
                status TEXT
            );
            """
        )


@dag(
    params={
        "focus": Param(
            type="string",
            default=(
                "Flag any mismatch that would break a CDC "
                "pipeline copying rows from the primary "
                "into the alternate warehouse."
            ),
        ),
    },
    tags=["Common AI Syntax Example"],
)
def example_llm_schema_compare():

    @task
    def upstream_task(**context) -> str:
        seed_primary()
        seed_alt_with_drift()
        return context["params"]["focus"]

    @task.llm_schema_compare(
        llm_conn_id="pydanticai_default",
        db_conn_ids=[
            "space_logistics_primary",
            "space_logistics_alt",
        ],
        table_names=["spacecraft"],
    )
    def compare_schemas(focus: str) -> str:
        return f"Compare the given tables. {focus}"

    @task
    def downstream_task(report: dict):
        print(f"Compatible: {report.get('compatible')}")
        for mismatch in report.get("mismatches", []) or []:
            print(f"  mismatch: {mismatch}")
        for action in report.get("suggested_actions", []) or []:
            print(f"  action: {action}")
        return report

    _upstream_task = upstream_task()
    _comparison = compare_schemas(_upstream_task)
    downstream_task(_comparison)


example_llm_schema_compare()
