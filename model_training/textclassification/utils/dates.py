from datetime import datetime, timedelta


def generate_partition_dates(
    start_partition_date: str, last_partition_date: str
) -> list[str]:
    date_format = "%Y%m%d"
    start_date = datetime.strptime(start_partition_date, date_format)
    end_date = datetime.strptime(last_partition_date, date_format)
    partition_dates = []

    current_date = start_date
    while current_date <= end_date:
        partition_dates.append(int(current_date.strftime(date_format)))
        current_date += timedelta(days=1)

    return partition_dates
