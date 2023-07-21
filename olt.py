import telnetlib
import re
import time

resultado_final = []
modelos_de_ativacao = {
    "110Gb": "intelbras-110b",
    "121AC": "intelbras-121ac",
    "120AC": "intelbras-121ac",
    "R1v2": "intelbras-r1",
    "110Gi": "intelbras-110",
    "R1": "intelbras-r1",
    "padrao": "intelbras-default"
} 

opcoes_velocidade = {
    "00": "Desativada",
    "21": "10 Mbps Half-Duplex",
    "11": "10 Mbps Full-Duplex",
    "22": "100 Mbps Half-Duplex",
    "12": "100 Mbps Full-Duplex",
    "23": "1 Gbps Half-Duplex",
    "13": "1 Gbps Full-Duplex"
}

def busca_onu_na_pon(ponto_de_acesso, pon):
    try:
        if ponto_de_acesso == 'alca':
            ip = '172.31.0.21'
        elif ponto_de_acesso == 'jamic':
            ip = '10.9.250.6'
        elif ponto_de_acesso == 'bujaru':
            ip = '10.7.250.10'
        elif ponto_de_acesso == 'local':
            ip = '10.9.250.10'

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
        tn.close()

        if f'intelbras-olt> {comando}' not in linhas:
            inicio_filtro = linhas.index(f'Free slots in GPON Link {pon}:')
            filtrado = linhas[inicio_filtro:]
            return formata_retorno(filtrado, pon, ponto_de_acesso)
        else:
            inicio_filtro2 = linhas.index(f'intelbras-olt> {comando}')
            filtrado2 = linhas[inicio_filtro2:]
            return formata_retorno(filtrado2, pon, ponto_de_acesso)
        
    except Exception as e:
        print('erro na consulta:', str(e))


def formata_retorno(linhas, pon, ponto_de_acesso):
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

    temporario = list()
    # percore o dicionario e exibe as informações
    for pon_, posicao in dicionario.items():

        # posição disponivel pra onu na pon
        if posicao:
            #print(f'posição: {posicao[0]}')
            temporario.append(posicao[0])
        else:
            #print('fui chamado')
            return busca_onu_na_pon(ponto_de_acesso, pon)

    #print('exibe info chamada')
    return exibe_info(onus_discando, temporario[0], pon, ponto_de_acesso)


def exibe_info(onus_discando, posicao, pon, ponto_de_acesso):

    if len(onus_discando) == 0:
        return False
    
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
            modelo = 'modelo não encontrado'

        return fabricante, serial, modelo, modelo_permitido, posicao, pon, ponto_de_acesso

    else:
        for onu in onus_discando:
            modelo = onu[3]

            if modelo in modelos_de_ativacao:
                modelo_permitido = modelos_de_ativacao[modelo]  
                onu.append(modelo_permitido)
                
            else:
                modelo_permitido = modelos_de_ativacao['padrao']
                onu.append(modelo_permitido) 
                
        return onus_discando, posicao, pon, ponto_de_acesso, len(onus_discando)


def provisiona(gpon, vaga_onu, gpon_sn, modelo, pppoe, ponto_de_acesso):
    if ponto_de_acesso == 'alca':
        ip = '172.31.0.21'
    elif ponto_de_acesso == 'jamic':
        ip = '10.9.250.6'
    elif ponto_de_acesso == 'bujaru':
        ip = '10.7.250.10'
    elif ponto_de_acesso == 'local':
        ip = '10.9.250.10'

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

    comando1 = f'onu set gpon {gpon} onu {vaga_onu} serial-number {gpon_sn} meprof {modelo}'
    comando2 = f'bridge add gpon {gpon} onu {vaga_onu} downlink vlan 501 tagged eth 1'
    comando3 = f'onu description add gpon {gpon} onu {vaga_onu} text {pppoe}'

    tn.write(f"{comando1}\n".encode('ascii'))

    # Aguardar a resposta
    time.sleep(0)

    # Ler a resposta até encontrar o prompt novamente
    resultado1 = tn.read_until(b"olt8820plus login:", timeout=5).decode('ascii')
    resultado_final.append(resultado1)

    time.sleep(0)
    tn.write(f"{comando2}\n".encode('ascii'))

    # Aguardar a resposta
    time.sleep(0)

    # Ler a resposta até encontrar o prompt novamente
    resultado2 = tn.read_until(b"olt8820plus login:", timeout=5).decode('ascii')
    resultado_final.append(resultado2)

    time.sleep(0)
    tn.write(f"{comando3}\n".encode('ascii'))

    # Aguardar a resposta
    time.sleep(0)

    # Ler a resposta até encontrar o prompt novamente
    resultado3 = tn.read_until(b"olt8820plus login:", timeout=5).decode('ascii')
    resultado_final.append(resultado3)

    time.sleep(0)
    tn.close()

    encontrado1 = False
    encontrado2 = False
    encontrado3 = False

    for valor in resultado_final:

        if f'Onu {vaga_onu} successfully enabled with serial number {gpon_sn}' in valor:
            encontrado1 = True

        elif f'Adding bridge gpon {gpon} onu {vaga_onu} vlan 501 ........................ Ok' in valor:
            encontrado2 = True

        elif 'Command executed successfully' in valor:
            encontrado3 = True

    if not encontrado1:
        print(f"Valor 1 Onu {vaga_onu} successfully enabled with serial number {gpon_sn} não encontrado.")

    else:
        print('comando 1 ok')

    if not encontrado2:
        print(f"Valor 2 Adding bridge gpon {gpon} onu {vaga_onu} vlan 501 ........................ Ok não encontrado.")

    else:
        print('comando 2 ok')

    if not encontrado3:
        print(f"Valor 3 Command executed successfully não encontrado.")

    else:
        print('comando 3 ok')

    print(resultado_final)
    resultado_final.clear()
    
    retorno_final = f'''
✅ *TUDO CERTO!* ✅
    
O usuário *{pppoe}* foi provisionado com sucesso.
*Serial GPON:* `{gpon_sn}`
*Pon:* `{gpon}`
*Posição:* `{vaga_onu}` 

🎉 Parabéns! Seu usuário foi ativado com sucesso! 👍
'''
    return f'{retorno_final}\n\n{encontrado1}\n{encontrado2}\n{encontrado3}'
  
  
