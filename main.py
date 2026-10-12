import os
import threading
import telebot
from flask import Flask
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

# Render Free Server Setup
app = Flask(__name__)
@app.route('/')
def alive():
    return "Bot is live and running!"

def run_web():
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)

# Telegram Bot Setup
TOKEN = '8619695059:AAF-gsew25Ucg0UEz3jOsTBii1U89W_VNEY'
bot = telebot.TeleBot(TOKEN)
SHORTLINK = 'https://shrinkme.click/0QBj'

@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = InlineKeyboardMarkup()
    btn1 = InlineKeyboardButton("কাজ শুরু করুন 💸", url=SHORTLINK)
    markup.add(btn1)
    
    text = (
        f"স্বাগতম {message.from_user.first_name}!\n\n"
        "এটি Click 2 Cash বট। এখানে সহজ কিছু টাস্ক পূরণ করে আপনি প্রতিদিন টাকা আয় করতে পারবেন।\n"
        "আপনার আজকের টাস্ক কমপ্লিট করতে নিচের 'কাজ শুরু করুন' বাটনে ক্লিক করুন!"
    )
    bot.send_message(message.chat.id, text, reply_markup=markup)

if __name__ == "__main__":
    threading.Thread(target=run_web).start()
    bot.infinity_polling()
