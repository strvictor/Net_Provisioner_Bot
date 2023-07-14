import re

lista = []
dicionario = {}
chave_atual = None

resultado = '''
intelbras-olt> onu show gpon 1

Free slots in GPON Link 1:
=======================================
 41   42   43   44   45   46   47   48
 49   50   51   52   53   54   55   56
 57   58   59   60   61   62   63   64
 65   66   67   68   69   70   71   72
 73   74   75   76   77   78   79   80
 81   82   83   84   85   86   87   88
 89   90   91   92   93   94   95   96
 97   98   99  100  101  102  103  104
105  106  107  108  109  110  111  112
113  114  115  116  117  118  119  120
121  122  123  124  125  126  127  128

Discovered serial numbers
==============================================
sernoID   Vendor  Serial Number   Model       Time Discovered
34        ITBS    CFEBD229        121AC       Jul 01 11:20:04 2023
31        ITBS    CFEBD229        121AC       Jul 01 11:20:04 2023
11        ITBS    CFEBD212        110Gi       Jul 01 11:20:04 2023

intelbras-olt>
'''

linhas = resultado.splitlines()

modelos = """
Modelos disponíveis:
intelbras-110
intelbras-110b
intelbras-110g
intelbras-121ac
intelbras-121w
intelbras-1420g
intelbras-142ng
intelbras-142nw
intelbras-defaul

===============
110Gb  (intelbras-110b)
121AC  (intelbras-121ac)
R1v2   (intelbras-defaul)
110Gi  (intelbras-110)
R1     (intelbras-r1)
"""

modelos_de_ativacao = {
    "110Gb": "intelbras-110b",
    "121AC": "intelbras-121ac",
    "R1v2": "intelbras-defaul",
    "110Gi": "intelbras-110",
    "R1": "intelbras-r1"
} 
onus_discando = []
# Percorrer as linhas
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


if len(onus_discando) == 0:
    print('sem onu discando')
    
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

    print(f'''onu selecionada
    {id_onu}
    {fabricante}
    {serial}
    {modelo}
    {modelo_permitido}
    ''')
    
else:
    # tem mais de uma onu discando
    for i, onu in enumerate(onus_discando):

        print(f'{i + 1}_ escolha a sua onu {onu[1:3]}')
        #return f'{i}_ escolha a onu {onu}'

    escolha = int(input("> "))

    # verifica se oq o cara escolheu ta certo
    if escolha <= 0 or escolha > len(onus_discando):
        print('não existe esse indice')

    else:                

        onus_discando = onus_discando[escolha - 1]

        id_onu = onus_discando[0]
        fabricante = onus_discando[1]
        serial = onus_discando[2]
        modelo = onus_discando[3]

        if modelo in modelos_de_ativacao:
            modelo_permitido = modelos_de_ativacao[modelo]  

        else:
            modelo_permitido = modelos_de_ativacao['R1v2'] 

        print(f'''onu {escolha} selecionada
{id_onu}
{fabricante}
{serial}
{modelo}
{modelo_permitido}
''')