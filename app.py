import telebot
from voalle import validacontrato

class Provisionamento:
    # função principal - iniciador
    def __init__(self):
        # token do bot
        self.token = '6351402549:AAH6Vccy0PKeSEuIbjS6aOcBvrw-YSQRHt8'
        self.bot = telebot.TeleBot(self.token)


    # função responsável pelo menu 
    def menu(self, chat_id):
        mensagem = 'menu\n1_ /provisionamento\n2_ /consulta'

        id_usuario = chat_id # id do usuario
        self.bot.send_message(id_usuario, mensagem)


    # função responsável pelo menu provisionamento
    def provisionamento(self, chat_id):
        mensagem = 'Informe o número do contrato, por favor!'
        
        id_usuario = chat_id  # id do usuário
        self.bot.send_message(id_usuario, mensagem)

        # escuta a resposta do contrato
        @self.bot.message_handler(func=lambda message: True)
        def captura_contrato(mensagem):
            contrato = mensagem.text

            mensagem_valicacao = validacontrato(contrato)
            self.bot.send_message(id_usuario, mensagem_valicacao)

        self.bot.register_next_step_handler_by_chat_id(chat_id, captura_contrato)

    # função responsável pelo menu consulta
    def consulta(self, chat_id):
        mensagem = 'em construção, aguarde...'

        id_usuario = chat_id # id do usuario
        self.bot.send_message(id_usuario, mensagem)       


    # função responsável por iniciar a escuta do bot
    def inicia_bot(self):
        @self.bot.message_handler(func=lambda message: True)
        def escuta_msg(mensagem):
            id_usuario = mensagem.chat.id
            retorno_usuario = mensagem.text

            print('ID USUARIO', id_usuario, '>', retorno_usuario)
            
            if retorno_usuario == '/start' or retorno_usuario == '/menu':
                self.menu(id_usuario)

            elif retorno_usuario == '/provisionamento':
                self.provisionamento(id_usuario)

            elif retorno_usuario == '/consulta':
                self.consulta(id_usuario)      


        self.bot.infinity_polling()

# uso da classe Provisionamento
provisionamento1 = Provisionamento()
provisionamento1.inicia_bot()
