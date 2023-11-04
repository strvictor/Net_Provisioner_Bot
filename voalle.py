import json
import requests


def validacontrato(num_contrato):
    id_do_cliente = None # esse id é oq vai me permitir fazer alterações em sua conexão no voalle
    
    # verifica se o contrato tem somente numeros
    valida_numero = str(num_contrato).isnumeric()
    if valida_numero:
        url = "https://erp.gbsn.com.br:45701/api/v1/isp/connection/integration/by/userdata"

        # pega o token atualizado
        with open('token-api-mapas-2.txt', 'r') as arquivo:
            token = arquivo.readline()
            arquivo.close()
            
        # Dados ajustados
        dados = {
            "contractIds": [f'{num_contrato}']
        }

        # Converter os dados em formato JSON
        dados_json = json.dumps(dados)

        # Definir cabeçalhos
        headers = {
            'Authorization': f'Bearer {token}',  # Certifique-se de adicionar seu token aqui
            
            'accept': 'application/json',
            'Content-Type': 'application/json'
        }

        #bloqueei a requisição de momento
        dados = requests.post(url, headers=headers, data=dados_json)
        
        dados_corrigidos = json.loads(dados.text)

        # verifica se tem resposta de contrato 
        if len(dados_corrigidos['response']) == 0:
            return 'contrato não localizado', id_do_cliente
        else:
            
            for dados in dados_corrigidos['response']:
                
                id_do_cliente = dados['id']
                contrato_cliente = num_contrato
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
ℹ️  DADOS DO CLIENTE ℹ️          
            
📄 CONTRATO: {contrato_cliente}               
👤 NOME: {nome_cliente}   
🆔 CPF/CNPJ: {cpf_cliente}      
🌐 PONTO DE ACESSO: {ponto_de_acesso}       
🏙️ CIDADE: {cidade}
🏡 BAIRRO: {bairro}
🛣️ RUA: {rua}
🏠 NUMERO: {numero_casa}
💻 PPPOE: {pppoe}                   
🔐 SENHA: {senha_pppoe} 
""", id_do_cliente
        
    else:
        # retorna falso, pra validar no arquivo app.py e chamar novamente a função
        return False, id_do_cliente
    


def Atualiza_Conexao(id_cliente, id_olt, serial_gpon, id_cto, porta_cto):
    
    url = f"https://erp.gbsn.com.br:45715/external/integrations/thirdparty/updateconnection/{id_cliente}"

    # pega o token atualizado
    with open('token-api-external.txt', 'r') as arquivo:
        token = arquivo.readline()
        arquivo.close()

    payload = {
        "id": id_cliente,
        "fiberMac": " ",
        "mac": " ",
        "password": "112233",
        "equipmentType": 5, # Huawei
        "oltId": id_olt,
        "slotOlt": 0,
        "portOlt": 0,
        "equipmentSerialNumber": serial_gpon,
        "ipType": 1, # ip fixo
        "equipmentUser": " ",
        "equipmentPassword": "GbsNet9009",
        "authenticationSplitterId": id_cto, # CTO
        "port": porta_cto, # PORTA
        "wifiName": " ",
        "wifiPassword": " ",
        "technologyType": None, #  Conforme Ponto de Acesso
        "authenticationAccessPointId": 0,
        "updateConnectionParameter": True,
        "shouldMacUpdate": True,
        "user": "", # teste.update.conexao
        "complement": "descrição add via api",
        "isIPoE": False
    }

    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }

    response = requests.put(url, headers=headers, data=json.dumps(payload))

    if response.status_code == 200:
        mensagem = json.loads(response.text)
        mensagem = mensagem['dataResponseType']
        print(mensagem)
    else:
        print(response.status_code, response.text)
        
        
Atualiza_Conexao(24553, 10, 'serial gpon', 1221, 4)