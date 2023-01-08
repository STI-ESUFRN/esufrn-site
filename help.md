
[//]: # (Use `pandoc help.md | lynx -stdin` para melhor visualização)

# Comandos úteis

## Índice

- [Banco de dados](#banco-de-dados)
- [Apache](#apache)
- [Serviços](#serviços)
- [Permissões de arquivo e pasta](#permissões-de-arquivo-e-pasta)
- [Arquivos comprimidos](#arquivos-comprimidos)
- [Temas (django-admin-interface)](#temas)

## Banco de dados (MySQL)

### Acessando o MySQL por linha de comando

```bash
mysql -u [USER] -p
```

### Fazendo backup do banco de dados completo

```bash
mysqldump -u [USER] -p --all-databases > [CAMINHO_DO_ARQUIVO].sql
```

### Fazendo backup de bancos de dados específicos

```bash
mysqldump -u [USER] -p --databases [DATABASE1 DATABASE2 ...] > [CAMINHO_DO_ARQUIVO].sql
```

### Fazendo backup de uma tabela específica do bancos de dados

```bash
mysqldump -u [USER] -p [DATABASE] [TABLE1 TABLE2 ...] > [CAMINHO_DO_ARQUIVO].sql
```

## Apache

### Ativando domínios virtuais

```bash
a2ensite [NOME_DO_DOMÍNIO]
```

### Desativando domínios virtuais

```bash
a2dissite [NOME_DO_DOMÍNIO]
```

### Verificando sintaxe

```bash
sudo apache2ctl configtest
```

## Serviços

### Gerenciando serviços

```bash
sudo systemctl [AÇÃO] [NOME_DO_SERVIÇO]
```

- Ações:
  - **start** - Inicia o serviço, se não estiver em execução;
  - **stop** - Interrompe o serviço, se não estiver em execução;
  - **restart** - Reinicia o serviço (stop ... start);
  - **reload** - Instrui ao *daemon* do serviço que recarregue suas configurações, sem necessariamente reiniciá-lo;
  - **status** - Mostra o estado atual do serviço e seu log de inicialização.
- Serviços
  - **apache2** - Serviço do servidor de internet Apache
  - **mysql** - Serviço do banco de dados SQL
  - **esufrn_site** - Serviço do site da Escola de Saúde (precisa dos dois serviços acima em execução)

## Permissões de arquivo e pasta

### Alterando proprietário

```bash
sudo chown [OPÇÕES] [USUÁRIO]:[GRUPO] [CAMINHO_DO_ARQUIVO]
```

Caso o arquivo informado seja um diretório, especificando a opção **-R**, o comando passará a afetar também os arquivos e subdiretórios **recursivamente**.

### Alterando permissões

```bash
sudo chmod [OPÇÕES] [PERMISSÃO] [CAMINHO_DO_ARQUIVO]
```

Todo arquivo ou diretório possui 3 tipos de permissões básicas:

- **r** - Permissão para ler;
- **w** - Permissão para gravar;
- **x** - Permissão para executar.

Usando o comando `ls -lah`, podemos conferir as permissões dos arquivos presentes no diretório especificado. Elas são apresentadas sempre na forma `_rwxrwxrwx`, onde o primeiro caractere identifica o tipo do arquivo, e cada conjunto de `rwx` representa, respectivamente, as permissões do proprietário, do grupo e dos demais usuários.
Essas permissões podem ser representadas por 3 dígitos inteiros de 1 a 7 carregando em seu valor binário, a propriedade que está sendo ou não garantida. Ex:

```bash
sudo chmod 756 foo.bar
```

7 em binário é 111, e neste exemplo, ele representa as permissões do proprietário. Logo, o proprietário terá permissão para ler, gravar e executar (rwx). Analogamente: 5 = 101<sub>2</sub> (r-x) e 6 = 110<sub>2</sub> (rw-)

Caso o arquivo informado seja um diretório, especificando a opção **-R**, o comando passará a afetar também os arquivos e subdiretórios **recursivamente**.

## Arquivos comprimidos

### Criando um arquivo comprimido

```bash
tar -czvf [NOME_DO_ARQUIVO].tar.gz [ARQUIVO(S)]
```

### Extraindo um arquivo comprimido

```bash
tar -xzvf [CAMINHO_DO_ARQUIVO].tar.gz
```

### Extraindo um arquivo comprimido no diretório especificado

```bash
tar -xzvf [CAMINHO_DO_ARQUIVO].tar.gz -C [DESTINO]
```

### Listando o conteúdo um arquivo comprimido

```bash
tar -tvf [CAMINHO_DO_ARQUIVO].tar.gz
```

- **-x** - Extrair o conteúdo de um arquivo;
- **-c** - Criar um novo arquivo;
- **-z** - Usar compressão gzip;
- **-v** - Listar os arquivos processados (verbose)
- **-t** - Lista o conteúdo do arquivo

[//]: # (Use `pandoc help.md | lynx -stdin` para melhor visualização)
