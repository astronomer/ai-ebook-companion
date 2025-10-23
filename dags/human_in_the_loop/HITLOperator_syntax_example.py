from airflow.providers.standard.operators.hitl import HITLOperator
from airflow.sdk import dag, task, chain, Param
from datetime import timedelta

@dag
def HITLOperator_syntax_example():

    @task
    def upstream_task():
        return "Review expense report and approve vendor payment method."

    _upstream_task = upstream_task()

    _hitl_task = HITLOperator(
        task_id="hitl_task",
        subject="Expense Approval Required", # Required
        body="{{ ti.xcom_pull(task_ids='upstream_task') }}",
        options=["ACH Transfer", "Wire Transfer", "Corporate Check"], # Required
        # defaults=["ACH Transfer"],
        multiple=False, # default: False
        params={
            "expense_amount": Param(
                10000,
                type="number",
            )
        },
        execution_timeout=timedelta(minutes=1), # default: None
        # assigned_users="admin"
    )

    @task
    def print_result(hitl_output):
        print(f"Expense amount: ${hitl_output['params_input']['expense_amount']}")
        print(f"Payment method: {hitl_output['chosen_options'][0]}")

    _print_result = print_result(_hitl_task.output)

    chain(_upstream_task, _hitl_task)


HITLOperator_syntax_example()
