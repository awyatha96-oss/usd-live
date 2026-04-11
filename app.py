import os
import requests
from flask import Flask, request
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

app = Flask(__name__)

TOKEN = "8382398265:AAGdhv10bZvsHB-MZxIptP872P7rFjyfaiU"
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
                game = event.get('GameName', 'Unknown Game')
                market = event.get('MarketName', 'Unknown Bet')
                reply += f"⚽ {game}\n🎯 {market}\n\n"
            await update.message.reply_text(reply)
        else:
            await update.message.reply_text("❌ Code မတွေ့ပါ။")
    except:
        await update.message.reply_text("⚠️ Connection Error")

# Webhook Endpoint (Error တက်နေတဲ့ argument ပြဿနာကို ဒီမှာ ရှင်းထားပါတယ်)
@app.route(f'/{TOKEN}', methods=['POST'])
async def webhook_handler():
    if request.method == "POST":
        update = Update.de_json(request.get_json(force=True), application.bot)
        await application.process_update(update)
    return "OK", 200

@app.route('/')
def index():
    return "Bot is Alive"

if __name__ == '__main__':
    # Handler များထည့်ခြင်း
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, convert_logic))
    
    # Webhook ကို Telegram မှာ Register လုပ်ခြင်း
    webhook_url = f"{RENDER_URL}/{TOKEN}"
    requests.get(f"https://api.telegram.org/bot{TOKEN}/setWebhook?url={webhook_url}")
    
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
