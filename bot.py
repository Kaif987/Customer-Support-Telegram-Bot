import os
import telebot
from dotenv import load_dotenv
import telebot.async_telebot
load_dotenv()
from utils import get_daily_horoscope
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

# @bot.message_handler(commands=['horoscope'])
# async def sign_handler(message):
#     text = "What's yor zodiac sign?\nChoose one: *Aries*, *Taurus*, *Gemini*, *Cancer,* *Leo*, *Virgo*, *Libra*, *Scorpio*, *Sagittarius*, *Capricorn*, *Aquarius*, and *Pisces*."
#     sent_msg = bot.send_message(message.chat.id, text, parse_mode="Markdown")
#     bot.register_next_step_handler(sent_msg, day_handler)

# @bot.message_handler(commands=['customer-support'])
# async def customer_support_handler(message):
#     text = "Hi I am a **customer support agent**. How can I help you ? Please write your query"
#     sent_msg = bot.send_message(message.chat.id, text, parse_mode="Markdown")
#     bot.register_next_step_handler(sent_msg, query_handler)

# async def query_handler(message):
#     query = message.text
#     input_message = {"messages": [("user", query)]}
#     result = await customer_support.ainvoke(
#         input_message,
#         config=RunnableConfig(configurable={"thread_id": uuid4(), "passenger_id": "3442 587242"}),
#     ) 
#     await bot.send_message(message.chat.id, result["messages"][-1])


# async def day_handler(message):
#     sign = message.text
#     text = "What day do you want to know?\nChoose one: *TODAY*, *TOMORROW*, *YESTERDAY*, or a date in format YYYY-MM-DD."
#     sent_msg = bot.send_message(
#         message.chat.id, text, parse_mode="Markdown")
#     bot.register_next_step_handler(
#         sent_msg, fetch_horoscope, sign.capitalize())


# async def fetch_horoscope(message, sign):
#     day = message.text
#     horoscope = get_daily_horoscope(sign, day)
#     data = horoscope["data"]
#     horoscope_message = f'*Horoscope:* {data["horoscope_data"]}\n*Sign:* {sign}\n*Day:* {data["date"]}'
#     await bot.send_message(message.chat.id, "Here's your horoscope!")
#     await bot.send_message(message.chat.id, horoscope_message, parse_mode="Markdown")


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