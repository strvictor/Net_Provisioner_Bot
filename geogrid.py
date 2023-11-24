import requests, random, os, json
from dotenv import load_dotenv


load_dotenv(override=True)
API_GEOGRID = os.getenv('API_KEY_GEOGRID')

dados_cliente_removido = list()

def Portas_Livres(item_rede, porta_informarda, contrato, pppoe):
    
    encontrou = False
    url = f"https://ares.geogridmaps.com.br/norte/api/v3/viabilidade/{item_rede}/portas"
    headers = {
        "Accept": "application/json",
        "api-key": API_GEOGRID
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
    lista_portas.clear()

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
                            
                            if len(dados_cliente_removido) > 1:
                                
                                copia_lista_temp = list(dados_cliente_removido)
                                
                                usuario_cliente_removido = copia_lista_temp[0]
                                porta_cliente_removido = copia_lista_temp[1]
                                mensagem_geogrid = 'cliente vinculado no geogrid com sucesso'
                                
                                dados_cliente_removido.clear()
                                
                                return mensagem_geogrid, usuario_cliente_removido, porta_cliente_removido
                            
                            else:
                                return 'cliente vinculado no geogrid com sucesso'
                        
                        return atende_cliente
                        
                    else:
                        # upando o cliente para o geogrid
                        atende_cliente = Atende_Cliente(id_porta, resposta, item_rede)
                        if len(atende_cliente) == 2:
                            # cliente castrado no geogrid com sucesso

                            if len(dados_cliente_removido) > 1:
                                
                                copia_lista_temp = list(dados_cliente_removido)
                                
                                usuario_cliente_removido = copia_lista_temp[0]
                                porta_cliente_removido = copia_lista_temp[1]
                                mensagem_geogrid = 'cliente vinculado no geogrid com sucesso'
                                
                                dados_cliente_removido.clear()
                                
                                return mensagem_geogrid, usuario_cliente_removido, porta_cliente_removido
                            
                            else:
                                return 'cliente vinculado no geogrid com sucesso'
                        
                        return atende_cliente
                    
                    
        if encontrou is False:
            return 'porta ocupada para uso'
            
    else:
        print(f"Erro na requisição: {response.status_code}, {response.text}")
        # retornando o codigo http, pra verificar no app.py e seguir normal
        return response.status_code


def Cadastro_Cliente(contrato, pppoe, integracao):
    usuario = str(contrato) + '.' + str(pppoe)

    url = "https://ares.geogridmaps.com.br/norte/api/v3/clientes"
    headers = {
        'Accept': 'application/json',
        'api-key': API_GEOGRID,
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
        'api-key': API_GEOGRID,
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

    return response.text


def Forca_Integracao(item_rede, porta_informada, contrato, pppoe):

    url = f"https://ares.geogridmaps.com.br/norte/api/v3/equipamentos/itemRede/{item_rede}/portas"

    params = {
        'atendimento[]': 'S',
        'modoProjeto[]': ['S', 'N'],
        'tipo[]': ['S', 'E'],
        'disponivel': 'N'
    }

    headers = {
        'Accept': 'application/json',
        'api-key': API_GEOGRID
    }

    response = requests.get(url, params=params, headers=headers)

    if response.status_code == 200:
        dados = response.json()
    
        registros = dados['registros'][0]['portas']

        for i, dado in enumerate(registros):
            if i == 0:
                pass
            
            else:
                try:
                    id_porta = dado['dados']['id']
                    porta = dado['dados']['porta']
                    id_cliente = dado['cliente']['id']
                    nome_cliente = dado['cliente']['nome']
                    
                    if int(porta_informada) == int(porta):
                        print(f'Cliente removido: {nome_cliente}\nPorta cedida: {porta}')
                        dados_cliente_removido.clear()
                        dados_cliente_removido.append(nome_cliente)
                        dados_cliente_removido.append(porta)
                        
                        remove = Remove_Cliente(item_rede, id_porta, id_cliente)
                        
                        # adiciona o cliente
                        if len(remove) == 2:
                            atualiza = Portas_Livres(item_rede, porta_informada, contrato, pppoe)
                            return atualiza
                        
                        return remove

                except:
                    continue
    else:
        return f"Erro na requisição. Código de status: {response.status_code} {response.text}"
        

def Remove_Cliente(item_rede, id_porta, id_cliente):
    url = f"https://ares.geogridmaps.com.br/norte/api/v3/integracao/atender/{id_porta}/{id_cliente}"

    headers = {
        'Accept': 'application/json',
        'api-key': API_GEOGRID
    }

    response = requests.delete(url, headers=headers)

    if response.status_code == 200:
        print(f'remove cliente sucesso {response.text}')
        return response.text
    else:
        retorno = json.loads(response.text)
        print(f'remove cliente falha {retorno}')
        
        if retorno['portaReservada'] == 'A porta está reservada':
            
            print('a porta esta reservada, mas irei atender pra remover depois')
            atende_reservado = Atende_Cliente(id_porta, id_cliente, item_rede)
            print('tentativa de atender o reservado: ', atende_reservado)
            
            remove_cliente_que_foi_atendido = Remove_Cliente(item_rede, id_porta, id_cliente)
            
            return remove_cliente_que_foi_atendido
            
            #return '😕 Infelizmente a porta está *reservada*, dessa forma não consegui remover o usuario antigo'
        return retorno
