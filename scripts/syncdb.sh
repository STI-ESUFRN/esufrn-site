#!/bin/sh

FILE="esufrn_site-dump[`date +"%Y%m%d%H%M"`].sql"

ssh esparadrapo@escoladesaude.ufrn.br -p 9922 "cd esufrn-site && docker compose run --rm mysql mysqldump -u suporte -p esufrn_site --ignore-table=esurn_site.django_migrations --ignore-table=esurn_site.django_session" > $FILE
cat $FILE | docker compose exec -T mysql /usr/bin/mysql --password='root_database_password' esufrn_site
