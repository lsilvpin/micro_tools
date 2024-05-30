#!/bin/bash

{
    echo "Applying deployment..."

    microk8s kubectl apply -f deployment.yaml

    echo "Deployment applied successfully."

    echo "Applying service..."

    microk8s kubectl apply -f service.yaml

    echo "Service applied successfully."
} || {
    error_msg=$?
    echo "An error ocurred"
    echo $error_msg
    exit 1
}