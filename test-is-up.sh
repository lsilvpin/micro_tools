#!/bin/bash

host_name=${1:-"platao"}
port=${2:-"32000"}
protocol=${3:-"http"}

echo "Checking if service is up..."
echo "Host: $host_name"
echo "Port: $port"
echo "Protocol: $protocol"

timeout_sec=15
limit_counter=0

while [ $(curl -s -o /dev/null -w "%{http_code}" $protocol://$host_name:$port/info) != "200" ]; do

    echo "Service is not up yet. Waiting for 5 seconds..."
    sleep 5
    limit_counter=$((limit_counter+1))

    if [ $limit_counter -eq $timeout_sec ]; then
        echo "Service is taking too long to start. Exiting..."
        exit 1
    fi
done
