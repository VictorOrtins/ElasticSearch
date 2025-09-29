# Parte 2: Parte Prática

## Pré-requisitos

Como pré-requisito, o Elasticsearch tem que estar rodando como na parte 1. Além disso, é necessário um terminal ou Postman para fazer as requisições.

## Verificando se o Elasticsearch está Rodando

Vamos verificar se o Elasticsearch está rodando:

```bash
# Verificar saúde do cluster
curl -X GET "localhost:9200/_cluster/health?pretty"

# Listar todos os índices (deve estar vazio inicialmente)
curl -X GET "localhost:9200/_cat/indices?v"

# Ver configurações do cluster
curl -X GET "localhost:9200/_cluster/settings?pretty"
```

## Criando um Índice com Shards e Réplicas Customizados

Após isso, vamos criar um índice com Shards e Réplicas customizados. Inicialmente vamos criar um índice de "produtos" com configurações específicas:

```bash
curl -X PUT "localhost:9200/produtos" -H 'Content-Type: application/json' -d'
{
  "settings": {
    "index": {
      "number_of_shards": 3,
      "number_of_replicas": 1
    }
  },
  "mappings": {
    "properties": {
      "nome": {
        "type": "text",
        "fields": {
          "keyword": {
            "type": "keyword"
          }
        }
      },
      "descricao": {
        "type": "text"
      },
      "preco": {
        "type": "float"
      },
      "estoque": {
        "type": "integer"
      },
      "categoria": {
        "type": "keyword"
      },
      "data_cadastro": {
        "type": "date"
      },
      "ativo": {
        "type": "boolean"
      }
    }
  }
}'
```

## Verificando os Índices Criados

Próximo passo é verificar os índices criados, para isso rode os seguintes comandos:

```bash
# Ver detalhes do índice
curl -X GET "localhost:9200/produtos?pretty"

# Ver shards do índice
curl -X GET "localhost:9200/_cat/shards/produtos?v"

# Ver estatísticas do índice
curl -X GET "localhost:9200/produtos/_stats?pretty"
```

Como estamos rodando apenas um node, as réplicas ficarão em estado "unassigned". Isso é normal em desenvolvimento.

## Ajustando o Número de Réplicas para um Ambiente Single-Node

Em seguida precisamos ajustar o número de réplicas para um ambiente single-node:

```bash
curl -X PUT "localhost:9200/produtos/_settings" -H 'Content-Type: application/json' -d'
{
  "index": {
    "number_of_replicas": 0
  }
}'
```

## Operações da API REST

Agora que temos nós para se trabalhar, podemos realizar operações da API REST descritas na parte anterior.

### CREATE - Criando Documentos

Primeiro vamos criar um novo documento com a rota do tipo POST:

```bash
curl -X POST "localhost:9200/produtos/_doc" -H 'Content-Type: application/json' -d'
{
  "nome": "Notebook Dell XPS 15",
  "descricao": "Notebook profissional com tela 4K, processador Intel i7 e 16GB RAM",
  "preco": 8599.90,
  "estoque": 12,
  "categoria": "informatica",
  "data_cadastro": "2024-09-12",
  "ativo": true
}'
```

Se quiser, também é possível criar com ID específico:

```bash
curl -X PUT "localhost:9200/produtos/_doc/1" -H 'Content-Type: application/json' -d'
{
  "nome": "Mouse Logitech MX Master 3",
  "descricao": "Mouse sem fio ergonômico com sensor de alta precisão",
  "preco": 549.00,
  "estoque": 45,
  "categoria": "perifericos",
  "data_cadastro": "2024-09-12",
  "ativo": true
}'
```

Para ser mais eficiente, também é possível adicionar múltiplos documentos de uma vez:

