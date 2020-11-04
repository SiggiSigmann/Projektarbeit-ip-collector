From mysql/mysql-server:latest

COPY ./sql/init.sql /docker-entrypoint-initdb.d/init.sql

ENV MYSQL_ROOT_PASSWORD=1234567
ENV MYSQL_ROOT_HOST=172.21.0.2