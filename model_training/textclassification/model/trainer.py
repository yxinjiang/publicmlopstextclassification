import mlflow

from textclassification.utils.configurations import (MLFLOW_EXPERIMENT_NAME,
                                                     MLFLOW_RUN_NAME)


def train_and_log_model(model, train_ds, val_ds, test_ds, partition_date):
    mlflow.set_experiment(f"/{MLFLOW_EXPERIMENT_NAME}")
    with mlflow.start_run(run_name=MLFLOW_RUN_NAME) as run:
        model.fit(train_ds, validation_data=val_ds, epochs=10)
        mlflow.tensorflow.log_model(model, artifact_path="model")

        loss, accuracy = model.evaluate(test_ds)
        mlflow.log_params(
            {
                "loss": loss,
                "accuracy": accuracy,
                "latest_partition_date": partition_date,
            }
        )

    return run


def retrain_and_evaluate_model(model, train_ds, val_ds, test_ds):
    mlflow.set_experiment(f"/{MLFLOW_EXPERIMENT_NAME}")
    with mlflow.start_run(run_name=MLFLOW_RUN_NAME) as run:
        model.fit(train_ds, validation_data=val_ds, epochs=10)
        mlflow.tensorflow.log_model(model, artifact_path="model")
        loss, accuracy = model.evaluate(test_ds)
        mlflow.log_params({"loss": loss, "accuracy": accuracy})
        return accuracy, run.info.run_id
