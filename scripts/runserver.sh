#!/bin/sh

docker compose -f docker-compose.yml -f main.docker-compose.yml up --build -d
