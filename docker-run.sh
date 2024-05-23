#!/bin/bash

echo "Running Docker container..."

container_name=${1:-"python-microservice-container"}
image_name=${2:-"python-microservice-image"}
image_tag=${3:-"v1.0.0"}

docker container stop $container_name
docker container rm $container_name

docker run -d \
    -p 8000:8000 \
    --name $container_name \
    $image_name:$image_tag \
    sh -c "sleep 10; uvicorn main.entrypoint.main:app --host 0.0.0.0 --port 8000"

while [ $(docker container inspect -f '{{.State.Running}}' $container_name) != "true" ]; do
    echo "Waiting for container to be ready..."
    sleep 1
done
