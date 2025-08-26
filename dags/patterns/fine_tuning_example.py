from airflow.sdk import dag, task, chain
import logging

t_log = logging.getLogger("airflow.task")

from include.custom_operators.gpt_fine_tune import OpenAIFineTuneOperator

_EXAMPLES_FILE_PATH = "include/examples/train/starfleet_incident_response.jsonl"
_VALIDATION_EXAMPLES_FILE_PATH = "include/examples/validation/starfleet_incident_validation.jsonl"

@dag(
    render_template_as_native_obj=True,
    tags=["Pattern Example"]
)
def fine_tuning_example():

    @task
    def upload_examples_file_to_openai(examples_file_path: str) -> str:
        """
        Uploads an examples file to OpenAI.
        Args:
            examples_file_path (str): Path to the examples file.
        Returns:
            str: File ID of the uploaded examples file.
        """

        from openai import OpenAI

        client = OpenAI()  # fetches the API key from the environment var OPENAI_API_KEY
        r = client.files.create(
            file=open(examples_file_path, "rb"), purpose="fine-tune"
        )

        t_log.info(f"Uploaded examples file to OpenAI. File ID: {r.id}")
        t_log.info(f"File name: {r.filename}")
        t_log.info(f"File size: {round(r.bytes / 1000, 2)} KB")

        return r.id

    upload_train_examples_file_to_openai_obj = upload_examples_file_to_openai.override(
        task_id="upload_train_examples_file_to_openai"
    )(
        examples_file_path=_EXAMPLES_FILE_PATH
    )

    upload_validation_examples_file_to_openai_obj = (
        upload_examples_file_to_openai.override(
            task_id="upload_validation_examples_file_to_openai"
        )(
            examples_file_path=_VALIDATION_EXAMPLES_FILE_PATH
        )
    )

    fine_tune = OpenAIFineTuneOperator(
        task_id="fine_tune",
        fine_tuning_file_id=upload_train_examples_file_to_openai_obj,
        validation_file_id=upload_validation_examples_file_to_openai_obj,
        model="gpt-4o-mini-2024-07-18",
        suffix="{{ dag_run.run_id }}",
        wait_for_completion=True,
        deferrable=True,
        poke_interval=5,
        retries=0,
    )

    @task
    def get_model_model_results(result_files: list[str], **context) -> list[float]:
        """
        Get the results of the fine-tuning job. Plot them and save them to a file.
        Args:
            result_files (List[str]): List of file IDs containing the fine-tuning results.
        Returns:
            List[float]: List of the last validation mean token accuracy for each result file.
        """
        from openai import OpenAI
        from io import StringIO
        import pandas as pd
        import base64
        import os
        import json

        from include.task_functions.plotting import plot_model_train_val_graph

        client = OpenAI()

        os.makedirs("include/model_results/plots", exist_ok=True)
        ts = context["ts_nodash"]

        validation_mean_token_acc_list = []

        fine_tuned_model = context["ti"].xcom_pull(
            task_ids="fine_tune", key="fine_tune_model"
        )

        for file in result_files:
            result_file_info = client.files.content(file).content
            decoded_bytes = base64.b64decode(result_file_info)
            decoded_string = decoded_bytes.decode('utf-8')

            df = pd.read_csv(StringIO(decoded_string))

            plot_model_train_val_graph(fine_tuned_model, df, ts)

            last_validation_mean_token_acc = df["valid_mean_token_accuracy"].iloc[-1]
            validation_mean_token_acc_list.append(last_validation_mean_token_acc)

            os.makedirs("include/model_results/challenger", exist_ok=True)

            with open(
                "include/model_results/challenger/challenger_accuracy.json", "w"
            ) as f:
                f.write(
                    json.dumps(
                        {
                            "challenger_model_id": fine_tuned_model,
                            "accuracy": last_validation_mean_token_acc,
                        }
                    )
                )
        return validation_mean_token_acc_list

    get_model_results_obj = get_model_model_results(
        result_files=fine_tune.output,
    )
    chain(fine_tune, get_model_results_obj)


fine_tuning_example()