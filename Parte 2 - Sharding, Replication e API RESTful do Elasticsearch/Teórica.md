# Parte 2: Sharding, Replication e API RESTful do Elasticsearch

## Sharding: A Base da Escalabilidade Horizontal

Para entender essa seção corretamente, é importante lembrar os conceitos de Cluster, Node e Shard.

- **Cluster**: Um conjunto de um ou mais nodes (servidores) que trabalham juntos. Compartilha carga de trabalho e dados entre os nodes e mantém estado global.
- **Node**: Uma instância única do Elasticsearch em execução, basicamente um servidor rodando o mesmo. Cada node tem um nome único no cluster, armazena dados em shards e possui vários shards.
- **Shard**: A unidade fundamental de armazenamento no Elasticsearch, essencialmente uma instância completa e independente do Apache Lucene. Cada shard é capaz de:
  - Armazenar documentos
  - Executar queries
  - Retornar resultados de busca

Sem o shard, caso deseje-se ter um índice com 1TB de dados, você precisaria de uma máquina capaz de armazenar e processar todo esse volume. Com sharding é possível:

- Dividir os dados com 1TB dividido em 5 shards
- Cada shard é um nó diferente, então a carga também é dividida
- Queries podem executar simultaneamente em múltiplos shards

### Tipos de Shards

Os shards são divididos em alguns tipos:

- **Primary Shard**: São os shards originais onde os documentos são indexados primeiro e são responsáveis por operações de escrita.
- **Replica Shards**: Armazenam cópias dos shards primários e servem operações de leitura de backup.

Para promover escalabilidade horizontal, cada documento é roteado para um shard em específico, baseado em seu ID, garantindo distribuição uniforme.

```python
# Algoritmo de roteamento do Elasticsearch
shard_number = hash(document_id) % number_of_primary_shards
```

Quando se executa uma busca, o cliente "bate" no coordinating node e busca nos shards a informação, resultados são agregados e retornados.

Podemos ter dois tipos de crescimento, como sabemos em sistemas distribuídos:

- **Escala Vertical**: Tendo um servidor mais potente
- **Escala Horizontal**: Adicionando mais nós ao cluster

## Replication: Garantindo Alta Disponibilidade

Esse é o processo de manter cópias sincronizadas dos dados em múltiplos locais. No Elasticsearch, cada primary shard pode ter zero ou mais réplicas.

### Benefícios da Replicação

Existem vários benefícios com essa abordagem:

- **Alta disponibilidade**: Se um node com replica e shard primário falhar, o cluster ainda continua operacional.
- **Aumento na vazão de leitura**: Sem réplicas, 1 shard pode ter por exemplo 100 requisições por segundo, enquanto três cópias tem 300 requisições por segundo.
- **Manutenção sem downtime**: É possível fazer manutenção nos nodes de forma individual sem downtime, já que as réplicas assumiriam o tráfego total e após o retorno o nó seria atualizado.

### Processo de Replicação

O processo de replicação é feito da seguinte maneira:

1. Escrita chega ao Primary Shard
2. Primary valida e indexa o documento
3. Primary envia operação para todas as réplicas
4. Réplicas confirmam sucesso
5. Primary confirma sucesso ao cliente

Por fim, Elasticsearch implementa consistência eventual com garantias configuráveis, definindo quantos shards devem estar ativos antes de processar, e a frequência de tornar mudanças visíveis para busca.

## API RESTful do Elasticsearch

A API do Elasticsearch segue os princípios REST:

- Recursos identificados por URLs
- Verbos HTTP
- Stateless (cada request é independente)
- JSON como formato de dados

### Estrutura das Respostas

As respostas ao acessar as rotas são dadas dessa maneira:

```json
{
  "_index": "produtos",
  "_id": "1",
  "_version": 2,
  "result": "updated",
  "_shards": {
    "total": 2,
    "successful": 2,
    "failed": 0
  }
}
```

### Roteamento de Requisições

Quando você faz uma requisição REST, o Elasticsearch:

1. Faz o roteamento, determinando qual shard possui ou vai conter o documento
2. O node que recebe a requisição coordena os shards
3. A operação é então executada nos shards apropriados
4. Após isso é feita agregação dos resultados se necessário
5. A resposta em formato de JSON via HTTP

### Métodos HTTP

Alguns dos possíveis métodos para o Elasticsearch são:

- **GET**: Para buscar documentos
- **POST**: Criar documentos
- **PUT**: Atualizar documento
- **DELETE**: Remover documento
- **HEAD**: Verifica a existência de um documento

### Códigos de Status

Códigos de status comuns (que são retornados para cada uma das operações acima, com base no sucesso ou fracasso das mesmas):

- **200**: Operação bem sucedida
- **201**: Documento criado
- **404**: Não encontrado
- **409**: Conflito de versão
- **503**: Cluster não saudável

### Vantagens da API RESTful

Existem várias vantagens em utilizar uma API RESTful para gerenciar o Elasticsearch, como:

- Qualquer cliente HTTP pode interagir
- Funciona com qualquer linguagem de programação
- As requisições GET podem ser cacheadas

## Conclusão

Graças a tudo isso, o Elasticsearch é:

- **Escalável**: Você pode adicionar nós como necessário
- **Resiliente**: Falhas não causam perda de dados
- **Performático**: Operações acontecem paralelamente entre múltiplos shards
- **Flexível**: Adapta-se a diferentes necessidades
