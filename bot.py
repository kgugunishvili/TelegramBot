import telebot
import config
import db_handler

FIELDS = [['Phones', 'TEXT'], ['Names', 'TEXT']]

bot = telebot.TeleBot(token=config.token)
database = db_handler.Record()

@bot.message_handler(commands=['start'])
def setup(message):
    bot.send_message(message.chat.id, "How nice to see you!")
    database.create_table(message.chat.id, fields=FIELDS)

@bot.message_handler(commands=['add'])
def send_add(message):
    # message.text might look like: /add 24135135 - Komron
    # by default seperates by spaces
    data = message.text.split()[1:]
    data_ready = []
    # data might look like: ['24135135', '-', 'Komron']

    for element in data:
        if not element == '-':
            data_ready.append(element)

    # now data might look like: ['24135135', 'Komron']
    database.add_record(message.chat.id, data=data_ready)
    bot.send_message(message.chat.id, "Successful entry of data.")

@bot.message_handler(commands=['list'])
def list(message):
    pass


bot.polling()
