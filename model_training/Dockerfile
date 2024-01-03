FROM databricksruntime/python:13.3-LTS AS builder

ENV PATH $PATH:/databricks/python3/bin

RUN python -m pip install poetry==1.4.2
RUN poetry config virtualenvs.create false
RUN poetry config cache-dir /tmp/poetry-cache

RUN mkdir -p /app/
WORKDIR /app


COPY pyproject.toml poetry.lock /app/
COPY textclassification /app/textclassification
COPY entrypoint.py /app

RUN poetry install --only main

FROM databricksruntime/python:13.3-LTS AS development

# setup mlflow credentials
ENV MLFLOW_TRACKING_URI=databricks

ARG MLFLOW_DATABRICKS_URL
ARG MLFLOW_DATABRICKS_TOKEN

RUN printf "[DEFAULT]\nhost = %s\ntoken = %s\n" "${MLFLOW_DATABRICKS_URL}" "${MLFLOW_DATABRICKS_TOKEN}" > "/root/.databrickscfg"

ENV PATH $PATH:/databricks/python3/bin

COPY --from=builder /app/ /app/
COPY --from=builder /databricks/python3 /databricks/python3
