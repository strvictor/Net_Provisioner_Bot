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
        # se for caracteres retorna essa msg
        mensagem = 'Opa, só aceitamos o numero do contrato por aqui 😊\nDigite apenas números, por favor!'
        return mensagem
           

