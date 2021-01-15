#!/bin/bash
chmod +x flaskserver/execute.sh
chmod +x backup/backup.sh

#start server
docker-compose up --force-recreate --build -d