Olá! Este é o meu projeto para o desafio de Engenharia de Dados da Lighthouse que recebi via e-mail.

O objetivo aqui foi construir um pipeline de dados do zero de acordo com o desafio enviado no Word sobre Engenharia de Dados. A ideia era pegar dados de lugares diferentes (um banco de dados antigo e um arquivo CSV), organizar tudo e carregar em um lugar central e confiável, que chamamos de Data Warehouse. Todo esse processo é automatizado usando uma ferramenta chamada Apache Airflow.

Basicamente, eu criei uma linha de montagem de dados que faz o seguinte:

1. **Busca os Dados:** O processo começa buscando dados de dois lugares ao mesmo tempo para ser mais rápido:

      * As informações principais do banco "BanVic" (clientes, contas, etc.)
      * Um arquivo CSV com todas as transações financeiras.

2. **Organiza a Bagunça:** Antes de carregar, os dados são salvos como novos arquivos CSV em uma pasta temporária chamada "output". Eles são organizados por data, para sabermos exatamente o que foi extraído em cada dia.

3. **Carrega no Destino Final:** Depois que a busca dos dados termina com sucesso, a linha de montagem pega esses arquivos organizados e os carrega no nosso Data Warehouse, que é um banco de dados PostgreSQL criado do zero. Uma regra importante que implementei aqui é que, se rodarmos o processo de novo no mesmo dia, os dados antigos são apagados antes de carregar os novos. Isso evita duplicação de dados.

## Ferramentas usadas no projeto

  * **Orquestração:** Apache Airflow (para ser o chefe que comanda/gerencia todo o processo)
  * **Ambiente:** Docker e Docker Compose (para criar máquinas virtuais e garantir que o projeto rode em qualquer computador, evitar o famoso "funciona na minha máquina")
  * **Linguagem:** Python 3
  * **Banco de Dados:** PostgreSQL
  * **Bibliotecas Auxiliares:** Utilizei "pandas" para mexer com os dados como se fossem planilhas, e "psycopg2/SQLAlchemy" para fazer o Python conversar com os bancos de dados, são bibliotecas mais modernas e que funcionam melhor.

## Como rodar o projeto

Tutorial:

**O que você precisa ter instalado:**
  * Docker (Compose)
  * Python 3
  * VS Code

**Passo a passo:**

1.  **Preparar o ambiente:**
    Depois de baixar a pasta do projeto, só precisa garantir que o arquivo "transacoes.csv" esteja na pasta "data/" e o "banvic.sql" esteja na pasta principal. Também é necessário que "docker-compose.yaml" e "docker-compose-banco-de-dados.yml" esteja na pasta raiz do projeto.

2.  **Ligar as Máquinas:**
    Abra o terminal na pasta principal do projeto (também pode ser pelo VS Code desde que esteja na pasta raiz do projeto) e rode o comando abaixo. Ele vai construir e iniciar todos os containers do nosso Docker (o banco de dados antigo, o Airflow e o nosso Data Warehouse).

    docker-compose -f docker-compose-banco-de-dados.yml up -d
    docker-compose up -d --build
	
    **Atenção**: Esse processo pode levar uns 2 ou 3 minutos dependendo do seu hardware e da sua conexão com a rede/internet.

3.  **Visitar o Painel de Controle (Airflow):**
    Quando tudo estiver pronto, abra seu navegador e vá para "http://localhost:8080".
	Para entrar, use:
    **Login:** airflow
    **Senha:** airflow

4.  **Dashboard**

      * Na tela do Airflow, clique no botão de DAG no painel da esquerda. Irá abrir a parte de DAG, nessa tela você procure pelo pipeline "pipeline_dados_indicium".
      * Ative-o no botão à esquerda.
      * Para rodar, é só clicar no botão de "Trigger" que fica do lado direito.

5.  **Parar a execução**

      * Para parar a execução do Docker, utilizem esses comandos:

      docker-compose -f docker-compose-banco-de-dados.yml down
      docker-compose up down

      * Também é possível deletar usando o parâmetro -v (Mas tomem cuidado pois isso apaga tudo)

## Check List caso tenha dado certo

Depois que o pipeline rodar (as tarefas na interface do Airflow ficarão verdes), você pode confirmar o sucesso de duas formas:

1.  **Os Arquivos Temporários:**
    Dê uma olhada na pasta "output". Você verá que ela foi criada com os arquivos CSV que a primeira etapa do processo gerou.

2.  **Data Warehouse (PostgreSQL):**
    Nesse momento, conseguimos ver que os dados já foram alimentados ao banco de dados. Use um programa de banco de dados de sua preferencia (eu usei a extensão do VS Code) para conectar ao Data Warehouse.

      * **Host:** "localhost"
      * **Port:** "5433"
      * **User:** "dw_user"
      * **Password:** "dw_password"
      * **Banco de Dados:** "data_warehouse"

    Lá dentro, você vai encontrar as 5 tabelas ("agencias", "clientes", etc.) com todos os dados organizados.

Obrigado pela oportunidade e pela atenção!
Fico a disposição!