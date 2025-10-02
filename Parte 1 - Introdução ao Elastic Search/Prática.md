# Guia Prático: Executando o Elasticsearch Localmente com Docker Compose

Este guia mostra como iniciar um ambiente de desenvolvimento local do Elasticsearch de forma rápida e simples usando Docker Compose.

## Pré-requisitos

Antes de começar, garanta que você tenha os seguintes softwares instalados:

[Docker](https://www.docker.com/get-started/)

[Docker Compose](https://docs.docker.com/compose/install/) (geralmente incluído no docker)

# Arquivo de Configuração

Crie um arquivo chamado docker-compose.yml no diretório do seu projeto com o seguinte conteúdo. 

Esta configuração inicia um único nó do Elasticsearch com a camada de segurança desabilitada para facilitar o desenvolvimento.

```YAML
version: '3.8'

services:
  es01:
    image: docker.elastic.co/elasticsearch/elasticsearch:8.10.2
    container_name: es01
    environment:
      - discovery.type=single-node
      - xpack.security.enabled=false
      - ES_JAVA_OPTS=-Xms1g -Xmx1g
    ports:
      - "9200:9200"
      - "9300:9300"
    volumes:
      - esdata01:/usr/share/elasticsearch/data

volumes:
  esdata01:
    driver: local
```

O arquivo está também presente dentro da pasta docker

# Execução do Ambiente

Com o arquivo docker-compose.yml salvo, abra um terminal no mesmo diretório e execute os seguintes comandos.

## Subindo o Ambiente

Para iniciar o contêiner do Elasticsearch em segundo plano (-d), execute:
Bash

```bash
docker-compose up -d
```

O Docker irá baixar a imagem (se for a primeira vez) e iniciar o serviço.

Alternativamente, você também pode baixar a extensão [Docker no VSCode](https://marketplace.visualstudio.com/items?itemName=ms-azuretools.vscode-docker), apertar com o botão direito em cima do yaml e selecionar o comando "Compose Up"

## Parando o Ambiente

Quando terminar de usar, você pode parar e remover o contêiner e o volume de dados com o comando:
Bash

```bash
docker-compose down -v
```

Alternativamente, se tiver a extensão instalada, você pode apertar com o botão direito em cima do yaml e selecionar o comando "Compose Down"

# Verificação do Cluster

Após iniciar o ambiente, você pode verificar se tudo está funcionando corretamente executando os comandos abaixo em seu terminal.

## Teste de Conexão

Este comando verifica se o nó está no ar e respondendo a requisições HTTP.

```bash
curl -X GET "localhost:9200"
```

Você deve receber como resposta algo do tipo:

```json
{
  "name" : "4a949d22bee2",
  "cluster_name" : "docker-cluster",
  "cluster_uuid" : "Hqr_2JjXT2278-oPsO8gyg",
  "version" : {
    "number" : "8.10.2",
    "build_flavor" : "default",
    "build_type" : "docker",
    "build_hash" : "6d20dd8ce62365be9b1aca96427de4622e970e9e",
    "build_date" : "2023-09-19T08:16:24.564900370Z",
    "build_snapshot" : false,
    "lucene_version" : "9.7.0",
    "minimum_wire_compatibility_version" : "7.17.0",
    "minimum_index_compatibility_version" : "7.0.0"
  },
  "tagline" : "You Know, for Search"
}
```

## Saúde do Cluster

Verifica o status geral do cluster.

```Bash
curl -X GET "localhost:9200/_cluster/health?pretty"
```

Você deve receber como resposta algo do tipo:

```json
{
  "cluster_name" : "docker-cluster",
  "status" : "green",
  "timed_out" : false,
  "number_of_nodes" : 1,
  "number_of_data_nodes" : 1,
  "active_primary_shards" : 0,
  "active_shards" : 0,
  "relocating_shards" : 0,
  "initializing_shards" : 0,
  "unassigned_shards" : 0,
  "delayed_unassigned_shards" : 0,
  "number_of_pending_tasks" : 0,
  "number_of_in_flight_fetch" : 0,
  "task_max_waiting_in_queue_millis" : 0,
  "active_shards_percent_as_number" : 100.0
}
```

## Listar Nós

Lista os nós que compõem o cluster.
```Bash
curl -X GET "localhost:9200/_cat/nodes?v"
```

```bash
ip         heap.percent ram.percent cpu load_1m load_5m load_15m node.role   master name
172.18.0.2           24          97   0    0.86    0.84     0.50 cdfhilmrstw *      4a949d22bee2
```