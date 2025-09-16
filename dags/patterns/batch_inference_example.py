from typing import Literal
from airflow.sdk import dag, task, Param
import airflow_ai_sdk as ai_sdk


class ProductFeedbackSummary(ai_sdk.BaseModel):
    summary: str
    sentiment: Literal["positive", "negative", "neutral"]
    feature_requests: list[str]


@dag(
    params={
        "statements": Param(
            type="array",
            default=[
                "Absolutely game-changing! Airflow has revolutionized our data pipeline workflow. Would love to see native Kubernetes auto-scaling integration! 🚀",
                "The DAG visualization is decent, but honestly the error handling could be way more intuitive. Sometimes I spend hours debugging what should be simple issues 😤",
                "Been using Airflow for 2 years now. It's solid but nothing revolutionary. The scheduling works fine. Maybe add some AI-powered DAG optimization?",
                "OMG this platform is a nightmare! Dependencies break constantly and the documentation is scattered everywhere. Please fix the connection management! 😡",
                "Love the flexibility, but the learning curve is STEEP. Could really use interactive tutorials and better onboarding for new users 📚",
                "Airflow + Kubernetes = pure magic ✨ But the UI feels stuck in 2015. Modern React components would be amazing!",
                "Decent tool overall. Gets the job done. The Python integration is smooth. Not much else to say really 🤷‍♀️",
                "Total disaster trying to set this up with our enterprise security requirements. Need better SSO integration and role-based permissions ASAP!",
                "Mind-blown by the extensibility! Built custom operators in hours. Could you add drag-and-drop DAG builder for less technical users? 🎨",
                "Works great until it doesn't. Random task failures with no clear logs. Please improve observability and add better monitoring dashboards! 📊",
                "Perfect for our ML pipelines! The sensor capabilities are chef's kiss 👌 But please add native MLflow integration!",
                "This software makes me question my career choices. Why is scheduling a simple cron job so complicated?! 😫"
            ],
        ),
    },
    tags=["Pattern Example"]
)
def batch_inference_example():

    @task
    def extract_product_feedback(**context):
        return context["params"]["statements"]

    @task.llm(
        model="gpt-4o-mini",
        system_prompt="Determine the sentiment of the statement given.",
        output_type=ProductFeedbackSummary,
    )
    def sentiment_analysis(statement: str):
        return statement

    @task
    def load_sentiment_to_db(llm_output: ProductFeedbackSummary):
        print(f"Summary: {llm_output['summary']}")
        print(f"Sentiment: {llm_output['sentiment']}")
        print(f"Feature Requests: {llm_output['feature_requests']}")
        return llm_output["feature_requests"]

    _extract_product_feedback = extract_product_feedback()
    _sentiment_analysis = sentiment_analysis.expand(statement=_extract_product_feedback)
    _load_sentiment_to_db = load_sentiment_to_db.expand(llm_output=_sentiment_analysis)


batch_inference_example()
