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
        buttons = ["Нет конечно", "Может быть"]
        keyboard.add(*buttons)
        await message.answer("Правильно он поступил?", reply_markup=keyboard)
    if message.text == '20 билетов':
        await User.bilet20.set()
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        buttons = ["Да", "Нет"]
        keyboard.add(*buttons)
        await message.answer("Стоит ли давать взятки?", reply_markup=keyboard)
    if message.text == '30 билетов':
        await User.bilet30.set()
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        buttons = ["Нарушает закон", "Превышает скорость"]
        keyboard.add(*buttons)
        await message.answer("Что он делает?", reply_markup=keyboard)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)

