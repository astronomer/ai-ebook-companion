from airflow.sdk import dag, task, Param


def get_current_weather(
    latitude: float,
    longitude: float,
) -> str:
    import requests

    URL = (
        f"https://api.open-meteo.com/v1/forecast?"
        f"latitude={latitude}&longitude={longitude}&"
        f"hourly=temperature_2m&"
        f"current=temperature_2m,"
        f"precipitation,relative_humidity_2m"
    )
    response = requests.get(URL)
    return response.json()


WEATHER_REPORT_SYSTEM_PROMPT = """
You should create a personalized weather
report for a user based on their location.
You can use the get_current_weather tool
to get the current weather based on a
latitude and longitude.
"""


@dag(
    params={
        "location": Param(
            type="string",
            default="New York",
        ),
    },
    tags=["Common AI Syntax Example"]
)
def example_agent():

    @task
    def upstream_task(**context):
        return context["params"]["location"]

    @task.agent(
        llm_conn_id="pydanticai_default",
        system_prompt=WEATHER_REPORT_SYSTEM_PROMPT,
        agent_params={"tools": [get_current_weather]},
    )
    def create_weather_report(location: str) -> str:
        return location

    @task
    def downstream_task(response: str):
        return {
            "response": response,
            "word_count": len(response.split()),
            "character_count": len(response),
        }

    _upstream_task = upstream_task()
    agent_response = create_weather_report(
        location=_upstream_task
    )
    downstream_task(agent_response)


example_agent()
