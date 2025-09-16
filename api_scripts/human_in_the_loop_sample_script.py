import requests
from typing import Any

_USERNAME = "admin"
_PASSWORD = "admin"
_HOST = "http://localhost:8080/"  # To learn how to send API requests to Airflow running on Astro see: https://www.astronomer.io/docs/astro/airflow-api/

_DAG_ID = "HITLOperator_syntax_example"
_TASK_ID = "hitl_task"


def _pick_option(options: list[str]):
    print("Available options: ", options)
    chosen_option = input("Enter the option you want to select: ")
    return chosen_option


def _pick_params(param: dict[str, Any]):
    print("Input for param:", param)
    param_input = input("Enter your value for the param: ")
    return param_input


def _get_jwt_token():
    token_url = f"{_HOST}/auth/token"
    payload = {"username": _USERNAME, "password": _PASSWORD}
    headers = {"Content-Type": "application/json"}
    response = requests.post(token_url, json=payload, headers=headers)

    token = response.json().get("access_token")
    return token


def _get_running_dagruns_for_dag(dag_id: str):
    url = f"{_HOST}/api/v2/dags/{dag_id}/dagRuns?state=running"
    headers = {"Authorization": f"Bearer {_get_jwt_token()}"}
    response = requests.get(url, headers=headers)
    return response.json()


def _get_hitl_details(dag_id: str, dag_run_id: str, task_id: str):
    url = f"{_HOST}/api/v2/hitlDetails/{dag_id}/{dag_run_id}/{task_id}"
    headers = {"Authorization": f"Bearer {_get_jwt_token()}"}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        subject = response.json()["subject"]
        body = response.json()["body"]
        options = response.json()["options"]
        params = response.json()["params"]
        print("--------------------------------")
        print(
            "Required Action found for: ",
            dag_id,
            "DAG Run: ",
            dag_run_id,
            "Task: ",
            task_id,
        )
        print("Subject: ", subject)
        print("Body: ", body)
        print("Options: ", options)
        print("Params: ", params)
        print("--------------------------------")
        return {
            "subject": subject,
            "body": body,
            "options": options,
            "params": params,
        }
    elif response.status_code == 404:
        print("--------------------------------")
        print(
            "404 - No required action found for: ",
            dag_id,
            "DAG Run: ",
            dag_run_id,
            "Task: ",
            task_id,
        )
        print("Response: ", response.json())
        print("--------------------------------")
        return None
    else:
        print("--------------------------------")
        print("Error: ", response.status_code)
        print("Response: ", response.json())
        print("--------------------------------")
        return None


def _add_hitl_response(
    dag_id: str,
    dag_run_id: str,
    task_id: str,
    options: list[str],
    params: dict[str, Any],
):
    url = f"{_HOST}/api/v2/hitlDetails/{dag_id}/{dag_run_id}/{task_id}"
    headers = {"Authorization": f"Bearer {_get_jwt_token()}"}
    chosen_options = [_pick_option(options)]
    if params:
        params_input = {f"{param}": _pick_params(param) for param in params}
    else:
        params_input = {}
    response = requests.patch(
        url,
        headers=headers,
        json={"chosen_options": chosen_options, "params_input": params_input},
    )
    if response.status_code == 200:
        print("--------------------------------")
        print(
            "Hitl response added for DAG: ",
            dag_id,
            "DAG Run: ",
            dag_run_id,
            "Task: ",
            task_id,
        )
        print("Chosen options: ", chosen_options)
        print("Params input: ", params_input)
        print("Response status code: ", response.status_code)
        print("Response: ", response.json())
        print("--------------------------------")
    elif response.status_code == 409:
        print("--------------------------------")
        print(
            "409 - Already updated action for: ",
            dag_id,
            "DAG Run: ",
            dag_run_id,
            "Task: ",
            task_id,
        )
        print("Response: ", response.json())
        print("--------------------------------")
    else:
        print("--------------------------------")
        print("Error: ", response.status_code)
        print("Response: ", response.json())
        print("--------------------------------")


def main():
    dag_runs = _get_running_dagruns_for_dag(_DAG_ID)["dag_runs"]
    if not dag_runs:
        print("No running dag runs found for DAG: ", _DAG_ID)
        print("Please run the dag and wait for it to start running")
    else:
        for dag_run in dag_runs:
            hitl_details = _get_hitl_details(_DAG_ID, dag_run["dag_run_id"], _TASK_ID)
            if hitl_details:
                _add_hitl_response(
                    _DAG_ID,
                    dag_run["dag_run_id"],
                    _TASK_ID,
                    hitl_details["options"],
                    hitl_details["params"],
                )


if __name__ == "__main__":
    main()
