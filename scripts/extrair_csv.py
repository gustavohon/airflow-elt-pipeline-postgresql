import pandas as pd # biblioteca pandas pro csv
from pathlib import Path
from datetime import datetime

def extrair_e_salvar_csv(**kwargs):
    print("Iniciando a extração do arquivo CSV...")

    # caminho do projeto (necessário adicionar pasta raiz no docker-compose.yaml)
    caminho_projeto = Path('/opt/airflow/src/indicium-projeto')

    # montamos o caminho completo para o arquivo de origem e a pasta de destino
    caminho_origem = caminho_projeto / 'data' / 'transacoes.csv'
    data_hoje = datetime.now().strftime('%Y-%m-%d') # data
    caminho_destino_pasta = caminho_projeto / 'output' / data_hoje / 'csv'

    # garantimos que a pasta de destino exista antes de tentar salvar o arquivo
    caminho_destino_pasta.mkdir(parents=True, exist_ok=True)

    # forçamos a leitura em UTF-8 para evitar bugs com acentos
    dataframe_transacoes = pd.read_csv(caminho_origem, encoding='utf-8')

    # arquivo de transacoes.csv fornecido pelo desafio
    nome_arquivo_destino = f'transacoes_{data_hoje}.csv'
    caminho_arquivo_completo = caminho_destino_pasta / nome_arquivo_destino

    # salvamos o novo arquivo, também forçando a escrita em UTF-8
    dataframe_transacoes.to_csv(caminho_arquivo_completo, index=False, encoding='utf-8')

    print(f"Arquivo salvo com sucesso em: {caminho_arquivo_completo}")
    print("Extração do CSV concluída!")