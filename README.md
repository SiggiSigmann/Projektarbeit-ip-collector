# Projektarbeit IP based Login

## start / stop server

cd /home/ubuntu/projektarbeit-iobased-login/server/
docker-compose up -d
docker-compose down

Main Page: 193.196.38.56/7
Get IP: 193.196.38.56/ip
View Data: 193.196.38.56/data
Get Data: 193.196.38.56/data/json

## notes
docker-compose up --force-recreate --build -d
mysql -u test --password="1234567" networkdata
