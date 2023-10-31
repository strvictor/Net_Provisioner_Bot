import json
import requests
verifica = []

def validacontrato(num_contrato):
    
    # verifica se o contrato tem somente numeros
    valida_numero = str(num_contrato).isnumeric()
    if valida_numero:
        url = "https://erp-staging.gbsn.com.br:45701/api/v1/isp/connection/integration/by/userdata"

        # pega o token atualizado
        with open('token.txt', 'r') as arquivo:
            token = arquivo.readline()
            arquivo.close()
            
        # Dados ajustados
        dados = {
            "contractIds": [f'{num_contrato}']
        }

        # Converter os dados em formato JSON
        dados_json = json.dumps(dados)

        # Definir cabeçalhos
        headers = {
            'Authorization': f'Bearer {token}',  # Certifique-se de adicionar seu token aqui
            
            'accept': 'application/json',
            'Content-Type': 'application/json'
        }

        #bloqueei a requisição de momento
        dados = requests.post(url, headers=headers, data=dados_json)
        
#         # remover esse bloco de baixo
#         return f"""
# ℹ️  DADOS DO CLIENTE ℹ️          
            
# 📄 CONTRATO:44671               
# 👤 NOME: teste   
# 🆔 CPF: teste      
# 🌐 PONTO DE ACESSO: BLM Laguna OLT FTTH       
# 🏙️ CIDADE: alca
# 🏡 BAIRRO: alca
# 🛣️ RUA: alca
# 🏠 NUMERO: 0
# 💻 PPPOE: antoniel.oliveira.44671                   
# 🔐 SENHA: 112233
# """
        
        
        # Imprimir a resposta
        dados_corrigidos = json.loads(dados.text)

        # verifica se tem resposta de contrato 
        if len(dados_corrigidos['response']) == 0:
            return 'contrato não localizado'
        else:
            
            for dados in dados_corrigidos['response']:
                
                contrato_cliente = num_contrato
                nome_cliente = dados['client']['name'].title()
                cpf_cliente =  dados['client']['txId']
                ponto_de_acesso = dados['authenticationAccessPoint']['title']
                cidade = dados['address']['city']
                bairro = dados['address']['neighborhood'].title()
                rua = dados['address']['street'].title()
                numero_casa = dados['address']['number']
                pppoe = dados['user']
                senha_pppoe = 112233

                return f"""
ℹ️  DADOS DO CLIENTE ℹ️          
            
📄 CONTRATO:{contrato_cliente}               
👤 NOME: {nome_cliente}   
🆔 CPF: {cpf_cliente}      
🌐 PONTO DE ACESSO: {ponto_de_acesso}       
🏙️ CIDADE: {cidade}
🏡 BAIRRO: {bairro}
🛣️ RUA: {rua}
🏠 NUMERO: {numero_casa}
💻 PPPOE: {pppoe}                   
🔐 SENHA: {senha_pppoe} 
"""
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        #CONSULTA A API DO VOALLE AQUI ##

#         with open('base.txt', 'r') as arquivo:
#             # Carregue o conteúdo do arquivo
#             conteudo = arquivo.read()
        
#             # Analise o conteúdo como um objeto JSON
#             dados_json = json.loads(conteudo)

#             for dado in dados_json['registros']:
#                 #print(dado['dados']['ip'])
#                 contrato = dado['dados']['contrato']

#                 if num_contrato == contrato:
#                     verifica.clear()
#                     verifica.append(num_contrato)
#                     return f"""
# Localizamos esse contrato:

# Contrato: {dado['dados']['contrato']}
# Cliente: {dado['dados']['cliente']}
# Ponto de acesso: {dado['dados']['ponto de acesso']}
# Cidade: {dado['dados']['cidade']}
# Bairro: {dado['dados']['bairro']}
# Ip: {dado['dados']['ip']}
# Pppoe: {dado['dados']['pppoe']}
# Senha: {dado['dados']['senha']}
# """

#             if len(verifica) == 0:
#                 return "contrato não localizado"
        
         #CONSULTA A API DO VOALLE AQUI ##
    else:
        # retorna falso, pra validar no arquivo app.py e chamar novamente a função
        return False
           


