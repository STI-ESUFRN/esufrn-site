#!/bin/sh
cd ../nginx
mkdir -p ssl
openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout ./ssl/escoladesaude.ufrn.br.key -out ./ssl/Intermediate_domain_ca.crt -subj "/C=BR/ST=Rio Grande do Norte/L=Natal/O=UNIVERSIDADE FEDERAL DO RIO GRANDE DO NORTE/CN=localhost"
