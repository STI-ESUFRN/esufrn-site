#!/bin/sh

rsync -rue 'ssh -p 9922' --progress esparadrapo@escoladesaude.ufrn.br:/var/www/html/esufrn/novo-site/esufrn/public/media/ ../src/media
