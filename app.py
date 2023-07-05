import telebot
from telebot import types
from voalle import validacontrato, consulta_cliente
import time

class Provisionamento:

    # função principal - iniciador
    def __init__(self):
        # token do bot
        self.token = '6351402549:AAH6Vccy0PKeSEuIbjS6aOcBvrw-YSQRHt8'
        self.bot = telebot.TeleBot(self.token)
        self.user_states = {}

    # função responsável pelo menu
    def menu(self, chat_id):
        mensagem = 'Escolha uma opção:'

        id_usuario = chat_id  # id do usuario

        # Criando o layout do teclado inline
        teclado_inline = types.InlineKeyboardMarkup(row_width=1)

        # Criando os botões
        provisionar = types.InlineKeyboardButton("Provisionar Cliente", callback_data='provisionamento')
        consulta = types.InlineKeyboardButton("Consultar Cliente", callback_data='consulta')

        # Adicionando os botões ao teclado inline
        teclado_inline.add(provisionar, consulta)

        # Enviando a mensagem com o teclado inline
        self.bot.send_message(id_usuario, mensagem, reply_markup=teclado_inline)

    # função responsável pelo menu provisionamento
    def provisionamento(self, chat_id):
        mensagem = '> Informe o número do contrato, por favor!'

        id_usuario = chat_id  # id do usuário
        self.bot.send_message(id_usuario, mensagem)

        # escuta a resposta do contrato
        @self.bot.message_handler(func=lambda message: True)
        def captura_contrato(mensagem):
            contrato = mensagem.text

            mensagem_validacao = validacontrato(contrato)

            # valida retorno falso pra chamar a função provisionamento novamente
            if mensagem_validacao is False:
                mensagem = 'Opa, não aceitamos caracteres por aqui 😊\nDigite apenas números, por favor!'
                self.bot.send_message(id_usuario, mensagem)
                self.provisionamento(id_usuario)

            elif mensagem_validacao == 'contrato_bad':
                self.show_retry_menu(id_usuario)

            else:
                self.bot.send_message(id_usuario, mensagem_validacao)

        self.bot.register_next_step_handler_by_chat_id(chat_id, captura_contrato)

    # função responsável pelo menu consulta
    def consulta(self, chat_id):
        mensagem_validacao = consulta_cliente()

        id_usuario = chat_id  # id do usuario
        self.bot.send_message(id_usuario, mensagem_validacao)

    # função responsável por iniciar a escuta do bot
    def inicia_bot(self):
        @self.bot.message_handler(func=lambda message: True)
        def escuta_msg(mensagem):
            id_usuario = mensagem.chat.id
            retorno_usuario = mensagem.text

            print('ID USUARIO', id_usuario, '>', retorno_usuario)

            if retorno_usuario == '/start':
                self.menu(id_usuario)

        @self.bot.callback_query_handler(func=lambda call: True)
        def handle_inline_buttons(call):
            if call.data == 'provisionamento':
                user_id = call.from_user.id

                # Verificar se o botão já foi clicado recentemente
                if user_id in self.user_states and 'provisionamento' in self.user_states[user_id]:
                    return

                # Bloquear o clique no botão por 15 segundos
                self.user_states[user_id] = {'provisionamento': True}
                print(self.user_states)

                # Executar a ação correspondente
                self.provisionamento(call.message.chat.id)

                # Agendar a liberação do clique após 15```

                time.sleep(10)
                del self.user_states[user_id]['provisionamento']
                print(self.user_states)

            elif call.data == 'consulta':
                user_id = call.from_user.id

                # Verificar se o botão já foi clicado recentemente
                if user_id in self.user_states and 'consulta' in self.user_states[user_id]:
                    return

                # Bloquear o clique no botão por 15 segundos
                self.user_states[user_id] = {'consulta': True}
                print(self.user_states)

                # Executar a ação correspondente
                self.consulta(call.message.chat.id)

                # Agendar a liberação do clique após 15 segundos
                time.sleep(10)
                if user_id in self.user_states:
                    del self.user_states[user_id]['consulta']
                print(self.user_states)

        self.bot.infinity_polling()

    # função para exibir o menu de tentar novamente
    def show_retry_menu(self, chat_id):
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

    # função para lidar com o retorno dos botões do menu de tentar novamente
    def handle_retry_menu(self, chat_id, button_data):
        id_usuario = chat_id

        if button_data == 'voltar_menu':
            self.menu(id_usuario)
        elif button_data == 'tentar_novamente':
            self.provisionamento(id_usuario)

    # função para lidar com as ações dos botões inline
    def handle_inline_buttons(self, call):
        if call.data == 'provisionamento':
            user_id = call.from_user.id

            # Verificar se o botão já foi clicado recentemente
            if user_id in self.user_states and 'provisionamento' in self.user_states[user_id]:
                return

            # Bloquear o clique no botão por 15 segundos
            self.user_states[user_id] = {'provisionamento': True}
            print(self.user_states)

            # Executar a ação correspondente
            self.provisionamento(call.message.chat.id)

            # Agendar a liberação do clique após 30 segundos
            time.sleep(10)
            del self.user_states[user_id]['provisionamento']
            print(self.user_states)

        elif call.data == 'consulta':
            user_id = call.from_user.id

            # Verificar se o botão já foi clicado recentemente
            if user_id in self.user_states and 'consulta' in self.user_states[user_id]:
                return

            # Bloquear o clique no botão por 15 segundos
            self.user_states[user_id] = {'consulta': True}
            print(self.user_states)

            # Executar a ação correspondente
            self.consulta(call.message.chat.id)

            # Agendar a liberação do clique após 30 segundos
            time.sleep(10)
            if user_id in self.user_states:
                del self.user_states[user_id]['consulta']
            print(self.user_states)

        elif call.data == 'voltar_menu' or call.data == 'tentar_novamente':
            self.handle_retry_menu(call.message.chat.id, call.data)

    # função responsável por iniciar a escuta do bot
    def inicia_bot(self):
        @self.bot.message_handler(func=lambda message: True)
        def escuta_msg(mensagem):
            id_usuario = mensagem.chat.id
            retorno_usuario = mensagem.text

            print('ID USUARIO', id_usuario, '>', retorno_usuario)

            if retorno_usuario == '/start':
                self.menu(id_usuario)

        @self.bot.callback_query_handler(func=lambda call: True)
        def handle_inline_buttons(call):
            self.handle_inline_buttons(call)

        self.bot.infinity_polling()

# uso da classe Provisionamento
provisionamento1 = Provisionamento()
provisionamento1.inicia_bot()
