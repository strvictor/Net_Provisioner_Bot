
def cto_pon(cto):

    slot = ord(cto[1]) - 64 # se deixar 65 a letra 'A' fica 0

    pon = ord(cto[2]) - 64

    print(f'slot: {slot}\npon: {pon}')
    
    #slot = ord(cto[1]) - 65 # se deixar 65 a letra 'A' fica 0
    #pon = ord(cto[2]) - 65
    #print(f'slot: {slot}\npon: {pon}')


cto_pon('PAB-1')
