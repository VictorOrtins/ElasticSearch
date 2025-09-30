# Parte 3: Introdução à Busca Vetorial e Embeddings

## Introdução à Busca Vetorial

A busca vetorial representa uma evolução fundamental na forma como recuperamos informações, indo além da busca textual tradicional baseada em palavras-chave para uma abordagem semântica que compreende o **significado** e **contexto** dos dados.

### Limitações da Busca Tradicional

A busca tradicional (lexical) possui algumas limitações importantes:

- **Dependência de palavras exatas**: Buscar por "carro" não retorna documentos que contenham apenas "automóvel"
- **Falta de compreensão semântica**: Não entende sinônimos, contexto ou nuances linguísticas
- **Problema da polissemia**: Palavras com múltiplos significados podem gerar resultados irrelevantes
- **Limitações multilíngues**: Dificuldade em buscar conceitos similares em idiomas diferentes

### O que é Busca Vetorial?

A busca vetorial utiliza **representações numéricas densas** (embeddings) para capturar o significado semântico dos dados. Em vez de comparar palavras exatas, ela compara a **similaridade matemática** entre vetores multidimensionais.

**Principais características:**
- **Busca semântica**: Encontra conteúdo relacionado por significado, não apenas por palavras
- **Robustez a variações**: Funciona com sinônimos, paráfrases e diferentes formulações
- **Suporte multilíngue**: Embeddings podem mapear conceitos similares entre idiomas
- **Flexibilidade de domínio**: Aplicável a texto, imagens, áudio e outros tipos de dados

## Embeddings: A Base da Busca Vetorial

### Definição e Conceito

**Embeddings** são representações vetoriais densas de dados (texto, imagens, etc.) em um espaço multidimensional, onde a proximidade geométrica reflete similaridade semântica.

```python
# Exemplo conceitual de embeddings
"carro" → [0.2, -0.1, 0.8, 0.3, ..., 0.5]  # 768 dimensões
"automóvel" → [0.18, -0.09, 0.82, 0.28, ..., 0.48]  # Vetores similares
"bicicleta" → [0.15, -0.05, 0.7, 0.25, ..., 0.4]   # Relacionado (transporte)
"pizza" → [-0.3, 0.6, -0.2, 0.9, ..., -0.1]        # Completamente diferente
```

### Como os Embeddings são Gerados

Os embeddings são criados através de **modelos de machine learning** treinados em grandes volumes de dados:

#### 1. Modelos de Linguagem Pré-treinados
- **BERT** (Bidirectional Encoder Representations from Transformers)
- **Sentence-BERT**: Otimizado para embeddings de sentenças
- **OpenAI text-embedding-ada-002**: Modelo comercial de alta qualidade
- **Multilingual models**: Como mBERT para suporte a múltiplos idiomas

#### 2. Processo de Treinamento
1. **Pré-treinamento**: Modelo aprende representações gerais em grandes corpora
2. **Fine-tuning**: Ajuste para domínios específicos (opcional)
3. **Extração**: Geração de vetores para novos textos

### Propriedades Matemáticas dos Embeddings

#### Similaridade Coseno
A métrica mais comum para medir similaridade entre embeddings:

```python
import numpy as np

def cosine_similarity(vec1, vec2):
    """Calcula similaridade coseno entre dois vetores"""
    dot_product = np.dot(vec1, vec2)
    norm1 = np.linalg.norm(vec1)
    norm2 = np.linalg.norm(vec2)
    return dot_product / (norm1 * norm2)

# Valores entre -1 (opostos) e 1 (idênticos)
# Valores próximos a 1 indicam alta similaridade
```

#### Outras Métricas de Distância
- **Distância Euclidiana**: Distância geométrica direta
- **Distância Manhattan**: Soma das diferenças absolutas
- **Produto Interno (Dot Product)**: Usado quando vetores são normalizados

## Dense Vector no Elasticsearch

### Tipo de Campo dense_vector

O Elasticsearch introduziu o tipo `dense_vector` para armazenar e indexar embeddings:

```json
{
  "mappings": {
    "properties": {
      "title": {
        "type": "text"
      },
      "content": {
        "type": "text"
      },
      "title_embedding": {
        "type": "dense_vector",
        "dims": 768,
        "index": true,
        "similarity": "cosine"
      },
      "content_embedding": {
        "type": "dense_vector",
        "dims": 768,
        "index": true,
        "similarity": "dot_product"
      }
    }
  }
}
```

### Parâmetros Importantes

- **`dims`**: Número de dimensões do vetor (deve corresponder ao modelo usado)
- **`index`**: Se `true`, permite buscas kNN eficientes
- **`similarity`**: Métrica de similaridade (`cosine`, `dot_product`, `l2_norm`)

### Limitações e Considerações

- **Tamanho máximo**: Até 4096 dimensões por vetor
- **Memória**: Vetores consomem significativamente mais memória que texto
- **Performance**: Indexação de vetores é mais lenta que texto tradicional

## Algoritmo k-Nearest Neighbor (kNN)

### Conceito Fundamental

O algoritmo **k-Nearest Neighbor (kNN)** encontra os `k` vetores mais similares a um vetor de consulta em um espaço multidimensional.

### Desafios do kNN em Alta Dimensionalidade

#### Problema da "Maldição da Dimensionalidade"
- Em espaços de alta dimensão, todos os pontos tendem a ficar equidistantes
- Busca exaustiva torna-se computacionalmente proibitiva
- Necessidade de algoritmos de aproximação

#### Approximate Nearest Neighbor (ANN)
Para resolver os desafios de performance, utilizam-se algoritmos ANN:

### HNSW (Hierarchical Navigable Small World)

