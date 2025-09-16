import json

from airflow.providers.common.messaging.triggers.msg_queue import MessageQueueTrigger
from airflow.sdk import dag, Asset, AssetWatcher, task


def apply_function(*args, **kwargs):
    message = args[-1]
    val = json.loads(message.value())
    print(f"Value in message is {val}")
    return val


trigger = MessageQueueTrigger(
    queue="kafka://localhost:9092/my_topic",
    apply_function="dags.patterns.inference_execution_example.apply_function",
)

kafka_topic_asset = Asset(
    "kafka_topic_asset", watchers=[AssetWatcher(name="kafka_watcher", trigger=trigger)]
)


@dag(schedule=[kafka_topic_asset], tags=["Pattern Example", "Inference Execution"])
def inference_execution_example():

    @task
    def fetch_message_from_kafka(**context):
        # Extract the triggering asset events from the context
        triggering_asset_events = context["triggering_asset_events"]
        for event in triggering_asset_events[kafka_topic_asset]:
            # Get the message from the TriggerEvent payload
            print(f"Processing message: {event}")
            return event.extra["payload"]["content"]

    _fetch_message_from_kafka = fetch_message_from_kafka()

    @task.llm(
        model="gpt-4o",
        output_type=str,
        system_prompt="Tell me a fun fact about the topic given.",
    )
    def llm_task(message):
        return message

    _llm_task = llm_task(message=_fetch_message_from_kafka)

    @task
    def post_message_to_endpoint(llm_output):
        print(f"Posting message to endpoint: {llm_output}")

    _post_message_to_endpoint = post_message_to_endpoint(llm_output=_llm_task)


inference_execution_example()
