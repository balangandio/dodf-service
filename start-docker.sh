#!/bin/bash
docker build -t dodf-service .
docker run -p 56733:80 --name=dodf-service dodf-service