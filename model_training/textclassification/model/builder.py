import tensorflow as tf

from textclassification.utils.configurations import VOCAB_SIZE


def build_model(raw_train_ds):
    binary_vectorize_layer = tf.keras.layers.TextVectorization(
        max_tokens=VOCAB_SIZE, output_mode="binary"
    )

    train_text = raw_train_ds.map(lambda text, labels: text)
    binary_vectorize_layer.adapt(train_text)

    model = tf.keras.Sequential([binary_vectorize_layer, tf.keras.layers.Dense(4)])
    model.compile(
        loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
        optimizer="adam",
        metrics=["accuracy"],
    )

    return model
