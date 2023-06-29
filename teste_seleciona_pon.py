
jamic = 'R'
bujaru = 'P'
cto_lista  = []
while 1:
    cto = input('Informe a cto: ').upper().replace(' ','').strip()

    cto_lista.append(cto)

    if cto[0] == jamic or cto[0] == bujaru:

        print('cto é da jamic', cto_lista[0])
        
        slot = ord(cto[1]) - 64 # se deixar 65 a letra 'A' fica 0

        pon = ord(cto[2]) - 64

        print(f'slot: {slot}\npon: {pon}')

    else:
        
        slot = ord(cto[1]) - 65 # se deixar 65 a letra 'A' fica 0

        pon = ord(cto[2]) - 65

        print(f'slot: {slot}\npon: {pon}')
    cto_lista.clear()












