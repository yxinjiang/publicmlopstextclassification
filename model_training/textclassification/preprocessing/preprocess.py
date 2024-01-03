import tensorflow as tf
from pyspark.sql import DataFrame
from sklearn.model_selection import train_test_split

from textclassification.utils.configurations import BATCH_SIZE, SEED, TEST_SIZE


def prepare_classification_data_split(df: DataFrame):
    df_pandas = df.toPandas()
    features = df_pandas["value"]
    labels = df_pandas["label"].replace(
        {"csharp": 0, "java": 1, "javascript": 2, "python": 3}
    )
    train_features, test_features, train_labels, test_labels = train_test_split(
        features, labels, test_size=TEST_SIZE, random_state=SEED
    )
    train_features, val_features, train_labels, val_labels = train_test_split(
        train_features, train_labels, test_size=0.25, random_state=SEED
    )
    return (
        train_features,
        val_features,
        test_features,
        train_labels,
        val_labels,
        test_labels,
    )


def create_tf_datasets(
    train_features, train_labels, val_features, val_labels, test_features, test_labels
):
    raw_train_ds = tf.data.Dataset.from_tensor_slices(
        (train_features, train_labels)
    ).batch(BATCH_SIZE)
    raw_val_ds = tf.data.Dataset.from_tensor_slices((val_features, val_labels)).batch(
        BATCH_SIZE
    )
    raw_test_ds = tf.data.Dataset.from_tensor_slices(
        (test_features, test_labels)
    ).batch(BATCH_SIZE)

    # Add caching and prefetching
    raw_train_ds = raw_train_ds.cache().prefetch(buffer_size=tf.data.AUTOTUNE)
    raw_val_ds = raw_val_ds.cache().prefetch(buffer_size=tf.data.AUTOTUNE)
    raw_test_ds = raw_test_ds.prefetch(buffer_size=tf.data.AUTOTUNE)

    return raw_train_ds, raw_val_ds, raw_test_ds
