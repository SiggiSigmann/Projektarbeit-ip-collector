# Projektarbeit IP based Login

## start / stop server

* cd /home/ubuntu/projektarbeit-iobased-login/server/
* chmod +x flaskServer/execute.sh
* docker-compose up -d
* docker-compose down

* Main Page: 193.196.38.56/7
* Get IP: 193.196.38.56/ip
* View Data: 193.196.38.56/data
* Get Data: 193.196.38.56/data/json

## notes
* docker exec -it server_db_1 bash
* restart: docker-compose up --force-recreate --build -d
* connect to db in container: mysql -u test --password="1234567" networkdata
