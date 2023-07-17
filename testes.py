'''import telnetlib, re, time

modelos_de_ativacao = {
    "110Gb": "intelbras-110b",
    "121AC": "intelbras-121ac",
    "120AC": "intelbras-121ac",
    "R1v2": "intelbras-r1",
    "110Gi": "intelbras-110",
    "R1": "intelbras-r1"
} 

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
    tn.close()

    if f'intelbras-olt> {comando}' not in  linhas:
        #print(f'{comando} não encontrado')
        
        inicio_filtro = linhas.index(f'Free slots in GPON Link {pon}:')
        filtrado = linhas[inicio_filtro:]

        print(filtrado)


        return formata_retorno(filtrado, pon, ponto_de_acesso)
    
        #chama_func = busca_onu_na_pon(ponto_de_acesso, pon)
        #return chama_func
         
    else:

        inicio_filtro = linhas.index(f'intelbras-olt> {comando}')
        filtrado = linhas[inicio_filtro:]
        print(filtrado)
        return formata_retorno(filtrado, pon, ponto_de_acesso)





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
    return exibe_info(onus_discando, temporario[0], pon)

    


def exibe_info(onus_discando, posicao, pon):

    if len(onus_discando) == 0:
        return f'sem onu discando nessa pon {pon}'
    
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
    
        return fabricante, serial, modelo, modelo_permitido, posicao, pon
    


""" else:
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
    
        return f'''#onu {escolha} selecionada
#{id_onu}
#{fabricante}
#{serial}
#{modelo}
#{modelo_permitido}
'''
"""
retorno = busca_onu_na_pon('alca', '7')

print(retorno)

'''




'''

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

'''


'''
lista = ['\r\nonu set gpon 7 onu 1 serial-number ITBSCFC03303 meprof intelbras-121ac\r\n  _____ _   _ _______ ______ _      ____  _____             _____\r\n |_   _| \\ | |__   __|  ____| |    |  _ \\|  __ \\     /\\    / ____|\r\n   | | |  \\| |  | |  | |__  | |    | |_) | |__) |   /  \\  | (___\r\n   | | | . ` |  | |  |  __| | |    |  _ <|  _ <   /   / /\\ \\  \\___ \\ \r\n  _| |_| |\\  |  | |  | |____| |____| |_) | | \\ \\  / ____ \\ ____) |\r\n |_____|_| \\_|  |_|  |______|______|____/|_|  \\_\\/_/    \\_\\_____/\r\n\r\n           ____  _   _______ ___   ___ ___   ___  _\r\n          / __ \\| | |__   __/ _ \\ / _ \\__ \\ / _ \\(_)\r\n         | |  | | |    | | | (_) | (_) | ) |  | | |_\r\n         | |  | | |    | |  > _ < > _ < / /| | | | |\r\n         | |__| | |____| | | (_) | (_) / /_| |_| | |\r\n          \\____/|______|_|  \\___/ \\___/____|\\___/|_|\r\n\r\n\r\nIntelbras S.A.\r\nIndustria de Telecomunicacao Eletronica Brasileira\r\n\r\n\x1b[1;31m(!) 4 abnormals reboots happened, the first was in 2021-01-19 05:21\x1b[0m\r\n\r\n\x1b[93m(!) Warning, there are 36 active alarms\x1b[0m\r\n\r\nintelbras-olt> onu set gpon 7 onu 1 serial-number ITBSCFC03303 meprof intelbr\r< 7 onu 1 serial-number ITBSCFC03303 meprof intelbra                         \x08\x08\x08\x08\x08\x08\x08\x08\x08\x08\x08\x08\x08\x08\x08\x08\x08\x08\x08\x08\x08\x08\x08\x08s-121ac\r\nOnu 1 successfully enabled with serial number ITBSCFC03303\r\nintelbras-olt> ', 'bridge add gpon 7 onu 1 downlink vlan 501 tagged eth 1\r\nAdding bridge gpon 7 onu 1 vlan 501 ........................ Ok\r\nintelbras-olt> ', 'onu description add gpon 7 onu 1 text primeira.ativacao.bot\r\nCommand executed successfully\r\nintelbras-olt> ']

valor1 = 'Onu 1 successfully enabled with serial number ITBSCFC03303'
valor2 = 'Adding bridge gpon 7 onu 1 vlan 501 ........................ Ok'
valor3 = 'Command executed successfully'

for item in lista:
    if valor1 in item:
        print("Valor 1 encontrado!")
    elif valor2 in item:
        print("Valor 2 encontrado!")
    elif valor3 in item:
        print("Valor 3 encontrado!")
 


'''
'''
import telebot
from telebot import types

# Substitua 'SEU_TOKEN' pelo token do seu bot
bot = telebot.TeleBot('5935745695:AAHcP4dAquoEEg0pv9YOlj0HHLiofldVMY4')

# Função para criar o teclado com os botões
def create_keyboard():
    keyboard = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    
    # Botão de texto
    text_button = types.KeyboardButton(text="Clique aqui para enviar um texto")
    
    # Botão de solicitação de número de telefone
    phone_button = types.KeyboardButton(text="Compartilhar número de telefone", request_contact=True)
    
    # Botão de solicitação de contato
    contact_button = types.KeyboardButton(text="Compartilhar contato", request_contact=True)
    
    # Adiciona os botões ao teclado
    keyboard.add(text_button, phone_button, contact_button)
    
    return keyboard

# Função para responder à mensagem do usuário
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    bot.send_message(message.chat.id, "Clique em um dos botões abaixo:", reply_markup=create_keyboard())

# Função para capturar o texto enviado pelo usuário
@bot.message_handler(func=lambda message: message.text == "Clique aqui para enviar um texto")
def handle_text(message):
    bot.send_message(message.chat.id, "Você clicou no botão de texto!")

# Função para capturar o número de telefone enviado pelo usuário
@bot.message_handler(content_types=['contact'])
def handle_contact(message):
    bot.send_message(message.chat.id, f"Você compartilhou o número de telefone: {message.contact.phone_number}")

# Função para capturar o contato enviado pelo usuário
@bot.message_handler(content_types=['contact'])
def handle_contact(message):
    contact_name = message.contact.first_name
    contact_phone = message.contact.phone_number
    bot.send_message(message.chat.id, f"Você compartilhou o contato: {contact_name}, {contact_phone}")

# Iniciar o bot
bot.polling()
'''

retorno = """
intelbras-olt> onu status gpon 1 onu 10 details
GPON 1

     Serial                OMCI Config     ONU         ONU         OLT         OLT        Distance          GPON              Uptime                 Power          Bias       Temperature
ONU  Number    OperStatus   Status       Rx Power    Tx Power    Rx Power    Tx Power       (km)          ONU Status       ddd:hh:mm:ss    Auto   Voltage (V)   Current (mA)       (C)
=== ========= =========== ============= =========== =========== =========== =========== =========== ==================== ================ ====== ============= ============== =============
10  2CEA0325  Active      OK            -18.21 dBm  2.68 dBm    -20.76 dBm  4.96 dBm    0.516                            0:5:13:50        yes    3.3           11.628         48.5
intelbras-olt>
"""
linhas = retorno.splitlines()

resultado_das_inf = linhas[-2].split()


print(resultado_das_inf)
