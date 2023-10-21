import requests
import json
import random


def portas_livres(item_rede, porta_informarda, contrato, pppoe):
    encontrou = False
    url = f"https://ares.geogridmaps.com.br/norte/api/v3/viabilidade/{item_rede}/portas"
    headers = {
        "Accept": "application/json",
        "api-key": "9e782fbf03f7c6dec8c41ccae792a036e428f5ee"
    }

    params = {
        "pagina": "1",
        "registrosPorPagina": "10",
        "modoProjeto": "S,n",
        "equipamentosAtendimento": "s,n",
        "tipo": "e,s",
        "disponivel": "S"
    }

    response = requests.get(url, headers=headers, params=params)

    lista_portas = []

    if response.status_code == 200:
        data = response.json()
        
        registros = data['registros']
        
        for dado in registros:
            dados = dado['dados']
            disponibilidade = dado['disponivel']
            
            id_porta = dados['id']
            porta = dados['porta']
            integrador = random.randint(1000, 2000)
            print(integrador)
            
            if disponibilidade:
                lista_portas.append(porta)
            
                if int(porta_informarda) == int(porta):
                    encontrou = True
                    
                    print(f"Id da porta: {id_porta}\nPorta disponível: {porta}\nDisponibilidade: {disponibilidade}\n")
                    # realizando o cadastro
                    resposta = Cadastro_Cliente(contrato, pppoe, integrador)
                    print(resposta)
                    
                    if resposta == 'Código de integração já está cadastrado':
                        resposta = Cadastro_Cliente(contrato, pppoe, integrador)
                        print(resposta)
                        atende_cliente = Atende_Cliente(id_porta, resposta, item_rede)
                        
                        if len(atende_cliente) == 2:
                            # cliente castrado no geogrid com sucesso
                            return 'cliente vinculado no geogrid com sucesso'
                        
                        return atende_cliente
                        
                    else:
                        # upando o cliente para o geogrid
                        atende_cliente = Atende_Cliente(id_porta, resposta, item_rede)
                        if len(atende_cliente) == 2:
                            # cliente castrado no geogrid com sucesso
                            return 'cliente vinculado no geogrid com sucesso'
                        
                        return atende_cliente
                    
        if encontrou is False:
            return f'porta ocupada para uso'
            
        
    else:
        return "Erro na requisição:", response.status_code



def Cadastro_Cliente(contrato, pppoe, integracao):
    usuario = str(contrato) + '.' + str(pppoe)

    url = "https://ares.geogridmaps.com.br/norte/api/v3/clientes"
    headers = {
        'Accept': 'application/json',
        'api-key': '9e782fbf03f7c6dec8c41ccae792a036e428f5ee',
        'Content-Type': 'application/json'
    }

    data = {
    "dados": {
        "nome": usuario,
        "cpfCnpj": "",
        "tipo": "F",
        "rg": "",
        "email": "",
        "telefone": "",
        "celular": "",
        "cep": "",
        "endereco": "",
        "bairro": "",
        "cidade": "",
        "estado": "PA",
        "observacao": "usuario criado via API - @strvictor",
        "nascimento": "2010-05-23",
        "nomeFantasia": usuario,
        "inscricaoEstadual": "",
        "codigoIntegracao": integracao
    }
    }

    response = requests.post(url, headers=headers, json=data)

    dados = json.loads(response.text)
    #print(dados)

    try:
        id_cliente = dados['dados']['id']
            
        return id_cliente
    
    except:
        try:
            if dados['codigoIntegracao'] == 'Código de integração já está cadastrado':
                return 'Código de integração já está cadastrado'
        except:
            pass
        




def Atende_Cliente(id_porta, id_cliente, item_rede):

    url = "https://ares.geogridmaps.com.br/norte/api/v3/integracao/atender"
    headers = {
        'Accept': 'application/json',
        'api-key': '9e782fbf03f7c6dec8c41ccae792a036e428f5ee',
        'Content-Type': 'application/json'
    }

    data = {
        "idPorta": id_porta,
        "idCliente": id_cliente,
        "local": {
            "latitude": "",
            "longitude": "-",
            "idItemRedeCliente": item_rede
        },
        "idCaboTipo": 5,
        "pontos": [
            {
                "latitude": "",
                "longitude": ""
            }
        ]
    }

    response = requests.post(url, headers=headers, json=data)

    return  response.text


def Forca_Integracao(item_de_rede, porta_informada):
    pass