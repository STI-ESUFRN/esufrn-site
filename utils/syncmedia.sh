#!/bin/sh
mkdir -p ../src/media
rsync -rue 'ssh -p 9922' --progress esparadrapo@escoladesaude.ufrn.br:/home/esparadrapo/esufrn-site/src/media/ ../src/media
