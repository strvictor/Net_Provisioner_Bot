import json

def Valida_Cto(cto):
    iformacoes = list()
    iformacoes.clear()
    
    encontrou = False
    cto_informada = str(cto).replace(' ', '').strip().upper()
    
    with open('ctos-atualizadas.txt', 'r') as arquivo:
        base = arquivo.read()
        base_atualizada = json.loads(base)
        
        for cto_ in base_atualizada['response']:
            if cto_informada in cto_['title']:
                encontrou = True
                print(cto_)
                
                item_rede = cto_['code']
                remove_prefixo = cto_['title'].replace('CTO', '').replace(' ', '')
                
                iformacoes.append(remove_prefixo)
                iformacoes.append(item_rede)
                
                return iformacoes
                
        if encontrou is False:
            return  'cto não encontrada'
        
        
def Valida_Porta(porta):

    if str(porta).isdigit():
        porta_num = int(porta)

        if 1 <= porta_num <= 16:
            return porta_num
        
        else:
            return "porta invalida"
    else:
        return 'não é numero'


def Pon_Cto(cto):

    slot = ord(cto[1]) - 64 # se deixar 65 a letra 'A' fica 0
    pon = ord(cto[2]) - 64
    return pon
    
    #slot = ord(cto[1]) - 65 # se deixar 65 a letra 'A' fica 0
    #pon = ord(cto[2]) - 65
    #print(f'slot: {slot}\npon: {pon}')
