# Guia de Comandos: Preparando o Ambiente Elasticsearch

Este guia descreve os comandos necessários para iniciar um cluster local do Elasticsearch via Docker com a segurança básica habilitada. Este é o pré-requisito para executar o script Python de automação.

## Pré-requisitos

-   Docker instalado e em execução na sua máquina.

## Passo 1: Iniciar o Cluster Elasticsearch Seguro


Com o arquivo docker-compose.yml salvo, abra um terminal no mesmo diretório e execute os seguintes comandos.

## Subindo o Ambiente

Para iniciar o contêiner do Elasticsearch em segundo plano (-d), execute:
Bash

```bash
docker-compose up -d
```

**⚠️ IMPORTANTE:** Ao executar este comando pela primeira vez, o Elasticsearch gerará senhas para os usuários padrão (`elastic`, `kibana`, etc.). A senha para o usuário `elastic` será exibida no log do terminal. **Copie e guarde esta senha em um local seguro**, pois ela será necessária para o script Python.

## Passo 2: Verificar a Saúde do Cluster

Após o contêiner iniciar, abra um **novo terminal** e execute o comando `curl` a seguir para confirmar que o cluster está online e protegido por senha.

-   `-u elastic`: Especifica que a autenticação será feita com o usuário `elastic`. Você será solicitado a inserir a senha que guardou.
-   `-k`: Ignora a verificação do certificado TLS autoassinado, comum em ambientes locais.

```bash
curl -u elastic -k "https://localhost:9200/_cluster/health?pretty"
```

Se o comando retornar um JSON com o status `"green"` ou `"yellow"`, seu cluster está pronto para ser usado pelo script Python.