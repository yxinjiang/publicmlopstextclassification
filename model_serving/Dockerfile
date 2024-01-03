# Stage 1: Download and Export the Model
FROM python:3.10-slim as builder

ENV MLFLOW_TRACKING_URI=databricks

ARG MLFLOW_DATABRICKS_URL
ARG MLFLOW_DATABRICKS_TOKEN

# Set working directory
WORKDIR /app

# Install dependencies
RUN pip install mlflow

# setup databricks credentials (requirement for mlflow)
RUN printf "[DEFAULT]\nhost = %s\ntoken = %s\n" "${MLFLOW_DATABRICKS_URL}" "${MLFLOW_DATABRICKS_TOKEN}" > "/root/.databrickscfg"

RUN mlflow artifacts download --artifact-uri models:/TextClassificationModel/Production --dst-path /app/models

# Copy the script to download and export the model
RUN mkdir /app/serving && mkdir /app/serving/1
RUN cp -r /app/models/data/model/* /app/serving/1

# Stage 2: Setup TensorFlow Serving
FROM tensorflow/serving

# Copy the exported model from the builder stage
COPY --from=builder /app/serving/* /models/textclassification/1
COPY monitoring_config.yaml /models/monitoring_config.yaml

# Set environment variable for the model name (adjust as needed)
ENV MODEL_NAME=textclassification

# Expose the TensorFlow Serving port (8501 for REST API)
EXPOSE 8501
CMD ["tensorflow_model_server", "--rest_api_port=8501", "--model_name=textclassification", "--model_base_path=/models/textclassification", "--monitoring_config_file=/models/monitoring_config.yaml"]
