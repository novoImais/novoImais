# [iMais] - Processing XML Files in Near Real-Time with Apache Kafka
> this application reads data in a schedule basis from blob storage, perform sets of business logics and sends the xml files to apache kafka [kafka producer api] using python

### housekeeping
> * delete files from processed blob storage location
> * verify files inside of base container
> * clean metadata store [postgres]

### flow of process ~ [cfe] model
> * imais_cfe_events.py [objects] = responsible to understand, parse and deal with the xml files   
> * cfe_json_producer.py [kafka] = split the xml elements and sends to different kafka topics  
> * cfe_items_json_producer.py [kafka] = decouple the xml items and uses the cfe number to produce into a kafka topic
> * postgres.py [metadata] = interact with the metadata to store processed files  
> * read_blob_files.py [blob_storage] = class that handles the communication with the blob storage [files]
> * validate_file_type.py [blob_storage] = cleaner logic to not break the processing logic per xml type
> * main.py = invoke the program to process files [imais]

### microsoft azure
```sh
# main directory where application connects to process the files 
https://repositorionotas.blob.core.windows.net/01379480000106

# folder statistics ~ 07/02/2021
16,386 blobs; 173,731,995 bytes
```

### init app 
```sh
# trigger app
python3.8 main.py
```

### dockerize app
```sh
# build app [dockerfile] location
docker build --tag python-events-imais-json .

# open container
docker run -i -t python-events-imais-json /bin/bash

# run app [local postgres] address
docker run python-events-imais-json python3.8 main.py

# tag image
docker tag python-events-imais-json owshq/python-events-imais-json:0.5

# push image to registry
docker push owshq/python-events-imais-json:0.5

# verify image on docker hub [container registry]
https://hub.docker.com/repository/docker/owshq/python-events-imais-json
```

### deploy app on kubernetes [k8s]
```sh
# get cluster context 
kubectx aks-martins-poc

# deploy app ~ cronjob [scheduler]
# folder ~ /xml-reader-producer/deployment
k apply -f cronjob.yaml -n app

# cronjob info
k get cronjob 
k describe cronjob cj-python-events-imais-json

# verify logs
POD=cj-python-events-imais-json-1614379080-9phqn
k logs $POD -f

# remove deployment
k delete cronjob python-events-imais-json
```

### read topics from kafka
```sh
# reading topics
BROKER_IP=52.251.67.205:9094
kafkacat -C -b $BROKER_IP -t src-app-items-json -J -o end
kafkacat -C -b $BROKER_IP -t src-app-det-json -J -o end
```

### delete all topics on kafka 
```sh
# delete topics 
kubectl exec edh-kafka-0 -c kafka -i -t -- bin/kafka-topics.sh --bootstrap-server localhost:9092 --delete --topic src-app-dest-json
kubectl exec edh-kafka-0 -c kafka -i -t -- bin/kafka-topics.sh --bootstrap-server localhost:9092 --delete --topic src-app-det-json
kubectl exec edh-kafka-0 -c kafka -i -t -- bin/kafka-topics.sh --bootstrap-server localhost:9092 --delete --topic src-app-emit-json
kubectl exec edh-kafka-0 -c kafka -i -t -- bin/kafka-topics.sh --bootstrap-server localhost:9092 --delete --topic src-app-ide-json
kubectl exec edh-kafka-0 -c kafka -i -t -- bin/kafka-topics.sh --bootstrap-server localhost:9092 --delete --topic src-app-inf-adic-json
kubectl exec edh-kafka-0 -c kafka -i -t -- bin/kafka-topics.sh --bootstrap-server localhost:9092 --delete --topic src-app-pgto-json
kubectl exec edh-kafka-0 -c kafka -i -t -- bin/kafka-topics.sh --bootstrap-server localhost:9092 --delete --topic src-app-total-json
kubectl exec edh-kafka-0 -c kafka -i -t -- bin/kafka-topics.sh --bootstrap-server localhost:9092 --delete --topic src-app-items-json
```