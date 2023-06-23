import re

lista = []
dicionario = {}
chave_atual = None

resultado = '''
intelbras-olt> onu show

Free slots in GPON Link 1:
=======================================
 21   22   23   24   25   26   27   28
 29   30   31   32   33   34   35   36
 37   38   39   40   41   42   43   44
 45   46   47   48   49   50   51   52
 53   54   55   56   57   58   59   60
 61   62   63   64   65   66   67   68
 69   70   71   72   73   74   75   76
 77   78   79   80   81   82   83   84
 85   86   87   88   89   90   91   92
 93   94   95   96   97   98   99  100
101  102  103  104  105  106  107  108
109  110  111  112  113  114  115  116
117  118  119  120  121  122  123  124
125  126  127  128

Discovered serial numbers
==============================================
sernoID   Vendor  Serial Number   Model       Time Discovered



Free slots in GPON Link 2:
=======================================
 22   23   24   25   26   27   28   29
 30   31   32   33   34   35   36   37
 38   39   40   41   42   43   44   45
 46   47   48   49   50   51   52   53
 54   55   56   57   58   59   60   61
 62   63   64   65   66   67   68   69
 70   71   72   73   74   75   76   77
 78   79   80   81   82   83   84   85
 86   87   88   89   90   91   92   93
 94   95   96   97   98   99  100  101
102  103  104  105  106  107  108  109
110  111  112  113  114  115  116  117
118  119  120  121  122  123  124  125
126  127  128

Discovered serial numbers
==============================================
sernoID   Vendor  Serial Number   Model       Time Discovered



Free slots in GPON Link 3:
=======================================
 12   13   14   15   16   17   18   19
 20   21   22   23   24   25   26   27
 28   29   30   31   32   33   34   35
 36   37   38   39   40   41   42   43
 44   45   46   47   48   49   50   51
 52   53   54   55   56   57   58   59
 60   61   62   63   64   65   66   67
 68   69   70   71   72   73   74   75
 76   77   78   79   80   81   82   83
 84   85   86   87   88   89   90   91
 92   93   94   95   96   97   98   99
100  101  102  103  104  105  106  107
108  109  110  111  112  113  114  115
116  117  118  119  120  121  122  123
124  125  126  127  128

Discovered serial numbers
==============================================
sernoID   Vendor  Serial Number   Model       Time Discovered



Free slots in GPON Link 4:
=======================================
  5    6    7    8    9   10   11   12
 13   14   15   16   17   18   19   20
 21   22   23   24   25   26   27   28
 29   30   31   32   33   34   35   36
 37   38   39   40   41   42   43   44
 45   46   47   48   49   50   51   52
 53   54   55   56   57   58   59   60
 61   62   63   64   65   66   67   68
 69   70   71   72   73   74   75   76
 77   78   79   80   81   82   83   84
 85   86   87   88   89   90   91   92
 93   94   95   96   97   98   99  100
101  102  103  104  105  106  107  108
109  110  111  112  113  114  115  116
117  118  119  120  121  122  123  124
125  126  127  128

Discovered serial numbers
==============================================
sernoID   Vendor  Serial Number   Model       Time Discovered



Free slots in GPON Link 5:
=======================================
  5    6    7    8    9   10   11   12
 13   14   15   16   17   18   19   20
 21   22   23   24   25   26   27   28
 29   30   31   32   33   34   35   36
 37   38   39   40   41   42   43   44
 45   46   47   48   49   50   51   52
 53   54   55   56   57   58   59   60
 61   62   63   64   65   66   67   68
 69   70   71   72   73   74   75   76
 77   78   79   80   81   82   83   84
 85   86   87   88   89   90   91   92
 93   94   95   96   97   98   99  100
101  102  103  104  105  106  107  108
109  110  111  112  113  114  115  116
117  118  119  120  121  122  123  124
125  126  127  128

Discovered serial numbers
==============================================
sernoID   Vendor  Serial Number   Model       Time Discovered



Free slots in GPON Link 6:
=======================================
  1    2    3    4    5    6    7    8
  9   10   11   12   13   14   15   16
 17   18   19   20   21   22   23   24
 25   26   27   28   29   30   31   32
 33   34   35   36   37   38   39   40
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



Free slots in GPON Link 7:
=======================================
  1    2    3    4    5    6    7    8
  9   10   11   12   13   14   15   16
 17   18   19   20   21   22   23   24
 25   26   27   28   29   30   31   32
 33   34   35   36   37   38   39   40
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



Free slots in GPON Link 8:
=======================================
  4    5    6    7    8
  9   10   11   12   13   14   15   16
 17   18   19   20   21   22   23   24
 25   26   27   28   29   30   31   32
 33   34   35   36   37   38   39   40
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


intelbras-olt>
'''

linhas = resultado.splitlines()

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
