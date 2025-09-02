from airflow.providers.standard.operators.hitl import ApprovalOperator
from airflow.sdk import dag, task, chain, Param


@dag
def ApprovalOperator_syntax_example():

    @task
    def upstream_task():
        return "Pineapple on pizza?"

    _upstream_task = upstream_task()

    _hitl_task = ApprovalOperator(
        task_id="approval_task",
        subject="Your task:",
        body="{{ ti.xcom_pull(task_ids='upstream_task') }}",
        defaults="Approve", # other option: "Reject"
        params={
            "second_topping": Param(
                "olives",
                type="string",
            )
        },
    )

    @task
    def print_result(hitl_output):
        print(f"Params input: {hitl_output['params_input']}")
        print(f"Chosen options: {hitl_output['chosen_options']}")

    _print_result = print_result(_hitl_task.output)

    chain(_upstream_task, _hitl_task)


ApprovalOperator_syntax_example()
