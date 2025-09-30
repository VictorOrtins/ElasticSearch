# Parte 3: Prática - Pipeline de Busca Vetorial com Embeddings

## Pré-requisitos

- Elasticsearch rodando (conforme Parte 1)
- Python 3.8+ instalado
- Bibliotecas Python necessárias

## Instalação das Dependências

Primeiro, vamos instalar as bibliotecas necessárias:

```bash
pip install sentence-transformers elasticsearch numpy requests
```

## Configuração do Ambiente

### 1. Verificando o Elasticsearch

```bash
curl -X GET "localhost:9200/_cluster/health?pretty"
```

### 2. Criando o Índice com Suporte a Vetores

Vamos criar um índice otimizado para busca vetorial.

**Nota**: A partir do Elasticsearch 8.0+, o suporte a vetores densos (`dense_vector`) é nativo e não requer configurações especiais de kNN no nível do índice.

```bash
curl -X PUT "localhost:9200/artigos_vetorial" -H 'Content-Type: application/json' -d'
{
  "settings": {
    "number_of_shards": 1,
    "number_of_replicas": 0
  },
  "mappings": {
    "properties": {
      "titulo": {
        "type": "text",
        "fields": {
          "keyword": {
            "type": "keyword"
          }
        }
      },
      "conteudo": {
        "type": "text"
      },
      "categoria": {
        "type": "keyword"
      },
      "data_publicacao": {
        "type": "date"
      },
      "titulo_embedding": {
        "type": "dense_vector",
        "dims": 384,
        "index": true,
        "similarity": "cosine"
      },
      "conteudo_embedding": {
        "type": "dense_vector",
        "dims": 384,
        "index": true,
        "similarity": "cosine"
      }
    }
  }
}'
```

## Pipeline de Geração de Embeddings

### 1. Script Python para Gerar Embeddings

Crie um arquivo `generate_embeddings.py`:

```python
from sentence_transformers import SentenceTransformer
from elasticsearch import Elasticsearch
import sys
import logging

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

# Inicializar modelo e Elasticsearch
logger.info("Carregando modelo SentenceTransformer")
model = SentenceTransformer('all-MiniLM-L6-v2')

logger.info("Conectando ao Elasticsearch")
es = Elasticsearch(['http://localhost:9200'])

# Verificar conexão
try:
    info = es.info()
    logger.info(f"Conectado ao Elasticsearch {info['version']['number']}")
except Exception as e:
    logger.error(f"Não foi possível conectar ao Elasticsearch: {e}")
    sys.exit(1)

# Dados de exemplo
artigos = [
    {
        "titulo": "Inteligência Artificial e Machine Learning",
        "conteudo": "A inteligência artificial está revolucionando diversos setores da economia. Machine learning permite que computadores aprendam sem programação explícita.",
        "categoria": "tecnologia",
        "data_publicacao": "2024-09-15"
    },
    {
        "titulo": "Redes Neurais e Deep Learning",
        "conteudo": "Deep learning utiliza redes neurais artificiais com múltiplas camadas para resolver problemas complexos de reconhecimento de padrões.",
        "categoria": "tecnologia", 
        "data_publicacao": "2024-09-14"
    },
    {
        "titulo": "Culinária Italiana Tradicional",
        "conteudo": "A culinária italiana é famosa mundialmente por seus sabores autênticos. Massas, pizzas e risotos são pratos tradicionais italianos.",
        "categoria": "gastronomia",
        "data_publicacao": "2024-09-13"
    },
    {
        "titulo": "Exercícios Físicos e Saúde",
        "conteudo": "A prática regular de exercícios físicos é fundamental para manter a saúde. Atividades aeróbicas fortalecem o sistema cardiovascular.",
        "categoria": "saude",
        "data_publicacao": "2024-09-12"
    },
    {
        "titulo": "Algoritmos de Busca e Ordenação",
        "conteudo": "Algoritmos são fundamentais na ciência da computação. Busca binária e ordenação por merge são exemplos de algoritmos eficientes.",
        "categoria": "tecnologia",
        "data_publicacao": "2024-09-11"
    }
]

# Função para gerar embeddings
def gerar_embeddings(texto):
    embedding = model.encode(texto)
    return embedding.tolist()

# Indexar documentos com embeddings
for i, artigo in enumerate(artigos, 1):
    # Gerar embeddings
    titulo_embedding = gerar_embeddings(artigo["titulo"])
    conteudo_embedding = gerar_embeddings(artigo["conteudo"])
    
    # Preparar documento
    doc = {
        **artigo,
        "titulo_embedding": titulo_embedding,
        "conteudo_embedding": conteudo_embedding
    }
    
    try:
        # Indexar no Elasticsearch
        response = es.index(
            index="artigos_vetorial",
            id=i,
            document=doc
        )
        
        logger.info(f"Documento {i} indexado: {response['result']}")
        
    except Exception as e:
        logger.error(f"Erro ao indexar documento {i}: {e}")

# Forçar refresh do índice
es.indices.refresh(index="artigos_vetorial")

logger.info("Pipeline concluído com sucesso")
logger.info("Estatísticas do índice:")

# Mostrar estatísticas
stats = es.count(index="artigos_vetorial")
logger.info(f"Total de documentos: {stats['count']}")

# Verificar saúde do índice
health = es.cluster.health(index="artigos_vetorial")
logger.info(f"Status do índice: {health['status']}")
```

