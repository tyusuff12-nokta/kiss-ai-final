import telebot
import requests
import os
from flask import Flask
import threading

app = Flask('')
@app.route('/')
def home(): return "Bot Calisiyor!"

def run_web():
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))

TELEGRAM_TOKEN = "8820492539:AAFcVflzM7ofNrZRR1BhlFSSzT0qvLPKAiE"
CHAT_ID = "1534680402"
GEMINI_API_KEY = "AIzaSyAvhDhq89VmyIj-cKkahv3qjjPZj0MHGRE"

bot = telebot.TeleBot(TELEGRAM_TOKEN)

def ogretmen_beyni(istek):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"
    payload = {"contents": [{"parts": [{"text": f"Sen uzman KPSS Tarih öğretmenisin. Konu: {istek}. 3 cümlelik hap bilgi ver."}]}]}
    try:
        response = requests.post(url, json=payload, timeout=15)
        return response.json()['candidates'][0]['content']['parts'][0]['text']
    except:
        return "Şu an Gemini'ye ulaşılamadı."

@bot.message_handler(commands=['start', 'bilgi'])
def cevapla(message):
    bot.send_message(message.chat.id, ogretmen_beyni("Önemli bir KPSS Tarih bilgisi"))

if __name__ == "__main__":
    threading.Thread(target=run_web).start()
    bot.infinity_polling()
