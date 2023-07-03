
jamic = 'R'
bujaru = 'P'
vila_nova = 'G'

cto_lista  = []
def cto_pon(cto):

    cto = str(cto).upper().replace(' ','').strip()

    cto_lista.append(cto)
    if cto[0] == jamic or cto[0] == bujaru or cto[0] == vila_nova:
 
        slot = ord(cto[1]) - 64 # se deixar 65 a letra 'A' fica 0

        pon = ord(cto[2]) - 64

        print(f'slot: {slot}\npon: {pon}')

    else:
        
        slot = ord(cto[1]) - 65 # se deixar 65 a letra 'A' fica 0

        pon = ord(cto[2]) - 65

        print(f'slot: {slot}\npon: {pon}')
    cto_lista.clear()


cto = 'pae1-8'
cto_pon(cto)

