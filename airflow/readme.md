# How to run airflow
in windows first make sure the entrypoint.sh end-file format is compatible with unix by using `dos2unix airflow/entrypoint.sh`

1. build image from dockerfile
```
docker build -t airflow_img .
```
2. run services
```
docker-compose up
```
3. access airflow locally (with admin/admin)
```
http://localhost:8081
```
4. create databricks-connection
5. run airflow dag


# Problems

```
docker run airflow_img
/usr/bin/env: ‘bash\r’: Permission denied

fix with -> dos2unix entrypoint.sh
```
