#!/bin/bash

docker image prune -a -f
docker container prune -f
docker volume prune -f
docker network prune -f