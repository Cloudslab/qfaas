#!/bin/sh
filename=$1
while read line; do
# reading each line
faas-cli build -f ./functions.yml --filter "$line"

# Push Docker image
echo -n "$CI_DOCKER_PASSWORD" | docker login --username ${CI_DOCKER_USER} --password-stdin
faas-cli push -f ./functions.yml --filter "$line"

#Deploy to OpenFaaS
echo -n "$CI_OPENFAAS_PASSWORD" | faas-cli login --username admin --password-stdin --gateway $CI_OPENFAAS_URL
faas-cli deploy -f ./functions.yml --filter "$line" --namespace openfaas-fn
done < $filename
