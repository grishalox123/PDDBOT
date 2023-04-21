import datetime
import logging
import os
from venv import *
import aiogram.utils.markdown as md
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ParseMode
from aiogram.utils import executor
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import random



logging.basicConfig(level=logging.INFO)

bot = Bot(token=os.getenv('TOKEN'))

cred = credentials.Certificate("pddbot-e8a65-firebase-adminsdk-oeb2t-f1f7d6ecc1.json")
firebase_admin.initialize_app(cred)
storage = MemoryStorage()
errors_count={ }
tickets_count={ }
user_question={ }
db = firestore.client()
dp = Dispatcher(bot, storage=storage)

users_ref = db.collection(u'bileti')
docs = users_ref.stream()

buttons_emodji = {1 :'1️⃣', 2 : "2️⃣", 3 : "3️⃣", 4 : '4️⃣'}


docs_array=[]

for doc in docs:
    docs_array.append(doc.to_dict())



class User(StatesGroup):
    menu = State()
    bilets = State()
    bilets1 = State()

@dp.message_handler(state='*', commands='start')
@dp.message_handler(commands="start")
async def cmd_start(message: types.Message):
    global connection
    print(message.chat.id)
    photo_q = open('q.jpg', 'rb')
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = ["/begin"]
    keyboard.add(*buttons)
    await message.answer_photo(photo_q,caption=
                               f"Здравствуй, уважаемый(ая) <b>{message.from_user.username}</b>!\n"
                               "\n"
                               "Этот бот создан, чтобы помочь Вам подготовиться к экзамену по билетам ПДД.\n"
                               "Все билеты взяты с официальных источников.\n"
                               "Вам осталось только нажать кнопку :) \n \n<b>Желаем удачи!</b>"
                               , parse_mode='HTML', reply_markup=keyboard)

@dp.message_handler(state='*', commands=['begin'])
async def question(message: types.Message):
    await User.menu.set()
    errors_count[message.chat.id] = 0
    tickets_count[message.chat.id] = tickets_count.get(message.chat.id, 0) + 1

    random_index = random.randint(0, len(docs_array) - 1)
    print(docs_array[random_index])

    url = docs_array[random_index].get('url')

    variants = docs_array[random_index].get('variants').split(' | ')

    buttons = []

    user_question[message.chat.id] = {'variant': variants,'anwser': variants.index(docs_array[random_index].get('question'))+1}

    for i in range(len(variants)) :
        variants[i] = str(i+1)+'. '+variants[i]
        buttons.append(buttons_emodji.get(i+1))

    buttons.append('Выйти')

    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*buttons)
    await message.answer_photo(url,
                               caption = '<b>'+ docs_array[random_index].get('answer')+ '</b>' + '\n\n' + '\n\n'.join(variants), reply_markup=keyboard, parse_mode='HTML')

@dp.message_handler(state=User.menu)
async def anwser(message: types.Message):
    global connection

    if message.text == buttons_emodji.get(user_question.get(message.chat.id).get('anwser')):

        tickets_count[message.chat.id] = tickets_count.get(message.chat.id, 0) + 1

        random_index = random.randint(0, len(docs_array) - 1)
        print(docs_array[random_index])

        url = docs_array[random_index].get('url')

        variants = docs_array[random_index].get('variants').split(' | ')

        buttons = []

        user_question[message.chat.id] = {'variant': variants,'anwser': variants.index(docs_array[random_index].get('question'))+1}

        for i in range(len(variants)):
            variants[i] = str(i + 1) + '. ' + variants[i]
            buttons.append(buttons_emodji.get(i + 1))

        buttons.append('Выйти')

        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add(*buttons)
        await message.answer_photo(
            url,
            caption='<b>' + docs_array[random_index].get('answer') + '</b>' + '\n\n' + '\n\n'.join(variants),
            reply_markup=keyboard, parse_mode='HTML')

    elif message.text == "Выйти":
        await User.menu.set()
        photo_q = open('itogi.jpg', 'rb')
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        buttons = ["/begin"]
        keyboard.add(*buttons)
        await message.answer_photo(photo_q, caption=
        f"Количество решенных билетов : {tickets_count[message.chat.id]}\n"
        "\n"
        f"Количество ошибок : {errors_count[message.chat.id]}\n"
        "\n"
        "Попробуем еще?", reply_markup=keyboard)
        errors_count[message.chat.id]=0
        tickets_count[message.chat.id]=0
    else:
        await message.answer('❌ <b>Подумай еще!</b> ❌', parse_mode='HTML')
        errors_count[message.chat.id]= errors_count.get(message.chat.id,0) + 1



if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)

