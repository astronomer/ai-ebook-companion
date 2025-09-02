from airflow.sdk import BaseNotifier, Context, dag, task, Param
from airflow.providers.standard.operators.hitl import HITLOperator
from datetime import timedelta

_BASE_URL = "http://localhost:28080"

class MyNotifier(BaseNotifier):
    template_fields = ("message",)

    def __init__(self, message: str = "") -> None:
        self.message = message

    def notify(self, context: Context) -> None:

        task_state = context['ti'].state
        if task_state == "running":

            # this method generates a direct link to the UI page where the user can respond
            url = HITLOperator.generate_link_to_ui_from_context(
                context=context,
                base_url=_BASE_URL,
            )

            # placeholder code, you can send the URL to any service you want
            self.log.info(self.message)
            self.log.info("Url to respond %s", url)
        else:
            self.log.info("Task state: %s", task_state)
            self.log.info("No response needed!")


notifier_class = MyNotifier(
    message="""
Subject: {{ task.subject }}
Body: {{ task.body }}
Options: {{ task.options }}
"""
)


@dag
def notifier_example():
    HITLOperator(
        task_id="hitl_task",
        subject="Choose a number: ",
        options=["23", "19", "42"],
        notifiers=[notifier_class],
    )


notifier_example()
