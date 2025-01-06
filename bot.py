import os
from dotenv import load_dotenv
load_dotenv()
from customer_support_multiagent import customer_support
from uuid import uuid4
from langchain_core.runnables import RunnableConfig
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
    input_message = {"messages": [("user", query)]}
    result = await customer_support.ainvoke(
        input_message,
        config=RunnableConfig(configurable={"thread_id": uuid4(), "passenger_id": "3442 587242"}),
    )  
    await bot.send_message(message.chat.id, result["messages"][-1].content, parse_mode="Markdown")

asyncio.run(bot.infinity_polling())