```bash
curl -X POST "localhost:9200/produtos/_bulk" -H 'Content-Type: application/json' -d'
{"index": {"_id": "2"}}
{"nome": "Teclado Mecânico Keychron K2", "descricao": "Teclado mecânico wireless com switches brown", "preco": 799.00, "estoque": 23, "categoria": "perifericos", "data_cadastro": "2024-09-11", "ativo": true}
{"index": {"_id": "3"}}
{"nome": "Monitor LG UltraWide 34", "descricao": "Monitor ultrawide 34 polegadas com resolução QHD", "preco": 2899.00, "estoque": 8, "categoria": "monitores", "data_cadastro": "2024-09-10", "ativo": true}
{"index": {"_id": "4"}}
{"nome": "Webcam Logitech C920", "descricao": "Webcam Full HD 1080p com correção automática de luz", "preco": 399.00, "estoque": 67, "categoria": "perifericos", "data_cadastro": "2024-09-09", "ativo": true}
{"index": {"_id": "5"}}
{"nome": "SSD Samsung 980 Pro 1TB", "descricao": "SSD NVMe M.2 com velocidade de leitura até 7000MB/s", "preco": 899.00, "estoque": 34, "categoria": "armazenamento", "data_cadastro": "2024-09-08", "ativo": true}
{"index": {"_id": "6"}}
{"nome": "Cadeira Gamer ThunderX3", "descricao": "Cadeira gamer ergonômica com apoio lombar", "preco": 1899.00, "estoque": 0, "categoria": "moveis", "data_cadastro": "2024-09-07", "ativo": false}
'
```

### READ - Lendo Documentos

Agora, é possível dar o READ nos documentos já criados, buscando por ID:

```bash
curl -X GET "localhost:9200/produtos/_doc/1?pretty"
```

Ou também é possível buscar por vários IDs:

```bash
curl -X POST "localhost:9200/produtos/_mget" -H 'Content-Type: application/json' -d'
{
  "ids": ["1", "2", "3"]
}'
```

Se for necessário é possível também buscar todos os documentos:

```bash
curl -X GET "localhost:9200/produtos/_search?pretty"
```

#### Buscas com Queries

Você pode pesquisar usando uma query simples:

```bash
# Buscar produtos com "mouse" no nome
curl -X GET "localhost:9200/produtos/_search?pretty" -H 'Content-Type: application/json' -d'
{
  "query": {
    "match": {
      "nome": "mouse"
    }
  }
}'
```

Ou se preferir é possível uma busca com filtros múltiplos:

```bash
# Produtos ativos com preço entre 500 e 1000
curl -X GET "localhost:9200/produtos/_search?pretty" -H 'Content-Type: application/json' -d'
{
  "query": {
    "bool": {
      "must": [
        { "term": { "ativo": true } }
      ],
      "filter": [
        {
          "range": {
            "preco": {
              "gte": 500,
              "lte": 1000
            }
          }
        }
      ]
    }
  }
}'
```

### UPDATE - Atualizando Documentos

Além de poder listar e criar, podemos atualizar documentos. O comando a seguir mostra como atualizar um documento completo:

```bash
curl -X PUT "localhost:9200/produtos/_doc/1" -H 'Content-Type: application/json' -d'
{
  "nome": "Mouse Logitech MX Master 3S",
  "descricao": "Mouse sem fio ergonômico com sensor de alta precisão e cliques silenciosos",
  "preco": 599.00,
  "estoque": 38,
  "categoria": "perifericos",
  "data_cadastro": "2024-09-12",
  "ativo": true
}'
```

Pode-se fazer um update parcial também:

```bash
curl -X POST "localhost:9200/produtos/_update/1" -H 'Content-Type: application/json' -d'
{
  "doc": {
    "preco": 629.90,
    "estoque": 35
  }
}'
```

Update com script também é possível:

```bash
# Decrementar estoque em 1
curl -X POST "localhost:9200/produtos/_update/1" -H 'Content-Type: application/json' -d'
{
  "script": {
    "source": "ctx._source.estoque -= params.quantidade",
    "params": {
      "quantidade": 1
    }
  }
}'
```

