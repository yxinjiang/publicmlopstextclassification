import mlflow
from mlflow.tracking import MlflowClient


def _setup():
    mlflow.set_tracking_uri("databricks")
    return MlflowClient()


def load_model(model_name: str, stage: str):
    model_uri = f"models:/{model_name}/{stage}"
    return mlflow.tensorflow.load_model(model_uri), model_uri


def store_model(model_uri, model_name):
    client = _setup()

    # register model
    model_details = mlflow.register_model(model_uri=model_uri, name=model_name,)

    # Transition Model to Production
    client.transition_model_version_stage(
        name=model_name, version=model_details.version, stage="Production"
    )


def get_previous_model_info(model_name, stage):
    client = _setup()
    latest_model_index = 0
    latest_version_info = client.get_latest_versions(model_name, stages=[stage])[
        latest_model_index
    ]
    run_id = latest_version_info.run_id
    run_info = mlflow.get_run(run_id)
    before_partition_date = run_info.data.params["latest_partition_date"]
    return before_partition_date, latest_version_info


def promote_model(model_name: str, stage: str, run_id: str):
    client = _setup()
    model_uri = f"runs:/{run_id}/model"
    model_details = mlflow.register_model(model_uri=model_uri, name=model_name)
    client.transition_model_version_stage(
        name=model_name, version=model_details.version, stage=stage
    )


def promote_model_if_improved(
    model_name: str, stage: str, accuracy: float, before_accuracy: float, run_id: str
) -> bool:
    if accuracy <= before_accuracy:
        return False

    promote_model(model_name, stage, run_id)
    return True
