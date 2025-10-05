# gerenciar_elastic.py

import os
from getpass import getpass
from elasticsearch import Elasticsearch, ApiError
import time

# ==============================================================================
# SEÇÃO 1: CONFIGURAÇÃO E CRIAÇÃO DE USUÁRIO COM PERMISSÕES RESTRITAS
# ==============================================================================

def setup_security_and_user(admin_client: Elasticsearch):
    """
    Cria um papel com permissão de leitura e um usuário associado a esse papel.
    """
    print("--- INICIANDO CONFIGURAÇÃO DE SEGURANÇA ---")
    
    # Definições do papel e do usuário
    role_name = "leitor_de_logs_especifico"
    user_name = "analista_de_leitura"
    user_password = "Password123!" # Senha para o novo usuário
    index_pattern = "meu-indice-especifico-*"

    # 1.1: Criar um papel (role) com permissão de apenas leitura a um índice específico
    print(f"1. Criando o papel '{role_name}' para ler o padrão de índice '{index_pattern}'...")
    try:
        admin_client.security.put_role(
            name=role_name,
            body={
                "indices": [
                    {
                        "names": [index_pattern],
                        "privileges": ["read"]
                    }
                ]
            }
        )
        print(f"-> Papel '{role_name}' criado com sucesso.")
    except ApiError as e:
        if e.status_code == 400 and "already exists" in str(e.body):
            print(f"-> Papel '{role_name}' já existe. Pulando criação.")
        else:
            print(f"Erro inesperado ao criar papel: {e}")
            return None, None # Retorna None em caso de falha

    # 1.2: Criar um novo usuário e associá-lo ao papel criado
    print(f"2. Criando o usuário '{user_name}' com o papel '{role_name}'...")
    try:
        admin_client.security.put_user(
            username=user_name,
            body={
                "password": user_password,
                "roles": [role_name],
                "full_name": "Analista com Acesso Restrito"
            }
        )
        print(f"-> Usuário '{user_name}' criado com sucesso.")
    except ApiError as e:
        if e.status_code == 400 and "already exists" in str(e.body):
             print(f"-> Usuário '{user_name}' já existe. Pulando criação.")
        else:
            print(f"Erro inesperado ao criar usuário: {e}")
            return None, None
            
    return user_name, user_password


# ==============================================================================
# SEÇÃO 2: TESTES DE PERFORMANCE DE BUSCA VETORIAL
# ==============================================================================

def run_performance_tests(admin_client: Elasticsearch):
    """
    Compara o tempo de resposta de uma busca vetorial otimizada (ANN)
    com uma busca não-otimizada (kNN exato com script_score).
    """
    print("\n--- INICIANDO TESTES DE PERFORMANCE ---")
    index_name = "indice-vetorial-teste"
    vector_dim = 4

    # 2.1: Preparar o ambiente de teste
    print(f"1. Preparando o índice '{index_name}' para o teste...")
    if admin_client.indices.exists(index=index_name):
        admin_client.indices.delete(index=index_name)
    
    admin_client.indices.create(
        index=index_name,
        mappings={
            "properties": {
                "vetor": {
                    "type": "dense_vector",
                    "dims": vector_dim,
                    "index": "true",       # Habilita a indexação HNSW
                    "similarity": "cosine"
                }
            }
        }
    )
    # Indexa 1000 documentos com vetores aleatórios
    for i in range(1000):
        admin_client.index(index=index_name, document={"vetor": list(np.random.rand(vector_dim))})
    admin_client.indices.refresh(index=index_name)
    print("-> Índice preparado com 1000 documentos.")

    query_vector = list(np.random.rand(vector_dim))
    print(f"2. Usando vetor de consulta aleatório.")

    # 2.2: Teste com otimização (Busca ANN com HNSW)
    print("\n-> Executando busca VETORIAL OTIMIZADA (ANN)...")
    response_ann = admin_client.search(
        index=index_name,
        knn={
            "field": "vetor",
            "query_vector": query_vector,
            "k": 10,
            "num_candidates": 100
        }
    )
    print(f"   Resultado: {response_ann['took']} ms")

    # 2.3: Teste sem otimização (Busca kNN Exata com script_score)
    print("-> Executando busca VETORIAL NÃO-OTIMIZADA (kNN Exato)...")
    response_exact = admin_client.search(
        index=index_name,
        query={
            "script_score": {
                "query": {"match_all": {}},
                "script": {
                    "source": "cosineSimilarity(params.query_vector, 'vetor') + 1.0",
                    "params": {"query_vector": query_vector}
                }
            }
        },
        size=10
    )
    print(f"   Resultado: {response_exact['took']} ms")


# ==============================================================================
# FUNÇÃO PRINCIPAL
# ==============================================================================

if __name__ == "__main__":
    # Tenta obter a senha de uma variável de ambiente. Se não conseguir, pede ao usuário.
    try:
        elastic_password = "7vkRX0wy7Qgog5yw8Et-"
    except KeyError:
        elastic_password = getpass("Digite a senha do usuário 'elastic' do Elasticsearch: ")

    # Conecta-se ao cluster como o superusuário 'elastic'
    client = Elasticsearch(
        "http://localhost:9200",
        basic_auth=("elastic", elastic_password),
        verify_certs=False  # Para ambientes de dev com certificado auto-assinado
    )

    print("Conexão com Elasticsearch bem-sucedida!")
    # [cite_start]Executa a criação do usuário restrito [cite: 49]
    created_user, created_pass = setup_security_and_user(client)
    
    # [cite_start]Executa os testes de performance [cite: 50]
    # É necessário numpy para gerar os dados do teste
    try:
        import numpy as np
        run_performance_tests(client)
    except ImportError:
        print("\nAVISO: A biblioteca 'numpy' não está instalada. Testes de performance não serão executados.")
        print("Para rodar os testes, instale com: pip install numpy")