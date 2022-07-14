FROM mysql:5.7.38

ENV MYSQL_DATABASE=queue \
    MYSQL_ROOT_PASSWORD=queuerootpassword \
    MYSQL_USER=queue \
    MYSQL_PASSWORD=queue

ADD schema.sql /docker-entrypoint-initdb.d