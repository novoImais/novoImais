# Deployment

### cluster selection
```sh
# kubectx & kubens cli
kubectx aks-martins-poc
```

### set env deployment
```sh
# set variables
ARGOCD_PWD="38430fdb-b637-4b5d-a2f1-868c011dd84a"
ELK_PWD="ada90197-876e-47b3-90a4-4559f50f9973"
ORION_CLUSTER="aks-martins-poc"
REPOSITORY="https://bitbucket.org/owshq/martins.git"
```

### create namespace[s]
```sh
# create namespaces
k create namespace database
k create namespace ingestion
k create namespace processing
k create namespace datastore
k create namespace deepstorage
k create namespace tracing
k create namespace logging
k create namespace monitoring
k create namespace viz
k create namespace cicd
k create namespace app
k create namespace cost
k create namespace misc
```

### add & update repositories
```sh
# add & update helm list repos
helm repo add bitnami https://charts.bitnami.com/bitnami
helm repo add yugabytedb https://charts.yugabyte.com
helm repo add elastic https://helm.elastic.co
helm repo add incubator https://kubernetes-charts-incubator.storage.googleapis.com
helm repo add strimzi https://strimzi.io/charts/
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo add stable https://kubernetes-charts.storage.googleapis.com/
helm repo add infracloudio https://infracloudio.github.io/charts
helm repo update
```

### add operator's crds
```sh
# add prometheus crd's
k apply -f https://raw.githubusercontent.com/prometheus-operator/prometheus-operator/release-0.38/example/prometheus-operator-crd/monitoring.coreos.com_alertmanagers.yaml
k apply -f https://raw.githubusercontent.com/prometheus-operator/prometheus-operator/release-0.38/example/prometheus-operator-crd/monitoring.coreos.com_podmonitors.yaml
k apply -f https://raw.githubusercontent.com/prometheus-operator/prometheus-operator/release-0.38/example/prometheus-operator-crd/monitoring.coreos.com_prometheuses.yaml
k apply -f https://raw.githubusercontent.com/prometheus-operator/prometheus-operator/release-0.38/example/prometheus-operator-crd/monitoring.coreos.com_prometheusrules.yaml
k apply -f https://raw.githubusercontent.com/prometheus-operator/prometheus-operator/release-0.38/example/prometheus-operator-crd/monitoring.coreos.com_servicemonitors.yaml
k apply -f https://raw.githubusercontent.com/prometheus-operator/prometheus-operator/release-0.38/example/prometheus-operator-crd/monitoring.coreos.com_thanosrulers.yaml
```

### install crd's [custom resources]
```sh
# install argo-cd
k apply -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml --namespace cicd

# install strimzi
helm install kafka strimzi/strimzi-kafka-operator --namespace ingestion --version 0.21.0 --wait
```

### install argo-cd [gitops]
```sh
# get password to log into argo cd portal
kubens cicd && k get pods -n cicd -l app.kubernetes.io/name=argocd-server -o name | cut -d'/' -f 2 | xargs -t -I {} argocd login --port-forward --username admin --password {}

# change admin password
k get pods -n cicd -l app.kubernetes.io/name=argocd-server -o name | cut -d'/' -f 2 | xargs -t -I {} argocd account --port-forward update-password --current-password {} --new-password $ARGOCD_PWD --account admin

# create cluster role binding for admin user [sa]
k create clusterrolebinding cluster-admin-binding --clusterrole=cluster-admin --user=system:serviceaccount:cicd:argocd-application-controller -n cicd

# register cluster
argocd cluster add $ORION_CLUSTER --port-forward --in-cluster

# add repo into argo-cd repositories
argocd repo add $REPOSITORY --username gitusers --password gitpassword --port-forward
```

### install apps [orion]
```sh
# get cluster name
https://kubernetes.default.svc

# misc
k apply -f 2-repository/app-manifests/misc/load-balancers-svc.yaml

# database
k apply -f 2-repository/app-manifests/database/postgresql.yaml
k apply -f 2-repository/app-manifests/database/yugabytedb.yaml

# ingestion
k apply -f 2-repository/app-manifests/ingestion/kafka-broker.yaml
k apply -f 2-repository/app-manifests/ingestion/schema-registry.yaml
k apply -f 2-repository/app-manifests/ingestion/kafka-connect.yaml
k apply -f 2-repository/app-manifests/ingestion/cruise-control.yaml
k apply -f 2-repository/app-manifests/ingestion/kafka-bridge.yaml
k apply -f 2-repository/app-manifests/ingestion/kafka-lag-exporter.yaml
k apply -f 2-repository/app-manifests/ingestion/kafka-connectors.yaml

# deep storage
k apply -f 2-repository/app-manifests/deepstorage/minio.yaml

# processing
k apply -f 2-repository/app-manifests/processing/ksqldb.yaml

# logging
k apply -f 2-repository/app-manifests/logging/elasticsearch.yaml
k apply -f 2-repository/app-manifests/logging/filebeat.yaml
k apply -f 2-repository/app-manifests/logging/kibana.yaml

4-products/5-elk/create-index-pattern-filebeat.json
4-products/5-elk/modify-index-lifecycle-policy.json

# monitoring
k apply -f 2-repository/app-manifests/monitoring/prometheus-alertmanager-grafana.yaml
k apply -f 2-repository/app-manifests/monitoring/botkube.yaml

# cost
k apply -f 2-repository/app-manifests/cost/kubecost.yaml

# viz
k apply -f 2-repository/app-manifests/viz/metabase.yaml

# deployed apps
k get applications -n cicd
```
