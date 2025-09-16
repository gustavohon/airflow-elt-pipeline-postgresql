
import pandas as pd
from pathlib import Path
from datetime import datetime
from sqlalchemy import create_engine # SQLAlchemy é ótimo para carregar DataFrames em bancos SQL

def carregar_dados_no_dw(**kwargs):
    print("Iniciando o carregamento dos dados para o Data Warehouse...")
    try:
        # caminho do projeto (necessário adicionar pasta raiz no docker-compose.yaml)
        caminho_projeto = Path('/opt/airflow/src/indicium-projeto')
        data_hoje = datetime.now().strftime('%Y-%m-%d')
        pasta_origem = caminho_projeto / 'output' / data_hoje

        # montamos um dicionário com o nome da tabela de destino e o caminho completo do arquivo de origem
        arquivos_para_carregar = {
            'agencias': pasta_origem / 'sql' / f'agencias_{data_hoje}.csv',
            'clientes': pasta_origem / 'sql' / f'clientes_{data_hoje}.csv',
            'colaboradores': pasta_origem / 'sql' / f'colaboradores_{data_hoje}.csv',
            'contas': pasta_origem / 'sql' / f'contas_{data_hoje}.csv',
            'transacoes': pasta_origem / 'csv' / f'transacoes_{data_hoje}.csv',
        }

        # conexão com novo banco de dados Data Warehouse (obs.: porta 5432)
        string_conexao_dw = "postgresql://dw_user:dw_password@postgres-dw:5432/data_warehouse"
        engine = create_engine(string_conexao_dw)
        print("Conexão com o Data Warehouse bem-sucedida!")

        # leitura do CSV e carregando pra dentro do banco de dados Data Warehouse
        for nome_tabela, caminho_arquivo in arquivos_para_carregar.items():
            print(f"Carregando dados do arquivo {caminho_arquivo.name} para a tabela '{nome_tabela}'...")

            df = pd.read_csv(caminho_arquivo, encoding='utf-8') # lemos em UTF-8 pra evitar os bugs de acentuação

            # O método .to_sql() do pandas serve para carregar os dados
            # if_exists='replace' é a chave para a idempotência solicitada no desafio: se rodarmos a DAG de novo
            # para o mesmo dia, os dados antigos serão apagados antes de inserir os novos, evitando dados duplicados
            # também usamos chunksize para contornar o bug que pandas tem de as vezes não conseguir apagar os tipos de dados associados a tabela antiga
            df.to_sql(nome_tabela, con=engine, if_exists='replace', index=False, chunksize=1000)
            print(f"Tabela '{nome_tabela}' carregada com sucesso.")

    except Exception as e:
        print(f"Ocorreu um erro durante o carregamento dos dados: {e}")
        raise e

    finally:
        print("\nCarregamento de dados para o Data Warehouse concluído!")