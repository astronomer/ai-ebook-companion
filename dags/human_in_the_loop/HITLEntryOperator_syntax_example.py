from airflow.providers.standard.operators.hitl import HITLEntryOperator
from airflow.sdk import dag, task, chain, Param


@dag
def HITLEntryOperator_syntax_example():

    @task
    def upstream_task():
        return "How can I auto-pause a dag if it fails?"

    _upstream_task = upstream_task()

    _hitl_task = HITLEntryOperator(
        task_id="hitl_task",
        subject="Please respond to this ticket!",
        body="{{ ti.xcom_pull(task_ids='upstream_task') }}",
        params={
            "response": Param(
                "You can use the max_consecutive_failed_dag_runs parameter! :)",
                type="string",
            ),
            "urgency": Param(
                "p3",
                type="string",
            ),
        },
    )

    @task
    def print_result(hitl_output):
        print(f"Params input: {hitl_output['params_input']}")
        print(f"Chosen options: {hitl_output['chosen_options']}")

    _print_result = print_result(_hitl_task.output)

    chain(_upstream_task, _hitl_task)


HITLEntryOperator_syntax_example()
