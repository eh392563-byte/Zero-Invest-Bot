import os
import threading
import sqlite3
import telebot
from flask import Flask
from telebot.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

# Render Free Server Setup
app = Flask(__name__)
@app.route('/')
def alive():
    return "Advanced Bot is live and running!"

def run_web():
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)

# Telegram Bot Setup
TOKEN = '8619695059:AAF-gsew25Ucg0UEz3jOsTBii1U89W_VNEY'
bot = telebot.TeleBot(TOKEN)
ADMIN_ID = 6048990081  # আপনার অ্যাডমিন আইডি লক করা হয়েছে

# Database Setup
conn = sqlite3.connect('bot_database.db', check_same_thread=False)
cursor = conn.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS users (user_id INTEGER PRIMARY KEY, name TEXT, balance REAL, tasks INTEGER)''')
cursor.execute('''CREATE TABLE IF NOT EXISTS settings (key TEXT PRIMARY KEY, value TEXT)''')
conn.commit()

# Default Links Setup
cursor.execute("INSERT OR IGNORE INTO settings (key, value) VALUES ('cpa_link', 'https://example.com')")
cursor.execute("INSERT OR IGNORE INTO settings (key, value) VALUES ('regular_link', 'https://shrinkme.click/0QBj')")
conn.commit()

def get_setting(key):
    cursor.execute("SELECT value FROM settings WHERE key=?", (key,))
    res = cursor.fetchone()
    return res[0] if res else ""

def set_setting(key, value):
    cursor.execute("UPDATE settings SET value=? WHERE key=?", (value, key))
    conn.commit()

# Main Menu Design
def main_menu():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row(KeyboardButton("👤 আমার প্রোফাইল"), KeyboardButton("💳 উইথড্র"))
    markup.row(KeyboardButton("🔗 রেগুলার কাজ"), KeyboardButton("🌟 প্রিমিয়াম কাজ"))
    return markup

# Start Command & Registration
@bot.message_handler(commands=['start'])
def send_welcome(message):
    user_id = message.from_user.id
    name = message.from_user.first_name
    
    # Register New User in Database
    cursor.execute("SELECT * FROM users WHERE user_id=?", (user_id,))
    if not cursor.fetchone():
        cursor.execute("INSERT INTO users (user_id, name, balance, tasks) VALUES (?, ?, 0.0, 0)", (user_id, name))
        conn.commit()
        
    text = (
        f"স্বাগতম {name}!\n\n"
        "এটি Click 2 Cash বট। এখানে কাজ করে প্রতিদিন টাকা আয় করতে পারবেন। "
        "নিচের মেনু থেকে আপনার কাজ বেছে নিন:"
    )
    bot.send_message(message.chat.id, text, reply_markup=main_menu())

# Profile Button
@bot.message_handler(func=lambda message: message.text == "👤 আমার প্রোফাইল")
def profile(message):
    user_id = message.from_user.id
    cursor.execute("SELECT balance, tasks FROM users WHERE user_id=?", (user_id,))
    res = cursor.fetchone()
    if res:
        bal, tasks = res
        text = f"👤 **আপনার প্রোফাইল**\n\n🆔 আইডি: `{user_id}`\n💰 ব্যালেন্স: **${bal:.3f}**\n✅ মোট সম্পন্ন কাজ: {tasks} টি"
        bot.send_message(message.chat.id, text, parse_mode="Markdown")

# Regular Task (ShrinkMe + Adsterra)
@bot.message_handler(func=lambda message: message.text == "🔗 রেগুলার কাজ")
def regular_task(message):
    link = get_setting('regular_link')
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("রেগুলার কাজ শুরু করুন (+$0.001)", url=link))
    bot.send_message(message.chat.id, "🔹 **রেগুলার কাজ (ছোট কাজ)**\n\nনিচের লিংকে ক্লিক করে টাস্ক কমপ্লিট করুন। কাজ শেষ হলে একটি স্ক্রিনশট এখানে জমা দিন।", reply_markup=markup, parse_mode="Markdown")

# Premium Task (CPA)
@bot.message_handler(func=lambda message: message.text == "🌟 প্রিমিয়াম কাজ")
def premium_task(message):
    link = get_setting('cpa_link')
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("প্রিমিয়াম অফার কমপ্লিট করুন (+$0.03)", url=link))
    bot.send_message(message.chat.id, "🌟 **প্রিমিয়াম কাজ (বড় কাজ)**\n\nনিচের লিংকে গিয়ে অফারটি (যেমন: ইমেইল সাবমিট বা সাইন-আপ) সম্পূর্ণ করুন এবং কাজের প্রমাণস্বরূপ স্ক্রিনশট এখানে আপলোড করুন।", reply_markup=markup, parse_mode="Markdown")

# Withdraw Button
@bot.message_handler(func=lambda message: message.text == "💳 উইথড্র")
def withdraw(message):
    user_id = message.from_user.id
    cursor.execute("SELECT balance FROM users WHERE user_id=?", (user_id,))
    res = cursor.fetchone()
    if res and res[0] >= 0.20:
        bot.send_message(message.chat.id, "✅ আপনার ব্যালেন্স উইথড্র করার জন্য যথেষ্ট ($0.20+)। দয়া করে আপনার বিকাশ/নগদ নাম্বার এবং টাকার পরিমাণ লিখে মেসেজ দিন।")
    else:
        bot.send_message(message.chat.id, "❌ আপনার পর্যাপ্ত ব্যালেন্স নেই। উইথড্র করতে কমপক্ষে $0.20 লাগবে।")

# Handle Screenshot Uploads
@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    bot.send_message(message.chat.id, "✅ আপনার কাজের প্রমাণ (স্ক্রিনশট) জমা দেওয়া হয়েছে! অ্যাডমিন চেক করে আপনার ব্যালেন্সে টাকা যোগ করে দেবেন।")
    
    # Forward screenshot to Admin
    caption = f"📸 **নতুন কাজের প্রমাণ!**\n\n👤 ইউজার নাম: {message.from_user.first_name}\n🆔 ইউজার আইডি: `{message.from_user.id}`\n\n_চেক করে ব্যালেন্স অ্যাড করতে কমান্ড দিন:_\n`/add {message.from_user.id} 0.001` (রেগুলার কাজের জন্য)\n`/add {message.from_user.id} 0.03` (প্রিমিয়াম কাজের জন্য)"
    bot.send_photo(ADMIN_ID, message.photo[-1].file_id, caption=caption, parse_mode="Markdown")

# ================= ADMIN PANEL COMMANDS =================

@bot.message_handler(commands=['admin'])
def admin_panel(message):
    if message.from_user.id == ADMIN_ID:
        text = (
            "👨‍💻 **অ্যাডমিন কন্ট্রোল প্যানেল**\n\n"
            "🔹 `/users` - বটের মোট ইউজার দেখুন\n"
            "🔹 `/setcpa [লিংক]` - প্রিমিয়াম কাজের লিংক পরিবর্তন করুন\n"
            "🔹 `/add [ইউজার_আইডি] [টাকার_পরিমাণ]` - যে কাউকে ব্যালেন্স দিন"
        )
        bot.send_message(message.chat.id, text, parse_mode="Markdown")
    else:
        bot.send_message(message.chat.id, "❌ আপনি এই বটের অ্যাডমিন নন!")

@bot.message_handler(commands=['setcpa'])
def set_cpa(message):
    if message.from_user.id == ADMIN_ID:
        try:
            link = message.text.split()[1]
            set_setting('cpa_link', link)
            bot.reply_to(message, f"✅ প্রিমিয়াম কাজের CPA লিংক আপডেট করা হয়েছে:\n{link}")
        except:
            bot.reply_to(message, "⚠️ সঠিক নিয়ম: `/setcpa https://আপনার-লিংক.com`", parse_mode="Markdown")

@bot.message_handler(commands=['add'])
def add_balance(message):
    if message.from_user.id == ADMIN_ID:
        try:
            parts = message.text.split()
            target_id = int(parts[1])
            amount = float(parts[2])
            cursor.execute("UPDATE users SET balance = balance + ?, tasks = tasks + 1 WHERE user_id=?", (amount, target_id))
            conn.commit()
            bot.reply_to(message, f"✅ সফলভাবে `{target_id}` আইডিতে ${amount} যোগ করা হয়েছে।", parse_mode="Markdown")
            bot.send_message(target_id, f"🎉 অভিনন্দন! আপনার একটি টাস্ক অ্যাপ্রুভ হয়েছে এবং আপনার অ্যাকাউন্টে **${amount}** যোগ করা হয়েছে!")
        except:
            bot.reply_to(message, "⚠️ সঠিক নিয়ম: `/add UserID Amount`\nযেমন: `/add 123456789 0.001`", parse_mode="Markdown")

@bot.message_handler(commands=['users'])
def total_users(message):
    if message.from_user.id == ADMIN_ID:
        cursor.execute("SELECT COUNT(*) FROM users")
        count = cursor.fetchone()[0]
        bot.reply_to(message, f"👥 বটে বর্তমানে মোট ইউজার আছে: **{count} জন**", parse_mode="Markdown")

if __name__ == "__main__":
    threading.Thread(target=run_web).start()
    bot.infinity_polling()
