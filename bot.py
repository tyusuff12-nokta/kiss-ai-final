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

# --- AYARLAR ---
TELEGRAM_TOKEN = "8820492539:AAFcVflzM7ofNrZRR1BhlFSSzT0qvLPKAiE"
GEMINI_API_KEY = "AIzaSyAvhDhq89VmyIj-cKkahv3qjjPZj0MHGRE"

bot = telebot.TeleBot(TELEGRAM_TOKEN)

# ESKİ BAĞLANTILARI TEMİZLE (O garip reklam mesajlarını durdurur)
bot.remove_webhook()

def ogretmen_beyni(istek):
    # En stabil ve garanti model adresi (v1 kullanıyoruz)
    url = f"https://generativelanguage.googleapis.com/v1/models/gemini-pro:generateContent?key={GEMINI_API_KEY}"
    headers = {'Content-Type': 'application/json'}
    payload = {
        "contents": [{"parts": [{"text": f"Sen uzman KPSS Tarih öğretmenisin. Konu: {istek}. 3 cümlelik hap bilgi ver."}]}]
    }
    
    try:
        response = requests.post(url, json=payload, headers=headers, timeout=20)
        res_json = response.json()
        
        if 'candidates' in res_json:
            return res_json['candidates'][0]['content']['parts'][0]['text']
        else:
            return "Şu an KPSS notlarına ulaşılamıyor, lütfen tekrar deneyin."
    except:
        return "Bağlantı hatası oluştu."

@bot.message_handler(commands=['start', 'bilgi'])
def cevapla(message):
    bot.send_chat_action(message.chat.id, 'typing')
    cevap = ogretmen_beyni("Önemli bir KPSS Tarih bilgisi")
    bot.send_message(message.chat.id, cevap)

if __name__ == "__main__":
    threading.Thread(target=run_web).start()
    print("🚀 Bot en güvenli haliyle yayında!")
    bot.infinity_polling(skip_pending=True) # Bekleyen eski mesajları görmezden gel
