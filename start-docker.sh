#!/bin/bash
set -e

image_name='dodf-service'
container_name='dodf-service'

docker stop $container_name || true && docker rm $container_name || true && docker rmi $image_name || true
docker build -t $image_name .
docker run -d -p 4444:80 --name=$container_name $image_name