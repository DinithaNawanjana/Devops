# Solution

```bash
mkdir -p /root/mon
cat > /root/mon/docker-compose.yml <<'YML'
services:
  elasticsearch:
    image: docker.elastic.co/elasticsearch/elasticsearch:8.15.0
    environment:
      - discovery.type=single-node
  logstash:
    image: docker.elastic.co/logstash/logstash:8.15.0
  kibana:
    image: docker.elastic.co/kibana/kibana:8.15.0
    ports: ["5601:5601"]
YML
```
