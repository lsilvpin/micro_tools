#!/bin/bash

function throw_error_if_need() {
    if [ $? -ne 0 ]; then
        echo "An error ocurred"
        exit 1
    fi
}

echo "Building Docker image..."

image_name=${1:-"micro_tools_image"}
image_tag=${2:-"v1.0.0"}

docker build \
    -t $image_name:$image_tag \
    -f Base.Dockerfile \
    .    
throw_error_if_need

echo "Docker image built successfully."
