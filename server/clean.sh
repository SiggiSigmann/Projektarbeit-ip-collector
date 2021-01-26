#!/bin/bash

docker image prune -a
docker container prune
docker volume prune
docker network prune