from airflow.models.dag import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import sys

# caminho do projeto (necessário adicionar pasta raiz no docker-compose.yaml)
caminho_projeto_no_container = '/opt/airflow/src/indicium-projeto'
sys.path.insert(0, caminho_projeto_no_container)

# importação dos scripts que criei pro Airflow
from scripts.extrair_csv import extrair_e_salvar_csv
from scripts.extrair_sql import extrair_dados_do_sql
from scripts.carregamento_dw import carregar_dados_no_dw

# definimos as características da DAG aqui
with DAG(
    dag_id="pipeline_dados_indicium", # nome DAG -> pipeline_dados_indicium
    start_date=datetime(2025, 9, 11), # pode ser ser executada apartir dessa data
    schedule="35 4 * * *", # agendamento solicitado para 4:35 da manhã (expressao cron)
    catchup=False, # isso vai impedir que rode retroativo (DAG só olhará pro futuro)
    tags=["indicium", "dados"] # tag pra organizar a DAG na interface
) as dag:
    # cada bloco é a ação que a DAG executará
    tarefa_extracao_csv = PythonOperator(
        task_id="extrair_csv", # extração de CSV
        python_callable=extrair_e_salvar_csv #função Python
    )
    tarefa_extracao_sql = PythonOperator(
        task_id="extrair_sql", # extração de SQL
        python_callable=extrair_dados_do_sql #função Python
    )
    tarefa_carregamento_dw = PythonOperator(
        task_id="carregar_dados_dw", # carrega os dados no Data Warehouse
        python_callable=carregar_dados_no_dw #função Python
    )

    # definição do fluxo, ">>" significa "depende de", então só vai carregar os dados 
    # pro Data Warehouse quando as duas tarefas anteriores forem concluídas
    [tarefa_extracao_csv, tarefa_extracao_sql] >> tarefa_carregamento_dw