FROM apache/airflow:2.5.0

ARG AIRFLOW_USER_HOME=/opt/airflow
ENV AIRFLOW_HOME=${AIRFLOW_USER_HOME}

COPY entrypoint.sh /entrypoint.sh
COPY airflow.cfg ${AIRFLOW_USER_HOME}/airflow.cfg

RUN pip install apache-airflow-providers-databricks

USER root

RUN chmod u+x /entrypoint.sh

RUN chown airflow: /entrypoint.sh

USER airflow

ENV PYTHONPATH=/opt/airflow
ENV ENVIRONMENT=''

EXPOSE 8080 5555 8793

USER airflow

WORKDIR ${AIRFLOW_USER_HOME}
ENTRYPOINT ["/entrypoint.sh"]
CMD ["webserver"]
