from airflow.sdk import dag, task, Param


def get_current_weather(latitude: float, longitude: float) -> str:
    import requests

    URL = f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&hourly=temperature_2m&current=temperature_2m,precipitation,relative_humidity_2m"
    response = requests.get(URL)
    return response.json()


WEATHER_REPORT_SYSTEM_PROMPT = """
You should create a personalized weather report for a user based on their location.
You can use the get_current_weather tool to get the current weather based on a latitude and longitude.
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
def example_syntax_task_agent():

    @task.agent(
        llm_conn_id="pydanticai_default",
        system_prompt=WEATHER_REPORT_SYSTEM_PROMPT,
        agent_params={"tools": [get_current_weather]},
    )
    def create_weather_report(**context) -> str:
        location = context["params"]["location"]
        return location

    @task
    def process_response(response: str):
        """
        Process the agent's response.
        """
        return {
            "response": response,
            "word_count": len(response.split()),
            "character_count": len(response),
        }

    # Set up task dependencies
    agent_response = create_weather_report()
    process_response(agent_response)


example_syntax_task_agent()
