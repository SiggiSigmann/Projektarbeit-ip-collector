#!/bin/bash

cp -r ./backup/ /home/ubuntu/

#start backup
#todo: change paths in chron.txt and backup.sh
crontab /home/ubuntu/backup/cron.txt
#remove everything vrom chron ->crontab -r



#start server
chmod +x ./start.sh
./start.sh