import requests

def Atualiza_Token_Mapas2():
    url = "https://erp.gbsn.com.br:45700/connect/token"

    # Os dados de autenticação são fornecidos como um dicionário
    payload = {
        'grant_type': 'password',
        'scope': 'syngw',
        'client_id': 'synauth',
        'client_secret': 'df956154024a425eb80f1a2fc12fef0c',
        'username': 'gewerton',  
        'password': '3890328eb03aff62b0a36cdff5a4e61aacb1a3f2',   
        'syndata': 'TWpNMU9EYzVaakk1T0dSaU1USmxaalprWldFd00ySTFZV1JsTTJRMFptUT06WlhsS1ZHVlhOVWxpTTA0d1NXcHZhVTFVWXpOTWFrVjNUa00wZVU1VVRYVk5hazE1U1dsM2FWVXpiSFZTUjBscFQybEthMWx0Vm5SalJFRjNUbFJSZWtscGQybFNSMHBWWlZoQ2JFbHFiMmxqUnpsNlpFZGtlVnBZVFdsbVVUMDk6WlRoa01qTTFZamswWXpsaU5ETm1aRGczTURsa01qWTJZekF4TUdNM01HVT0='
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
        'client_id': '5acd7279-2e79-2788-b030-24141c2a0e40',
        'client_secret': '973ff5d6-a10a-0d23-62c2-5c2957986592',
        'syndata': 'TWpNMU9EYzVaakk1T0dSaU1USmxaalprWldFd00ySTFZV1JsTTJRMFptUT06WlhsS1ZHVlhOVWxpTTA0d1NXcHZhVTFVWXpOTWFrVjNUa00wZVU1VVRYVk5hazE1U1dsM2FWVXpiSFZTUjBscFQybEthMWx0Vm5SalJFRjNUbFJSZWtscGQybFNSMHBWWlZoQ2JFbHFiMmxqUnpsNlpFZGtlVnBZVFdsbVVUMDk6WlRoa01qTTFZamswWXpsaU5ETm1aRGczTURsa01qWTJZekF4TUdNM01HVT0='

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

