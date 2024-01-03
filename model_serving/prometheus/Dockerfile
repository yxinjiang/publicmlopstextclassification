FROM prom/prometheus

# Copy the configuration file into the container
COPY prometheus.yml /etc/prometheus/prometheus.yml

# Expose the Prometheus port
EXPOSE 9090

# Start Prometheus with the configuration file
CMD ["--config.file=/etc/prometheus/prometheus.yml"]