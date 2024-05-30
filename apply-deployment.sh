#!/bin/bash

echo "Applying deployment..."

microk8s kubectl apply -f deployment.yaml

echo "Deployment applied successfully."
