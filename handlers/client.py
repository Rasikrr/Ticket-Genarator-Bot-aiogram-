import os
import sys
import asyncio

import keyboards
from create_bot import dp, bot, music, ai
from aiogram import types, Dispatcher
from aiogram.types import InputFile
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.dispatcher import FSMContext, storage
from keyboards import get_main_kb, get_return_button, inline_for_feedback, get_developer_socials
from datetime import datetime

sys.path.append(r".\ticket_generator\ticket_generator_2.py")
from ticket_generator import ticket_generator_2

sys.path.append(r".\databases\database.py")
from databases import database


class GenerateTicketStates(StatesGroup):
    transport_num = State()
    ticket_cost = State()


class DownloadMusic(StatesGroup):
    author_and_music = State()


class ChatGPT(StatesGroup):
    inf = State()


class Report(StatesGroup):
    report_text = State()


# Start command
async def command_start(message: types.Message):
    await database.register_users(f"{message.from_user.first_name} {message.from_user.last_name}", message.from_user.id)
    await message.answer(f"Hello, {message.from_user.first_name}", reply_markup=get_main_kb())


# Ticket generator
async def generate_ticket(message: types.Message):
    await message.answer("Write your transport number:", reply_markup=get_return_button())
    await GenerateTicketStates.transport_num.set()


async def get_ticket_number(message: types.Message, state: FSMContext):
    if message.text in ("Return to menu", "/start"):
        await finish_states(message, state)
    else:
        async with state.proxy() as data:
            data["transport_num"] = message.text
        await message.answer("Write ticket's cost:")
        await GenerateTicketStates.next()


async def get_transport_cost(message: types.Message, state: FSMContext):
    if message.text in ("Return to menu", "/start"):
        await finish_states(message, state)
    else:
        async with state.proxy() as data:
            data["transport_cost"] = message.text
        await message.answer("Wait a few seconds")
        Generator = ticket_generator_2.TicketGenerator(data["transport_num"], data["transport_cost"])
        Generator.modify_ticket()
        photo = InputFile(fr".\ticket_generator\tickets\{data['transport_num']}.jpg")
        await bot.send_photo(chat_id=message.chat.id, photo=photo)
        await message.answer("Done!")
        await state.finish()
        await asyncio.sleep(0.5)
        await main_feedback_func(f"{message.from_user.first_name} {message.from_user.last_name}",
                                 message.from_user.id, message.chat.id)


# Finish states
async def finish_states(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer("How can I help You? 😊", reply_markup=get_main_kb())


async def back_to_menu(message: types.Message):
    await message.answer("How can I help You? 😊", reply_markup=get_main_kb())


# Download music


async def download_music(message: types.Message):
    await message.answer("Write author and song name:", reply_markup=get_return_button())
    await DownloadMusic.author_and_music.set()


async def get_author_and_song(message: types.Message, state: FSMContext):
    if message.text in ("Return to menu", "/start"):
        await finish_states(message, state)
    else:
        async with state.proxy() as data:
            data["song"] = message.text
        await message.answer("Wait a few seconds")
        if music.is_exist(data["song"].title()):
            with open(fr".\music_downloader\music\{message.text.title()}.wav", "rb") as file:
                await bot.send_audio(message.chat.id, file)
        else:
            try:
                music.download_audio(data["song"])
                with open(fr".\music_downloader\music\{message.text.title()}.wav", "rb") as file:
                    await bot.send_audio(message.chat.id, file)
            except:
                await message.answer("Sorry, can not find this song")
        await DownloadMusic.author_and_music.set()


# ChatGPT


async def chatgpt(message: types.Message):
    await message.answer("Ask something from ChatGPT: ", reply_markup=get_return_button())
    await ChatGPT.inf.set()


async def ask_from_chatgpt(message: types.Message, state: FSMContext):
    if message.text in ("Return to menu", "/start"):
        await finish_states(message, state)
    else:
        try:
            await message.answer("typing...")
            async with state.proxy() as data:
                data["inf"] = message.text
            await message.answer(ai.ask_to_ai(data["inf"]))
        except:
            await message.answer("Sorry, something went wrong. Write your answer again")
        await ChatGPT.inf.set()


# Feedback
async def feedback(message_chat_id):
    await bot.send_message(message_chat_id, "Do You like my bot ⁉", reply_markup=inline_for_feedback())


async def answer_to_feedback(callback: types.CallbackQuery):
    if callback.data == "NO":
        await bot.send_message(callback.message.chat.id, "Ну я запомил...")
    elif callback.data == "YES":
        await bot.send_message(callback.message.chat.id, "Thank you 💓")
    await bot.edit_message_reply_markup(callback.message.chat.id, callback.message.message_id, reply_markup=None)
    await database.insert_feedback_data(f"{callback.from_user.first_name} {callback.from_user.last_name}",
                                        callback.from_user.id, callback.data)


async def main_feedback_func(name, user_id, chat_id):
    answer = await database.is_questioned(name, user_id)
    if answer:
        await feedback(chat_id)

# Report about problem


async def report_about_problem(message: types.Message):
    await message.answer("Talk about your problem: ",reply_markup=get_return_button())
    await Report.report_text.set()


async def get_report_text(message: types.Message, state: FSMContext):
    if message.text in ("Return to menu", "/start"):
        await finish_states(message, state)
    else:
        async with state.proxy() as data:
            data["report"] = message.text
        user_message = f"{message.from_user.first_name} {message.from_user.last_name} \n" \
                    f"{str(datetime.now()).split('.')[0]}: \n" \
                       f"{data['report']}"
        await bot.send_message(os.getenv("ADMIN_ID"), user_message)
        await message.answer("Thank you for your report! I'll be sure to fix it. 😁", reply_markup=get_developer_socials())
        await state.finish()


# Handlers registration
def registration_handler_client(dp: Dispatcher):
    dp.register_message_handler(command_start, commands=["start"])
    dp.register_message_handler(generate_ticket, text="Generate ticket 🎟")
    dp.register_message_handler(get_ticket_number, state=GenerateTicketStates.transport_num)
    dp.register_message_handler(get_transport_cost, state=GenerateTicketStates.ticket_cost)
    dp.register_message_handler(download_music, text="Download Music 🎵")
    dp.register_message_handler(chatgpt, text="ChatGPT 🧠")
    dp.register_message_handler(report_about_problem, text="Report the problem ⛔")
    dp.register_message_handler(get_report_text, state=Report.report_text)
    dp.register_message_handler(ask_from_chatgpt, state=ChatGPT.inf)
    dp.register_message_handler(get_author_and_song, state=DownloadMusic.author_and_music)
    dp.register_callback_query_handler(answer_to_feedback, lambda c: c.data in ["YES", "NO"])
    dp.register_message_handler(back_to_menu, text="Return to menu")
