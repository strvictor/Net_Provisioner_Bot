import telebot, time
from telebot import types
from voalle import validacontrato, consulta_cliente
from cto import valida_cto, valida_porta, pon_cto

class Provisionamento():
    def __init__(self):
        self.token = '5935745695:AAHcP4dAquoEEg0pv9YOlj0HHLiofldVMY4'
        self.bot = telebot.TeleBot(self.token)
        self.cto_validada = list()


    def menu_principal(self, chat_id):
        mensagem = 'Escolha uma opção:'
        id_usuario = chat_id

        # Criando o layout do teclado inline
        teclado_inline = types.InlineKeyboardMarkup(row_width=1)

        # Criando os botões
        provisionar = types.InlineKeyboardButton("Provisionar Cliente", callback_data='provisionamento')
        consulta = types.InlineKeyboardButton("Consultar Cliente", callback_data='consulta')

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
                if mensagem_validacao:
                    self.bot.send_message(id_usuario, mensagem_validacao)
                else:
                    self.bot.send_message(id_usuario, "Erro: Mensagem vazia ou inválida.")

                time.sleep(3)
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
                time.sleep(2)
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
                time.sleep(2)

                # pegando qual é a pon da cto informada
                pon_consulta = pon_cto(self.cto_validada[0])

                # enviando informções da pon valida
                self.bot.send_message(id_usuario, f"Buscando na OLT...\nPON = {pon_consulta}")

                # limpando a lista para uma nova consulta
                self.cto_validada.clear()

        self.bot.register_next_step_handler_by_chat_id(chat_id, captura_porta)


    def consulta(self, chat_id):
        mensagem = consulta_cliente()
        id_usuario = chat_id
        self.bot.send_message(id_usuario, mensagem)

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
