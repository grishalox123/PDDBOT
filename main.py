import aiogram
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

token_api = "5661460090:AAHOPwFI4pT_eA-Ge8vcMEk3X_LbC7GLZFo"

bot = Bot(token_api)
dp = Dispatcher(bot)

kb = ReplyKeyboardMarkup(resize_keyboard=True)
kb.add(KeyboardButton('10 билетов'))
kb.add(KeyboardButton('20 билетов'))
kb.add(KeyboardButton('30 билетов'))
kb.add(KeyboardButton('40 билетов'))

keyb = ReplyKeyboardMarkup(resize_keyboard=True)
keyb.add(KeyboardButton("Правильно"))
keyb.insert(KeyboardButton("Не правильно"))
keyb.add(KeyboardButton("Круто"))
keyb.insert(KeyboardButton("Классно"))
keyb.add(KeyboardButton("Выйти"))

@dp.message_handler(commands=['start'])
async def start_command(message: types.message):
    await message.answer("<b>Салам алейкум!</b> Выбери сколько вопросов ты хочешь прорешать.",
                         parse_mode="HTML",
                         reply_markup=kb)

@dp.message_handler(text=["10 билетов"])
async def t10(message: types.message):
    await message.answer('Выбери правильный ответ.',
                           reply_markup=keyb)

@dp.message_handler(text=["20 билетов"])
async def t20(message: types.message):
    await message.answer('Выбери правильный ответ.',
                           reply_markup=keyb)

@dp.message_handler(text=["30 билетов"])
async def t30(message: types.message):
    await message.answer('Выбери правильный ответ.',
                           reply_markup=keyb)

@dp.message_handler(text=["40 билетов"])
async def t40(message: types.message):
    await message.answer('Выбери правильный ответ.',
                           reply_markup=keyb)

@dp.message_handler(text=['Выйти'])
async def open_st(message: types.message):
    await message.answer('Вы успешно вышли.',
                         reply_markup=kb)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)