### 2. Executando o Pipeline

```bash
python generate_embeddings.py
```

## Consultas kNN Básicas

**Método 2: Usando o script Python (recomendado para produção)**

Para gerar embeddings dinamicamente, use o script `busca_vetorial.py` que já está configurado:

### 2. Script Python para Consultas Interativas

O arquivo `busca_vetorial.py` já está implementado com as seguintes funcionalidades:

**Características principais:**
- Sistema de logging profissional
- Menu interativo completo
- Múltiplos tipos de busca
- Análise de performance em tempo real

**Funcionalidades disponíveis:**
1. Busca por similaridade
2. Busca híbrida (com filtros)
3. Busca combinada (vetorial + textual)
4. Recomendações baseadas em documento
5. Estatísticas do índice

**Exemplo de uso básico:**

```python
from sentence_transformers import SentenceTransformer
from elasticsearch import Elasticsearch
import logging

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Inicializar
model = SentenceTransformer('all-MiniLM-L6-v2')
es = Elasticsearch([{'host': 'localhost', 'port': 9200, 'scheme': 'http'}])

def buscar_por_similaridade(query, campo="conteudo_embedding", k=5):
    # Gerar embedding da consulta
    query_embedding = model.encode(query).tolist()
    
    # Executar busca kNN
    response = es.search(
        index="artigos_vetorial",
        body={
            "knn": {
                "field": campo,
                "query_vector": query_embedding,
                "k": k,
                "num_candidates": 50
            },
            "_source": ["titulo", "conteudo", "categoria", "data_publicacao"]
        }
    )
    
    return response

# Para executar o sistema interativo completo:
# python busca_vetorial.py

# Exemplo de uso programático:
if __name__ == "__main__":
    busca = BuscaVetorial()
    consulta = "redes neurais artificiais"
    resultados = busca.buscar_por_similaridade(consulta)
    busca.exibir_resultados(resultados)
```

## Consultas Híbridas

### 1. Combinando Busca Vetorial com Filtros

A implementação da busca híbrida no `busca_vetorial.py` funciona da seguinte forma:

```python
def busca_hibrida(self, query, categoria=None, k=5):
    """Busca híbrida combinando vetorial com filtros"""
    query_embedding = self.model.encode(query).tolist()
    
    # Construir consulta híbrida
    body = {
        "knn": {
            "field": "conteudo_embedding", 
            "query_vector": query_embedding,
            "k": k,
            "num_candidates": 100
        },
        "_source": ["titulo", "conteudo", "categoria", "data_publicacao"]
    }
    
    # Adicionar filtro de categoria se especificado
    if categoria:
        body["query"] = {
            "bool": {
                "filter": [
                    {"term": {"categoria": categoria}}
                ]
            }
        }
    
    response = self.es.search(index="artigos_vetorial", body=body)
    return response

# Exemplo de uso através do menu interativo ou:
busca = BuscaVetorial()
resultados = busca.busca_hibrida("inteligência artificial", categoria="tecnologia")
```

### 2. Busca Combinada (Vetorial + Textual)

```python
def busca_combinada(query, boost_vetorial=1.0, boost_textual=1.0, k=10):
    query_embedding = model.encode(query).tolist()
    
    body = {
        "query": {
            "bool": {
                "should": [
                    {
                        "multi_match": {
                            "query": query,
                            "fields": ["titulo^2", "conteudo"],
                            "boost": boost_textual
                        }
                    }
                ]
            }
        },
        "knn": {
            "field": "conteudo_embedding",
            "query_vector": query_embedding, 
            "k": k,
            "num_candidates": 100,
            "boost": boost_vetorial
        }
    }
    
    return es.search(index="artigos_vetorial", body=body)
```

## Análise de Performance

### 1. Medindo Latência de Consultas

```python
import time

def benchmark_busca(query, num_execucoes=10):
    tempos = []
    
    for _ in range(num_execucoes):
        inicio = time.time()
        buscar_por_similaridade(query)
        fim = time.time()
        tempos.append(fim - inicio)
    
    tempo_medio = sum(tempos) / len(tempos)
    print(f"Tempo médio: {tempo_medio:.3f}s")
    print(f"Min: {min(tempos):.3f}s, Max: {max(tempos):.3f}s")

# Teste de performance
benchmark_busca("machine learning algorithms")
```

