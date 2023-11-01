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
        pass
        #print(f"Erro na solicitação HTTP. Código de status: {response.status_code}")
        #print(f"Resposta: {response.text}")





token_antigo = '''eyJhbGciOiJSUzI1NiIsImtpZCI6IjBBRjZDREEyRDU0MTRDRTY1MUM0RTk3NTM3QTFGNEY0QTMyNUQ5QTMiLCJ0eXAiOiJKV1QiLCJ4NXQiOiJDdmJOb3RWQlRPWlJ4T2wxTjZIMDlLTWwyYU0ifQ.eyJuYmYiOjE2OTg4NjgwNzksImV4cCI6MTY5ODg3MTY3OSwiaXNzIjoiaHR0cHM6Ly9lcnAuZ2Jzbi5jb20uYnI6NDU3MDAiLCJhdWQiOlsiaHR0cHM6Ly9lcnAuZ2Jzbi5jb20uYnI6NDU3MDAvcmVzb3VyY2VzIiwic3luZ3ciXSwiY2xpZW50X2lkIjoiNWFjZDcyNzktMmU3OS0yNzg4LWIwMzAtMjQxNDFjMmEwZTQwIiwiaWQiOiIyNDQiLCJsb2dpbiI6Imdicy5pbnRlZ3JhY2FvIiwibW9kZSI6InN5c3RlbSIsIm5hbWUiOiJOT1JURSBURUxFQ09NVU5JQ0FDT0VTIFNFUlZJQ09TIERFIElOVEVSTkVUIExUREEiLCJwZXJzb25lbWFpbCI6ImZpbmFuY2Vpcm9AZ2JuLmNvbS5iciIsInBlcnNvbmlkIjoiMSIsInBlcnNvbm5hbWUiOiJOT1JURSBURUxFQ09NVU5JQ0FDT0VTIFNFUlZJQ09TIERFIElOVEVSTkVUIExUREEiLCJwbGFjZWlkIjoiMSIsInByb2ZpbGVpZCI6IjIyIiwic3luZGF0YSI6IlRXcE5NVTlFWXpWYWFrazFUMGRTYVUxVVNteGFhbHByV2xkRmQwMHlTVEZaVjFKc1RUSlJNRnB0VVQwNldsaHNTMVpIVmxoT1ZXeHBUVEEwZDFOWGNIWmhWVEZWV1hwT1RXRnJWak5VYTAwd1pWVTFWVlJZVms1aGF6RTFVMWRzTTJGV1ZYcGlTRlpUVWpCc2NGUXliRXRoTVd4MFZtNVNhbEpGUmpOVWJGSlNaV3RzZFUxRU1EMDZXbFJvYTAxcVRURlphbXN3V1hwc2FVNUVUbTFhUkdjelRVUnNhMDFxV1RKWmVrRjRUVWROTTAxSFZUMD0iLCJ0eGlkIjoiMDg5NjgwNzIwMDAxMzkiLCJ0eXBldHhpZCI6IjEiLCJsaXZlY2hhdGFnZW50IjoiRmFsc2UiLCJ0eXBlIjoiaW50ZWdyYXRpb24iLCJpbnRlZ3JhdGlvbiI6InRoaXJkcGFydHkiLCJzdWIiOiJnYnMuaW50ZWdyYWNhbyIsInNjb3BlIjpbInN5bmd3Il19.R_ck2wd5vZJsEuIC0R3iOHHpp09An0PJxRsijwGtGmlFSNAeawiYSESb67Vhg61cWnBjpp2sxlXJOMh6BHqqsfmUe3ODoxA9K5znZSWRFjT--rXWjqYr3FYs0Ur8826v9fbaSdyZqxTGiHhufPYU-0dTFgo2-VUkuC9qW9SA6OI-jDuBv-yPeW51B3leIWt8e4Ndvh72jGx3bW6KkmaVZ2dvr5O05OLL-bWZZ2rD_Cp2SBQPQk79Hpud7ifDbVYA_q9ED7jqdqCFUATI1LETYBGGYpHNXpqI4M4xuP1zR47Ru4duZ6IBWBd0EJxSyos1qFPQa-KujcLAx_AsNZmm_F4wSfb4GNacZo_EjQB8Narv3X55f9LVnrC22CjLWVxMYaH4aQx0A6ob8Xnn8xdvX5F-7FkZiLDHyh2zqmFmSqbEvNFoFbM8dRWgCFTd2sAJRE-GSp7LaZfuto8P6ko2CDlt8Gcir3UzmR2I5xEEpskYAS7lrFEU26AzocA31eKe-9c1qxGgVYBhcAvvEssya82kBLErjkq7Ty4iQVxuXf1EwAvHe8MX23s3wsTKMs847YaW2HQ2BItDRXO4UN7BnCwN0KG1BQjM8yd9n1w3CtnfcSE8Dob6ctOje3wHe_rjdipyrhDxhH5772PFQ6x4UqhtxlDBV-R5Xnd_txi1Kf8'''


def Atualiza_Token_External(token_antigo):
    url = "https://erp.gbsn.com.br:45700/connect/token"

    payload = {
        'grant_type': 'refresh_token',
        'client_id': 'synauth',
        'client_secret': 'df956154024a425eb80f1a2fc12fef0c',
        'refresh_token': f'Baerer {token_antigo}'
    }

    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
}

    response = requests.post(url, data=payload, headers=headers)

    print(response.text)


# Atualiza_Token_External(token_antigo)