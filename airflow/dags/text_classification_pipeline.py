from airflow import DAG
from airflow.models import Variable
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.python_operator import PythonOperator, BranchPythonOperator
from airflow.operators.trigger_dagrun import TriggerDagRunOperator
from airflow.providers.databricks.operators.databricks import DatabricksRunNowOperator
from airflow.models.param import Param
from datetime import datetime
import requests

# DAG Configuration
DAG_ID = "TrainRetrainModel"
DESCRIPTION = "Train or Retrain text classification model and deploy if retrained"
START_DATE = datetime(2023, 1, 1)
SCHEDULE_INTERVAL = "@daily"  # Trigger-based, no schedule

# Define default arguments
default_args = {
    "start_date": START_DATE,
    "schedule_interval": SCHEDULE_INTERVAL,
    "catchup": False,
    "email_on_failure": False,
    "depends_on_past": False,
    "email_on_retry": False,
    'is_paused_upon_creation': False,
    'params':{
        "train_model_from_scratch": Param(False, type="boolean"),
    }
}

# Custom Function to Trigger GitHub Actions
def trigger_github_actions():
    url = "https://api.github.com/repos/pbmiguel/mlopstextclassification/actions/workflows/model_serving.yaml/dispatches"
    pat = Variable.get("GITHUB_PAT")
    headers = {
        "Authorization": f"token {pat}",
        "Accept": "application/vnd.github.v3+json"
    }
    payload = {
        "ref": "master",
    }
    
    response = requests.post(url, headers=headers, json=payload)
    return response.raise_for_status()

# Function to choose training or retraining based on the trigger configuration
def choose_training_path(train_model_from_scratch: str):
    print("train_model_from_scratch=", train_model_from_scratch)
    # Convert the string argument to a boolean
    train_model_from_scratch = train_model_from_scratch.lower() == 'true'
    return "train_model" if train_model_from_scratch else "retrain_model"



# DAG definition
with DAG(DAG_ID, default_args=default_args, description=DESCRIPTION, catchup=False) as dag:
    
    start_task = DummyOperator(task_id='start')

    # Decision point
    decision_task = BranchPythonOperator(
        task_id='choose_training_path',
        op_args=[
         "{{ params.train_model_from_scratch }}",
        ],
        python_callable=choose_training_path,
    )

    train_model_task = DatabricksRunNowOperator(
        task_id="train_model",
        databricks_conn_id="databricks",
        job_id=394791233351120,
        notebook_params={"partition_date": "{{ ds_nodash }}"},
    )

    retrain_model_task = DatabricksRunNowOperator(
        task_id="retrain_model",
        databricks_conn_id="databricks",
        job_id=142184915612720,
        notebook_params={"partition_date": "{{ ds_nodash }}"},
    )

    deploy_model_task = PythonOperator(
        task_id='deploy_model',
        python_callable=trigger_github_actions,
    )

    # Defining the DAG structure
    start_task >> decision_task >> [train_model_task, retrain_model_task]
    retrain_model_task >> deploy_model_task
    train_model_task >> deploy_model_task