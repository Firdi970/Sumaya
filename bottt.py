import telebot
import sqlite3
import random
import schedule
import time
import threading
import requests

TOKEN = "8125168069:AAGHyGn8We9oM9vSAmXacaOmEfN5jIX11hY"
CHAT_ID = "6717101748"

bot = telebot.TeleBot(TOKEN)

conn = sqlite3.connect("messages.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS messages (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    type TEXT,
    text TEXT
)
""")
conn.commit()

cursor.execute("SELECT COUNT(*) FROM messages")
if cursor.fetchone()[0] == 0:
    messages = [
        ("compliment", "Ты - как роза Медины, чья красота в скромности и вере."),
        ("compliment", "Твоя улыбка — милость Аллаха, озаряющая всё вокруг."),
        ("dua", "О Аллах, сделай нас утешением друг для друга в этом мире и в ахирате."),
        ("dua", "О Аллах, защити мою любимую и подари ей счастье в обоих мирах."),
        ("quote", "«Лучший из вас тот, кто лучше всех относится к своей жене» (хадис)."),
        ("story", "Однажды караванщик увидел звезду в пустыне. Это была ты, моя Сумая."),
        ("gift", "Дарю тебе дуа о счастье и розу из сада моей души 🌹.")
    ]
    cursor.executemany("INSERT INTO messages (type, text) VALUES (?, ?)", messages)
    conn.commit()

def send_random_message():
    cursor.execute("SELECT text FROM messages ORDER BY RANDOM() LIMIT 1")
    message = cursor.fetchone()
    if message:
        bot.send_message(CHAT_ID, message[0])

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, "Ассаляму алейкум, моя Сумая 🌹! Бот работает!")
    bot.send_message(CHAT_ID, "Ассаляму алейкум, моя Сумая 🌹! Бот запущен!")

@bot.message_handler(commands=['compliment'])
def send_compliment(message):
    cursor.execute("SELECT text FROM messages WHERE type='compliment' ORDER BY RANDOM() LIMIT 1")
    compliment = cursor.fetchone()
    if compliment:
        bot.send_message(CHAT_ID, f"О моя Сумая, {compliment[0]}")

schedule.every().day.at("08:00").do(send_random_message)
schedule.every().day.at("12:00").do(send_random_message)
schedule.every().day.at("18:00").do(send_random_message)

def run_bot():
    while True:
        schedule.run_pending()
        time.sleep(60)

send_random_message()
threading.Thread(target=run_bot, daemon=True).start()
bot.polling()
