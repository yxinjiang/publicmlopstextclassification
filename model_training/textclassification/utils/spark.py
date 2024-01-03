from pyspark.sql import SparkSession


def create_spark_session():
    """Create and return a Spark session."""
    return SparkSession.builder.appName("Model Training and Retraining").getOrCreate()
