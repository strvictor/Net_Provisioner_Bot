import telnetlib, re, time

modelos_de_ativacao = {
    "110Gb": "intelbras-110b",
    "121AC": "intelbras-121ac",
    "R1v2": "intelbras-r1",
    "110Gi": "intelbras-110",
    "R1": "intelbras-r1"
} 


def busca_onu_na_pon(ponto_de_acesso, pon):

    onus_discando = []
    lista = []
    dicionario = {}
    chave_atual = None
    
    if ponto_de_acesso == 'alca':
        ip = '172.31.0.21'

    elif ponto_de_acesso == 'jamic':
        ip = '10.9.250.6'

    HOST = str(ip)  # Endereço do dispositivo Telnet
    PORT = 23  # Porta Telnet padrão

    # Obter nome de usuário e senha do usuário
    username = 'admin'
    password = 'admin'

    # Criar objeto Telnet e conectar ao dispositivo
    tn = telnetlib.Telnet(HOST, PORT)

    # Fazer login
    tn.read_until(b"olt8820plus login: ")
    tn.write(username.encode('ascii') + b"\n")
    if password:
        tn.read_until(b"Password: ")
        tn.write(password.encode('ascii') + b"\n")
        time.sleep(1)  # Aguardar um segundo após enviar a senha

    comando = f"onu show gpon {pon}"

    tn.write(f"{comando}\n".encode('ascii'))

    # Aguardar a resposta
    time.sleep(1)

    # Ler a resposta até encontrar o prompt novamente
    resultado = tn.read_until(b"olt8820plus login:", timeout=5).decode('ascii')

    # Fechar a conexão Telnet
    tn.close()

    linhas = resultado.splitlines()


    inicio_filtro = linhas.index(f'intelbras-olt> {comando}')
    linhas = linhas[inicio_filtro:]



 #######################################################################

    for linha in linhas:
        if 'ITBS' in linha:
            linha_onu = linha.split()
            # adiciona na lista as onus discando
            onus_discando.append(linha_onu)

        # Encontrar os números em cada linha
        numeros = re.findall(r'\d+', linha)
        # Verificar se existem números na linha
        if numeros:
            if len(numeros) == 1:
                numeros = f'PON {numeros}'.replace("'", '').replace('[', '').replace(']', '').strip()
                # adiciona na lista a pon atual
                lista.append(numeros)

            else:
                for numero in numeros:
                    # adiciona na lista as posições disponiveis de todas as pons
                    lista.append(numero)

    #converte para dicionario (facilita pegar os valores)
    for item in lista:

        #verifica se começa com pon (que é o divisor)
        if item.startswith("PON"):
            chave_atual = item
            #cria a chave com a pon correspondente
            dicionario[chave_atual] = []

        else:
            # adiciona as posições à pon correspondente no dicionario
            dicionario[chave_atual].append(item)

    # percore o dicionario e exibe as informações
    for pon_, posicao in dicionario.items():

        # posição disponivel pra onu na pon
        posicao_disponivel_na_pon = posicao[0]



    if len(onus_discando) == 0:
        return 'sem onu discando nessa pon' 
    
    elif len(onus_discando) == 1:

        onus_discando = onus_discando[0]

        id_onu = onus_discando[0]
        fabricante = onus_discando[1]
        serial = onus_discando[2]
        modelo = onus_discando[3]

        if modelo in modelos_de_ativacao:
            modelo_permitido = modelos_de_ativacao[modelo]

        else:
            modelo_permitido = modelos_de_ativacao['R1v2']  

#        return f'''
#*PROVISIONAMENTO PREENCHIDO*

#📌 *Índice:* 01
#🔍 *Serial:* {fabricante}{serial}
#💡 *Modelo:* {modelo}

#'''    
        return fabricante, serial, modelo, modelo_permitido, posicao_disponivel_na_pon, pon

    else:
        # tem mais de uma onu discando
        for i, onu in enumerate(onus_discando):

            print(f'{i + 1}_ escolha a sua onu {onu[1:3]}')
            #return f'{i}_ escolha a onu {onu}'

        escolha = int(input("> "))

        # verifica se oq o cara escolheu ta certo
        if escolha <= 0 or escolha > len(onus_discando):
            return 'não existe esse indice'
                                 
        
        onus_discando = onus_discando[escolha - 1]

        id_onu = onus_discando[0]
        fabricante = onus_discando[1]
        serial = onus_discando[2]
        modelo = onus_discando[3]

        if modelo in modelos_de_ativacao:
            modelo_permitido = modelos_de_ativacao[modelo]  

        else:
            modelo_permitido = modelos_de_ativacao['R1v2'] 
    
        return f'''onu {escolha} selecionada
{id_onu}
{fabricante}
{serial}
{modelo}
{modelo_permitido}
    '''








def provisiona_olt(ponto_de_acesso, pon):
    pass


