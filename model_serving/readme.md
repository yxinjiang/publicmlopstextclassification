# Model Serving Application
It serves a text classification model by pulling the latest registered product model from Databricks MLFlow. 

Scripts:
```
# run model serving api locally
docker build -t 

docker run -p 8501:8501 modelserving

# run prometheus scrapper
docker run \
    --name prometheus \
    -v $(pwd)/prometheus.yml:/etc/prometheus/prometheus.yml \
    -p 9090:9090 \
    prom/prometheus:v2.41.0

# run grafana
docker run -d --name=grafana -p 3000:3000 grafana/grafana

# run performance tests
docker run -v $(pwd)/my-config.yml:/bzt-configs/my-config.yml -it blazemeter/taurus my-config.yml

```