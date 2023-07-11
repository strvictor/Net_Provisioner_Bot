import telnetlib, re, time

def busca_onu_na_pon(ponto_de_acesso, pon):

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

    linhas = resultado.splitlines()

    if f'intelbras-olt> {comando}' not in  linhas:str
        print(f'{comando} não encontrado')
        busca_onu_na_pon(ponto_de_acesso, pon)

    else:

        inicio_filtro = linhas.index(f'intelbras-olt> {comando}')
        filtrado = linhas[inicio_filtro:]

        formatado = formata_retorno(filtrado)
        print(formatado)

    tn.close()



def formata_retorno(linhas):
    onus_discando = []
    lista = []
    dicionario = {}
    chave_atual = None

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
        if posicao:
            return 'posição:', posicao[0] 
        else:
            print('fui chamado')
            busca_onu_na_pon('alca', '6')

busca_onu_na_pon('alca', '6')













def busca_onu_na_pon(ponto_de_acesso):
    
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

    comando_1 = 'onu set gpon 2 onu 10 serial-number ITBS3246A9DC meprof intelbras-110b'
    comando_2 = 'bridge add gpon 2 onu 10 downlink vlan 501 tagged eth 1'
    comando_3 = 'onu description add gpon 2 onu 10 text primeira.ativacao.bot'
    


    tn.write(f"{comando_1}\n".encode('ascii'))

    # Aguardar a resposta
    time.sleep(2)

    # Ler a resposta até encontrar o prompt novamente
    resultado = tn.read_until(b"olt8820plus login:", timeout=5).decode('ascii')

    print(resultado)

    tn.write(f"{comando_2}\n".encode('ascii'))

    # Aguardar a resposta
    time.sleep(2)

    # Ler a resposta até encontrar o prompt novamente
    resultado = tn.read_until(b"olt8820plus login:", timeout=5).decode('ascii')

    print(resultado)

    tn.write(f"{comando_3}\n".encode('ascii'))

    # Aguardar a resposta
    time.sleep(2)

    # Ler a resposta até encontrar o prompt novamente
    resultado = tn.read_until(b"olt8820plus login:", timeout=5).decode('ascii')

    print(resultado)


    # Fechar a conexão Telnet
    tn.close()



