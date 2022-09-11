#!/bin/sh

FILE="esufrn_site-dump[`date +"%Y%m%d%H%M"`].sql"

ssh esparadrapo@escoladesaude.ufrn.br -p 9922 'mysqldump -u root -p esufrn_site --ignore-table=esurn_site.django_migrations --ignore-table=esurn_site.django_session' > $FILE
cat $FILE | docker compose -f ../docker-compose.yml -f ../docker-compose.dev.yml exec -T mysql /usr/bin/mysql --password='dEM7wJm78!D0kJNR' esufrn_site