import pymongo
from pymongo import MongoClient

URL = 'mongodb+srv://rot:dGjVGpqqW7w2C4dO@mycluster.kpura.mongodb.net/'

client = MongoClient(URL)

mydb = client["mydatabase"]
users = mydb["users"]

from telebot import TeleBot, types
from telebot.types import Update

bot = TeleBot("1555241940:AAF94uFpVDs4S7OtoH3qI0MKi3twv_Z1TCo", threaded=False)


@bot.message_handler(commands=["start"])
def start(message):
    chat_id = message.from_user.id

    tg_id = message.from_user.id
    f_name = message.from_user.first_name
    l_name = message.from_user.last_name
    print(message.from_user)

    user = users.find_one({"tg_id": tg_id})

    if user:
        bot.send_message(chat_id, "this user has already been added")
    else:
        bot.send_message(chat_id, "Hi ^_^ I have already added you to my database")
        users.insert({
            "tg_id": message.from_user.id,
            "f_name": message.from_user.first_name,
            "l_name": message.from_user.last_name,
            "favorite_book": None,
            "favorite_person": None
        })

    msg = bot.send_message(chat_id, "write your favorite book")
    bot.register_next_step_handler(msg, book)


def book(message):
    user = users.find_one({"tg_id": message.from_user.id})
    chat_id = message.from_user.id
    text = message.text
    print(text)
    if user:
        users.update_one({"tg_id": message.from_user.id}, {"$set": {"favorite_book": text}})

    bot.send_message(chat_id, "I added your book")
    msg = bot.send_message(chat_id, "write your favorite person")
    bot.register_next_step_handler(msg, person)

def person(message):
    user = users.find_one({"tg_id": message.from_user.id})
    chat_id = message.from_user.id
    text = message.text
    print(text)
    if user:
        users.update_one({"tg_id": message.from_user.id}, {"$set": {"favorite_person": text}})

    bot.send_message(chat_id, "I added your person")

bot.polling()
