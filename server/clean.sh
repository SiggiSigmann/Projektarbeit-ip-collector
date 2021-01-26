#!/bin/bash

docker image prune -a -y
docker container prune -y
docker volume prune -y 
docker network prune -y