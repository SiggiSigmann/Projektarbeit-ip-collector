docker exec server_db_1 mysqldump -u root --password="1234567" networkdata > /home/ubuntu/projektarbeit-iobased-login/server/backup/backup.sql

#load backupscript
#cat backup.sql | docker exec -i server_db_1 mysql -u root --password=1234567 networkdata
