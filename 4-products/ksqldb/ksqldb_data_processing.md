# Working with Enriched Topics

### verify topics
```sh
# read topics
k exec edh-kafka-0 -c kafka -i -t -- bin/kafka-topics.sh --bootstrap-server localhost:9092 --list

# enriched topics [json]
ksqldb-stream-nfe-avro
```

### working with ksqldb
```sh
# access ksqldb server
k exec ksqldb-server-6664496848-xr8p2 -n processing -i -t -- bash ksql

# set latest offset read
SET 'auto.offset.reset' = 'earliest';

# show info
SHOW TOPICS;
SHOW STREAMS;
SHOW TABLES;
SHOW QUERIES;

# describe ksqldb object
DESCRIBE EXTENDED ksqldb_stream_nfe_avro;
```

### processing flow of topics - raw ~ enrichment
```sh
# read raw messages
RAWTOPIC=

kafka-avro-console-consumer \
--bootstrap-server edh-kafka-bootstrap:9092 \
--property schema.registry.url=http://localhost:8081 \
--property print.key=true \
--topic $RAWTOPIC \
--from-beginning

# get enriched topic
ENRTOPIC=

kafka-avro-console-consumer \
--bootstrap-server edh-kafka-bootstrap:9092 \
--property schema.registry.url=http://localhost:8081 \
--topic $ENRTOPIC \
--from-beginning
```

### remove topics on [kafka broker]
```sh
# delete topics
k exec edh-kafka-0 -c kafka -i -t -- bin/kafka-topics.sh --bootstrap-server localhost:9092 --delete --topic output-ksqldb-stream-nfe-json
```
