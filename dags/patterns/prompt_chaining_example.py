from typing import Literal
from airflow.sdk import dag, task, Param
import airflow_ai_sdk as ai_sdk


class TicketAnalysis(ai_sdk.BaseModel):
    category: Literal[
        "billing",
        "technical",
        "account",
        "product_feature",
        "bug_report",
        "general_inquiry",
    ]
    urgency: Literal["low", "medium", "high", "critical"]
    sentiment: Literal["frustrated", "neutral", "satisfied", "angry", "confused"]
    key_issues: list[str]
    customer_tier: Literal["free", "basic", "premium", "enterprise"]
    suggested_resolution_time: str
    requires_escalation: bool


class CustomerResponse(ai_sdk.BaseModel):
    response_type: Literal[
        "immediate_resolution", "investigation_needed", "escalation", "educational"
    ]
    personalized_message: str
    next_steps: list[str]
    estimated_resolution_time: str
    follow_up_required: bool


class EscalationNotes(ai_sdk.BaseModel):
    escalation_reason: str
    technical_details: str
    recommended_team: Literal[
        "engineering", "billing", "product", "security", "data_team"
    ]
    priority_level: Literal["p1", "p2", "p3", "p4"]
    business_impact: str


@dag(
    params={
        "support_tickets": Param(
            type="array",
            default=[
                {
                    "ticket_id": "TICK-2025-001",
                    "customer_name": "Captain Jean-Luc Picard",
                    "customer_tier": "enterprise",
                    "subject": "CRITICAL: Main Computer Data Processing Failure - Mission Impact",
                    "message": "Our primary data processing systems have been offline for 6 hours! This is affecting our stellar cartography and navigation algorithms that are essential for our deep space mission. The main computer shows 'operational' but no sensor data is being processed. We have Starfleet Command commitments and this is a Priority One situation. Request immediate escalation to Engineering!",
                },
                {
                    "ticket_id": "TICK-2025-002",
                    "customer_name": "Lieutenant Nyota Uhura",
                    "customer_tier": "basic",
                    "subject": "Communications Array Resource Allocation Inquiry",
                    "message": "Greetings! I'm currently operating with basic communications protocols, but our diplomatic missions are expanding. Could you help me understand the resource requirements for premium subspace relay access? Also, when I upgrade, do I keep my existing frequency configurations and encryption keys? Thanks!",
                },
                {
                    "ticket_id": "TICK-2025-003",
                    "customer_name": "Dr. Leonard McCoy",
                    "customer_tier": "premium",
                    "subject": "Feature Request: Enhanced Bioneural Processing for Medical Analysis",
                    "message": "I'm loving the current medical database system for our sickbay! We're analyzing complex xenobiology data and would really benefit from enhanced bioneural gel pack processing capabilities. Is this on Starfleet's technical roadmap? I'd be happy to beta test if needed - our current medical tricorder workarounds are getting clunky.",
                },
                {
                    "ticket_id": "TICK-2025-004",
                    "customer_name": "Commander William Riker",
                    "customer_tier": "free",
                    "subject": "HELP! Cannot Access Ship's Database from Bridge Station",
                    "message": "I'm new to this starship and completely overwhelmed 😭 Following the Academy protocols but my bridge workstation keeps rejecting connections to the main database. Error says 'access denied' but I can connect fine using the Captain's terminal. What am I doing wrong?? This is for a critical diplomatic mission briefing tomorrow!",
                },
                {
                    "ticket_id": "TICK-2025-005",
                    "customer_name": "Commander Spock",
                    "customer_tier": "enterprise",
                    "subject": "SECURITY ALERT: Unauthorized Access to Classified Federation Data",
                    "message": "URGENT: Logic dictates immediate investigation. I have detected anomalous access patterns in our security logs. An unknown entity has accessed classified Federation tactical data through our main computer systems. The access should have been restricted by security protocols. Starfleet Intelligence must be notified. Our security department requires immediate assistance.",
                },
                {
                    "ticket_id": "TICK-2025-006",
                    "customer_name": "Captain Kathryn Janeway",
                    "customer_tier": "premium",
                    "subject": "Ship Systems Performance Degradation After Latest Software Update",
                    "message": "Since updating to the latest Starfleet OS version, our ship's systems are running at 33% efficiency. Warp core monitoring is delayed, replicator queues are backing up, and the holodeck is lagging terribly. We're considering reverting to the previous version if this isn't resolved soon. Very concerning as we were quite satisfied with system performance before this update.",
                },
            ],
        ),
    },
    tags=["Pattern Example"]
)
def prompt_chaining_example():

    @task
    def extract_support_tickets(**context):
        return context["params"]["support_tickets"]

    @task.llm(
        model="gpt-4o-mini",
        system_prompt=(
            "You are an expert customer support analyst. Analyze the support ticket and extract key information. "
            "Consider the customer's tone, urgency indicators, technical complexity, and business impact. "
            "Categorize accurately and determine if escalation is needed based on severity, customer tier, or complexity."
        ),
        output_type=TicketAnalysis,
    )
    def analyze_ticket(ticket: dict) -> str:

        analysis_prompt = f"""
        TICKET DETAILS:
        - Ticket ID: {ticket['ticket_id']}
        - Customer: {ticket['customer_name']} ({ticket['customer_tier']} tier)
        - Subject: {ticket['subject']}
        - Message: {ticket['message']}
        
        Please analyze this support ticket thoroughly.
        """
        return analysis_prompt

    @task.llm(
        model="gpt-4o-mini",
        system_prompt=(
            "You are a skilled customer support representative. Based on the ticket analysis, "
            "craft a personalized, empathetic, and solution-oriented response. "
            "Match the tone to the customer's sentiment and tier. Be specific about next steps and timelines. "
            "For technical issues, provide clear guidance. For billing, be helpful and upselling when appropriate."
        ),
        output_type=CustomerResponse,
    )
    def generate_customer_response(ticket: dict, analysis: TicketAnalysis) -> str:
        response_prompt = f"""
        ORIGINAL TICKET:
        - Customer: {ticket['customer_name']} ({analysis["customer_tier"]} tier customer)
        - Subject: {ticket['subject']}
        - Message: {ticket['message']}

        ANALYSIS RESULTS:
        - Category: {analysis["category"]}
        - Urgency: {analysis["urgency"]}
        - Sentiment: {analysis["sentiment"]}
        - Key Issues: {', '.join(analysis["key_issues"])}
        - Suggested Resolution Time: {analysis["suggested_resolution_time"]}
        - Requires Escalation: {analysis["requires_escalation"]}

        Generate a personalized customer response that addresses their specific concerns and situation.
        """
        return response_prompt

    @task.llm(
        model="gpt-4o-mini",
        system_prompt=(
            "You are a technical escalation specialist. When a ticket requires escalation, "
            "create detailed internal notes for the engineering or specialist teams. "
            "Include technical details, business impact, customer context, and clear action items. "
            "Only activate for tickets that truly need escalation based on the analysis."
        ),
        output_type=EscalationNotes,
    )
    def generate_escalation_notes(
        ticket: dict, analysis: TicketAnalysis, response: CustomerResponse
    ) -> str:
        if analysis["requires_escalation"] == False:
            return "No escalation needed - ticket can be resolved at L1 support level."

        escalation_prompt = f"""
        ESCALATION REQUIRED - TICKET ANALYSIS:
        
        CUSTOMER CONTEXT:
        - Customer: {ticket['customer_name']} ({analysis["customer_tier"]} tier)
        - Ticket ID: {ticket['ticket_id']}
        - Subject: {ticket['subject']}
        
        TECHNICAL DETAILS:
        - Category: {analysis["category"]}
        - Urgency: {analysis["urgency"]}
        - Key Issues: {', '.join(analysis["key_issues"])}
        - Customer Sentiment: {analysis["sentiment"]}
        
        PLANNED RESPONSE:
        - Response Type: {response["response_type"]}
        - Estimated Resolution: {response["estimated_resolution_time"]}
        - Next Steps: {', '.join(response["next_steps"])}
        
        ORIGINAL MESSAGE:
        {ticket['message']}
        
        Create detailed escalation notes for the appropriate team.
        """
        return escalation_prompt

    @task
    def compile_ticket_results(
        ticket: dict,
        analysis: TicketAnalysis,
        response: CustomerResponse,
        escalation: EscalationNotes,
    ):
        print(f"\n🎫 TICKET PROCESSING COMPLETE: {ticket['ticket_id']}")
        print(f"👤 Customer: {ticket['customer_name']} ({analysis['customer_tier']})")
        print(
            f"📊 Analysis: {analysis['category']} | {analysis['urgency']} urgency | {analysis['sentiment']} sentiment"
        )
        print(f"⏰ Est. Resolution: {response['estimated_resolution_time']}")
        print(f"🎯 Response Type: {response['response_type']}")

        if analysis["requires_escalation"] == True:
            print(
                f"🚨 ESCALATED TO: {escalation['recommended_team']} ({escalation['priority_level']})"
            )
            print(f"💼 Business Impact: {escalation['business_impact']}")
        else:
            print("✅ Resolved at L1 support level")

        print(
            f"📝 Customer Message Preview: {response['personalized_message'][:100]}..."
        )
        print("-" * 80)

        return {
            "ticket_id": ticket["ticket_id"],
            "customer": ticket["customer_name"],
            "resolution_type": response["response_type"],
            "escalated": analysis["requires_escalation"],
            "estimated_time": response["estimated_resolution_time"],
        }

    @task
    def zip_ticket_analysis_pairs(tickets: list, analyses: list):
        return [
            {"ticket": ticket, "analysis": analysis}
            for ticket, analysis in zip(tickets, analyses)
        ]

    @task
    def zip_response_generation_data(tickets: list, analyses: list):
        return [
            {"ticket": ticket, "analysis": analysis}
            for ticket, analysis in zip(tickets, analyses)
        ]

    @task
    def zip_escalation_data(tickets: list, analyses: list, responses: list):
        return [
            {"ticket": ticket, "analysis": analysis, "response": response}
            for ticket, analysis, response in zip(tickets, analyses, responses)
        ]

    @task
    def zip_final_results_data(
        tickets: list, analyses: list, responses: list, escalations: list
    ):

        return [
            {
                "ticket": ticket,
                "analysis": analysis,
                "response": response,
                "escalation": escalation,
            }
            for ticket, analysis, response, escalation in zip(
                tickets, analyses, responses, escalations
            )
        ]

    tickets = extract_support_tickets()

    ticket_analyses = analyze_ticket.expand(ticket=tickets)

    response_pairs = zip_response_generation_data(tickets, ticket_analyses)
    customer_responses = generate_customer_response.expand_kwargs(response_pairs)

    escalation_triplets = zip_escalation_data(
        tickets, ticket_analyses, customer_responses
    )
    escalation_notes = generate_escalation_notes.expand_kwargs(escalation_triplets)

    final_data_sets = zip_final_results_data(
        tickets, ticket_analyses, customer_responses, escalation_notes
    )
    final_results = compile_ticket_results.expand_kwargs(final_data_sets)


prompt_chaining_example()
