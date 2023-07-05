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

comando = "onu show"


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




#print(linhas)
# Percorrer as linhas
for linha in linhas:
    if 'ITBS' in linha:
        linha_onu = linha.split()

        id = linha_onu[0]
        vendor = linha_onu[1]
        serial_number = linha_onu[2]

        print(f'achei {id} onu discando: {vendor} | {serial_number}')
    else:
        pass
        #print('não existe onu discando nessa pon')

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
for pon, posicao in dicionario.items():
    print(f"Na {pon} tem o valor {posicao[0]} disponivel para o provisionamento")