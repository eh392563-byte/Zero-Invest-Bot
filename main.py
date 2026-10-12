import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton

# আপনার বটের টোকেন এবং অ্যাডমিন আইডি বসানো আছে
BOT_TOKEN = "8619695059:AAF-gsew25Ucg0UEz3jOsTBii1U89W_VNEY"
ADMIN_ID = 6048990081

bot = telebot.TeleBot(BOT_TOKEN)

# রেগুলার কাজের লিংক সেভ রাখার ভেরিয়েবল
regular_task_link = "https://globalfinanceinfo24.blogspot.com"

# ইউজারদের ব্যালেন্স সেভ রাখার জন্য 
user_balances = {}

# /start কমান্ড এবং মেইন মেনু
@bot.message_handler(commands=['start'])
def send_welcome(message):
    user_id = message.chat.id
    if user_id not in user_balances:
        user_balances[user_id] = 0.0

    # কীবোর্ড বাটন তৈরি
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = KeyboardButton("🎯 রেগুলার কাজ")
    btn2 = KeyboardButton("💰 ব্যালেন্স")
    btn3 = KeyboardButton("💳 উত্তোলন")
    markup.add(btn1, btn2)
    markup.add(btn3)

    bot.send_message(
        user_id,
        "স্বাগতম! Global Finance আর্নিং বটে আপনাকে স্বাগতম।\nনিচের বাটনগুলো ব্যবহার করে কাজ শুরু করুন:",
        reply_markup=markup
    )

# অ্যাডমিন কমান্ড: লিংক পরিবর্তন করার জন্য (/setregular)
@bot.message_handler(commands=['setregular'])
def set_regular_link(message):
    global regular_task_link
    user_id = message.chat.id
    
    if str(user_id) == str(ADMIN_ID):
        try:
            new_link = message.text.split()[1]
            regular_task_link = new_link
            bot.reply_to(message, f"✅ রেগুলার কাজের লিংক সফলভাবে আপডেট করা হয়েছে:\n{regular_task_link}")
        except IndexError:
            bot.reply_to(message, "⚠️ সঠিক নিয়ম: /setregular <আপনার-লিংক>")
    else:
        bot.reply_to(message, "⛔ আপনার এই কমান্ডটি ব্যবহার করার অনুমতি নেই।")

# "রেগুলার কাজ" বাটনের কাজ
@bot.message_handler(func=lambda message: message.text in ['🎯 রেগুলার কাজ', 'রেগুলার কাজ'])
def send_regular_task(message):
    text = (
        "🎯 **আজকের টাস্ক:**\n\n"
        "১. নিচের লিংকে ক্লিক করে ওয়েবসাইটে যান।\n"
        "২. সাইটের যেকোনো একটি বিজ্ঞাপনে (অ্যাড) ক্লিক করুন।\n"
        "৩. অ্যাড ওপেন হওয়ার পর ১৫-২০ সেকেন্ড অপেক্ষা করুন।\n"
        "৪. এরপর একটি স্ক্রিনশট নিয়ে এখানে জমা দিন।\n\n"
        f"🌐 **লিংক:** {regular_task_link}"
    )
    bot.reply_to(message, text, parse_mode='Markdown')

# "ব্যালেন্স" বাটনের কাজ
@bot.message_handler(func=lambda message: message.text in ['💰 ব্যালেন্স', 'ব্যালেন্স'])
def show_balance(message):
    user_id = message.chat.id
    balance = user_balances.get(user_id, 0.0)
    bot.reply_to(message, f"আপনার বর্তমান ব্যালেন্স: {balance} টাকা")

# "উত্তোলন" বাটনের কাজ
@bot.message_handler(func=lambda message: message.text in ['💳 উত্তোলন', 'উত্তোলন'])
def withdraw_money(message):
    bot.reply_to(message, "উত্তোলন করার জন্য আপনার অ্যাকাউন্টে পর্যাপ্ত ব্যালেন্স থাকতে হবে। বিস্তারিত জানতে অ্যাডমিনের সাথে যোগাযোগ করুন।")

# টাস্ক কমপ্লিট (ইউজার স্ক্রিনশট বা ছবি পাঠালে যা হবে)
@bot.message_handler(content_types=['photo'])
def handle_screenshot(message):
    user_id = message.chat.id
    
    if user_id in user_balances:
        user_balances[user_id] += 2.0
    else:
        user_balances[user_id] = 2.0
        
    bot.reply_to(message, "✅ আপনার টাস্ক সফলভাবে সম্পন্ন হয়েছে! আপনার অ্যাকাউন্টে ২ টাকা যোগ করা হয়েছে।")

print("বট সফলভাবে চালু হয়েছে...")
bot.polling(none_stop=True)
