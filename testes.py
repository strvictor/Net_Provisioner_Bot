# import telebot
# from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

# # Substitua "SEU_TOKEN_DO_BOT" pelo token real do seu bot
# bot = telebot.TeleBot("5935745695:AAHcP4dAquoEEg0pv9YOlj0HHLiofldVMY4")

# @bot.message_handler(commands=['popup'])
# def exibir_teclado(message):
#     # O chat_id é usado para responder ao mesmo chat onde o comando foi enviado
#     chat_id = message.chat.id

#     # Texto da mensagem que será exibida antes do teclado
#     texto = "Clique no botão abaixo para ver o conteúdo do pop-up."

#     # Crie o teclado personalizado
#     keyboard = InlineKeyboardMarkup()
#     button = InlineKeyboardButton(text="Mostrar Pop-up", callback_data="mostrar_popup")
#     keyboard.add(button)

#     # Envie a mensagem com o teclado personalizado
#     bot.send_message(chat_id, texto, reply_markup=keyboard)

# @bot.callback_query_handler(func=lambda call: call.data == "mostrar_popup")
# def mostrar_popup(callback_query):
#     # O chat_id é usado para responder ao mesmo chat onde o teclado foi exibido
#     chat_id = callback_query.message.chat.id
#     print(callback_query.id)


#     # Texto do pop-up
#     popup_text = "Por medida de segurança irei excluir a mensagem que me informou a senha."

#     # Envie o pop-up como resposta ao callback
#     bot.answer_callback_query(callback_query.id, popup_text, show_alert=True, cache_time=1)
#     bot.answer_inline_query

# # Inicie o bot
# bot.polling()



# import telebot, time

# # Substitua "SEU_TOKEN_DO_BOT" pelo token real do seu bot
# bot = telebot.TeleBot("5935745695:AAHcP4dAquoEEg0pv9YOlj0HHLiofldVMY4")

# @bot.message_handler(commands=['start'])
# def send_welcome(message):
#     # Envia uma ação de chat "digitando..." quando o usuário envia o comando /start
#     bot.send_chat_action(message.chat.id, 'typing')

#     # Simula um processamento pesado por 3 segundos
#     time.sleep(2)

#     # Envia uma mensagem de boas-vindas após o processamento
#     bot.reply_to(message, "Olá! Bem-vindo ao meu bot.")

# # Inicie o bot
# bot.polling()


# import telebot

# # Substitua "SEU_TOKEN_DO_BOT" pelo token real do seu bot
# bot = telebot.TeleBot("5935745695:AAHcP4dAquoEEg0pv9YOlj0HHLiofldVMY4")

# @bot.message_handler(commands=['location'])
# def send_location(message):
#     # Envia informações sobre um local específico
#     bot.send_venue(message.chat.id, latitude=-2.418652, longitude=-48.241671, title='CLIENTE X', address='Tomé-Açu - PA')

# # Inicie o bot
# bot.polling()





# import telebot

# # Crie uma instância do bot com o token do seu bot
# bot = telebot.TeleBot('5935745695:AAHcP4dAquoEEg0pv9YOlj0HHLiofldVMY4')

# # ID do chat para o qual você deseja enviar o adesivo
# chat_id = '5138023764'

# # Caminho para o arquivo do adesivo (sticker) que você deseja enviar
# caminho_adesivo = r'C:\Users\victor.silva\Downloads\sticker.png'

# # Envie o adesivo


# # Inicie o bot
# bot.polling()



from loguru import logger

# Configuração básica para imprimir logs no console
logger.add(
    "file.log",
    level="DEBUG",
    format="{time:DD-MM-YYYY HH:mm:ss} {level} {message}",
    rotation="10 MB"
)

# Exemplos de logs
debug = logger.debug("teste")
info = logger.info("usuario cadastrado")
warning = logger.warning("não provisionado")
error = logger.error("olt off")


