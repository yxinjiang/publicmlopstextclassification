from textclassification.utils.configurations import (ADLS_CONTAINER,
                                                     ADLS_STORAGE_ACCOUNT)
from textclassification.utils.dates import generate_partition_dates
from textclassification.utils.spark import create_spark_session


def _build_base_path() -> str:
    return f"abfss://{ADLS_CONTAINER}@{ADLS_STORAGE_ACCOUNT}.dfs.core.windows.net"


def get_stack_overflow_feedback(start_partition_date: str, last_partition_date: str):
    spark_session = create_spark_session()
    partition_dates = generate_partition_dates(
        start_partition_date, last_partition_date
    )

    return spark_session.read.parquet(
        f"{_build_base_path()}/stack_overflow_perday/partition_date={set(partition_dates)}"
    )
