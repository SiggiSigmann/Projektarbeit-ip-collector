#!/bin/bash

#start backup
#todo: change paths in chron.txt and backup.sh
crontab ./backup/cron.txt

#start server
./start.sh