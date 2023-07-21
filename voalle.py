import json
verifica = []

def validacontrato(num_contrato):
    valida_numero = str(num_contrato).isnumeric()

    if valida_numero:
        #CONSULTA A API DO VOALLE AQUI ##

        with open('base.txt', 'r') as arquivo:
            # Carregue o conteúdo do arquivo
            conteudo = arquivo.read()
        
            # Analise o conteúdo como um objeto JSON
            dados_json = json.loads(conteudo)

            for dado in dados_json['registros']:
                #print(dado['dados']['ip'])
                contrato = dado['dados']['contrato']

                if num_contrato == contrato:
                    verifica.clear()
                    verifica.append(num_contrato)
                    return f"""
Localizamos esse contrato:

Contrato: {dado['dados']['contrato']}
Cliente: {dado['dados']['cliente']}
Ponto de acesso: {dado['dados']['ponto de acesso']}
Cidade: {dado['dados']['cidade']}
Bairro: {dado['dados']['bairro']}
Ip: {dado['dados']['ip']}
Pppoe: {dado['dados']['pppoe']}
Senha: {dado['dados']['senha']}
"""

            if len(verifica) == 0:
                return "contrato não localizado"
        
         #CONSULTA A API DO VOALLE AQUI ##
    else:
        # retorna falso, pra validar no arquivo app.py e chamar novamente a função
        return False
           


