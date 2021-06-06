#!/bin/bash
docker stop certificates-mysql
docker rm certificates-mysql
docker-compose   build  --no-cache  mysqldb
docker-compose up -d mysqldb
docker-compose up -d dcob-backend

