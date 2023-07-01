'''
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
        mensagem = 'Informe o numero do contrato, por favor!'

        id_usuario = chat_id # id do usuario
        self.bot.send_message(id_usuario, mensagem)


    # função responsável pelo menu consulta
    def consulta(self, chat_id):
        mensagem = 'em construção, aguarde...'

        id_usuario = chat_id # id do usuario
        self.bot.send_message(id_usuario, mensagem)       


    # função responsável pro iniciar a escuta do bot
    def inicia_bot(self):
        @self.bot.message_handler(func=lambda message: True)
        def escuta_msg(mensagem):
            id_usuario = mensagem.chat.id
            retorno_usuario = mensagem.text

            print(retorno_usuario)
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
'''

import telebot

bot = telebot.TeleBot('6351402549:AAH6Vccy0PKeSEuIbjS6aOcBvrw-YSQRHt8')

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    # Lógica de processamento da mensagem aqui
    bot.send_message(message.chat.id, 'Resposta')

updates = bot.get_updates()

for update in updates:
    # Processar as mensagens conforme necessário
    message = update.message
    print(message)
    bot.send_message(message.chat.id, 'Resposta')

    # Se atingir a condição desejada para parar de buscar atualizações
    #break
