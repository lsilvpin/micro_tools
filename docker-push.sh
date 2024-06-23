#!/bin/bash

function throw_error_if_need() {
    if [ $? -ne 0 ]; then
        echo "An error ocurred"
        exit 1
    fi
}

# Define the GitHub Container Registry (GHCR) and the username
ghcr="ghcr.io"
username="lsilvpin"

# Define the image name and tag
repo="lsilvpin/micro_tools"
image_name="micro_tools_image"
image_tag="v1.0.0"
remote_image="$ghcr/$repo/$image_name:$image_tag"

# Build the image
echo "Pushing image to Docker Hub..."

cat .ghcr_token | docker login $ghcr --username lsilvpin --password-stdin
throw_error_if_need

docker tag $image_name:$image_tag $remote_image
throw_error_if_need

docker push $remote_image
throw_error_if_need

echo "Image pushed successfully."
