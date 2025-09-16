import json
from airflow.providers.common.messaging.triggers.msg_queue import MessageQueueTrigger
from airflow.sdk import dag, task, chain, Asset, AssetWatcher


def apply_incident_function(*args, **kwargs):
    message = args[-1]
    incident_data = json.loads(message.value())
    print(f"Received incident report via subspace: {incident_data}")
    return incident_data


incident_trigger = MessageQueueTrigger(
    queue="kafka://localhost:9092/incident_channel",
    apply_function="dags.patterns.routing_example.apply_incident_function",
)

incident_asset = Asset(
    "incident_channel",
    watchers=[AssetWatcher(name="incident_watcher", trigger=incident_trigger)],
)


@dag(
    schedule=[incident_asset],
    tags=["Pattern Example", "Routing"],
)
def routing_example():

    @task
    def fetch_incident(**context):
        triggering_asset_events = context["triggering_asset_events"]
        for event in triggering_asset_events[incident_asset]:
            incident_data = event.extra["payload"]
            print(
                f"Starfleet Command: Processing incident {incident_data['incident_id']}"
            )
            print(f"Location: {incident_data['location']}")
            print(f"Reported by: {incident_data['reported_by']}")
            return incident_data

    @task.llm_branch(
        model="gpt-4o-mini",
        system_prompt=(
            "You are an advanced incident triage system. Analyze the incident report and route it appropriately:\n"
            "- handle_critical: Life-threatening emergencies, ship-threatening situations, Priority One alerts\n"
            "- handle_standard: Operational issues that need attention but aren't emergencies\n"
            "- handle_low_priority: Minor issues that can wait for regular maintenance\n"
            "Consider severity indicators, location criticality, and impact on ship operations."
        ),
        allow_multiple_branches=False,
    )
    def route_incident(incident: dict) -> str:
        routing_prompt = f"""
        INCIDENT REPORT:
        ID: {incident['incident_id']}
        Reported by: {incident['reported_by']}
        Location: {incident['location']}
        Description: {incident['description']}
        Severity Indicators: {', '.join(incident['severity_indicators'])}
        
        Route this incident to the appropriate response team.
        """
        return routing_prompt

    @task
    def handle_critical(incident: dict):
        print(f"CRITICAL ALERT - INCIDENT {incident['incident_id']}")
        print(f"Location: {incident['location']}")
        print(f"Reported by: {incident['reported_by']}")
        print(f"EMERGENCY RESPONSE ACTIVATED")
        print(f"Actions: Captain and senior staff notified")
        print(f"All hands alert status initiated")
        print(f"Emergency teams dispatched immediately")
        print(f"Description: {incident['description']}")
        print("=" * 60)
        return {"status": "critical_response_activated", "response_time": "immediate"}

    @task
    def handle_standard(incident: dict):
        print(f"STANDARD INCIDENT - {incident['incident_id']}")
        print(f"Location: {incident['location']}")
        print(f"Reported by: {incident['reported_by']}")
        print(f"Standard operational response initiated")
        print(f"Actions: Department head notified")
        print(f"Work order created for next duty shift")
        print(f"Diagnostic team will investigate")
        print(f"Description: {incident['description']}")
        print("-" * 60)
        return {"status": "standard_response_queued", "response_time": "next_shift"}

    @task
    def handle_low_priority(incident: dict):
        print(f"LOW PRIORITY - {incident['incident_id']}")
        print(f"Location: {incident['location']}")
        print(f"Reported by: {incident['reported_by']}")
        print(f"Added to maintenance backlog")
        print(f"Actions: Routine maintenance scheduled")
        print(f"No immediate impact on operations")
        print(f"Will be resolved during regular maintenance")
        print(f"Description: {incident['description']}")
        print("." * 60)
        return {"status": "maintenance_scheduled", "response_time": "routine"}

    _fetch_incident = fetch_incident()

    _routed_incident = route_incident(incident=_fetch_incident)

    chain(
        _routed_incident,
        [
            handle_critical(incident=_fetch_incident),
            handle_standard(incident=_fetch_incident),
            handle_low_priority(incident=_fetch_incident),
        ],
    )


routing_example()
