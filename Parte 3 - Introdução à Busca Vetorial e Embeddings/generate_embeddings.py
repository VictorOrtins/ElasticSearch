#!/usr/bin/env python3
"""
Pipeline de Geração de Embeddings para Elasticsearch
Parte 3: Introdução à Busca Vetorial e Embeddings
"""

from sentence_transformers import SentenceTransformer
from elasticsearch import Elasticsearch
import sys
import logging

from data import artigos


def main():
    # Configurar logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    logger = logging.getLogger(__name__)

    logger.info("Iniciando pipeline de geração de embeddings")

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

    logger.info("Conexão estabelecida com sucesso")

    # Dados de exemplo

    # Função para gerar embeddings

    def gerar_embeddings(texto):
        embedding = model.encode(texto)
        return embedding.tolist()

    logger.info(f"Processando {len(artigos)} documentos")

    # Indexar documentos com embeddings
    for i, artigo in enumerate(artigos, 1):
        logger.info(
            f"Processando documento {i}/{len(artigos)}: {artigo['titulo'][:50]}")

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


if __name__ == "__main__":
    main()
