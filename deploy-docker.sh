#!/bin/bash

function throw_error_if_need() {
    if [ $? -ne 0 ]; then
        echo "An error ocurred"
        exit 1
    fi
}

echo "Running Docker container..."

container_name=${1:-"micro_tools_container"}
image_name=${2:-"micro_tools_image"}
image_tag=${3:-"v1.0.0"}
port=${4:-"32000"}
env_var_default=${5:-"hml"}

docker container stop $container_name
docker container rm $container_name

docker run -d \
    -e MICRO_TOOLS_SYS_ENV=$env_var_default \
    -p $port:8000 \
    --name $container_name \
    $image_name:$image_tag \
    sh -c "sleep 10; uvicorn main.entrypoint.main:app --host 0.0.0.0 --port 8000"
throw_error_if_need

timeout_sec=15
counter=0
while [ $(docker container inspect -f '{{.State.Running}}' $container_name) != "true" ]; do
    echo "Waiting for container to be ready..."
    sleep 1
    counter=$((counter+1))
    if [ $counter -eq $timeout_sec ]; then
        echo "Timeout reached"
        exit 1
    fi
done
