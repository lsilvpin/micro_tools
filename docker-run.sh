#!/bin/bash

{
    echo "Running Docker container..."

    container_name=${1:-"micro_tools_container"}
    image_name=${2:-"micro_tools_image"}
    image_tag=${3:-"v1.0.0"}
    port=${4:-"9000"}

    docker container stop $container_name
    docker container rm $container_name

    docker run -d \
        -p $port:8000 \
        --name $container_name \
        $image_name:$image_tag \
        sh -c "sleep 10; uvicorn main.entrypoint.main:app --host 0.0.0.0 --port 8000"

    while [ $(docker container inspect -f '{{.State.Running}}' $container_name) != "true" ]; do
        echo "Waiting for container to be ready..."
        sleep 1
    done

} || {
    error_msg=$?
    echo "An error ocurred"
    echo $error_msg
    exit 1
}