# Projektarbeit IP Collector
![CD Pipeline](https://github.com/SiggiSigmann/projektarbeit-iobased-login/workflows/CD/badge.svg?branch=[pi])

This Repository contains a Project in cooperation with Hochschule Karlsruhe.
The Projects contains a Server which collects IP Adresses and metadata.
This data can be used to train AI Models and detect user when they access other Websites.

The user will need to send informations to the Server regulay. To do so Android users can use
https://llamalab.com/automate/community/flows/38312 and https://llamalab.com/automate/community/flows/38310.


## start / update server
* cd /home/ubuntu/projektarbeit-iobased-login/server/
* To setup the server (edit links in cron.txt and backup.sh): ./setup.sh
* To start the server: ./start.sh
* To clean the server: ./clean.sh

## notes
* restart: docker-compose up --force-recreate --build -d
* connect to db in container: 1: docker exec -it server_db_1 bash 2: mysql -u test --password="1234567" networkdata
