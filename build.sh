#!/bin/bash

docker build  --tag us.gcr.io/bumblebee-mit/bumblebee:0.0.13 .

gcloud docker -- push us.gcr.io/bumblebee-mit/bumblebee:0.0.13

kubectl apply -f kubernetes.yml
