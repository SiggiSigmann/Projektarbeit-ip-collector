#!/bin/bash
chmod +x flaskServer/startFlask.sh
chmod +x backup/backup.sh

#start server
docker-compose up --force-recreate --build -d