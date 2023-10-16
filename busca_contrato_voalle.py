
import requests
import json

def Busca_info_contrato(contrato):
    
    #atualiza_token.Atualiza_Token()
    valida_numero = str(contrato).isdigit()
    if valida_numero is False:
        return 'Digite apenas numeros, por favor'
    
    url = "https://erp-staging.gbsn.com.br:45701/api/v1/isp/connection/integration/by/userdata"

    # pega o token atualizado
    with open('token.txt', 'r') as arquivo:
        token = arquivo.readline()
        arquivo.close()
        
    # Dados ajustados
    dados = {
        "contractIds": [f'{contrato}']
    }

    # Converter os dados em formato JSON
    dados_json = json.dumps(dados)

    # Definir cabeçalhos
    headers = {
        'Authorization': f'Bearer {token}',  # Certifique-se de adicionar seu token aqui
        
        'accept': 'application/json',
        'Content-Type': 'application/json'
    }

    # Realizar a requisição POST
    dados = requests.post(url, headers=headers, data=dados_json)

    # Imprimir a resposta
    dados_corrigidos = json.loads(dados.text)

    # verifica se tem resposta de contrato 
    if len(dados_corrigidos['response']) == 0:
        return 'Contrato não localizado!'
    else:
        
        for dados in dados_corrigidos['response']:
            
            contrato_cliente = contrato
            nome_cliente = dados['client']['name'].title()
            cpf_cliente =  dados['client']['txId']
            ponto_de_acesso = dados['authenticationAccessPoint']['title']
            cidade = dados['address']['city']
            bairro = dados['address']['neighborhood'].title()
            rua = dados['address']['street'].title()
            numero_casa = dados['address']['number']
            pppoe = dados['user']
            senha_pppoe = 112233

            return f"""
CONTRATO: {contrato_cliente}                  
NOME: {nome_cliente}     
CPF: {cpf_cliente}      
PONTO DE ACESSO: {ponto_de_acesso}       
CIDADE: {cidade}
BAIRRO: {bairro}
RUA: {rua}
NUMERO: {numero_casa}
PPPOE: {pppoe}                   
SENHA: {senha_pppoe} 
"""
    
# dados = Busca_info_contrato('9996')

# print(dados)