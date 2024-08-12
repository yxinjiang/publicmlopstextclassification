# [Public Repo - Text Classification Auto-Trainable Machine Learning Pipeline](https://medium.com/@paulomiguelbarbosa/autonomous-machine-learning-pipeline-project-design-and-execution-f62870c230ef)
This project is a machine learning pipeline designed for classifying Stack Overflow questions into categories based on programming languages such as Python, C#, Java, or JavaScript. The pipeline emphasizes an auto-trainable and auto-deployable architecture, ensuring that models are continuously updated and deployed with minimal manual intervention.

## Key Features:
**Automated Model Retraining and Deployment**: Uses Apache Airflow to retrain models with new data and deploy them via GitHub Actions if improvements are detected.  
**MLFlow Integration**: Leverages Databricks-provided MLFlow for experiment tracking and model registry.  
**Customized Databricks Docker Containers**: Ensures a consistent, isolated environment for each job via Databricks job clusters.  
**Performance Monitoring**: Utilizes Grafana and Prometheus for real-time monitoring, with metrics such as request rate and latency.  

## Limitations
While the pipeline successfully achieves its primary goal of auto-training and auto-deployment, it currently has a few limitations:

- Non-scalable API: Designed initially to validate the auto-trainable model concept; scalability is planned for future updates.
- Limited Testing: Comprehensive testing frameworks are under development, with a focus on extending beyond the current performance tests.
- Proactive Monitoring: The existing monitoring supports the automation process, with more sophisticated tools planned for subsequent phases.

## Ideal For:
This is project is great for **MLOps Engineers** looking to enhance their pipeline.

## Getting Started:
- Model Serving: You can build the docker image and deploy it locally along with all monitoring and perfomance docker images
- Model Training: You'll have to use the Databricks Infrastructure, specifically Databricks Job Cluster with a custom docker image built from this project.

## Requirements:
1. Setup of Github Secrets related to Azure Container Registry and Databricks MLflow
- AZURE_CREDENTIALS: The entire JSON output from the service principal creation step
- REGISTRY_LOGIN_SERVER: The login server name of your registry (all lowercase). Example: myregistry.azurecr.io
- REGISTRY_USERNAME: The clientId from the JSON output from the service principal creation
- REGISTRY_PASSWORD: The clientSecret from the JSON output from the service principal creation
- RESOURCE_GROUP: The name of the resource group you used to scope the service principal
- MLFLOW_DATABRICKS_URL: The url of the databricks workspace
- MLFLOW_DATABRICKS_TOKEN: The token for accessing the model in MLFlow Registry

## License
This project is licensed under the MIT License.
