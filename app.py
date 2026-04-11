import os
import requests
import asyncio
from flask import Flask, request
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

app = Flask(__name__)

TOKEN = "8382398265:AAGdhv10bZvsHB-MZxIptP872P7rFjyfaiU"
# ပုံ (၁၃) ထဲက URL ကို အတိအကျ သုံးထားပါတယ်
RENDER_URL = "https://usd-live.onrender.com"

# Application Setup
application = Application.builder().token(TOKEN).build()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🇲🇲 1xBet France Code Converter\n\nပြင်သစ် Code ပို့ပေးပါ။")

async def convert_logic(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_code = update.message.text.upper().strip()
    await update.message.reply_text(f"🔍 စစ်ဆေးနေသည်: {user_code}...")
    try:
        url = f"https://1xbet.com/service-api/betslip/get/{user_code}?lng=en&country=201"
        r = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'}, timeout=10)
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
        await update.message.reply_text("⚠️ Connection Error")

@app.route(f'/{TOKEN}', methods=['POST'])
async def webhook(token):
    if request.method == "POST":
        update = Update.de_json(request.get_json(force=True), application.bot)
        await application.process_update(update)
    return "OK", 200

@app.route('/')
def index():
    return "Bot is Alive"

# Webhook ကို Force ပြန်လုပ်ဖို့ function
def setup_webhook():
    webhook_url = f"{RENDER_URL}/{TOKEN}"
    requests.get(f"https://api.telegram.org/bot{TOKEN}/setWebhook?url={webhook_url}")

if __name__ == '__main__':
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, convert_logic))
    
    # Bot စတင်ချိန်မှာ Webhook ကို တစ်ခါတည်း ချိတ်မယ်
    setup_webhook()
    
    port = int(os.environ.get("PORT", 5000))
    # Threading သုံးပြီး flask ကို run ပါမယ်
    app.run(host='0.0.0.0', port=port)
