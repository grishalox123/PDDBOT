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


logging.basicConfig(level=logging.INFO)

bot = Bot(token=os.getenv('TOKEN'))

# For example use simple MemoryStorage for Dispatcher.
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
errors_count={ }
tickets_count={ }

# States
class User(StatesGroup):
    menu = State()
    bilets = State()
    bilets1 = State()
    bilets2 = State()

@dp.message_handler(state='*', commands='start')
@dp.message_handler(commands="start")
async def cmd_start(message: types.Message):
    global connection
    print(message.chat.id)
    await User.menu.set()
    photo_q = open('q.jpg', 'rb')
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = ["Начать решать"]
    keyboard.add(*buttons)
    await message.answer_photo(photo_q,caption=
                               f"Здравствуй, уважаемый(ая) <b>{message.from_user.username}</b>!\n"
                               "\n"
                               "Этот бот создан, чтобы помочь Вам подготовиться к экзамену по билетам ПДД.\n"
                               "Все билеты взяты с официальных источников.\n"
                               "Вам осталось только нажать кнопку :) \n \n<b>Желаем удачи!</b>"
                               , parse_mode='HTML', reply_markup=keyboard)

@dp.message_handler(state=User.menu)
async def menu(message: types.Message):
    global connection
    if message.text == 'Начать решать' or 'Давай попробуем!':
        await User.bilets.set()
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        buttons = ['1️⃣',
                   "2️⃣",
                   "3️⃣",
                   'Выйти']
        keyboard.add(*buttons)
        await message.answer("<b>В каком случае Вы совершите вынужденную остановку?</b>\n"
                             "\n"
                             "Варианты ответа:\n"
                             "\n"
                             " 1. Остановившись непосредственно перед пешеходным переходом, чтобы уступить "
                             " дорогу пешеходу.\n"
                             " 2. Остановившись на проезжей части из-за технической неисправности транспортного средства.\n"
                             " 3. В обоих перечисленных случаях", parse_mode='HTML', reply_markup=keyboard)

@dp.message_handler(state=User.bilets)
async def anwser_1(message: types.Message):
    global connection

    if message.text == "2️⃣":
        await User.bilets1.set()
        tickets_count[message.chat.id] = tickets_count.get(message.chat.id, 0) + 1

        photo = open('2.jpg','rb')

        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        buttons = ['1️⃣',
                   "2️⃣",
                   "3️⃣",
                   'Выйти']
        keyboard.add(*buttons)
        await message.answer_photo( photo, caption = "Можно ли Вам остановиться в указанном месте для посадки пассажира?\n"
                             "\n"
                             "Варианты ответа:\n"
                             "\n"
                             " 1. Можно.\n"
                             " 2. Можно, если Вы управляете такси.\n"
                             " 3. Нельзя", reply_markup=keyboard)
    elif message.text == "Выйти":
        await User.menu.set()
        photo_q = open('itogi.jpg', 'rb')
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        buttons = ["Давай попробуем!"]
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

@dp.message_handler(state=User.bilets1)
async def anwser_2(message: types.Message):
    global connection

    if message.text == "1️⃣":
        await User.bilets2.set()
        tickets_count[message.chat.id] = tickets_count.get(message.chat.id, 0) + 1

        photo = open('3.jpg', 'rb')

        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        buttons = ['1️⃣',
                   "2️⃣",
                   "3️⃣",
                   'Выйти']
        keyboard.add(*buttons)
        await message.answer_photo(photo, caption=
        "<b>Можно ли водителю легкового автомобиля выполнить опережение грузовых"
        "автомобилей вне населенного пункта по такой траектории?</b>\n"
        "\n"
        "Варианты ответа:\n"
        "\n"
        "1. Можно.\n"
        "2. Можно, если скорость грузовых автомобилей менее 30 км/ч.\n"
        "3. Нельзя.\n", parse_mode='HTML', reply_markup=keyboard)
    elif message.text == "Выйти":
        await User.menu.set()
        photo_q = open('itogi.jpg', 'rb')
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        buttons = ["Давай попробуем!"]
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
        await message.answer('❌<b>Подумай еще!</b>❌', parse_mode='HTML')
        errors_count[message.chat.id]= errors_count.get(message.chat.id,0) + 1


@dp.message_handler(state=User.bilets2)
async def anwser_3(message: types.Message):
    global connection

    if message.text == "1️⃣":

        tickets_count[message.chat.id] = tickets_count.get(message.chat.id, 0) + 1

        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)

        photo = open('1.jpg', 'rb')

        buttons = ['1️⃣',
                   "2️⃣",
                   "3️⃣",
                   'Выйти']
        keyboard.add(*buttons)
        await message.answer_photo(photo, caption=
        "<b>Разрешен ли Вам съезд на дорогу с грунтовым покрытием?</b>\n"
        "\n"
        "Варианты ответа:\n"
        "\n"
        " 1. Разрешен.\n "
        " 2. Разрешен только при технической неисправности транспортного средства.\n"
        " 3. Запрещен.", parse_mode='HTML', reply_markup=keyboard)
    elif message.text == "Выйти":
        await User.menu.set()
        photo_q = open('itogi.jpg', 'rb')
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        buttons = ["Давай попробуем!"]
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
        await message.answer('❌<b>Подумай еще!</b>❌', parse_mode='HTML')
        errors_count[message.chat.id]= errors_count.get(message.chat.id,0) + 1


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)

