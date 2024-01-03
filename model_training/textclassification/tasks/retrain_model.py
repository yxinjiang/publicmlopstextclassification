from datetime import datetime, timedelta

from textclassification.gateways.mlflow import (get_previous_model_info,
                                                load_model,
                                                promote_model_if_improved)
from textclassification.gateways.stackoverflow import \
    get_stack_overflow_feedback
from textclassification.model.trainer import retrain_and_evaluate_model
from textclassification.preprocessing.preprocess import (
    create_tf_datasets, prepare_classification_data_split)
from textclassification.utils.configurations import (DATE_FORMAT,
                                                     MLFLOW_MODEL_NAME, STAGE)


def retrain_model(latest_partition_date: str):
    prod_model, model_uri = load_model(MLFLOW_MODEL_NAME, STAGE)
    before_partition_date, latest_version_info = get_previous_model_info(
        MLFLOW_MODEL_NAME
    )

    if int(latest_partition_date) <= int(before_partition_date):
        raise ValueError("Invalid partition date for retraining.")

    start_date = (
        datetime.strptime(before_partition_date, DATE_FORMAT) + timedelta(days=1)
    ).strftime(DATE_FORMAT)
    stack_overflow_df = get_stack_overflow_feedback(start_date, latest_partition_date)

    (
        train_features,
        val_features,
        test_features,
        train_labels,
        val_labels,
        test_labels,
    ) = prepare_classification_data_split(stack_overflow_df)
    train_ds, val_ds, test_ds = create_tf_datasets(
        train_features,
        train_labels,
        val_features,
        val_labels,
        test_features,
        test_labels,
    )

    before_loss, before_accuracy = prod_model.evaluate(test_ds)

    accuracy, run_id = retrain_and_evaluate_model(prod_model, train_ds, val_ds, test_ds)

    if not promote_model_if_improved(
        MLFLOW_MODEL_NAME, STAGE, accuracy, before_accuracy, run_id
    ):
        raise ValueError("Model not improved; not promoting to production.")
