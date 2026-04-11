import os
import requests
import threading
from flask import Flask
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Flask Setup
app = Flask(__name__)

@app.route('/')
def home():
    return "OK"

TOKEN = "8382398265:AAF92uZPHGmB6APcl3G3yhh0oFWw39nBm8A"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🇲🇲 1xBet France Code Converter\n\nCode ပို့ပေးပါ။")

async def convert_logic(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_code = update.message.text.upper().strip()
    await update.message.reply_text(f"🔍 Checking: {user_code} ...")
    
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
        await update.message.reply_text("⚠️ Server Error")

def run_bot():
    # Bot ကို start လုပ်တဲ့ နေရာမှာ အမှားနည်းအောင် လုပ်ထားပါတယ်
    application = Application.builder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, convert_logic))
    application.run_polling()

if __name__ == '__main__':
    # Bot ကို Thread နဲ့ ခွဲမောင်းမယ်
    threading.Thread(target=run_bot, daemon=True).start()
    
    # Flask ကို Main မှာ မောင်းမယ်
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
