#!/bin/bash

docker build  --tag us.gcr.io/bumblebee-mit/bumblebee:0.0.15 .

gcloud docker -- push us.gcr.io/bumblebee-mit/bumblebee:0.0.15

kubectl apply -f kubernetes.yml
