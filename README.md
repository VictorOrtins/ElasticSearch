# Projeto Final: Arquitetura Distribuída com Elasticsearch

Este repositório contém o desenvolvimento e a documentação do projeto final para a disciplina de Engenharia de Sistemas Distribuídos. O trabalho foca na análise aprofundada da arquitetura do Elasticsearch, explorando sua aplicação como uma solução robusta para buscas modernas e, em especial, sua capacidade de operar como um banco de dados vetorial para buscas de embeddings em larga escala.

# 👨‍💻 Membros da Equipe

    ANA CAROLINA RODRIGUES LIMA DE AGUIAR

    CASSIANO SABINO

    FRANCISCO SANTANA DE SOUSA JUNIOR

    GEOVANA MARIA DOS SANTOS LIMA

    PEDRO AUGUSTO GOMES MEDEIROS

    VICTOR PESSOA OLIVEIRA ORTINS

# Tabela de Conteúdos

    Objetivos do Projeto

    Tópicos Abordados

    Cronograma de Entregas

    Tecnologias Utilizadas

    Como Executar os Exemplos

    Licença

# 🎯 Objetivos do Projeto
## Objetivo Geral

Apresentar e analisar a arquitetura distribuída do Elasticsearch como uma solução robusta e escalável para sistemas de busca modernos, com um foco aprofundado em sua capacidade de operar como um banco de dados vetorial para buscas de embeddings em larga escala.

## Objetivos Específicos

    Detalhar a arquitetura fundamental do Elasticsearch (cluster, nós, shards, réplicas) e como seus componentes garantem escalabilidade e confiabilidade.

    Explorar a API RESTful como a principal interface de comunicação para gerenciamento e operações de dados no cluster.

    Apresentar o conceito de busca vetorial (Vector Search) e sua implementação nativa no Elasticsearch para consultas de similaridade em embeddings.

    Investigar e documentar casos de uso reais de empresas que utilizam Elasticsearch para busca semântica de textos ou sistemas de recomendação.

    Analisar os principais atributos de qualidade não-funcionais (desempenho e segurança) em um ambiente de produção com Elasticsearch.

# 📚 Tópicos Abordados

    Arquitetura de Sistemas Distribuídos: Análise prática da arquitetura do Elasticsearch, focando em conceitos de particionamento de dados (sharding) e tolerância a falhas (replication).

    Comunicação e Interoperabilidade via APIs: Estudo da interface RESTful como padrão para comunicação em ecossistemas de microsserviços que interagem com o Elasticsearch.

    Indexação e Algoritmos de Busca Avançada: Investigação das estruturas de dados (ex: Inverted Index) e algoritmos (ex: HNSW para Approximate Nearest Neighbor) que garantem a performance.

    Escalabilidade Horizontal e Confiabilidade: Demonstração de como a arquitetura permite o crescimento do sistema e a manutenção da disponibilidade mesmo com falhas de componentes.

    Segurança em Camadas para Sistemas Distribuídos: Abordagem das primitivas de segurança (autenticação, autorização, criptografia) essenciais para proteger um cluster distribuído.

# 🚀 Cronograma de Entregas

O projeto está estruturado em 5 entregas, cada uma composta por uma seção teórica e uma demonstração prática.

## Entrega 1: Fundamentos da Arquitetura Distribuída do Elasticsearch

    Data: Sexta, 05 de Setembro

    Teoria: Explicação conceitual de clusters, nós, índices, shards e réplicas, com um diagrama da arquitetura.

    Prática: Tutorial para iniciar uma instância local do Elasticsearch via Docker e executar comandos básicos de verificação de saúde do cluster.

## Entrega 2: Escalabilidade, Confiabilidade e a API RESTful

    Data: Sexta, 12 de Setembro

    Teoria: Aprofundamento em como sharding promove escalabilidade horizontal e replication garante alta disponibilidade. Explanação sobre a API RESTful.

    Prática: Criação de um índice com número customizado de shards e réplicas. Execução de operações CRUD (Create, Read, Update, Delete) via API REST.

## Entrega 3: Introdução à Busca Vetorial e Embeddings

    Data: Sexta, 19 de Setembro

    Teoria: Explicação sobre embeddings, busca por similaridade, o tipo dense_vector e o algoritmo k-Nearest Neighbor (kNN) no Elasticsearch.

    Prática: Criação de um pipeline para gerar embeddings de texto, indexação dos vetores e execução de uma consulta knn para encontrar textos similares.

## Entrega 4: Casos de Uso Reais com Busca Vetorial

    Data: Sexta, 26 de Setembro

    Pesquisa: Estudo de caso de 2 a 3 empresas, detalhando o problema de negócio e a solução arquitetural implementada com busca vetorial no Elasticsearch.

## Entrega 5: Atributos de Qualidade: Desempenho e Segurança

    Data: Sexta, 03 de Outubro

    Teoria: Análise do algoritmo HNSW (Hierarchical Navigable Small World) para otimização de performance e detalhamento das camadas de segurança do Elasticsearch (autenticação, RBAC, criptografia).

    Prática: Habilitação da segurança básica no cluster local, criação de um usuário com permissões restritas e execução de testes simples de performance.

# 🛠️ Tecnologias Utilizadas

    Elasticsearch: Núcleo do projeto, utilizado para busca, análise e armazenamento de dados.

    Docker & Docker Compose: Para provisionar e gerenciar o ambiente de desenvolvimento de forma isolada e reproduzível.

    API REST: Interface primária para interagir com o cluster Elasticsearch.

    cURL / Kibana Dev Tools: Utilitários para realizar chamadas à API.

# ⚙️ Como Executar os Exemplos

Para executar os exemplos práticos de cada entrega, é necessário ter o Docker e o Docker Compose instalados.

    Clone o repositório:

    git clone <URL_DO_SEU_REPOSITORIO>
    cd <NOME_DO_SEU_REPOSITORIO>

    Navegue até a pasta da entrega desejada:

    cd aula-desejada/

    Inicie o ambiente com Docker Compose:

    docker-compose up -d

    Siga as instruções detalhadas no README.md específico de cada entrega para executar os comandos e testes práticos.

📄 Licença

Este projeto é distribuído sob a licença MIT. Veja o arquivo LICENSE para mais detalhes.