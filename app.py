import telebot, time
from telebot import types
from voalle import validacontrato
from cto import valida_cto, valida_porta, pon_cto
from olt import busca_onu_na_pon, provisiona, consulta_gpon

class Provisionamento():
    def __init__(self):
        self.token = '5935745695:AAHcP4dAquoEEg0pv9YOlj0HHLiofldVMY4'
        self.bot = telebot.TeleBot(self.token)
        self.cto_validada = list()
        self.ponto_de_acesso = list()
        self.pppoe_cliente = list()


    def menu_principal(self, chat_id):
        mensagem = 'Escolha uma opção:'
        id_usuario = chat_id

        # Criando o layout do teclado inline
        teclado_inline = types.InlineKeyboardMarkup(row_width=1)

        # Criando os botões
        provisionar = types.InlineKeyboardButton("Provisionar ONU", callback_data='provisionamento')
        consulta = types.InlineKeyboardButton("Consultar ONU", callback_data='consulta')

        # Adicionando os botões ao teclado inline
        teclado_inline.add(provisionar, consulta)

        # Enviando a mensagem com o teclado inline
        self.bot.send_message(id_usuario, mensagem, reply_markup=teclado_inline)


    def menu_nova_tentativa(self, chat_id):
        id_usuario = chat_id

        # Criando o layout do teclado inline
        teclado_inline = types.InlineKeyboardMarkup(row_width=1)

        # Criando os botões
        voltar_menu = types.InlineKeyboardButton("Voltar - Menu", callback_data='voltar_menu')
        tentar_novamente = types.InlineKeyboardButton("Tentar Novamente", callback_data='tentar_novamente')

        # Adicionando os botões ao teclado inline
        teclado_inline.add(voltar_menu, tentar_novamente)

        # Enviando a mensagem com o teclado inline
        mensagem = "Não consegui localizar o contrato desse cliente 🙁\nO que você deseja fazer?"
        self.bot.send_message(id_usuario, mensagem, reply_markup=teclado_inline)


    def menu_confirmacao_olt(self, chat_id):
        id_usuario = chat_id

        teclado_inline = types.InlineKeyboardMarkup(row_width=1)

        confirmar = types.InlineKeyboardButton("Tudo certo!", callback_data='tudo_certo_olt')
        tentar_novamente = types.InlineKeyboardButton("Tentar Novamente", callback_data='tentar_novamente_cto')

        teclado_inline.add(confirmar, tentar_novamente)
        mensagem = "Antes de continuar, por favor confirme as informações"
        self.bot.send_message(id_usuario, mensagem, reply_markup=teclado_inline)


    def menu_confirmacao_olt_onu_n_encontrada(self, chat_id):
        id_usuario = chat_id

        teclado_inline = types.InlineKeyboardMarkup(row_width=1)

        tentar_novamente = types.InlineKeyboardButton("Tentar Novamente", callback_data='tentar_novamente_cto')
        volta_menu = types.InlineKeyboardButton("Volta Menu", callback_data='volta_menu')

        teclado_inline.add(tentar_novamente, volta_menu)

        mensagem = "Não consegui localizar nenhuma ONU discando nessa pon 🙁\nO que você deseja fazer?"
        self.bot.send_message(id_usuario, mensagem, reply_markup=teclado_inline)


    def menu_confirmacao(self, chat_id):
        id_usuario = chat_id

        teclado_inline = types.InlineKeyboardMarkup(row_width=1)

        correto = types.InlineKeyboardButton("Tudo certo!", callback_data='correto')
        incorreto = types.InlineKeyboardButton("Tentar novamente", callback_data='incorreto')

        teclado_inline.add(correto, incorreto)

        mensagem = "Antes de continuar, por favor confirme as informações"
        self.bot.send_message(id_usuario, mensagem, reply_markup=teclado_inline)


    def provisionamento(self, chat_id):
        mensagem = '> Informe o número do contrato, por favor!'
        id_usuario = chat_id
        self.bot.send_message(id_usuario, mensagem)

        # escuta a resposta do contrato
        @self.bot.message_handler(func=lambda message: True)
        def captura_contrato(mensagem): 
            contrato = mensagem.text

            mensagem_validacao = validacontrato(contrato)

            if mensagem_validacao is False:
                mensagem = 'Opa, não aceitamos caracteres por aqui 😊\nDigite apenas números, por favor!'
                self.bot.send_message(id_usuario, mensagem)
                self.provisionamento(id_usuario)

            elif mensagem_validacao == 'contrato não localizado':
                self.menu_nova_tentativa(id_usuario)

            else:
                # se cair aqui significa que achou um contrato valido
                self.bot.send_message(id_usuario, mensagem_validacao)
                
                self.ponto_de_acesso.append(mensagem_validacao.split('\n')[5].split(':')[1].strip())

                self.pppoe_cliente.append(mensagem_validacao.split('\n')[9].split(':')[1].strip())

                time.sleep(1)
                self.menu_confirmacao(id_usuario)

        self.bot.register_next_step_handler_by_chat_id(chat_id, captura_contrato)


    def solicita_cto(self, chat_id):
        mensagem = 'Informe a CTO que conectou o cliente:\n_Sugestão: AAA1-1_'
        id_usuario = chat_id
        self.bot.send_message(id_usuario, mensagem, parse_mode="Markdown")

        @self.bot.message_handler(func=lambda message: True)
        def captura_cto(cto):
            cto = cto.text

            cto_validacao = valida_cto(cto)

            if cto_validacao == 'inicial_invalida':
                self.bot.send_message(id_usuario, "CTO inválida!\n> Localidade não encontrada ")
                time.sleep(1)
                self.solicita_cto(id_usuario)

            elif cto_validacao == 'tamanho_invalido':
                self.bot.send_message(id_usuario, "CTO inválida!\n> CTO informada ta em tamanho fora do esperado")
                time.sleep(1)
                self.solicita_cto(id_usuario)

            elif cto_validacao == 'letras_invalidas':
                self.bot.send_message(id_usuario, "CTO inválida!\n> Caracteres não permitidos")
                time.sleep(1)
                self.solicita_cto(id_usuario)

            elif cto_validacao == 'numero1_invalido':
                self.bot.send_message(id_usuario, "CTO inválida!\n> Numero fora do range")
                time.sleep(1)
                self.solicita_cto(id_usuario)

            elif cto_validacao == 'hifen_invalido':
                self.bot.send_message(id_usuario, "CTO inválida!\n> Hífen não localizado")
                time.sleep(1)
                self.solicita_cto(id_usuario)

            elif cto_validacao == 'numero2_invalido':
                self.bot.send_message(id_usuario, "CTO inválida!\n> Numero fora do range")
                time.sleep(1)
                self.solicita_cto(id_usuario)

            else:
                # se a cto for valida ele cai aqui
                self.bot.send_message(id_usuario, f'CTO VÁLIDA {cto_validacao}')

                #adiciona cto validada na lista
                self.cto_validada.append(cto_validacao)
                time.sleep(1)
                self.solicita_porta_cto(id_usuario)

        self.bot.register_next_step_handler_by_chat_id(chat_id, captura_cto)


    def solicita_porta_cto(self, chat_id):
        mensagem = 'Informe a PORTA que conectou o cliente:\n_Sugestão: 1 à 16_'
        id_usuario = chat_id
        self.bot.send_message(id_usuario, mensagem, parse_mode="Markdown")

        @self.bot.message_handler(func=lambda message: True)
        def captura_porta(porta):
            porta = porta.text

            porta_cto = valida_porta(porta)

            if porta_cto == 'não é numero':
                self.bot.send_message(id_usuario, "Digite apenas numeros, por favor!")
                time.sleep(1)
                self.solicita_porta_cto(id_usuario)

            elif porta_cto == 'porta invalida':
                self.bot.send_message(id_usuario, "Digite apenas valores entre 1 e 16")
                time.sleep(1)
                self.solicita_porta_cto(id_usuario)

            else:
                self.bot.send_message(id_usuario, f"PORTA VÁLIDA {porta_cto}")
                time.sleep(1)

                # pegando qual é a pon da cto informada
                pon_consulta = pon_cto(self.cto_validada[0])

                # verifica se tem algum ponto de acesso na agulha
                if len(self.ponto_de_acesso) == 0:
                    self.bot.send_message(id_usuario, 'Digite o contrato do cliente para continuar')
                    self.provisionamento(id_usuario)

                else:
                    #chama  afunção pra tratar os retornos da olt
                    print(self.ponto_de_acesso[0])
                    self.consulta_olt(id_usuario, self.ponto_de_acesso[0], pon_consulta)

                # limpando a lista para uma nova consulta
                self.cto_validada.clear()
                self.ponto_de_acesso.clear()
                #self.pppoe_cliente.clear()

        self.bot.register_next_step_handler_by_chat_id(chat_id, captura_porta)


    def consulta_olt(self, chat_id, ponto_de_acesso, pon):
        id_usuario = chat_id
        self.bot.send_message(id_usuario, f"Buscando na OLT...\nPON = {pon}")

        try:
            print('chamei a função busca onu na pon')
            retorno = busca_onu_na_pon(ponto_de_acesso, pon)
            
            if retorno == False:
                print('cai no false')
                
                time.sleep(1)
                self.menu_confirmacao_olt_onu_n_encontrada(id_usuario)
                
            else:
                try:
                    print('cai no else, com os paramentros')
                    
                    self.itbs, self.serial, self.modelo, self.modelo_permtido, self.posicao_na_pon, self.pon_atual, self.ponto_acesso = retorno

                    retorno_final = f'''
📌 *PROVISIONAMENTO PREENCHIDO* 📌

ℹ️ *ONU ENCONTRADA:* ℹ️

🔒 *Serial GPON:* {self.itbs}{self.serial}
💡 *Modelo:* {self.modelo}
    ''' 
                    self.bot.send_message(id_usuario, retorno_final, parse_mode="Markdown")

                    time.sleep(1)
                    self.menu_confirmacao_olt(id_usuario)
                    
                except Exception as e:
                    
                    onus_discando, posicao_na_pon, pon_atual, ponto_acesso, quantidade_onu = retorno
                       
                    print(f'erro foi: {str(e)}')
                        
                    print(onus_discando, posicao_na_pon, pon_atual, ponto_acesso, quantidade_onu)

                    mensagem = f'''
ℹ️ *Encontramos {quantidade_onu} ONU(s) disponíveis:* ℹ️
'''
                    for i, onu in enumerate(onus_discando):
                        indice = i + 1
                        fabricante = onu[1]
                        serial = onu[2]
                        modelo = onu[3]

                        mensagem += f'''
🆔 *ID:* 0{indice}
🔒 *Serial GPON:* `{fabricante}{serial}`
💡 *Modelo:* {modelo}
'''                    
                    self.bot.send_message(id_usuario, mensagem, parse_mode="Markdown")

                    self.trata_mais_de_uma_onu(onus_discando, posicao_na_pon, pon_atual, ponto_acesso, id_usuario)

        except:
            print('cai no except')
            retorno_final = busca_onu_na_pon(ponto_de_acesso, pon)

            if retorno_final == False:
                time.sleep(1)
                self.menu_confirmacao_olt_onu_n_encontrada(id_usuario)
                
                
    def trata_mais_de_uma_onu(self, onus_discando, posicao_na_pon, pon_atual, ponto_acesso, chat_id):
        id_usuario = chat_id
        mensagem = 'Copie o *Serial GPON* da _ONU_ que quer provisionar e cole aqui:'
        
        self.bot.send_message(id_usuario, mensagem, parse_mode="Markdown")
        
        self.itbs = None
        self.serial = None
        self.modelo_permtido = None
        self.posicao_na_pon = None
        self.pon_atual = None
        self.ponto_acesso = None    
        
        @self.bot.message_handler(func=lambda message: True)
        def captura_gpon(mensagem): 
            achei = False
            mensagem = mensagem.text

            for gpon  in onus_discando:
                gpon_sn = gpon[1] + gpon[2]
                modelo = gpon[3]
                
                if mensagem == gpon_sn:
                    achei = True
                    self.itbs = gpon[1]
                    self.serial = gpon[2]
                    self.modelo_permtido = gpon[-1]
                    self.posicao_na_pon = posicao_na_pon
                    self.pon_atual = pon_atual
                    self.ponto_acesso = ponto_acesso
                    
                    retorno_final = f'''
📌 *PROVISIONAMENTO PREENCHIDO* 📌

ℹ️ *ONU SELECIONADA:* ℹ️

🔒 *Serial GPON:* {gpon_sn}
💡 *Modelo:* {modelo}
''' 
                    self.bot.send_message(id_usuario, retorno_final, parse_mode="Markdown")
                    time.sleep(1)
                    self.menu_confirmacao_olt(id_usuario)
                     
            if achei is False:
                
                self.bot.send_message(id_usuario, 'Não encontrei esse gpon, verifique novamente, por favor')
            
                self.trata_mais_de_uma_onu(onus_discando, posicao_na_pon, pon_atual, ponto_acesso, chat_id)
            
        self.bot.register_next_step_handler_by_chat_id(chat_id, captura_gpon)
    
        
    def provisiona_onu(self, itbs, serial, modelo_permtido, posicao_na_pon, pon_atual, ponto_de_acesso, pppoe, chat_id):
        id_usuario = chat_id
        gpon_sn = itbs + serial
        modelo_profile = modelo_permtido
        gpon = pon_atual
        posi_disponivel = posicao_na_pon
        usuario_pppoe = pppoe
        pontode_acesso = ponto_de_acesso

        self.bot.send_message(id_usuario, '*INICIANDO O PROVISIONAMENTO...*', parse_mode="Markdown")

        resultado = provisiona(gpon, posi_disponivel, gpon_sn, modelo_profile, usuario_pppoe, pontode_acesso)

        self.bot.send_message(id_usuario, resultado, parse_mode="Markdown")

        self.pppoe_cliente.clear()

        print(self.pppoe_cliente, self.ponto_de_acesso, self.cto_validada)
        time.sleep(2)
        self.menu_principal(id_usuario)


    def consulta(self, chat_id):
        id_usuario = chat_id
        self.bot.send_message(id_usuario, "Digite os ultimos 8 números do *GPON-SN* da _ONU_", parse_mode="Markdown")
        
        @self.bot.message_handler(func=lambda message: True)
        def captura_gpon_consulta(mensagem): 
            mensagem = mensagem.text
        
            retorno = consulta_gpon(mensagem) 
            
            if retorno == 'tamanho inválido':
                self.bot.send_message(id_usuario, "Tamanho inválido 😕\nO serial gpon contém 8 caracteres alfanuméricos", parse_mode="Markdown")
                time.sleep(1)
                self.consulta(id_usuario)
                
            elif retorno == 'alfanumericos false':
                self.bot.send_message(id_usuario, "Caracteres inválidos 😕\nDigite somente letras e números", parse_mode="Markdown")
                time.sleep(1)
                self.consulta(id_usuario)
            
            else:
                self.bot.send_message(id_usuario, retorno, parse_mode="Markdown")
        
        self.bot.register_next_step_handler_by_chat_id(chat_id, captura_gpon_consulta)


    def tratativa_dos_botoes(self, call):
        id_usuario = call.message.chat.id

        if call.data == 'provisionamento':
            print('botão provisionamento chamado')
            self.provisionamento(id_usuario)

        elif call.data == 'consulta':
            print('botão consulta chamado')
            self.consulta(id_usuario)

        elif call.data == 'voltar_menu':
            print('botão voltar menu chamado')
            self.menu_principal(id_usuario)

        elif call.data == 'tentar_novamente':
            print('botão tentar novamente chamado')
            self.provisionamento(id_usuario)

        elif call.data == 'correto':
            print('botão tudo certo chamado')
            self.solicita_cto(id_usuario)

        elif call.data == 'incorreto':
            print('botão incorreto chamado')
            self.provisionamento(id_usuario)

        elif call.data == 'tudo_certo_olt':
            print('botão tudo certo olt chamado')
            self.provisiona_onu(self.itbs, self.serial, self.modelo_permtido, self.posicao_na_pon, self.pon_atual, self.ponto_acesso, self.pppoe_cliente[0], id_usuario)

        elif call.data == 'tentar_novamente_cto':
            print('botão tentar novamente cto chamado')          
            self.solicita_cto(id_usuario)

        elif call.data == 'volta_menu':
            print('botão tentar novamente cto chamado')          
            self.menu_principal(id_usuario)


    def inicia_bot(self):
        @self.bot.message_handler(func=lambda message: True)
        def escuta_msg(mensagem):
            id_usuario = mensagem.chat.id
            retorno_usuario = mensagem.text

            print('ID USUARIO', id_usuario, '>', retorno_usuario)

            if retorno_usuario == '/start':
                self.menu_principal(id_usuario)

        @self.bot.callback_query_handler(func=lambda call: True)
        def escuta_botoes(call):
            self.tratativa_dos_botoes(call)

        self.bot.infinity_polling()

# Uso da classe Provisionamento
provisionamento1 = Provisionamento()
provisionamento1.inicia_bot()
