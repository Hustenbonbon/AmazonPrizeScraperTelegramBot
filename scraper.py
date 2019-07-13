import requests
from bs4 import BeautifulSoup
import logging
import datetime
from pytz import timezone
from telegram.ext import Updater, CommandHandler
from secret import TOKEN

def send_updates(bot, job):
    for product in watchedProducts:
        title, price = check_price(product)
        bot.send_message(chat_id=product[0], text=f"Price of {title} is now {price} €!")

def start(bot, update):
    text = update.message.text
    print(text)
    emoji = u'\U0001F609'
    bot.send_message(chat_id=update.message.chat_id, text=f"Hi, I am the amazon price checker! Type '/register https://smile.amazon.de/gp/product/PRODUCT_LINK' to let me watch a product for you, I'll send you price updates daily {emoji!s}")

def registerProduct(bot, update):
    text = update.message.text
    print(text)
    if (".amazon.de/" not in text):
        bot.send_message(chat_id=update.message.chat_id, text="Your message does not contain an amazon.de link!")
        print("test12")
    else:
        print("test0")
        parts = text.split()
        if (len(parts) != 2):
            print("test5")
            bot.send_message(chat_id=update.message.chat_id, text="The format of your request was wrong. Please send it like '/register https://smile.amazon.de/gp/product/B07GDR2LYK")
        else:
            print("testX")
            watchedProducts.append([update.message.chat_id,parts[1]])
            print(parts[1])
            title, price = check_price(parts[1])
            print("test2")
            bot.send_message(chat_id=update.message.chat_id, text=f"Checking for {title} with current price {price} € daily")

def check_price(url):
    print("url " + url)
    page = requests.get(url, headers=HEADERS)
    soup = BeautifulSoup(page.content, 'html.parser')

    title = soup.find(id="productTitle").get_text().strip()
    price = soup.find(id="priceblock_ourprice").get_text().strip()

    price = price[0:price.find(',')]

    return title, price

watchedProducts = []

HEADERS = {"User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'}


updater = Updater(token=TOKEN)
dispatcher = updater.dispatcher
jobQueue = updater.job_queue

start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)
dispatcher.add_handler(CommandHandler('register', registerProduct))
updater.start_polling()
jobQueue.run_daily(send_updates,datetime.time(hour=15, minute=51))