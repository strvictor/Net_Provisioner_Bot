import re

lista = []
dicionario = {}
chave_atual = None

resultado = '''
intelbras-olt> onu show

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

profile_cpe = {
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

        onus_discando.append(linha_onu)

        id = linha_onu[0]
        vendor = linha_onu[1]
        serial_number = linha_onu[2]
        model = linha_onu[3]

        print(f'senor_id: {id}\nserial_number: {vendor} | {serial_number}\nmodel: {model}')

        if model in profile_cpe:
            print('me profile:', profile_cpe[model])

        else:
            print('me profile:', profile_cpe["R1v2"])
        print(' ')

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


print(f'tem {len(onus_discando)} discando\n{onus_discando}')