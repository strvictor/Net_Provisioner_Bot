import json
import requests
import datetime


def Valida_Contrato(num_contrato):
    id_do_cliente = None # esse id é oq vai me permitir fazer alterações em sua conexão no voalle
    id_cliente_cria_solicitacao = None 
    
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
            print(dados_corrigidos)
            for dados in dados_corrigidos['response']:
                
                id_cliente_cria_solicitacao = dados['client']['id'] # tem que retornar pra o app.py
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

                mensagem_formatada = f'''
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
'''
                return mensagem_formatada, id_do_cliente, id_cliente_cria_solicitacao
        
    else:
        # retorna falso, pra validar no arquivo app.py e chamar novamente a função
        return False, id_do_cliente, id_cliente_cria_solicitacao
    

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
        "complement": "", # descrição add via api
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
        return mensagem
    else:
        return f'{response.status_code}, {response.text}'
        

def Captura_Id_Cto(cto_informada):
    # esse id é o responsavel por escrever no voalle a cto correspondente

    with open('splitters.txt', 'r') as arquivo:
        base = arquivo.read()
        base_atualizada = json.loads(base)
        
        for cto_dados in base_atualizada['response']:
            id_cto_voalle = cto_dados['id'] 
            cto_ = cto_dados['networkBox']['title']
            tipo = cto_dados['type']['text']

                        
            if cto_informada in cto_ and tipo == 'Atendimento':
                print(tipo, id_cto_voalle)
                return id_cto_voalle
            
        arquivo.close()
        return 'id da cto não localizado'
    
    
def Cria_Solicitacao(id_tecnico, cto_em_destaque, cliente_antigo, cliente_novo, porta_da_cto, contrato, codigo_cliente):
    # Obtenha a data e hora atuais
    data_e_hora_atual = datetime.datetime.now()

    # Converta a data e hora em uma string formatada
    data_e_hora_formatada = data_e_hora_atual.strftime("%d-%m-%Y %H:%M:%S")

    mensagem = f"""📝 REGISTRO DE ALTERAÇÃO DE PORTA (GeoGrid) - PRO-BETA-bot \
Provisionamento efetuado pelo técnico ID = {id_tecnico}. Foi removido os seguinte dados da CTO: {cto_em_destaque}. Cliente: {cliente_antigo} da porta: {porta_da_cto}, na seguinte data: {data_e_hora_formatada}. Posteriormente foi adicionado o Cliente: \
{cliente_novo} na porta: {porta_da_cto} em {data_e_hora_formatada}."""
    
    # pega o token atualizado
    with open('token-api-external.txt', 'r') as arquivo:
        token = arquivo.readline()
        arquivo.close()
    
    url = "https://erp.gbsn.com.br:45715/external/integrations/thirdparty/opensolicitation"

    payload = {
        "description": mensagem,
        "clientId": codigo_cliente,
        "contractId": contrato,
        "contractServiceTagId":'',
        "close": True
    }

    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }

    response = requests.post(url, headers=headers, data=json.dumps(payload))

    if response.status_code == 200:
        resposta = json.loads(response.text)

        dados = resposta['response']

        status = dados['status']
        protocolo = dados['protocol']

        if status == 'OK':
            return f'✅ Alteração bem-sucedida! A alteração foi protocolada no sistema e recebeu o número de protocolo *{protocolo}*.'
        
    else:
        return f'erro na requisição: {response.text}, status: {response.status_code}'
