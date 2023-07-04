import telebot
from telebot import types

# Criando o objeto bot
bot = telebot.TeleBot("6351402549:AAH6Vccy0PKeSEuIbjS6aOcBvrw-YSQRHt8")

# Função para lidar com o comando /start
@bot.message_handler(commands=['start'])
def handle_start(message):
    # Criando os botões
    button1 = types.InlineKeyboardButton("Provisionamento", callback_data='button1')
    button2 = types.InlineKeyboardButton("Consulta", callback_data='button2')

    # Criando o layout do teclado inline
    inline_keyboard = types.InlineKeyboardMarkup(row_width=2)
    inline_keyboard.add(button1, button2)

    # Enviando a mensagem com o teclado inline
    bot.send_message(message.chat.id, "Escolha uma opção:", reply_markup=inline_keyboard)

# Função para lidar com os botões do teclado inline
@bot.callback_query_handler(func=lambda call: True)
def handle_inline_buttons(call):
    if call.data == 'button1':
        bot.send_message(call.message.chat.id, "Chama a função provisionamento()")
    elif call.data == 'button2':
        bot.send_message(call.message.chat.id, "Chama a função consulta()")

# Iniciando o bot
bot.polling()
