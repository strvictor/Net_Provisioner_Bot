import telebot

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
        def valida_contrato(mensagem):
            contrato = mensagem.text

            # Aqui você pode implementar a lógica de validação do contrato
            if contrato == '12345':
                self.bot.send_message(id_usuario, "Contrato válido!")
            else:
                self.bot.send_message(id_usuario, "Contrato inválido!")

        self.bot.register_next_step_handler_by_chat_id(chat_id, valida_contrato)


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

# Exemplo de uso da classe Provisionamento
provisionamento1 = Provisionamento()
provisionamento1.inicia_bot()
