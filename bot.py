import os
from dotenv import load_dotenv
load_dotenv()
from uuid import uuid4
from utility import call_agent
from telebot.async_telebot import AsyncTeleBot
import asyncio

BOT_TOKEN = os.environ.get('BOT_TOKEN')
bot = AsyncTeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start', 'hello'])
async def send_welcome(message):
    await bot.reply_to(message, "Howdy, how are you doing?")

@bot.message_handler(func=lambda msg: True)
async def echo_all(message):
    query = message.text
    result = await call_agent(msg=query, thread_id=str(uuid4()))
    await bot.send_message(message.chat.id, result.messages[-1].content , parse_mode="Markdown")

asyncio.run(bot.infinity_polling())