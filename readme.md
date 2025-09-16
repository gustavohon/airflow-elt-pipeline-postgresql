Pipeline de Dados para Análise Financeira com Airflow e Docker
🎯 Objetivo do Projeto
Este projeto demonstra a construção de um pipeline de dados ELT (Extract, Load, Transform) de ponta a ponta, simulando um cenário real de engenharia de dados para uma instituição financeira.

O objetivo principal é consolidar dados de fontes heterogêneas — um banco de dados transacional (PostgreSQL) e arquivos de dados brutos (CSV) — em um Data Warehouse centralizado, pronto para análises e business intelligence. Todo o processo é orquestrado e automatizado com o Apache Airflow, garantindo que o pipeline seja robusto, agendável e idempotente.

🏗️ Arquitetura e Fluxo de Dados
O pipeline foi projetado para ser eficiente e escalável, seguindo as melhores práticas de engenharia de dados:

Extração Paralela:

Os dados são extraídos simultaneamente de duas fontes para otimizar o tempo de execução:

Banco de Dados Relacional: Informações cadastrais de clientes, agências, contas e colaboradores de um banco de dados PostgreSQL.

Arquivos CSV: Dados históricos de transações financeiras.

Staging (Área de Passagem):

Os dados brutos extraídos são padronizados para o formato CSV e salvos em uma área de passagem (staging area). Os arquivos são organizados em diretórios com a data da execução, criando um histórico e facilitando a depuração.

Carregamento (Load):

Após a conclusão bem-sucedida de ambas as extrações, uma tarefa de carregamento é acionada.

Ela lê os arquivos da área de passagem e os insere em tabelas correspondentes em um Data Warehouse PostgreSQL dedicado.

A lógica de carregamento utiliza if_exists='replace' para garantir a idempotência, permitindo que o pipeline seja re-executado para o mesmo dia sem risco de duplicar dados.

🛠️ Tecnologias Utilizadas
Orquestração: Apache Airflow

Contêineres: Docker e Docker Compose

Linguagem: Python

Bancos de Dados: PostgreSQL (tanto como fonte quanto como Data Warehouse)

Bibliotecas Python: pandas para manipulação de dados, psycopg2 e SQLAlchemy para a interação com os bancos de dados.

▶️ Como Executar o Projeto
Pré-requisitos:

Docker

Docker Compose

Passo a passo para a execução:

Clone o repositório para a sua máquina.

Inicie o Ambiente Docker:
Abra um terminal na pasta raiz do projeto e execute o comando abaixo. Ele irá construir e iniciar todos os serviços necessários (o banco de dados fonte, o Airflow e o Data Warehouse).

Bash

docker-compose up -d --build
Aguarde alguns minutos para que todos os serviços do Airflow estejam completamente no ar.

Acesse a Interface do Airflow:
Abra seu navegador e acesse http://localhost:8080. As credenciais padrão são:

Login: airflow

Senha: airflow

Execute o Pipeline:

Na interface do Airflow, localize a DAG pipeline_dados_indicium.

Ative-a utilizando o botão de "toggle" à esquerda.

Inicie uma execução manual clicando no botão de "Play" (▶️) à direita.

✅ Verificando o Resultado
Após a execução bem-sucedida da DAG (todas as tarefas ficarão verdes na interface), você pode confirmar o resultado:

Arquivos de Staging:
Uma pasta output/ será criada na raiz do projeto, contendo os arquivos CSV extraídos e organizados por data.

Dados no Data Warehouse:
Utilize um cliente de banco de dados de sua preferência para se conectar ao Data Warehouse:

Host: localhost

Porta: 5433

Usuário: dw_user

Senha: dw_password

Banco de Dados: data_warehouse

Dentro do banco, você encontrará as cinco tabelas (agencias, clientes, colaboradores, contas e transacoes) populadas com os dados processados pelo pipeline.
