
inicial_cto_validas = ['R', 'P', 'G']

def valida_cto(cto):

    cto = str(cto).replace(' ', '').strip().upper()
    if cto[0] not in inicial_cto_validas:
        return 'inicial_invalida'
    
    if len(cto) > 7:
        return 'tamanho_invalido'

    #letra1 = cto[0]  # r
    letra2 = cto[1]  # a
    letra3 = cto[2]  # a
    numero1 = cto[3]  # 1
    hifen = cto[4]  # -
    numero2 = cto[5]  # 1
    try:
        numero3 = cto[6]
    except:
        pass

    if not letra2.isalpha() or not letra3.isalpha():
        return 'letras_invalidas'

    if not numero1.isdigit() or int(numero1) < 1 or int(numero1) > 2:
        return 'numero1_invalido'

    if hifen != "-":
        return 'hifen_invalido'

    if not numero2.isdigit() or int(numero2) < 1 or int(numero2) > 16 and int(numero3) > 16:
        return 'numero2_invalido'

    return f'CTO VALIDA {cto}'



"""
range validos [['1-1 - 1-16'], ['2-1 - 2-3']]



primeirp numero varia de 1 a 2

segundo numero varia de 1 a 16
"""







"""if __name__ == '__main__':
    valida_cto('rac1   -  5')
"""