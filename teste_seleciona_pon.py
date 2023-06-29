jamic = 'R'
cto_lista  = []

cto = input('Informe a cto: ').upper().replace(' ','').strip()

cto_lista.append(cto)

if cto[0] == jamic:

    print('cto é da jamic', cto_lista[0])
    
    slot = ord(cto[1]) - 64 # se deixar 65 a letra 'A' fica 0

    pon = ord(cto[2]) - 64

    print(f'slot: {slot}\npon: {pon}')
















def converte_p_numero(letra):
    print(ord(letra.upper()) - 65)
    return ord(letra.upper()) - 65
    






