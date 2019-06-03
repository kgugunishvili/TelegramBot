import string

import config
import db_handler
from utilities import check_addition

import telebot


ALLOWED_PHONE_CHARS = list(string.digits) + ['#', '-', '+']
ALLOWED_NAME_CHARS = list(string.ascii_letters) + [' ']
FIELDS = [['Phones', 'TEXT'], ['Names', 'TEXT']]

bot = telebot.TeleBot(token=config.token)
database = db_handler.Record()

@bot.message_handler(commands=['start'])
def setup(message):
    bot.send_message(message.chat.id, "How nice to see you!")
    database.create_table(message.chat.id, fields=FIELDS)


@bot.message_handler(commands=['add'])
def send_add(message):
    uid = message.chat.id
    database.create_table(user_id=uid, fields=FIELDS)
    # message.text might look like: "/add 24135135 - Komron"
    # by default seperates by spaces
    data = message.text.split(maxsplit=3)[1:]
    data_ready = []
    # data might look like: ['24135135', '-', 'Komron']

    for element in data:
        if not element == '-':
            data_ready.append(element)

    if len(data_ready) != 2:
        bot.send_message(uid, "Data entered incorrectly!")
        return
    # phone number contains only: numbers, #, +, -
    if not check_addition(data_ready[0], ALLOWED_PHONE_CHARS):
        bot.send_message(uid, "Error! You can only enter numbers and symbols: #, +, - as your phone number.")
        return

    if not check_addition(data_ready[1], ALLOWED_NAME_CHARS):
        bot.send_message(uid, "Error! You can only enter letters as your name.")
        return

    # now data might look like: ['24135135', 'Komron']
    database.add_record(uid, data=data_ready)
    bot.send_message(uid, "Successful entry of data.")


@bot.message_handler(commands=['list'])
def list(message):
    uid = message.chat.id
    database.create_table(user_id=uid, fields=FIELDS)
    info_list = database.list_all(user_id=uid)

    if len(info_list) == 0:
        bot.send_message(uid, "Sorry, you didn't enter any contacts")
    else:
        info = ''
        for element in info_list:
            info += element[1] + ': ' + element[0] + '\n'
        bot.send_message(uid, info)


@bot.message_handler(commands=['search'])
def search(message):
    uid = message.chat.id

    demand = message.text.split(maxsplit=1)[1]
    results = database.search(user_id=uid, demand=demand)
    # results look like: [('12345',), ('54321',), ...]

    ready_results = f"Phones for {demand}:\n"

    for element in results:
        ready_results += "- " + element[0] + "\n"

    ready_results = ready_results[:-1]
    bot.send_message(uid, ready_results)




bot.polling()
