import telebot
import requests
import os
from flask import Flask
import threading

# RENDER İÇİN GEREKLİ WEB SUNUCUSU
app = Flask('')
@app.route('/')
def home(): return "Bot Calisiyor!"

def run_web():
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))

# --- AYARLAR ---
TELEGRAM_TOKEN = "8820492539:AAFcVflzM7ofNrZRR1BhlFSSzT0qvLPKAiE"
CHAT_ID = "1534680402"
GEMINI_API_KEY = "AIzaSyAvhDhq89VmyIj-cKkahv3qjjPZj0MHGRE"

bot = telebot.TeleBot(TELEGRAM_TOKEN)

def ogretmen_beyni(istek):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"
    # İŞTE EKSİK OLAN KRİTİK SATIR BURASIYDI:
    headers = {'Content-Type': 'application/json'}
    payload = {"contents": [{"parts": [{"text": f"Sen uzman KPSS Tarih öğretmenisin. Konu: {istek}. 3 cümlelik hap bilgi ver."}]}]}
    
    try:
        response = requests.post(url, json=payload, headers=headers, timeout=20)
        res_json = response.json()
        
        if 'candidates' in res_json:
            return res_json['candidates'][0]['content']['parts'][0]['text']
        else:
            return f"🚨 API Hatası: {res_json.get('error', {}).get('message', 'Bilinmeyen sorun')}"
    except Exception as e:
        return f"🚨 Bağlantı koptu: {str(e)}"

@bot.message_handler(commands=['start', 'bilgi'])
def cevapla(message):
    bot.send_chat_action(message.chat.id, 'typing')
    cevap = ogretmen_beyni("Önemli bir KPSS Tarih bilgisi")
    bot.send_message(message.chat.id, cevap)

if __name__ == "__main__":
    threading.Thread(target=run_web).start()
    print("🚀 Bot Render üzerinde aktif!")
    bot.infinity_polling()
