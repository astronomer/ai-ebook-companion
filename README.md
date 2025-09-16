# AI Pattern example repository

This repository contains a collection of AI pattern examples for Apache Airflow® as an extension of the Best Practices for GenAI Pipelines presentation at [Beyond Analytics 2025](https://www.astronomer.io/lp/beyond-analytics-de/). 

> [!TIP]
> This repository is using a pre-released version of Airflow 3.1 in order to be able to show human-in-the-loop functionality and is not meant to be used in production. For more information on human-in-the-loop and other exciting Airflow 3.1 features, sign up for the free [Airflow 3.1 webinar](https://www.astronomer.io/events/webinars/airflow-3-1-release-video/).

## How to run this repository locally

1. Fork this repo and clone it to your local machine.

2. Make sure you have the [Astro CLI](https://www.astronomer.io/docs/astro/cli/install-cli) installed and are at least on version 1.34.0 to run Airflow 3.

3. Copy the `.env_example` file to a new file called `.env` and add your information. The only information you need to provide is your [OpenAI API Key](https://platform.openai.com/api-keys) in order to use the Airflow AI SDK. 

3. Start the Airflow project with the following command:
   ```bash
   astro dev start
   ```

    This command starts 7 containers:
    - Postgres: Airflow's Metadata Database
    - Scheduler: The Airflow component responsible for monitoring and triggering tasks
    - Dag Processor: The Airflow component responsible for parsing dags
    - API Server: The Airflow component responsible for serving the Airflow UI and API
    - Triggerer: The Airflow component responsible for triggering deferred tasks
    - Kafka: A local Kafka server with one topic `my_topic`. The connection `kafka_default` in `.env_example` is configured to use this Kafka server.
    - weaviate: A local Weaviate vector database to interact with from within Airflow tasks. The connection `weaviate_default` in `.env_example` is configured to use this database.

4. Access the Airflow UI at `localhost:8080`. 
5. Run the dags and make changes to experiment with the features. 

Note that two dags (inference_execution_example and routing_example) are using an event-driven schedule.
In order to run them you need to unpause them, then trigger the relevant helper dag (helper_inference_execution_producer_dag or helper_routing_producer_dag).

## Content

Human-in-the-loop example dags:

- [ApprovalOperator_syntax_example](dags/human_in_the_loop/ApprovalOperator_syntax_example.py): This dag shows how to use the ApprovalOperator to make a human-in-the-loop approve or reject information created by the dag, affecting its execution.
- [HITLBranchOperator_syntax_example](dags/human_in_the_loop/HITLBranchOperator_syntax_example.py): Demonstrates multi-select branching for quarterly budget approval workflow where finance managers can select multiple budget categories to approve.
- [HITLEntryOperator_syntax_example](dags/human_in_the_loop/HITLEntryOperator_syntax_example.py): Shows text entry functionality for customer support ticket responses with custom parameters for urgency and response fields.
- [HITLOperator_syntax_example](dags/human_in_the_loop/HITLOperator_syntax_example.py): Basic HITL example for expense approval with dropdown options for payment methods and execution timeout settings.
- [notifier_example](dags/human_in_the_loop/notifier_example.py): Custom notifier implementation that generates direct links to HITL UI pages and sends notifications through external services.

GenAI pattern dags:

- [batch_inference_example](dags/patterns/batch_inference_example.py): Processes batches of customer feedback statements to extract sentiment analysis, summaries, and feature requests using structured AI output models.
- [fine_tuning_example](dags/patterns/fine_tuning_example.py): Dag for fine-tuning OpenAI models using custom training data, including file uploads, fine-tuning jobs, and model deployment for incident response. Fine-tuning is done using a custom deferrable operator located [here](include/custom_operators/gpt_fine_tune.py).
- [inference_execution_example](dags/patterns/inference_execution_example.py): Inference execution pattern for processing individual requests through trained AI models.
- [multi_agent_example](dags/patterns/multi_agent_example.py): Multi-agent system with an orchestrator agent coordinating multiple worker agents.
- [prompt_chaining_example](dags/patterns/prompt_chaining_example.py): Chaining multiple AI prompts together for multi-step reasoning and analysis workflows.
- [rag_example](dags/patterns/rag_example.py): Retrieval Augmented Generation (RAG) implementation using Weaviate vector database for embedding storage and semantic search capabilities.
- [routing_example](dags/patterns/routing_example.py): Incident routing system that uses LLM branching to classify and route incidents based on severity to appropriate response teams.

Helper dags. These dags are used to produce messages to Kafka topics that will start the event-driven patterns inference_execution_example and routing_example.

- [helper_inference_execution_producer_dag](dags/patterns/helper_inference_execution_producer_dag.py): Producer DAG that generates data for the inference execution pattern.
- [helper_routing_producer_dag](dags/patterns/helper_routing_producer_dag.py): Producer DAG that generates incident data for the routing pattern demonstration.

Simple AI SDK example dags:

- [example_agent](dags/simple_examples_ai_sdk/example_agent.py): Weather report agent that uses external API tools to fetch weather data based on coordinates and generate personalized weather reports.
- [example_llm_branch](dags/simple_examples_ai_sdk/example_llm_branch.py): Simple LLM-based branching logic that evaluates statement truthfulness and routes to appropriate downstream tasks.
- [example_syntax_task_agent](dags/simple_examples_ai_sdk/example_syntax_task_agent.py): Basic syntax demonstration for using AI agents within Airflow tasks.
- [example_syntax_task_llm_branch](dags/simple_examples_ai_sdk/example_syntax_task_llm_branch.py): Syntax example showing how to implement LLM branching decorators in task definitions.
- [example_syntax_task_llm](dags/simple_examples_ai_sdk/example_syntax_task_llm.py): Fundamental example of using the @task.llm decorator to generate fun facts about user-specified topics.


## Resources

- [Event-driven scheduling](https://www.astronomer.io/docs/learn/airflow-event-driven-scheduling)
- [Airflow AI SDK - Quick Notes](https://www.astronomer.io/ebooks/quick-notes-airflow-ai-sdk-decorators-code-snippets/)
- [Airflow AI SDK - Repository](https://github.com/astronomer/airflow-ai-sdk)
