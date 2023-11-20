import requests, os
from dotenv import load_dotenv

# OBS: AS FUNÇÕES "Atualiza_Token_Mapas2" E "Atualiza_Token_External" NÃO POSSUEM UM METODO DE RENOVAÇÃO DE TOKEN, ENTÃO BASICAMENTE SE MUDAR A SENHA DE ACESSO AO ERP AS FUNÇÕES PARAM DE EXECUTAR

# importando as variaveis de ambiente
load_dotenv(override=True)
API_PASSWORD_MAPAS = os.getenv('API_KEY_PASSWORD_MAPAS_VOALLE')

API_SYNDATA = os.getenv('API_KEY_SYNDATA_VOALLE')

API_USUARIO = os.getenv('API_KEY_USUARIO_MAPAS_VOALLE')

API_CLIENTE_ID = os.getenv('API_KEY_CLIENTE_ID_EXTERNAL_VOALLE')

API_CLIENTE_SECRET = os.getenv('API_KEY_CLIENTE_SECRET_EXTERNAL_VOALLE')


def Atualiza_Token_Mapas2():
    url = "https://erp.gbsn.com.br:45700/connect/token"

    # Os dados de autenticação são fornecidos como um dicionário
    payload = {
        'grant_type': 'password',
        'scope': 'syngw',
        'client_id': 'synauth',
        'client_secret': 'df956154024a425eb80f1a2fc12fef0c',
        'username': API_USUARIO,
        'password': API_PASSWORD_MAPAS,
        'syndata': API_SYNDATA
    }

    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    response = requests.post(url, headers=headers, data=payload)
    #print(response.text)
    # Verifica se a solicitação foi bem-sucedida (código de status 200)
    if response.status_code == 200:
        # Conteúdo da resposta (dados retornados pela API)
        dados_resposta = response.json()

        token = dados_resposta['access_token']
        # gravando o token no .txt
        with open('token-api-mapas-2.txt', 'w') as arquivo:
            arquivo.write(token)
            arquivo.close()
    else:
        print(f"{response.text} - ERRO AO RENOVAR O TOKEN, FUNÇÃO: Atualiza_Token_Mapas2")
        


def Atualiza_Token_External():
    url = "https://erp.gbsn.com.br:45700/connect/token"

    payload = {
        'grant_type': 'client_credentials',
        'scope': 'syngw',
        'client_id': API_CLIENTE_ID,
        'client_secret': API_CLIENTE_SECRET, 
        'syndata': API_SYNDATA

    }

    response = requests.post(url, data=payload)

    if response.status_code == 200:
        dados = response.json()
        
        token = dados['access_token']
         # gravando o token no .txt
        with open('token-api-external.txt', 'w') as arquivo:
            arquivo.write(token)
            arquivo.close()
    else:
        print(f"{response.text} - ERRO AO RENOVAR O TOKEN, FUNÇÃO: Atualiza_Token_External")