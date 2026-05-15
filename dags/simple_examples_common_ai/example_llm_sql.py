from airflow.sdk import dag, task, Param
import sqlite3
from pathlib import Path

DB_PATH = "/tmp/space_logistics.db"


def seed_db():
    Path(DB_PATH).unlink(missing_ok=True)
    with sqlite3.connect(DB_PATH) as conn:
        conn.executescript(
            """
            CREATE TABLE spacecraft (
                id INTEGER PRIMARY KEY,
                name TEXT,
                capacity_tonnes REAL,
                current_status TEXT
            );
            INSERT INTO spacecraft (name, capacity_tonnes, current_status) VALUES
              ('Voyager', 12.5, 'available'),
              ('Nostromo', 80.0, 'available'),
              ('Serenity', 25.0, 'maintenance'),
              ('Rocinante', 60.0, 'available'),
              ('Heart of Gold', 5.0, 'available'),
              ('Millennium Falcon', 100.0, 'available');
            """
        )


@dag(
    params={
        "question": Param(
            type="string",
            default=(
                "Which spacecraft are currently available "
                "(current_status = 'available'), ordered by "
                "capacity_tonnes descending, limited to 3?"
            ),
        ),
    },
    tags=["Common AI Syntax Example"],
)
def example_llm_sql():

    @task
    def upstream_task(**context) -> str:
        seed_db()
        return context["params"]["question"]

    @task.llm_sql(
        llm_conn_id="pydanticai_default",
        system_prompt=(
            "Generate a syntactically valid SQLite query "
            "to answer the user's question. Avoid SELECT *."
        ),
        validate_sql=True,
        dialect="sqlite",
        db_conn_id="space_logistics_sqlite",
        table_names=["spacecraft"],
    )
    def generate_sql(question: str) -> str:
        return question

    @task
    def downstream_task(sql: str):
        print(f"Generated SQL:\n{sql}")
        with sqlite3.connect(DB_PATH) as conn:
            rows = conn.execute(sql).fetchall()
        for row in rows:
            print(row)
        return rows

    _upstream_task = upstream_task()
    _sql = generate_sql(_upstream_task)
    downstream_task(_sql)


example_llm_sql()