O Elasticsearch utiliza o algoritmo **HNSW** para buscas kNN eficientes:

#### Características do HNSW
- **Estrutura hierárquica**: Múltiplas camadas com diferentes níveis de conectividade
- **Navegação eficiente**: Busca começa em camadas superiores e desce gradualmente
- **Balanceamento**: Trade-off entre precisão e velocidade

#### Parâmetros de Configuração
```json
{
  "mappings": {
    "properties": {
      "embedding": {
        "type": "dense_vector",
        "dims": 768,
        "index": true,
        "similarity": "cosine",
        "index_options": {
          "type": "hnsw",
          "m": 16,
          "ef_construction": 200
        }
      }
    }
  }
}
```

- **`m`**: Número de conexões bidirecionais por nó (padrão: 16)
- **`ef_construction`**: Tamanho da lista dinâmica durante construção (padrão: 200)

### Performance e Trade-offs

#### Fatores que Afetam Performance
1. **Dimensionalidade**: Mais dimensões = maior complexidade
2. **Tamanho do dataset**: Mais vetores = busca mais lenta
3. **Parâmetros HNSW**: `m` e `ef_construction` afetam precisão vs velocidade
4. **Hardware**: RAM e CPU influenciam significativamente

#### Otimizações Recomendadas
- **Normalização de vetores**: Para usar `dot_product` eficientemente
- **Quantização**: Reduzir precisão para economizar memória
- **Sharding adequado**: Distribuir carga entre múltiplos shards

## Consultas kNN no Elasticsearch

### Sintaxe Básica da Consulta kNN

```json
{
  "knn": {
    "field": "embedding",
    "query_vector": [0.2, -0.1, 0.8, ...],
    "k": 10,
    "num_candidates": 100
  }
}
```

### Parâmetros da Consulta kNN

- **`field`**: Campo que contém os embeddings
- **`query_vector`**: Vetor de consulta para comparação
- **`k`**: Número de resultados mais similares a retornar
- **`num_candidates`**: Número de candidatos a considerar (afeta precisão)

### Consultas Híbridas

Combinação de busca vetorial com busca tradicional:

```json
{
  "query": {
    "bool": {
      "must": [
        {
          "match": {
            "category": "technology"
          }
        }
      ],
      "should": [
        {
          "knn": {
            "field": "content_embedding",
            "query_vector": [0.1, 0.2, ...],
            "k": 50,
            "boost": 2.0
          }
        }
      ]
    }
  }
}
```

## Casos de Uso da Busca Vetorial

### 1. Busca Semântica de Documentos
- **Problema**: Encontrar documentos relevantes mesmo sem palavras-chave exatas
- **Solução**: Embeddings capturam significado semântico
- **Exemplo**: Buscar "problemas cardíacos" e encontrar textos sobre "doenças do coração"

### 2. Sistemas de Recomendação
- **Problema**: Recomendar conteúdo similar baseado em preferências
- **Solução**: Similaridade entre embeddings de usuários/itens
- **Exemplo**: Netflix recomendando filmes similares

### 3. Detecção de Duplicatas e Plagiarismo
- **Problema**: Identificar conteúdo similar ou duplicado
- **Solução**: Alta similaridade entre embeddings indica duplicação
- **Exemplo**: Detectar artigos acadêmicos similares

### 4. Busca Multilíngue
- **Problema**: Encontrar conteúdo relevante em diferentes idiomas
- **Solução**: Embeddings multilíngues mapeiam conceitos entre idiomas
- **Exemplo**: Buscar em inglês e encontrar resultados em português

### 5. Análise de Sentimento e Classificação
- **Problema**: Categorizar texto por sentimento ou tópico
- **Solução**: Embeddings preservam informações semânticas para classificação
- **Exemplo**: Classificar reviews como positivos/negativos

## Vantagens e Limitações

### Vantagens da Busca Vetorial

1. **Compreensão semântica**: Entende significado além de palavras-chave
2. **Robustez linguística**: Funciona com sinônimos e paráfrases
3. **Flexibilidade de domínio**: Aplicável a diversos tipos de conteúdo
4. **Qualidade dos resultados**: Frequentemente mais relevantes que busca tradicional

### Limitações e Desafios

1. **Complexidade computacional**: Requer mais recursos que busca tradicional
2. **Interpretabilidade**: Difícil explicar por que um resultado foi retornado
3. **Dependência de modelos**: Qualidade depende do modelo de embedding usado
4. **Custo de infraestrutura**: Maior uso de memória e processamento

### Quando Usar Busca Vetorial

**Use busca vetorial quando:**
- Precisão semântica é mais importante que velocidade
- Usuários fazem consultas em linguagem natural
- Conteúdo possui muitos sinônimos ou variações
- Necessita busca multilíngue
- Dados são ricos em contexto semântico

**Use busca tradicional quando:**
- Buscas são principalmente por termos exatos
- Performance é crítica
- Recursos computacionais são limitados
- Interpretabilidade é essencial

## Conclusão

A busca vetorial representa uma evolução significativa na recuperação de informações, oferecendo capacidades semânticas que a busca tradicional não consegue alcançar. O Elasticsearch, com seu suporte nativo a `dense_vector` e algoritmos HNSW, fornece uma plataforma robusta para implementar soluções de busca vetorial em escala.

A combinação de embeddings de alta qualidade, algoritmos eficientes como HNSW, e a flexibilidade do Elasticsearch cria oportunidades para desenvolver aplicações de busca mais inteligentes e contextualmente relevantes.

**Próximos passos**: Na parte prática, implementaremos um pipeline completo de busca vetorial, desde a geração de embeddings até consultas kNN avançadas.
