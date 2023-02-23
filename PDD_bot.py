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

# States
class User(StatesGroup):
    menu = State()
    bilet10 = State()
    bilet20 = State()
    bilet30 = State()

@dp.message_handler(state='*', commands='start')
@dp.message_handler(commands="start")
async def cmd_start(message: types.Message):
    global connection
    print(message.chat.id)
    await User.menu.set()
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = ["10 билетов", "20 билетов", "30 билетов"]
    keyboard.add(*buttons)
    await message.answer("Сколько билетов ты хочешь прорешать?", reply_markup=keyboard)

@dp.message_handler(state='*')
async def menu(message: types.Message):
    global connection
    if message.text == '10 билетов':
        await User.bilet10.set()
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        buttons = ['1️⃣',
                   "2️⃣",
                   "3️⃣",
                   'Выйти']
        keyboard.add(*buttons)
        await message.answer("В каком случае Вы совершите вынужденную остановку?\n"
                             "\n"
                             "Варианты ответа:\n"
                             "\n"
                             " 1. Остановившись непосредственно перед пешеходным переходом, чтобы уступить "
                             " дорогу пешеходу.\n"
                             " 2. Остановившись на проезжей части из-за технической неисправности транспортного средства.\n"
                             " 3. В обоих перечисленных случаях", reply_markup=keyboard)
    if message.text == '20 билетов':
        await User.bilet20.set()
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)

        photo = open('1.jpg', 'rb')

        buttons = ['1️⃣',
                   "2️⃣",
                   "3️⃣",
                   'Выйти']
        keyboard.add(*buttons)
        await message.answer_photo(photo, caption=
                            "Разрешен ли Вам съезд на дорогу с грунтовым покрытием?\n"
                             "\n"
                             "Варианты ответа:\n"
                             "\n"
                             " 1. Разрешен.\n "
                             " 2. Разрешен только при технической неисправности транспортного средства.\n"
                             " 3. Запрещен.", reply_markup=keyboard)
    if message.text == '30 билетов':
        await User.bilet30.set()
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        buttons = ["Нарушает закон", "Превышает скорость"]
        keyboard.add(*buttons)
        await message.answer("Что он делает?", reply_markup=keyboard)

@dp.message_handler(state='bilet10')
async def anwser_10_1(message: types.Message):
    global connection
    if message.text == "2️⃣":
        await User.bilet10.set()

        photo = open('2.jpg','rb')

        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        buttons = ['1️⃣',
                   "2️⃣",
                   "3️⃣",
                   '/Выйти']
        keyboard.add(*buttons)
        await message.answer_photo( photo, caption = "Можно ли Вам остановиться в указанном месте для посадки пассажира?\n"
                             "\n"
                             "Варианты ответа:\n"
                             "\n"
                             " 1. Можно.\n"
                             " 2. Можно, если Вы управляете такси.\n"
                             " 3. Нельзя", reply_markup=keyboard)
    if message.text == '1️⃣' or "3️⃣":
        await message.answer('❌Подумай еще!❌')




if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)