### 2. Comparando Diferentes Configurações

```bash
# Verificar estatísticas do índice
curl -X GET "localhost:9200/artigos_vetorial/_stats?pretty"

# Verificar uso de memória dos vetores
curl -X GET "localhost:9200/_cat/segments/artigos_vetorial?v&h=segment,size,size.memory"
```

## Casos de Uso Avançados

### 1. Detecção de Duplicatas

```python
def detectar_duplicatas(threshold=0.9):
    # Buscar todos os documentos
    all_docs = es.search(
        index="artigos_vetorial",
        body={"query": {"match_all": {}}, "size": 100}
    )
    
    duplicatas = []
    docs = all_docs['hits']['hits']
    
    for i, doc1 in enumerate(docs):
        embedding1 = doc1['_source']['conteudo_embedding']
        
        # Buscar documentos similares
        similar = es.search(
            index="artigos_vetorial",
            body={
                "knn": {
                    "field": "conteudo_embedding",
                    "query_vector": embedding1,
                    "k": 10,
                    "num_candidates": 50
                }
            }
        )
        
        for hit in similar['hits']['hits']:
            if hit['_id'] != doc1['_id'] and hit['_score'] > threshold:
                duplicatas.append((doc1['_id'], hit['_id'], hit['_score']))
    
    return duplicatas
```

### 2. Recomendação de Conteúdo Similar

```python
def recomendar_similar(doc_id, k=3):
    # Obter documento original
    doc = es.get(index="artigos_vetorial", id=doc_id)
    embedding = doc['_source']['conteudo_embedding']
    
    # Buscar similares (excluindo o próprio documento)
    response = es.search(
        index="artigos_vetorial",
        body={
            "knn": {
                "field": "conteudo_embedding",
                "query_vector": embedding,
                "k": k + 1,
                "num_candidates": 50
            },
            "query": {
                "bool": {
                    "must_not": [
                        {"term": {"_id": doc_id}}
                    ]
                }
            }
        }
    )
    
    return response['hits']['hits'][:k]
```

## Otimizações e Boas Práticas

### 1. Configurações de Performance

```bash
# Otimizar configurações do índice
curl -X PUT "localhost:9200/artigos_vetorial/_settings" -H 'Content-Type: application/json' -d'
{
  "index": {
    "refresh_interval": "30s",
    "number_of_replicas": 0
  }
}'
```

### 2. Monitoramento

```python
def monitorar_performance():
    stats = es.indices.stats(index="artigos_vetorial")
    
    print("Estatísticas do Índice:")
    print(f"Documentos: {stats['indices']['artigos_vetorial']['total']['docs']['count']}")
    print(f"Tamanho: {stats['indices']['artigos_vetorial']['total']['store']['size_in_bytes']} bytes")
    print(f"Consultas: {stats['indices']['artigos_vetorial']['total']['search']['query_total']}")
    print(f"Tempo médio de consulta: {stats['indices']['artigos_vetorial']['total']['search']['query_time_in_millis']}ms")
```

## Limpeza e Troubleshooting

### Comandos Úteis

```bash
# Verificar saúde do cluster
curl -X GET "localhost:9200/_cluster/health?pretty"

# Verificar mapeamentos
curl -X GET "localhost:9200/artigos_vetorial/_mapping?pretty"

# Deletar índice (se necessário)
curl -X DELETE "localhost:9200/artigos_vetorial"

# Verificar logs de erro
curl -X GET "localhost:9200/_cat/indices?v&health=red"
```

### Problemas Comuns

1. **Erro "unknown setting [index.knn]"**: Este erro ocorre quando se usa configurações de versões antigas do Elasticsearch. A partir da versão 8.0+, remova a configuração `"index": {"knn": true}` das settings do índice.

2. **Erro de dimensão**: Verifique se o número de dimensões do embedding corresponde ao mapeamento (384 para all-MiniLM-L6-v2)

3. **Performance lenta**: Ajuste `num_candidates` e considere usar menos dimensões

4. **Memória insuficiente**: Reduza o número de documentos ou use quantização

5. **Erro de conexão**: Verifique se o Elasticsearch está rodando em `localhost:9200`

6. **Logs não aparecem**: O sistema usa logging profissional - verifique o nível de log configurado

## Próximos Passos

1. Implementar pipeline de produção com modelos maiores
2. Experimentar com diferentes modelos de embedding
3. Implementar re-ranking com múltiplos critérios
4. Adicionar monitoramento e alertas de performance

Este pipeline fornece uma base sólida para implementar busca vetorial em produção com Elasticsearch.
