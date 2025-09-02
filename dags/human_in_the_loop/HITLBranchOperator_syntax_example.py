from airflow.providers.standard.operators.hitl import HITLBranchOperator
from airflow.sdk import dag, task, chain


_budget_categories = ["marketing", "research_development", "facilities", "training", "technology"]


@dag
def HITLBranchOperator_syntax_example():
    """
    Quarterly budget approval workflow where finance manager selects
    multiple budget categories to approve for funding.
    """

    @task
    def upstream_task():
        return {
            "total_budget": "$4B",
        }

    _upstream_task = upstream_task()

    _hitl_branch_task = HITLBranchOperator(
        task_id="hitl_branch_task",
        subject="Budget Category Approval",
        body="""**Total Budget Available:** {{ ti.xcom_pull(task_ids='upstream_task')['total_budget'] }}

Select the funding proposals to approve for this quarter.""",
        options=[f"Approve {_} budget" for _ in _budget_categories],
        options_mapping={f"Approve {_} budget": _ for _ in _budget_categories},
        multiple=True,
    )

    for _category in _budget_categories:

        @task(
            task_id=f"{_category}",  # needs to match option in HITLBranchOperator
        )
        def category_task():
            print(f"Processing budget approval for {_category}")

        _category_task = category_task()
        chain(_hitl_branch_task, _category_task)

    chain(_upstream_task, _hitl_branch_task)


HITLBranchOperator_syntax_example()
