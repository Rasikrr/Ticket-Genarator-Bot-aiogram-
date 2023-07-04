from create_bot import dp, bot
from aiogram import types, Dispatcher, filters


async def other_words(message: types.Message):
    await message.answer("Don't understand you")


def registration_handler_other(dp: Dispatcher):
    dp.register_message_handler(other_words)