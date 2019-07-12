import requests
from bs4 import BeautifulSoup
from telegram.ext import Updater, CommandHandler
import logging
import datetime
from pytz import timezone
from secret import TOKEN

updater = Updater(token=TOKEN)
dispatcher = updater.dispatcher
jobQueue = updater.job_queue

watchedProducts = []

headers = {"User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'}

start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)
dispatcher.add_handler(CommandHandler('register', registerProduct))
updater.start_polling()
jobQueue.run_daily(check_price,datetime.time(hour=19))


def start(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text=f"Hi, I am the amazon price checker, our chat id is {update.message.chat_id!s}")

def registerProduct(bot, update):
    text = update.message.text
    print(text)
    if ("https://smile.amazon.de/" not in text):
        bot.send_message(chat_id=update.message.chat_id, text="Your message does not contain a smile.amazon.de link!")
    else:
        parts = text.split()
        if (len(parts) != 2):
            bot.send_message(chat_id=update.message.chat_id, text="The format of your request was wrong. Please send it like '/register https://smile.amazon.de/gp/product/B07GDR2LYK")
        else:
            watchedProducts.append([update.message.chat_id,parts[1]])

def check_price(bot, job):
    for product in watchedProducts:
        page = requests.get(product[1], headers=headers)
        soup = BeautifulSoup(page.content, 'html.parser')

        title = soup.find(id="productTitle").get_text().strip()
        price = soup.find(id="priceblock_ourprice").get_text().strip()

        price = float(price[0:price.find(',')])

        print(title)
        print(price)
        bot.send_message(chat_id=product[0], text=f"Price of {title} is now {price} €!")