Ou por query:

```bash
# Aplicar desconto de 10% em todos produtos da categoria periféricos
curl -X POST "localhost:9200/produtos/_update_by_query" -H 'Content-Type: application/json' -d'
{
  "script": {
    "source": "ctx._source.preco = ctx._source.preco * 0.9"
  },
  "query": {
    "term": {
      "categoria": "perifericos"
    }
  }
}'
```

### DELETE - Deletando Documentos

Além dessas operações, é possível fazer o DELETE de qualquer documento existente:

```bash
curl -X DELETE "localhost:9200/produtos/_doc/6"
```

Deletar por query:

```bash
# Deletar produtos inativos
curl -X POST "localhost:9200/produtos/_delete_by_query" -H 'Content-Type: application/json' -d'
{
  "query": {
    "term": {
      "ativo": false
    }
  }
}'
```

## Exploração de Sharding e Distribuição

Com essas operações sendo explicadas, vamos fazer uma exploração de Sharding e Distribuição, analisando primeiro em qual shard cada documento está:

```bash
curl -X GET "localhost:9200/produtos/_search?pretty" -H 'Content-Type: application/json' -d'
{
  "size": 10,
  "explain": true,
  "_source": ["nome"],
  "query": {
    "match_all": {}
  }
}'
```

Podemos verificar as estatísticas detalhadas por shard:

```bash
curl -X GET "localhost:9200/produtos/_stats?level=shards&pretty"
```

Se necessário podemos forçar refresh para ver mudanças imediatas:

```bash
curl -X POST "localhost:9200/produtos/_refresh"
```

## Testando Alta Disponibilidade

Vamos agora simular uma situação, testando alta disponibilidade. Para isso vamos criar um índice com réplicas para teste:

```bash
curl -X PUT "localhost:9200/teste_ha" -H 'Content-Type: application/json' -d'
{
  "settings": {
    "number_of_shards": 2,
    "number_of_replicas": 1
  }
}'
```

Vamos dividir os dados em 2 pedaços, cria uma cópia em cada pedaço, basicamente uma cópia de backup.

Se você inserir 1000 documentos, 500 vão para o shard 1, os outros vão para o shard 0, cada réplica terá cópia exata do seu primary.

Para verificar a alocação de shards, use esse comando:

```bash
curl -X GET "localhost:9200/_cat/shards/teste_ha?v"
```

## Comandos Úteis para Monitoramento

Agora que o Elasticsearch está populado, podemos fazer uso de vários comandos úteis para monitoramento:

```bash
# Status geral do cluster
curl -X GET "localhost:9200/_cluster/health?pretty"

# Alocação de shards
curl -X GET "localhost:9200/_cat/allocation?v"

# Uso de disco por node
curl -X GET "localhost:9200/_cat/nodes?v&h=name,disk.used,disk.avail,disk.total,disk.used_percent"

# Tasks em execução
curl -X GET "localhost:9200/_tasks?pretty"

# Thread pool stats
curl -X GET "localhost:9200/_nodes/stats/thread_pool?pretty"
```

## Limpeza (Opcional)

Se for necessário, também é possível fazer a limpeza dos índices de teste e produto, mas para fins deste tutorial é completamente opcional:

```bash
# Deletar índice de teste
curl -X DELETE "localhost:9200/teste_ha"

# Deletar índice produtos (se quiser recomeçar)
curl -X DELETE "localhost:9200/produtos"
```

## Troubleshooting

Caso durante o tutorial, alguma coisa der errado, veja essa tabela de troubleshooting:

_(Nota: A tabela de troubleshooting não estava presente no documento original)_

## Próximos Passos

Como próximos passos:

- Implementar segurança com X-pack
- Configurar Kibana para visualização
- Implementar pipeline de ingestão com Logstash
- Criar aplicação cliente em Python/Javascript
