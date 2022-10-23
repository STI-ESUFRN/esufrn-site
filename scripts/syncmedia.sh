#!/bin/sh

rsync -rue 'ssh -p 9922' --progress esparadrapo@escoladesaude.ufrn.br:/home/esparadrapo/esufrn-site/src/media/ /usr/local/src/es-site2/src/media
