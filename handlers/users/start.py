from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart

from loader import dp
from keyboards.default import menu


@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    await message.answer(f'Здавствуйте, {message.from_user.full_name}! Вы зашли в магазин DEMO.', reply_markup=menu)
