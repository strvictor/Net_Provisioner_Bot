import requests

def Atualiza_Token():
    url = "https://erp-staging.gbsn.com.br:45700/connect/token"

    # Os dados de autenticação são fornecidos como um dicionário
    payload = {
        'grant_type': 'password',
        'scope': 'syngw',
        'client_id': 'synauth',
        'client_secret': 'df956154024a425eb80f1a2fc12fef0c',
        'username': 'gewerton',  # Substitua com o nome de usuário real
        'password': '0c1f99a81796bcf36874a72f1fb53c1f55690a5c',    # Substitua com a senha real
        'syndata': 'TWpNMU9EYzVaakk1T0dSaU1USmxaalprWldFd00ySTFZV1JsTTJRMFptUT06WlhsS1ZHVlhOVWxpTTA0d1NXcHZhVnBZU25kTVdFNHdXVmRrY0dKdFkzVmFNa3A2WW1rMWFtSXlNSFZaYmtscFRFTktWR1ZYTlVWWmFVazJTVzFTYVZwWE1YZE5SRUV4VGtST1ptTXpVbWhhTW14MVdubEpjMGxyVW1sV1NHeDNXbE5KTmtsdVFuWmpNMUp1WTIxV2VrbHVNRDA9OlpUaGtNak0xWWprMFl6bGlORE5tWkRnM01EbGtNalkyWXpBeE1HTTNNR1U9'
    }

    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    response = requests.post(url, headers=headers, data=payload)

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