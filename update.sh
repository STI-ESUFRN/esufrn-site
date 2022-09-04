#!/bin/bash

# Baixa as alterações do repositório do git
git pull

# Ativa o ambiente virtual
source _env/bin/activate &&
cd esufrn &&
# Verifica alterações nos modelos
python manage.py makemigrations &&
# Aplica as alterações dos modelos
python manage.py migrate &&
# Atualiza os arquivos estáticos
python manage.py collectstatic --noinput &&
# Desativa o ambiente virtual
deactivate

sudo systemctl restart esufrn_site
