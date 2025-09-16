import pandas as pd # biblioteca pandas pra csv
from pathlib import Path
from datetime import datetime
import psycopg2 # tradutor para a linguagem do PostgreSQL

def extrair_dados_do_sql(**kwargs):
    print("Iniciando a extração dos dados do SQL...")

    try:
        # bloco de conexao ao banco de dados
        conn = psycopg2.connect(
            host="db",
            port="5432",
            dbname="banvic",
            user="data_engineer",
            password="v3rysecur&pas5w0rd"
        )
        print("Conexão com o banco de dados fonte bem-sucedida!")

        tabelas_para_extrair = ['agencias', 'clientes', 'colaboradores', 'contas']

        # preparando a pasta destino
    
        caminho_projeto = Path('/opt/airflow/src/indicium-projeto')
        data_hoje = datetime.now().strftime('%Y-%m-%d')
        caminho_destino_pasta = caminho_projeto / 'output' / data_hoje / 'sql'
        caminho_destino_pasta.mkdir(parents=True, exist_ok=True)
        
        # extraindo e salvando cada tabela da db
        for tabela in tabelas_para_extrair:
            print(f"Extraindo dados da tabela: {tabela}...")
            query = f"SELECT * FROM {tabela};"
            df = pd.read_sql_query(query, conn)

            nome_arquivo_destino = f'{tabela}_{data_hoje}.csv'
            caminho_arquivo_completo = caminho_destino_pasta / nome_arquivo_destino

            # garante UTF-8 para que não seja exibido caracteres incorretos quando tiver acentuação
            df.to_csv(caminho_arquivo_completo, index=False, encoding='utf-8')
            print(f"Tabela '{tabela}' salva com sucesso.")

    except Exception as e:
        print(f"Ocorreu um erro durante a extração do SQL: {e}")
        # lança o erro novamente para que o Airflow marque a tarefa como falha
        raise e

    finally:
        # sempre bom fechar a conexão com banco de dados quando não formos mais utilizar pra evitar vazamentos
        if 'conn' in locals() and conn is not None:
            conn.close()
            print("Conexão com o banco de dados fonte fechada.")

    print("\nExtração de todas as tabelas do SQL concluída!")