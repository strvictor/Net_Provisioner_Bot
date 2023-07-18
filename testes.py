
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

17 colunas
'''

retorno = """
intelbras-olt> onu status gpon 1 onu 1 details
GPON 1

     Serial                OMCI Config     ONU         ONU         OLT         OLT        Distance          GPON              Uptime                 Power          Bias       Temperature  LAN Port  LAN Port
ONU  Number    OperStatus   Status       Rx Power    Tx Power    Rx Power    Tx Power       (km)          ONU Status       ddd:hh:mm:ss    Auto   Voltage (V)   Current (mA)       (C)       Status     Speed
=== ========= =========== ============= =========== =========== =========== =========== =========== ==================== ================ ====== ============= ============== ============= ======== ===========
1   327278B9  Active      OK            -17.96 dBm  2.44 dBm    -20.75 dBm  5.23 dBm    0.427                            12:15:46:2        no     3.36          11.424         64.6          1        13
intelbras-olt>
"""
linhas = retorno.splitlines()

resultado_das_inf = linhas[-2].split()

# remove o dbm
for item in resultado_das_inf:
    if item == 'dBm':
        resultado_das_inf.remove(item)





import telnetlib, time


HOST = str('172.31.0.21')  # Endereço do dispositivo Telnet
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

comando = f"onu status gpon 2 onu 7 details"

tn.write(f"{comando}\n".encode('ascii'))

# Aguardar a resposta
time.sleep(1)

# Ler a resposta até encontrar o prompt novamente
resultado = tn.read_until(b"olt8820plus login:", timeout=5).decode('ascii')

linhas = resultado.splitlines()[-2].split()

if linhas[2] != 'Active':
    print("onu", linhas[2])
    
else:
    
    for item in linhas:
        if item == 'dBm':
            linhas.remove(item)
            
    print(linhas)
    onu = linhas[0]
    serial_gpon = linhas[1]
    status = linhas[2]
    omci_config_status = linhas[3]
    rx_onu = linhas[4]
    tx_onu = linhas[5]
    rx_olt = linhas[6]
    tx_olt = linhas[7]
    distancia = float(linhas[8])
    up_time = linhas[9].split(':')


    formatado = f'''
    ONU: {onu}
    GPON: {serial_gpon}
    STATUS: {status}
    STATUS OMCI: {omci_config_status}
    RX ONU: {rx_onu} dBm 
    TX ONU: {tx_onu} dBm
    RX OLT: {rx_olt} dBm
    TX OLT: {tx_olt} dBm
    DISTÂNCIA OLT --> ONU: {distancia * 1000:.0f} Mt
    TEMPO LIGADA: {up_time[0]} Dias, {up_time[1]} Horas, {up_time[2]} Minutos, {up_time[3]} Segundos
    '''
    print(formatado)

