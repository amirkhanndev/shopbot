import telebot
import requests
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

# Telegram bot tokenini qo'yish
TOKEN = '7355972337:AAHK5NL7u2gpFshTa5R_wTmmPqhX-H7eJRI'
bot = telebot.TeleBot(TOKEN)

# Backend API URL
API_URL = 'https://github.com/amirkhanndev/shopbot.git'

# /start komandasini qabul qilish
@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = InlineKeyboardMarkup()
    btn = InlineKeyboardButton('Shop Now', callback_data='shop')
    markup.add(btn)
    bot.send_message(message.chat.id, "Welcome to the Phone Accessories Store!", reply_markup=markup)

# "Shop Now" bosilganda mahsulotlar ro‘yxatini ko'rsatish
@bot.callback_query_handler(func=lambda call: call.data == 'shop')
def show_products(call):
    response = requests.get(API_URL)
    products = response.json()
    
    for product in products:
        product_text = f"*{product['name']}*\nPrice: ${product['price']}"
        markup = InlineKeyboardMarkup()
        review_button = InlineKeyboardButton('Reviews', callback_data=f"reviews_{product['id']}")
        markup.add(review_button)
        
        bot.send_photo(
            call.message.chat.id, 
            photo=open(product['image'], 'rb'),  # Mahsulot rasmni ochish
            caption=product_text, 
            parse_mode='Markdown',
            reply_markup=markup
        )

# Sharhlarni ko'rsatish
@bot.callback_query_handler(func=lambda call: call.data.startswith('reviews_'))
def show_reviews(call):
    product_id = int(call.data.split('_')[1])
    response = requests.get(API_URL)
    products = response.json()

    for product in products:
        if product['id'] == product_id:
            reviews_text = f"*Reviews for {product['name']}*\n"
            for review in product['reviews']:
                reviews_text += f"- {review['user']}: {review['comment']}\n"
            
            bot.send_message(call.message.chat.id, reviews_text, parse_mode='Markdown')

# Botni ishga tushirish
bot.polling()
