# KafkaCat

### retrieve cluster info
```sh
# set variables
BROKER=
TOPIC=
SR_IP=http://51.222.45.120:8081

# cluster metadata info
kafkacat -L -b $BROKER

# metadata formatted in json
kafkacat -b $BROKER -L -J | jq .

# list topic info
kafkacat -L -b $BROKER -t $TOPIC
```

### describe and read topics
```sh
# read json topics
kafkacat -C -b $BROKER -t $TOPIC -J -o end

# read avro topics
kafkacat -C -b $BROKER -t $TOPIC -s avro -r $SR_IP -o end -f 'key=%k, event=%s, partition=%p, offset=%o, timestamp=%T, key_length=%K, value_length=%S \n'
```
