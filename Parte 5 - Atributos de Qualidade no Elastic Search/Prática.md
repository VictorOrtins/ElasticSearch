# Guia do Script Python: Segurança e Performance no Elasticsearch

Este documento detalha o script Python `gerenciar_elastic.py`, que automatiza tarefas práticas de segurança e realiza testes de performance em um cluster Elasticsearch local.

## O que o script faz?

O script executa duas tarefas principais em sequência:

1.  [cite_start]**Habilitar a Segurança Básica e Criar um Usuário Restrito**[cite: 49]: Ele se conecta ao cluster como administrador e:
    -   Cria um **papel (role)** chamado `leitor_de_logs_especifico` que só tem permissão para ler (`read`) índices que correspondam ao padrão `meu-indice-especifico-*`.
    -   Cria um **usuário** chamado `analista_de_leitura` e o associa a esse papel, garantindo que ele tenha acesso limitado.

2.  [cite_start]**Executar Testes de Performance Simples**[cite: 50]: Ele compara o tempo de resposta de duas abordagens de busca vetorial para demonstrar o ganho de performance das otimizações:
    -   **Busca Otimizada (ANN):** Utiliza a funcionalidade `knn` nativa, que se baseia no algoritmo HNSW para encontrar resultados aproximados rapidamente.
    -   **Busca Não-Otimizada (kNN Exato):** Força o Elasticsearch a comparar o vetor de busca com todos os documentos do índice usando um `script_score`, resultando em uma busca mais lenta, porém exata.

## Pré-requisitos

1.  **Python 3** instalado.
2.  **Cluster Elasticsearch Seguro Rodando**: Você deve ter completado os passos do arquivo `setup_ambiente.md`.
3.  **Bibliotecas Python Instaladas**: Abra seu terminal e instale as dependências.
    ```bash
    pip install elasticsearch numpy
    ```
    * `elasticsearch`: Cliente oficial para interagir com a API do Elasticsearch.
    * `numpy`: Necessário para gerar os dados vetoriais para o teste de performance.

## Como Rodar o Script

1.  Salve o código da Parte 2 em um arquivo chamado `gerenciar_elastic.py`.

2.  Abra seu terminal no mesmo diretório onde salvou o arquivo.

3.  Execute o script com o comando:
    ```bash
    python gerenciar_elastic.py
    ```
4.  O script irá solicitar que você digite a senha do usuário `elastic` (a mesma que você guardou ao iniciar o contêiner Docker). Digite-a e pressione Enter.

    * **Alternativa**: Para não digitar a senha toda vez, você pode defini-la como uma variável de ambiente:
        ```bash
        # No Linux/macOS
        export ELASTIC_PASSWORD="sua_senha_aqui"

        # No Windows (PowerShell)
        $env:ELASTIC_PASSWORD="sua_senha_aqui"
        ```

## Entendendo o Código

-   **Conexão Inicial (`if __name__ == "__main__":`)**: O script começa se conectando ao cluster em `https://localhost:9200`. A opção `verify_certs=False` é importante para ambientes de desenvolvimento, pois ignora a validação do certificado auto-assinado do Docker. O `basic_auth` usa o usuário `elastic` e a senha fornecida para se autenticar como administrador.

-   **Função `setup_security_and_user()`**:
    -   Recebe o cliente administrador (`admin_client`).
    -   Usa `admin_client.security.put_role()` para criar o papel de leitura. O corpo da requisição define as permissões exatas.
    -   Usa `admin_client.security.put_user()` para criar o novo usuário, associando-o ao papel criado anteriormente.
    -   Inclui tratamento de erro para não falhar caso o script seja executado mais de uma vez e o usuário/papel já existam.

-   **Função `run_performance_tests()`**:
    -   Primeiro, ela limpa e cria um índice de teste (`indice-vetorial-teste`) com um mapeamento específico para `dense_vector`. A configuração `"index": "true"` no mapeamento é o que instrui o Elasticsearch a criar a estrutura de dados HNSW para otimização.
    -   Ela então indexa 1000 documentos com vetores aleatórios para criar uma base de dados para o teste.
    -   Executa a busca **otimizada** usando o parâmetro `knn`. Esta é a forma moderna e rápida de fazer buscas por similaridade.
    -   Executa a busca **não-otimizada** usando `script_score` com a função `cosineSimilarity`. Isso força um cálculo manual em todos os 1000 documentos.
    -   Ao final, imprime o valor do campo `took` de cada resposta, que representa o tempo (em milissegundos) que o Elasticsearch levou para processar a busca. A diferença entre os dois valores demonstra o impacto da otimização.