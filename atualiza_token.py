import requests

def Atualiza_Token():
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
        with open('token.txt', 'w') as arquivo:
            arquivo.write(token)
            arquivo.close()
    else:
        pass
        #print(f"Erro na solicitação HTTP. Código de status: {response.status_code}")
        #print(f"Resposta: {response.text}")



## criei a função que vai atualizar o token, falta a que faz de 60 em 60 minutos
