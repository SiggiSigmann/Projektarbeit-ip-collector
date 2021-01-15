#!/bin/bash
path_to_backup =  "/home/ubuntu/projektarbeit-iobased-login/server/backup"

#create backup
docker exec server_db_1 mysqldump -u root --password="1234567" networkdata > "${path_to_backup}/backup_$(date +"%Y_%m_%d_%I_%M_%p").sql"

#delete older file
find $path_to_backup -name "backup_*.sql" -type f -mtime +20 -depth -print

#load backupscript
#cat backup_date.sql | docker exec -i server_db_1 mysql -u root --password=1234567 networkdata
