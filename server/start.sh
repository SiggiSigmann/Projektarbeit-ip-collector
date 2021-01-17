#!/bin/bash
chmod +x flaskServer/execute.sh
chmod +x backup/backup.sh

#start server
docker-compose up --force-recreate --build -d