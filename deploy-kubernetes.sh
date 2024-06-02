#!/bin/bash

function throw_error_if_need() {
    if [ $? -ne 0 ]; then
        echo "An error ocurred"
        exit 1
    fi
}

echo "Applying deployment..."

microk8s kubectl apply -f deployment.yaml
throw_error_if_need

echo "Deployment applied successfully."

echo "Applying service..."

microk8s kubectl apply -f service.yaml
throw_error_if_need

echo "Service applied successfully."
