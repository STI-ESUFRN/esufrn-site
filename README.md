
[//]: # (Use `pandoc README.md | lynx -stdin` para melhor visualização)

<h2>Site da ESUFRN</h2>

<h1>Índice</h1>

- [1. Configuração inicial](#1-configuração-inicial)
  - [1.1. Clonando este repositório](#11-clonando-este-repositório)
  - [1.2. Instalando o Docker](#12-instalando-o-docker)
  - [1.3. Instalando o Poetry](#13-instalando-o-poetry)
  - [1.4. Instale as dependências do projeto](#14-instale-as-dependências-do-projeto)
  - [1.5. Renomeie "sample.env" para ".env"](#15-renomeie-sampleenv-para-env)
- [2. Execução](#2-execução)
  - [2.1. Desenvolvimento](#21-desenvolvimento)
  - [2.2. Produção](#22-produção)
- [Interrupção](#interrupção)
  - [2.1. Desenvolvimento](#21-desenvolvimento-1)

# 1. Configuração inicial

## 1.1. Clonando este repositório

```bash
git clone git@github.com:STI-ESUFRN/esufrn-site.git
```

## 1.2. Instalando o Docker

```bash
$ sudo apt-get update
$ sudo apt-get install ca-certificates curl gnupg lsb-release
$ sudo mkdir -p /etc/apt/keyrings
$ curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
$ echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
  $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
```

Feito isso, o repositório do Docker já está disponível. Basta então instalarmos.

```bash
sudo apt-get update
sudo apt-get install docker-ce docker-ce-cli containerd.io docker-compose-plugin
```

## 1.3. Instalando o Poetry

```bash
curl -sSL https://install.python-poetry.org | python3 -
```

## 1.4. Instale as dependências do projeto

```bash
cd planeja
poetry install
```

## 1.5. Renomeie "sample.env" para ".env"

Este projeto usa a biblioteca Python Dotenv para gerenciar variáveis de ambiente. Este arquivo contém as informações necessárias para que o projeto funcione. Note que algumas configurações não estão preparadas para o ambiente de produção.

```bash
cp sample.env .env
```

# 2. Execução

## 2.1. Desenvolvimento

```bash
docker compose up
```

## 2.2. Produção

```bash
docker compose up -d
```

# Interrupção

## 2.1. Desenvolvimento

```bash
docker compose down
```

Você ainda pode usar a flag `-v` para apagar os volumes criados. Note que essa opção destruirá a permanência dos dados, do MySQL inclusive.

[//]: # (Use `pandoc README.md | lynx -stdin` para melhor visualização)
