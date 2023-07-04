import sys
from aiogram import executor
from create_bot import dp
from handlers import client, other

sys.path.append(r".\databases\database.py")
from databases import database


async def start(_):
    await database.connect_database()
    print("The Bot is successfully running")


client.registration_handler_client(dp)
other.registration_handler_other(dp)

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True, on_startup=start)
