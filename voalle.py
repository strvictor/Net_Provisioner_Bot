def validacontrato(num_contrato):
    valida_numero = str(num_contrato).isnumeric()
    
    if valida_numero:
        #CONSULTA A API DO VOALLE AQUI ##

        if num_contrato == '123456':
            mensagem = 'Contrato Válido!'
            return mensagem
        
        else:
            mensagem = 'Contrato Inválido!'
            return mensagem
        
         #CONSULTA A API DO VOALLE AQUI ##
    else:
        # retorna falso, pra validar no arquivo app.py e chamar novamente a função
        return False
           

def consulta_cliente():
    return 'Em andamento...'
