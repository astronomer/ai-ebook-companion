from airflow.sdk import dag, task, chain
from airflow.providers.apache.kafka.operators.produce import ProduceToTopicOperator
from pendulum import datetime
import json
import random

KAFKA_TOPIC = "incident_channel"


def incident_producer_function():
    incident_reports = [
        {
            "incident_id": "INC-2025-007",
            "reported_by": "Captain Jean-Luc Picard",
            "location": "Bridge - Main Command",
            "description": "PRIORITY ALPHA: Unknown alien vessel has locked onto our ship with a tractor beam! We are being pulled toward an uncharted nebula. All attempts to break free have failed. Requesting immediate assistance from nearest Starfleet vessels!",
            "severity_indicators": ["priority alpha", "tractor beam", "uncharted", "immediate assistance"],
        },
        {
            "incident_id": "INC-2025-008", 
            "reported_by": "Commander Spock",
            "location": "Science Lab Alpha",
            "description": "Fascinating discovery requires immediate analysis. We have detected temporal anomalies in this sector that appear to be artificial in origin. Logic suggests we may have encountered evidence of time travel technology.",
            "severity_indicators": ["temporal anomalies", "artificial origin", "time travel"],
        },
        {
            "incident_id": "INC-2025-009",
            "reported_by": "Chief Engineer Montgomery Scott",
            "location": "Engineering - Main",  
            "description": "Captain! The dilithium crystals are showing signs of quantum decay! At this rate, we'll lose warp capability in 2 hours. I need to reroute power through the auxiliary systems, but it's risky business!",
            "severity_indicators": ["quantum decay", "lose warp capability", "risky"],
        },
        {
            "incident_id": "INC-2025-010",
            "reported_by": "Lieutenant Commander Data",
            "location": "Computer Core - Deck 16",
            "description": "I am detecting anomalous patterns in the ship's computer subroutines. Performance degradation is approximately 12.7% below optimal parameters. Recommend diagnostic and maintenance protocols be initiated within the next duty cycle.",
            "severity_indicators": ["performance degradation", "diagnostic required", "maintenance protocols"],
        },
        {
            "incident_id": "INC-2025-011",
            "reported_by": "Dr. Beverly Crusher",
            "location": "Sickbay - Medical Lab",
            "description": "I've discovered an unusual viral strain in the atmospheric recycling system. It appears to be benign to humanoids, but it's affecting some of our botanical specimens in the hydroponics bay. We should investigate before it spreads further.",
            "severity_indicators": ["viral strain", "botanical specimens", "investigate required"],
        },
        {
            "incident_id": "INC-2025-012",
            "reported_by": "Ensign Wesley Crusher",
            "location": "Ten Forward",
            "description": "The replicators in Ten Forward are producing synthehol that tastes slightly off. Guinan mentioned it might be a flavor calibration issue. Not urgent, but the crew is starting to notice. Maybe we could schedule a routine maintenance check when convenient.",
            "severity_indicators": ["flavor calibration", "routine maintenance", "convenience scheduling"],
        },
    ]

    selected_incident = random.choice(incident_reports)

    incident_key = f"incident_{selected_incident['incident_id']}"
    yield (json.dumps(incident_key), json.dumps(selected_incident))


@dag(tags=["Pattern Example", "Routing"])
def helper_routing_producer_dag():

    @task
    def prepare_incident_report():
        print("🚨 Starfleet Command: Preparing to transmit incident report via subspace relay...")
        print("📡 Establishing connection to incident response channel...")
        return "transmission_ready"

    produce_incident = ProduceToTopicOperator(
        task_id="transmit_incident_to_starfleet",
        kafka_config_id="kafka_default",
        topic=KAFKA_TOPIC,
        producer_function=incident_producer_function,
        poll_timeout=10,
    )

    @task
    def confirm_transmission():
        print(f"✅ Incident report successfully transmitted to Starfleet Command via {KAFKA_TOPIC}")
        print("🖖 Message received by incident response system")
        print("⚡ Automated routing and response protocols activated")
        return "transmission_confirmed"

    prepare_task = prepare_incident_report()
    confirm_task = confirm_transmission()

    chain(prepare_task, produce_incident, confirm_task)


helper_routing_producer_dag()
