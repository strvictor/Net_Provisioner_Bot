import telnetlib
import time
import re

lista = []
dicionario = {}
chave_atual = None

HOST = '10.9.250.6'  # Endereço do dispositivo Telnet
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

# Enviar o comando "onu show"

command = "onu show gpon"
gpon_id = 5

tn.write(f"{command} {gpon_id}\n".encode('ascii'))

# Aguardar a resposta
time.sleep(1)

# Ler a resposta até encontrar o prompt novamente
resultado = tn.read_until(b"olt8820plus login:", timeout=5).decode('ascii')


# Fechar a conexão Telnet
tn.close()




linhas = resultado.splitlines()

start_index = linhas.index(f'intelbras-olt> {command} {gpon_id}')
filtered_lines = linhas[start_index:]

print(filtered_lines)