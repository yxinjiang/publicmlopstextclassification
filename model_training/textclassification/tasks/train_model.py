from textclassification.gateways.mlflow import store_model
from textclassification.gateways.stackoverflow import \
    get_stack_overflow_feedback
from textclassification.model.builder import build_model
from textclassification.model.trainer import train_and_log_model
from textclassification.preprocessing.preprocess import (
    create_tf_datasets, prepare_classification_data_split)
from textclassification.utils.configurations import (MLFLOW_MODEL_NAME,
                                                     START_PARTITION_DATE)


def train_model(partition_date: str):
    stack_overflow_df = get_stack_overflow_feedback(
        START_PARTITION_DATE, partition_date
    )

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

    model = build_model(train_ds)
    run = train_and_log_model(model, train_ds, val_ds, test_ds, partition_date)

    store_model(
        model_uri=f"runs:/{run.info.run_id}/model", model_name=MLFLOW_MODEL_NAME
    )
