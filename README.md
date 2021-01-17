# Projektarbeit IP based Login

## start / stop server
* cd /home/ubuntu/projektarbeit-iobased-login/server/
* To setup the server (edit links in cron.txt and backup.sh): ./setup.sh

## notes
* docker exec -it server_db_1 bash
* restart: docker-compose up --force-recreate --build -d
* connect to db in container: mysql -u test --password="1234567" networkdata
