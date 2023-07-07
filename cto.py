
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
        num_duplado = numero2 + numero3

    except IndexError:
        pass

    if not letra2.isalpha() or not letra3.isalpha():
        return 'letras_invalidas'

    if not numero1.isdigit() or int(numero1) < 1 or int(numero1) > 2:
        return 'numero1_invalido'

    if hifen != "-":
        return 'hifen_invalido'

    if not numero2.isdigit() or int(numero2) < 1 or int(numero2) > 16:
        return 'numero2_invalido'
    
    try:
        if not num_duplado.isdigit() or int(num_duplado) < 1 or int(num_duplado) > 16:
            return 'numero2_invalido'
    except:
        pass

    return f'CTO VALIDA {cto}'


def valida_porta(porta):

    if str(porta).isdigit():
        porta_num = int(porta)

        if 1 <= porta_num <= 16:
            return porta_num
        
        else:
            return "porta invalida"
        
    else:
        return 'não é numero'
