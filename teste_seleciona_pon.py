
# # def cto_pon(cto):

# #     slot = ord(cto[1]) - 64 # se deixar 65 a letra 'A' fica 0

# #     pon = ord(cto[2]) - 64

# #     print(f'slot: {slot}\npon: {pon}')
    
# #     #slot = ord(cto[1]) - 65 # se deixar 65 a letra 'A' fica 0
# #     #pon = ord(cto[2]) - 65
# #     #print(f'slot: {slot}\npon: {pon}')


# # cto_pon('PAB-1')

# import requests, json


# def Forca_Integracao(item_rede, porta_informada):

#     url = f"https://ares.geogridmaps.com.br/norte/api/v3/equipamentos/itemRede/{item_rede}/portas"

#     params = {
#         'atendimento[]': 'S',
#         'modoProjeto[]': ['S', 'N'],
#         'tipo[]': ['S', 'E'],
#         'disponivel': 'N'
#     }

#     headers = {
#         'Accept': 'application/json',
#         'api-key': '2de9624bb1745bebf8bf12759543cd6ac3d2de36'
#     }

#     response = requests.get(url, params=params, headers=headers)

#     if response.status_code == 200:
#         dados = response.json()
    
#         registros = dados['registros'][0]['portas']

#         for i, dado in enumerate(registros):
#             if i == 0:
#                 pass
            
#             else:
#                 try:
#                     id_porta = dado['dados']['id']
#                     porta = dado['dados']['porta']
#                     id_cliente = dado['cliente']['id']
#                     nome_cliente = dado['cliente']['nome']
#                     print(id_porta, porta, id_cliente, nome_cliente)
                    
#                     if int(porta_informada) == int(porta):
#                         remove = Remove_Cliente(id_porta, id_cliente)
#                         return remove

#                 except:
#                     continue
#     else:
#         return f"Erro na requisição. Código de status: {response.status_code} {response.text}"
        

# def Remove_Cliente(id_porta, id_cliente):
#     url = f"https://ares.geogridmaps.com.br/norte/api/v3/integracao/atender/{id_porta}/{id_cliente}"

#     headers = {
#         'Accept': 'application/json',
#         'api-key': '2de9624bb1745bebf8bf12759543cd6ac3d2de36'
#     }

#     response = requests.delete(url, headers=headers)

#     if response.status_code == 200:
#         return response.text
#     else:
#         return json.loads(response.text)



# teste = Forca_Integracao(51247, 15)

# print(teste)


retorno = list()
item_rede = 1234

porta_informarda = 3

retorno.append('porta ocupada para uso')
retorno.append(item_rede)
retorno.append(porta_informarda)
            
print(retorno)