def consulta_gpon(gpon, ponto_de_acesso):
    print('consultando olt', gpon, ponto_de_acesso)
    
    gpon = gpon.upper()
    alfanumericos = gpon.isalnum()
    
    if len(gpon) != 8:
        return 'tamanho inválido'
    
    elif alfanumericos is False:
        return 'alfanumericos false'
    
    else:
        if ponto_de_acesso == 'alca':
            ip = '172.31.0.21'
        elif ponto_de_acesso == 'jamic':
            ip = '10.9.250.6'
        elif ponto_de_acesso == 'bujaru':
            ip = '10.7.250.10'
            
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

        comando = f"onu find fsan {gpon}"

        tn.write(f"{comando}\n".encode('ascii'))

        # Aguardar a resposta
        time.sleep(1)

        # Ler a resposta até encontrar o prompt novamente
        resultado = tn.read_until(b"olt8820plus login:", timeout=5).decode('ascii')

        linhas = resultado.splitlines()[-2].split()
        print(linhas)
        
        #achou o serial
        if 'gpon' in linhas[0]:
            slot = linhas[1]
            onu = linhas[3]
            modelo = linhas[-1]
            
            comando2 = f"onu status gpon {slot} onu {onu} details"

            tn.write(f"{comando2}\n".encode('ascii'))
        
            resultado2 = tn.read_until(b"olt8820plus login:", timeout=5).decode('ascii')
            linhas2 = resultado2.splitlines()[-2].split()
            #onu ativada
            if 'Active' in linhas2[2]:
                tn.close()
            
                for item in linhas2:
                    if item == 'dBm':
                        linhas2.remove(item)
                        
                print(linhas2)
                onu = linhas2[0]
                serial_gpon = linhas2[1]
                status = linhas2[2]
                omci_config_status = linhas2[3]
                rx_onu = linhas2[4]
                tx_onu = linhas2[5]
                rx_olt = linhas2[6]
                tx_olt = linhas2[7]
                distancia = float(linhas2[8])
                up_time = linhas2[9].split(':')
                temperatura = linhas2[-3]
                status_porta_lan = linhas2[-2]
                modulacao_porta_lan = linhas2[-1]

                if status_porta_lan == '1':
                    porta_lan = 'Ativa'
                    
                elif status_porta_lan == '2':
                    porta_lan = 'Desativada'
                    
                else:
                    porta_lan = '-'
                    
                if modulacao_porta_lan in opcoes_velocidade:
                    modulacao = opcoes_velocidade[modulacao_porta_lan]
                    
                else:
                    modulacao = '-'
                
                formatado = f'''
ℹ️ INFORMAÇÕES DA ONU ℹ️

⚙ *Posição na OLT:* {slot}/{onu}
⚙ *GPON-SN:* ITBS{serial_gpon}
⚙ *Modelo:* {modelo}
🔒 *Status:* {status}
🔒 *Status OMCI:* {omci_config_status}

📶 *Rx ONU:* {rx_onu} dBm 
📶 *Tx ONU:* {tx_onu} dBm
📶 *Rx OLT:* {rx_olt} dBm
📶 *Tx OLT:* {tx_olt} dBm

🔒 *Distância da OLT:* {distancia * 1000:.0f} Mt
🕒 *Tempo Ligada:* {up_time[0]} Dia(s), {up_time[1]} Hora(s), {up_time[2]} Minuto(s), {up_time[3]} Segundo(s)
🌡️  *Temperatura:* {temperatura} C°

🔌 *Porta LAN ONU:* {porta_lan}
🔌 *Modulação Porta LAN:* {modulacao}
'''
                return formatado
            
            elif 'Inactive' in linhas2[2]:
                tn.close()
                
                status_gpon = linhas2[9]
                # verifica se teve o status da queda
                if len(status_gpon) > 0 and status_gpon != '-':
                    if 'LOSI' in status_gpon:
                        descricao_alarme = "Recepção de Sinal Óptico Perdido."
                        
                    elif 'DGI' in status_gpon:
                        descricao_alarme = "ONU possívelmente desligada."
                    
                    elif 'DFI' in status_gpon:
                        descricao_alarme = "Poblemas na ONU, possivel defeito de fábrica."
                    
                    elif 'LOAMI' in status_gpon:
                        descricao_alarme = "Problemas na comunicação com a OLT"
                        
                    elif 'LOFI' in status_gpon:
                        descricao_alarme = "Perca de sincronia com a OLT"
                        
                    else:
                      descricao_alarme = ''
                        
                    serial_gpon = linhas2[1]
                    status = linhas2[2]
                    formatado = f'''
ℹ️ INFORMAÇÕES DA ONU ℹ️

🔒 *POSIÇÃO NA OLT:* {slot}/{onu}
🔒 *GPON:* ITBS{serial_gpon}
🔒 *MODELO:* {modelo}
🔒 *STATUS:* {status}
🔒 *CAUSA:* {status_gpon}
🔒 *DESCRIÇÃO:* {descricao_alarme}
'''
                    return formatado
                
                else:
                    serial_gpon = linhas2[1]
                    status = linhas2[2]
                    formatado = f'''
ℹ️ INFORMAÇÕES DA ONU ℹ️

🔒 *POSIÇÃO NA OLT:* {slot}/{onu}
🔒 *GPON:* ITBS{serial_gpon}
🔒 *MODELO:* {modelo}
🔒 *STATUS:* {status}
'''                
                    return formatado
            else:
                tn.close()
                return 'ONU bloqueada'
        else:
            tn.close()
            return f'Infelizmente não consegui localizar esse GPON-SN *{gpon}* na OLT *{ponto_de_acesso}* 😕'


