# Parte 3: Introdução à Busca Vetorial e Embeddings

## 📋 Visão Geral

Esta entrega apresenta os conceitos fundamentais de **busca vetorial** e **embeddings** no Elasticsearch, demonstrando como implementar um sistema de busca semântica completo que vai além da busca textual tradicional.

## 🎯 Objetivos

- **Teoria**: Compreender embeddings, busca por similaridade, o tipo `dense_vector` e o algoritmo k-Nearest Neighbor (kNN)
- **Prática**: Implementar um pipeline completo para gerar embeddings, indexar vetores e executar consultas kNN

## 📚 Conteúdo

### 📖 Parte Teórica (`Teórica.md`)
- Introdução à busca vetorial vs busca tradicional
- Conceitos fundamentais de embeddings
- Tipo `dense_vector` no Elasticsearch
- Algoritmo kNN e HNSW
- Casos de uso e aplicações práticas

### 🛠️ Parte Prática (`Prática.md`)
- Pipeline completo de geração de embeddings
- Configuração de índices vetoriais
- Consultas kNN básicas e avançadas
- Busca híbrida (vetorial + textual)
- Análise de performance e otimizações

## 🚀 Início Rápido

### 1. Pré-requisitos
- Elasticsearch rodando (conforme Parte 1)
- Python 3.8+
- Docker (para Elasticsearch)

### 2. Instalação das Dependências
```bash
pip install -r requirements.txt
```

### 3. Configurar o Índice Vetorial
```bash
curl -X PUT "localhost:9200/artigos_vetorial" -H 'Content-Type: application/json' -d'
{
  "settings": {
    "number_of_shards": 1,
    "number_of_replicas": 0
  },
  "mappings": {
    "properties": {
      "titulo": {"type": "text"},
      "conteudo": {"type": "text"},
      "categoria": {"type": "keyword"},
      "data_publicacao": {"type": "date"},
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

### 4. Gerar e Indexar Embeddings
```bash
python generate_embeddings.py
```

### 5. Executar Buscas Vetoriais
```bash
python busca_vetorial.py
```

## 🔧 Scripts Disponíveis

### `generate_embeddings.py`
Pipeline automatizado para:
- Configurar sistema de logging profissional
- Carregar modelo SentenceTransformer (all-MiniLM-L6-v2)
- Gerar embeddings para 8 documentos de exemplo
- Indexar no Elasticsearch com vetores (384 dimensões)
- Verificar conexão e saúde do índice

### `busca_vetorial.py`
Sistema interativo com:
- Sistema de logging profissional
- Menu interativo completo (6 opções)
- Busca por similaridade semântica
- Busca híbrida com filtros por categoria
- Busca combinada (vetorial + textual)
- Sistema de recomendações baseado em documentos
- Análise de performance em tempo real
- Estatísticas detalhadas do índice

## 📊 Funcionalidades Demonstradas

### 🔍 Busca Semântica
```python
# Buscar "aprendizado de máquina" encontra:
# - "Inteligência Artificial e Machine Learning"
# - "Redes Neurais e Deep Learning"
# - "Algoritmos de Busca e Ordenação"
```

### 🎯 Busca Híbrida
```python
# Combinar busca vetorial com filtros:
busca_hibrida("inteligência artificial", categoria="tecnologia")
```

### 💡 Recomendações
```python
# Encontrar documentos similares a um específico:
recomendar_similar(doc_id=1, k=3)
```

## 📈 Métricas de Performance

O sistema inclui medição de:
- **Tempo de geração de embeddings**
- **Latência de consultas kNN**
- **Precisão vs velocidade (trade-offs)**
- **Uso de memória**

## 🔬 Conceitos Avançados Abordados

### Algoritmo HNSW
- Estrutura hierárquica para busca eficiente
- Parâmetros `m` e `ef_construction`
- Trade-offs entre precisão e performance

### Métricas de Similaridade
- **Cosine Similarity**: Para vetores normalizados
- **Dot Product**: Para vetores não-normalizados
- **Euclidean Distance**: Distância geométrica

### Otimizações
- Configurações de índice para performance
- Quantização de vetores
- Sharding adequado para escala

## 🎓 Casos de Uso Demonstrados

1. **Busca Semântica**: Encontrar documentos por significado
2. **Detecção de Duplicatas**: Identificar conteúdo similar
3. **Sistema de Recomendação**: Sugerir conteúdo relacionado
4. **Busca Multilíngue**: Conceitos em diferentes idiomas
5. **Classificação por Similaridade**: Agrupar documentos similares

## 🔍 Exemplos de Consultas

### Busca Básica kNN
```bash
curl -X POST "localhost:9200/artigos_vetorial/_search" -H 'Content-Type: application/json' -d'
{
  "knn": {
    "field": "conteudo_embedding",
    "query_vector": [0.1, 0.2, ...],
    "k": 5,
    "num_candidates": 50
  }
}'
```

### Busca Híbrida
```bash
curl -X POST "localhost:9200/artigos_vetorial/_search" -H 'Content-Type: application/json' -d'
{
  "query": {
    "bool": {
      "filter": [{"term": {"categoria": "tecnologia"}}]
    }
  },
  "knn": {
    "field": "conteudo_embedding",
    "query_vector": [0.1, 0.2, ...],
    "k": 5
  }
}'
```

## 📚 Recursos Adicionais

### Modelos de Embedding Recomendados
- **all-MiniLM-L6-v2**: Rápido e eficiente (384 dims)
- **all-mpnet-base-v2**: Melhor qualidade (768 dims)
- **multilingual-e5-large**: Suporte multilíngue (1024 dims)

### Ferramentas de Análise
- **Kibana**: Visualização de dados vetoriais
- **Elasticsearch Head**: Monitoramento de índices
- **Python Notebooks**: Análise exploratória

## 🚨 Troubleshooting

### Problemas Comuns
1. **Erro "unknown setting [index.knn]"**: Remover configuração `"index": {"knn": true}` para Elasticsearch 8.0+
2. **Erro de dimensão**: Verificar se dims no mapping corresponde ao modelo (384 para all-MiniLM-L6-v2)
3. **Performance lenta**: Ajustar `num_candidates` e parâmetros HNSW
4. **Memória insuficiente**: Reduzir número de documentos ou usar quantização
5. **Erro de conexão**: Verificar se Elasticsearch está em `localhost:9200`
6. **Logs não aparecem**: Sistema usa logging profissional - verificar nível configurado

### Comandos Úteis
```bash
# Verificar saúde do cluster
curl -X GET "localhost:9200/_cluster/health?pretty"

# Verificar mapeamentos
curl -X GET "localhost:9200/artigos_vetorial/_mapping?pretty"

# Estatísticas do índice
curl -X GET "localhost:9200/artigos_vetorial/_stats?pretty"
```

## 🔄 Próximos Passos

1. **Entrega 4**: Casos de uso reais com busca vetorial
2. **Entrega 5**: Otimização de performance e segurança
3. **Implementações avançadas**: Re-ranking, modelos customizados
4. **Produção**: Monitoramento, alertas, escalabilidade

---

**Data de Entrega**: Sexta, 19 de Setembro  
**Equipe**: Ana Carolina, Cassiano, Francisco, Geovana, Pedro, Victor
