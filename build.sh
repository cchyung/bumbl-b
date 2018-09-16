#!/bin/bash
echo "setting variables"
export PROJECT="bumblebee-mit"
export CLUSTER="bumblebee"
export ZONE="us-central1-a"
export VERSION="0.0.16"

gcloud config set project $PROJECT
gcloud config set compute/zone $ZONE
gcloud config set container/cluster $CLUSTER
gcloud container clusters get-credentials $CLUSTER

echo "building indexer image"
docker build  --tag us.gcr.io/bumblebee-mit/bumblebee-indexer:$VERSION indexer
gcloud docker -- push us.gcr.io/bumblebee-mit/bumblebee-indexer:$VERSION

echo "building app image"
docker build  --tag us.gcr.io/bumblebee-mit/bumblebee-app:$VERSION .
gcloud docker -- push us.gcr.io/bumblebee-mit/bumblebee-app:$VERSION

envsubst < kubernetes.yml | kubectl apply -f -
