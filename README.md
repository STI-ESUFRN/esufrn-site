
[//]: # (Use `pandoc README.md | lynx -stdin` para melhor visualização)

<h2>Site da ESUFRN</h2>

<h1>Índice</h1>

- [1. Instalação](#1-instalação)
  - [1.1. Ambiente virtual](#11-ambiente-virtual)
    - [1.1.1. Instalando o python-virtualenv](#111-instalando-o-python-virtualenv)
    - [1.1.2. Criando o ambiente virtual](#112-criando-o-ambiente-virtual)
    - [1.1.3. Ativando o ambiente virtual](#113-ativando-o-ambiente-virtual)
  - [1.2. Dependências](#12-dependências)
    - [1.2.1. Pip](#121-pip)
    - [1.2.2. MySQL](#122-mysql)
    - [1.2.3. Apache](#123-apache)
    - [1.2.4. Outras dependências](#124-outras-dependências)
- [2. Configuração](#2-configuração)
  - [2.1. Apache](#21-apache)
    - [2.1.1. Arquivos de configuração](#211-arquivos-de-configuração)
    - [2.1.2. Usuário e grupo Apache](#212-usuário-e-grupo-apache)
    - [2.1.3. Firewall](#213-firewall)
    - [2.1.4. Habilitando módulos](#214-habilitando-módulos)
    - [2.1.5. Habilitando/desabilitando sites](#215-habilitandodesabilitando-sites)
    - [2.1.6. Recarregando configurações](#216-recarregando-configurações)
  - [2.2. Banco de dados](#22-banco-de-dados)
    - [2.2.1. Configuração do MySQL](#221-configuração-do-mysql)
    - [2.2.2. Migrações do Django](#222-migrações-do-django)
    - [2.2.3. Migração do banco](#223-migração-do-banco)
  - [2.3. Arquivos estáticos](#23-arquivos-estáticos)
  - [2.4. LSB Init](#24-lsb-init)
- [3. Execução](#3-execução)
  - [3.1. Desenvolvimento](#31-desenvolvimento)
  - [3.2. Produção](#32-produção)
- [4. Modificações](#4-modificações)
  - [4.1. Nos templates](#41-nos-templates)
  - [4.2. Nos arquivos estáticos](#42-nos-arquivos-estáticos)
  - [4.3. No backend do site](#43-no-backend-do-site)
    - [4.3.1. Alteração nos modelos (models)](#431-alteração-nos-modelos-models)
    - [4.3.2. Em desenvolvimento](#432-em-desenvolvimento)
    - [4.3.3. Em produção](#433-em-produção)
- [5. Backup e manutenção](#5-backup-e-manutenção)
  - [5.1. Banco de dados](#51-banco-de-dados)
    - [5.1.1. Migração do banco de dados](#511-migração-do-banco-de-dados)
    - [5.1.2. Backup do banco de dados](#512-backup-do-banco-de-dados)
    - [5.1.3. Restauração do banco de dados](#513-restauração-do-banco-de-dados)
  - [5.2. Arquivos estáticos](#52-arquivos-estáticos)
    - [5.2.1. Coletando arquivos estáticos](#521-coletando-arquivos-estáticos)
  - [5.3. Serviço de inicialização (LSB Init)](#53-serviço-de-inicialização-lsb-init)
    - [5.3.1. Configuração do serviço de inicialização](#531-configuração-do-serviço-de-inicialização)
    - [5.3.2. Gerenciamento do serviço de inicialização](#532-gerenciamento-do-serviço-de-inicialização)
  - [5.4. Temas](#54-temas)
    - [5.4.1. Backup de um tema](#541-backup-de-um-tema)
    - [5.4.2. Restaurando um tema](#542-restaurando-um-tema)
- [6. Considerações](#6-considerações)
  - [6.1. Acerca das modificações](#61-acerca-das-modificações)

[Backup do banco de dados]:#512-backup-do-banco-de-dados
[Arquivos estáticos]:#52-arquivos-estáticos
[LSB Init]:#24-lsb-init
[Gerenciamento do serviço de inicialização]:#532-gerenciamento-do-serviço-de-inicialização
[Migração do banco de dados]:#511-migração-do-banco-de-dados

# 1. Instalação
## 1.1. Ambiente virtual
### 1.1.1. Instalando o python-virtualenv
```bash
$ sudo apt update
$ sudo apt install python-virtualenv
```
### 1.1.2. Criando o ambiente virtual
```bash
$ cd /var/www/html/esufrn/novo-site
$ virtualenv _env
```
> OBS: NÃO executar este passo como `sudo`
### 1.1.3. Ativando o ambiente virtual
```bash
$ cd /var/www/html/esufrn/novo-site
$ source _env/bin/activate
```

## 1.2. Dependências
### 1.2.1. Pip
```bash
$ cd /var/www/html/esufrn/novo-site
$ source _env/bin/activate
(_env) $ pip install -r requirements.txt
```
> OBS: Instalar dependências somente com o ambiente virtual **ativado**
### 1.2.2. MySQL
```bash
$ sudo apt update
$ sudo apt install -y mysql-client mysql-server
```
### 1.2.3. Apache
```bash
$ sudo apt update
$ sudo apt install -y apache2
```
### 1.2.4. Outras dependências
```bash
$ sudo apt update
$ sudo apt install libmysqlclient-dev libjpeg-dev zlib1g-dev
```


# 2. Configuração
## 2.1. Apache
### 2.1.1. Arquivos de configuração
```bash
$ cd /var/www/html/esufrn/novo-site
$ sudo cp -r apache2 /etc
```
### 2.1.2. Usuário e grupo Apache
```bash
$ sudo addgroup --system apache
$ export APACHE_RUN_GROUP=apache
$ sudo adduser --system --no-create-home --ingroup apache apache
$ export APACHE_RUN_USER=apache
```
### 2.1.3. Firewall
```bash
$ sudo ufw allow 'Apache'
```
### 2.1.4. Habilitando módulos
```bash
$ sudo a2enmod rewrite proxy proxy_http proxy_balancer lbmethod_byrequests
```
### 2.1.5. Habilitando/desabilitando sites
```bash
$ sudo a2dissite 000-default
$ sudo a2ensite escoladesaude saeufrn planeja
```
### 2.1.6. Recarregando configurações
```bash
$ sudo systemctl reload apache2
```

## 2.2. Banco de dados

### 2.2.1. Configuração do MySQL

> **`PENDENTE:`**
>  - [ ] Configuração da senha do usuário root

</br>

```bash
$ mysql -u root -p
```
```sql
> CREATE DATABASE esufrn_site;
> exit
```
### 2.2.2. Migrações do Django
Antes de realizar a restauração do conteúdo, o Django precisa realizar as migrações das tabelas para que seja criada a estrutura básica do banco. Consulte [Migração do banco de dados] para entender como realizar o processo.
### 2.2.3. Migração do banco
```bash
$ cd /var/www/html/esufrn/novo-site
$ mysql -u root -p
```
```sql
> use esufrn_site;
> source [NOME_DO_ARQUIVO].sql;
```

> Para migrar o banco de dados, você precisará de um arquivo de dump atualizado. Consulte o tópico [Backup do banco de dados] para entender como funciona o processo.
## 2.3. Arquivos estáticos
> Os arquivos estáticos precisam ser *coletados* para que possam ficar disponíveis durante a fase de produção. Consulte [Arquivos estáticos] para entender o processo.
## 2.4. LSB Init
```bash
$ cd /etc/init.d
$ sudo ln -s /var/www/html/esufrn/novo-site/esufrn_site.sh esufrn_site
$ sudo systemctl daemon-reload
```

# 3. Execução
## 3.1. Desenvolvimento
```bash
$ cd /var/www/html/esufrn/novo-site
$ source _env/bin/activate
(_env) $ cd esufrn
(_env) $ python manage.py runserver 0.0.0.0:8002
```
O servidor ficará disponível em [0.0.0.0:8002](http://0.0.0.0:8002/) e quaisquer alterações no *backend* surtirão efeito imediato na aplicação. Requer que o serviço do MySQL esteja em execução.

> OBS: Evitar a execução do servidor de desenvolvimento no ambiente de produção (esparadrapo)

## 3.2. Produção
No ambiente de produção, o serviço do site é gerenciado por um serviço de inicialização. Consulte [Gerenciamento do serviço de inicialização] para saber como gerenciá-lo.

# 4. Modificações
## 4.1. Nos templates
Os templates podem ser alterados livremente, independentemente do estado de execução do servidor.

Todos os templates estão disponíveis em `esufrn/templates`

O Django renderiza os templates usando uma sintaxe específica da linguagem. Consulte a [documentação do Django](https://docs.djangoproject.com/pt-br/4.0/) para mais detalhes.
## 4.2. Nos arquivos estáticos
Os arquivos estáticos tais como scripts e folhas de estilo em cascasa (CSS) também podem ser alterados livremente, independentemente do estado de execução do servidor.

Os arquivos estáticos estão disponíveis em `esufrn/public/static`, porém, eles só devem ser modificados na raíz de seus respectivos aplicativos. Atualmente, podem ser localizados em: `esufrn/dashboard/static` e `esufrn/principal/static`

Após modificados, os arquivos devem ser coletados pelo Django. Consulte [Arquivos estáticos] para entender o processo.
## 4.3. No backend do site
### 4.3.1. Alteração nos modelos (models)
Alterações desse tipo modificam a estrutua da abstração do objeto, e consequentemente, a forma como são salvas no banco de daods. Portanto, é necessário que seja feita uma **migração**. Consulte [] para entender o processo.
### 4.3.2. Em desenvolvimento
Com o servidor de desenvolvimento executando, as alterações no backend do site provocarão o recarregamento imediato do serviço.
### 4.3.3. Em produção
As alterações no backend do site, sejam elas feitas manualmente ou por meio de um `git pull` não surtem efeito imediato no ambiente de produção. Para isto, o serviço do site precisa ser reiniciado.

Importante ressaltar que tanto os serviços do **Apache** quanto o serviço do **MySQL** são **independentes** de tal operação, não havendo necessidade de intervenção na execução.
# 5. Backup e manutenção
## 5.1. Banco de dados
### 5.1.1. Migração do banco de dados
```bash
$ cd /var/www/html/esufrn/novo-site
$ source _env/bin/activate
(_env) $ cd esufrn
(_env) $ python manage.py makemigrations
(_env) $ python manage.py migrate
```
A migração consiste no processo de espelhar e mapear as características ou alterações nos modelos do *backend* para as tabelas no banco de dados.
### 5.1.2. Backup do banco de dados
```bash
$ mysqldump -u root -p esufrn_site --ignore-table=esurn_site.django_migrations --ignore-table=esurn_site.django_session > esufrn_site-dump[`date +"%Y%m%d%H%M"`].sql
```
### 5.1.3. Restauração do banco de dados
Antes de realizar a restauração do banco é importante certificar-se de que o Django realizou todas as migrações com sucesso.
```bash
$ cd /var/www/html/esufrn/novo-site
$ mysql -u root -p
```
```sql
> use esufrn_site;
> source [NOME_DO_ARQUIVO].sql;
```
> OBS: É importante que o arquivo *sql* a ser usado como fonte esteja atualizado, isto é, que tenha correspondência entre as tabelas e os modelos implementados, e que não tenha informação de criaçao das tabelas. Dessa forma, podem ser evitados problemas com a migração do Django.

## 5.2. Arquivos estáticos
O ambiente de produção, a princípio, não serve arquivos estáticos. Para que isso aconteça, os arquivos precisam ser coletados de seus respectivos aplicativos e também do próprio ambiente virtual (arquivos estáticos do Django) para então serem acessados de `esufrn/public/static`.
### 5.2.1. Coletando arquivos estáticos
```bash
$ cd /var/www/html/esufrn/novo-site
$ source _env/bin/activate
(_env) $ python manage.py collectstatic --noinput
```
Feito isso, os arquivos estáticos já estarão disponíveis para o ambiente de produção.
## 5.3. Serviço de inicialização (LSB Init)
### 5.3.1. Configuração do serviço de inicialização
Consulte [LSB Init] para saber como configurar o serviço de inicialização
### 5.3.2. Gerenciamento do serviço de inicialização
```bash
$ sudo systemctl [start|stop|restart] esufrn_site
```
- *start* - Inicia o serviço do site
- *stop* - Interrompe o serviço do site
- *restart* - Interrompe, caso esteja executando, e inicia o serviço do site
## 5.4. Temas
### 5.4.1. Backup de um tema

```bash
$ cd /var/www/html/esufrn/novo-site
$ source _env/bin/activate
(_env) $ cd esufrn/
(_env) $ python manage.py dumpdata admin_interface.Theme --indent 4 -o admin_interface_theme_[NOME_DO_TEMA].json
```

### 5.4.2. Restaurando um tema

```bash
$ cd /var/www/html/esufrn/novo-site
$ source _env/bin/activate
(_env) $ cd esufrn/
(_env) $ python manage.py loaddata [CAMINHO_DO_ARQUIVO].json
```

# 6. Considerações
## 6.1. Acerca das modificações
As modificações no backend do sites têm que ser feitas preferencialmente no *servidor de desenvolvimento*, onde podem ser testadas com segurança sem interferir no funcionamento do site.







[//]: # (Use `pandoc README.md | lynx -stdin` para melhor visualização)
