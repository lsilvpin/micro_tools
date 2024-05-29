#!/bin/bash

echo "Building Docker image..."

image_name=${1:-"micro_tools_image"}
image_tag=${2:-"v1.0.0"}

docker build \
    -t $image_name:$image_tag \
    -f Base.Dockerfile \
    .    

echo "Docker image built successfully."
