#!/bin/bash

function throw_error_if_need() {
    if [ $? -ne 0 ]; then
        echo "An error ocurred"
        exit 1
    fi
}

echo "Removing previous deployment..."

microk8s kubectl delete -f deployment.yaml

echo "Previous deployment removed successfully."

echo "Removing previous service..."

microk8s kubectl delete -f service.yaml

echo "Previous service removed successfully."

echo "Applying deployment..."

microk8s kubectl apply -f deployment.yaml
throw_error_if_need

echo "Deployment applied successfully."

echo "Applying service..."

microk8s kubectl apply -f service.yaml
throw_error_if_need

echo "Service applied successfully."
