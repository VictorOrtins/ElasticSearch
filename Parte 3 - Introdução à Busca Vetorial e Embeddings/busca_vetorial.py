#!/usr/bin/env python3
"""
Sistema de Busca Vetorial Interativo
Parte 3: Introdução à Busca Vetorial e Embeddings
"""

from sentence_transformers import SentenceTransformer
from elasticsearch import Elasticsearch
import sys
import time
import logging


class BuscaVetorial:
    def __init__(self):
        # Configurar logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        self.logger = logging.getLogger(__name__)

        self.logger.info("Inicializando sistema de busca vetorial")

        # Inicializar modelo e Elasticsearch
        self.logger.info("Carregando modelo SentenceTransformer")
        self.model = SentenceTransformer('all-MiniLM-L6-v2')

        self.logger.info("Conectando ao Elasticsearch")
        self.es = Elasticsearch(
            [{'host': 'localhost', 'port': 9200, 'scheme': 'http'}])

        # Verificar conexão
        if not self.es.ping():
            self.logger.error("Não foi possível conectar ao Elasticsearch")
            sys.exit(1)

        self.logger.info("Sistema pronto para uso")

    def buscar_por_similaridade(self, query, campo="conteudo_embedding", k=5):
        """Busca por similaridade usando embeddings"""
        self.logger.info(f"Buscando por: '{query}'")

        # Gerar embedding da consulta
        inicio = time.time()
        query_embedding = self.model.encode(query).tolist()
        tempo_embedding = time.time() - inicio

        # Executar busca kNN
        inicio_busca = time.time()
        response = self.es.search(
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
        tempo_busca = time.time() - inicio_busca

        self.logger.info(f"Tempo de embedding: {tempo_embedding:.3f}s")
        self.logger.info(f"Tempo de busca: {tempo_busca:.3f}s")
        self.logger.info(
            f"Encontrados {len(response['hits']['hits'])} resultados")

        return response

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

    def busca_combinada(self, query, boost_vetorial=1.0, boost_textual=1.0, k=10):
        """Busca combinada (vetorial + textual)"""
        query_embedding = self.model.encode(query).tolist()

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
            },
            "_source": ["titulo", "conteudo", "categoria", "data_publicacao"]
        }

        return self.es.search(index="artigos_vetorial", body=body)

    def recomendar_similar(self, doc_id, k=3):
        """Recomenda documentos similares baseado em um documento específico"""
        try:
            # Obter documento original
            doc = self.es.get(index="artigos_vetorial", id=doc_id)
            embedding = doc['_source']['conteudo_embedding']

            # Buscar similares (excluindo o próprio documento)
            response = self.es.search(
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
                    },
                    "_source": ["titulo", "conteudo", "categoria", "data_publicacao"]
                }
            )

            return response['hits']['hits'][:k]

        except Exception as e:
            self.logger.error(f"Erro ao buscar recomendações: {e}")
            return []

    def exibir_resultados(self, response):
        """Exibe os resultados de forma formatada"""
        hits = response['hits']['hits']

        if not hits:
            print("Nenhum resultado encontrado")
            return

        print("\n" + "="*80)
        print("RESULTADOS DA BUSCA")
        print("="*80)

        for i, hit in enumerate(hits, 1):
            score = hit['_score']
            doc = hit['_source']

            print(f"\nResultado {i}")
            print(f"   Score: {score:.4f}")
            print(f"   Título: {doc['titulo']}")
            print(f"   Categoria: {doc['categoria']}")
            print(f"   Data: {doc['data_publicacao']}")
            print(f"   Conteúdo: {doc['conteudo'][:150]}...")
            print("-" * 80)

    def estatisticas_indice(self):
        """Mostra estatísticas do índice"""
        try:
            stats = self.es.indices.stats(index="artigos_vetorial")
            count = self.es.count(index="artigos_vetorial")

            print("\nESTATÍSTICAS DO ÍNDICE")
            print("="*50)
            print(f"Total de documentos: {count['count']}")
            print(
                f"Tamanho do índice: {stats['indices']['artigos_vetorial']['total']['store']['size_in_bytes']} bytes")
            print(
                f"Total de consultas: {stats['indices']['artigos_vetorial']['total']['search']['query_total']}")

            if stats['indices']['artigos_vetorial']['total']['search']['query_total'] > 0:
                tempo_medio = stats['indices']['artigos_vetorial']['total']['search']['query_time_in_millis'] / \
                    stats['indices']['artigos_vetorial']['total']['search']['query_total']
                print(f"Tempo médio de consulta: {tempo_medio:.2f}ms")

        except Exception as e:
            self.logger.error(f"Erro ao obter estatísticas: {e}")


def menu_interativo():
    """Menu interativo para demonstrar as funcionalidades"""
    busca = BuscaVetorial()

    while True:
        print("\n" + "="*60)
        print("SISTEMA DE BUSCA VETORIAL - MENU PRINCIPAL")
        print("="*60)
        print("1. Busca por similaridade")
        print("2. Busca híbrida (com filtros)")
        print("3. Busca combinada (vetorial + textual)")
        print("4. Recomendações baseadas em documento")
        print("5. Estatísticas do índice")
        print("6. Sair")

        opcao = input("\nEscolha uma opção (1-6): ").strip()

        if opcao == "1":
            query = input("Digite sua consulta: ").strip()
            if query:
                k = input("Número de resultados (padrão 5): ").strip()
                k = int(k) if k.isdigit() else 5

                resultados = busca.buscar_por_similaridade(query, k=k)
                busca.exibir_resultados(resultados)

        elif opcao == "2":
            query = input("Digite sua consulta: ").strip()
            categoria = input("Filtrar por categoria (opcional): ").strip()
            categoria = categoria if categoria else None

            if query:
                resultados = busca.busca_hibrida(query, categoria=categoria)
                busca.exibir_resultados(resultados)

        elif opcao == "3":
            query = input("Digite sua consulta: ").strip()
            if query:
                resultados = busca.busca_combinada(query)
                busca.exibir_resultados(resultados)

        elif opcao == "4":
            doc_id = input("Digite o ID do documento (1-8): ").strip()
            if doc_id.isdigit():
                recomendacoes = busca.recomendar_similar(doc_id)
                if recomendacoes:
                    print(f"\nDocumentos similares ao documento {doc_id}:")
                    for i, rec in enumerate(recomendacoes, 1):
                        doc = rec['_source']
                        score = rec['_score']
                        print(f"   {i}. {doc['titulo']} (Score: {score:.4f})")

        elif opcao == "5":
            busca.estatisticas_indice()

        elif opcao == "6":
            print("Obrigado por usar o sistema de busca vetorial!")
            break

        else:
            print("Opção inválida. Tente novamente.")


if __name__ == "__main__":
    try:
        menu_interativo()
    except KeyboardInterrupt:
        print("\n\nSistema encerrado pelo usuário.")
    except Exception as e:
        print(f"\nErro inesperado: {e}")
