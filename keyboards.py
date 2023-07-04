from aiogram.types import ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup


def inline_for_feedback():
    inline_kb = InlineKeyboardMarkup(row_width=2)
    inline_kb.add(
        InlineKeyboardButton(text="👍", callback_data="YES"),
        InlineKeyboardButton(text="👎", callback_data="NO")
    )
    return inline_kb


def get_main_kb():
    main_keyboard = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2).add("Generate ticket 🎟").add(
        "Download Music 🎵").add("ChatGPT 🧠").add("Report the problem ⛔")
    return main_keyboard


def get_return_button():
    kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add("Return to menu")
    return kb


def get_developer_socials():
    inline = InlineKeyboardMarkup(row_width=1)
    inline.add(
        InlineKeyboardButton(text="Instagram", url="https://www.instagram.com/_rasikrr_/")
    )
    return inline