def desprovisiona_gpon(gpon, ponto_de_acesso):
    print('consultando olt pra desprovisionar', gpon, ponto_de_acesso)
    
    gpon = gpon.upper()
    alfanumericos = gpon.isalnum()
    
    if len(gpon) != 8:
        return 'tamanho inválido'
    
    elif alfanumericos is False:
        return 'alfanumericos false'
    
    else:
        if ponto_de_acesso == 'alca':
            ip = '172.31.0.21'
        elif ponto_de_acesso == 'jamic':
            ip = '10.9.250.6'
        elif ponto_de_acesso == 'bujaru':
            ip = '10.7.250.10'
            
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

        comando = f"onu find fsan {gpon}"

        tn.write(f"{comando}\n".encode('ascii'))

        # Aguardar a resposta
        time.sleep(1)

        # Ler a resposta até encontrar o prompt novamente
        resultado = tn.read_until(b"olt8820plus login:", timeout=5).decode('ascii')

        linhas = resultado.splitlines()[-2].split()
        print(linhas)

        tn.close()
        #achou o serial
        if 'gpon' in linhas[0]:
            linhas.append(ponto_de_acesso)
            return linhas

        else:
            tn.close()
            return '*GPON-SN não encontrado* 😕'
        
        
def desprovisiona_efetivo(pon, onu, ponto_de_acesso):
    if ponto_de_acesso == 'alca':
        ip = '172.31.0.21'
    elif ponto_de_acesso == 'jamic':
        ip = '10.9.250.6'
    elif ponto_de_acesso == 'bujaru':
        ip = '10.7.250.10'
        
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
        
    comando_exclusao = f"onu delete gpon {pon} onu {onu}"
    comando_yes = 'yes'
    comando_no = 'no'
    
    # INICIA ENVIOS DE COMANDO PARA DESPROVISIONAR
    tn.write(f"{comando_exclusao}\n".encode('ascii'))

    resultado2 = tn.read_until(b"olt8820plus login:", timeout=5).decode('ascii')
    #linhas2 = resultado2.splitlines()[-2].split()
    print(resultado2)
    
    #comando yes
    tn.write(f"{comando_yes}\n".encode('ascii'))
    
    resultado2 = tn.read_until(b"olt8820plus login:", timeout=5).decode('ascii')
    print(resultado2)
    
    #comando no
    tn.write(f"{comando_no}\n".encode('ascii'))
    
    resultado2 = tn.read_until(b"olt8820plus login:", timeout=5).decode('ascii')
    print(resultado2)
    
    #comando yes
    tn.write(f"{comando_yes}\n".encode('ascii'))
    
    resultado2 = tn.read_until(b"olt8820plus login:", timeout=5).decode('ascii')
    
    linha = resultado2.splitlines()[-2]
    
    tn.close()
    # verifica se o retorno final bate com sucesso
    if f'deleting ONU at gpon {pon} onu {onu}' in linha:
        
        retorno_final = f"""
✅ *TUDO CERTO!* ✅

*Posição liberada:* `{onu}`
*Pon:* `{pon}`

🎉 ONU excluída com sucesso! 👍
"""
        
        print(retorno_final)
        return retorno_final
        
    else:
        return f'Ocorreu um erro ao excluir a ONU'