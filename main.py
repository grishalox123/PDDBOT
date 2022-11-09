import telebot
from telebot import types

bot = telebot.TeleBot('5661460090:AAHOPwFI4pT_eA-Ge8vcMEk3X_LbC7GLZFo')

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    mess = f'Ассалам алейкум, <b>{message.from_user.first_name}</b>! Выбери количество билетов для капитального прорешивания.'
    tickets10 = types.KeyboardButton('10 билетов')
    tickets25 = types.KeyboardButton('25 билетов')
    tickets50 = types.KeyboardButton('50 билетов')
    markup.add(tickets10, tickets25, tickets50)
    bot.send_message(message.chat.id, mess, reply_markup=markup, parse_mode='html')

@bot.message_handler(content_types=['text'])
def text(message):
    get_message_bot = message.text.strip().lower()

    if get_message_bot == "10 билетов":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        a = types.KeyboardButton('Да')
        b = types.KeyboardButton('Нет')
        c = types.KeyboardButton('Может быть')
        d = types.KeyboardButton('Не знаю')
        markup.add(a, b, d, c)
        final_mess = "Что из этого правильно?"
    else:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        final_mess = "Похоже ты выбрал что-то не то."

    bot.send_message(message.chat.id, final_mess, reply_markup=markup)


bot.polling(none_stop=True)

