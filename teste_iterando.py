import re

lista = []
dicionario = {}
chave_atual = None

# Abrir o arquivo
with open('olt_8820_find_return.txt', 'r') as arquivo:
    # Ler as linhas do arquivo
    linhas = arquivo.readlines()

    # Percorrer as linhas
    for linha in linhas:
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


testee