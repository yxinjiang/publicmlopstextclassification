```
docker run \
    --name prometheus \
    -v $(pwd)/prometheus.yml:/etc/prometheus/prometheus.yml \
    -p 9090:9090 \
    prom/prometheus:v2.41.0

```