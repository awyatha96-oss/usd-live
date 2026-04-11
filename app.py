import os
import requests
from flask import Flask, request
from telegram import Update, Bot
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Flask Setup
app = Flask(__name__)

# Bot Settings
TOKEN = "8382398265:AAGdhv10bZvsHB-MZxIptP872P7rFjyfaiU"
# Render ရဲ့ URL ကို ထည့်ပေးရပါမယ် (ဥပမာ- https://usd-live.onrender.com)
RENDER_URL = "https://usd-live.onrender.com" 

# Initialize Bot & Application
application = Application.builder().token(TOKEN).build()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🇲🇲 1xBet France Code Converter\n\nCode ပို့ပေးပါ။ ပွဲစဉ်များကို ဖတ်ပေးပါမည်။")

async def convert_logic(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_code = update.message.text.upper().strip()
    await update.message.reply_text(f"🔍 Checking: {user_code}...")
    
    headers = {'User-Agent': 'Mozilla/5.0'}
    try:
        url = f"https://1xbet.com/service-api/betslip/get/{user_code}?lng=en&country=201"
        r = requests.get(url, headers=headers, timeout=10)
        data = r.json()
        
        if data.get('success') and 'Value' in data:
            events = data['Value'].get('Events', [])
            reply = f"✅ Code: {user_code}\n\n"
            for event in events:
                reply += f"⚽ {event.get('GameName')}\n🎯 {event.get('MarketName')}\n\n"
            await update.message.reply_text(reply)
        else:
            await update.message.reply_text("❌ Code မတွေ့ပါ။")
    except:
        await update.message.reply_text("⚠️ Server Error")

# Webhook Endpoint
@app.route(f'/{TOKEN}', methods=['POST'])
async def webhook():
    if request.method == "POST":
        update = Update.de_json(request.get_json(force=True), application.bot)
        await application.process_update(update)
    return "OK", 200

@app.route('/')
def index():
    return "Bot is Alive"

# Webhook ကို Telegram မှာ Register လုပ်ခြင်း
def set_webhook():
    webhook_url = f"{RENDER_URL}/{TOKEN}"
    r = requests.get(f"https://api.telegram.org/bot{TOKEN}/setWebhook?url={webhook_url}")
    return r.json()

if __name__ == '__main__':
    # Bot Handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, convert_logic))
    
    # Webhook သတ်မှတ်ခြင်း
    set_webhook()
    
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
