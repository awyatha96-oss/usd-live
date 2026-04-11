import os
import requests
import threading
from flask import Flask
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Flask Setup (Render Health Check အတွက်)
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is Running"

# သင့်ရဲ့ Token အသစ်ကို ဒီမှာထည့်ထားပါတယ်
TOKEN = "8382398265:AAGdhv10bZvsHB-MZxIptP872P7rFjyfaiU"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🇲🇲 1xBet Converter\n\nပြင်သစ် Code ပို့ပေးပါ။")

async def convert_logic(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_code = update.message.text.upper().strip()
    await update.message.reply_text(f"🔍 Checking: {user_code} ...")
    try:
        url = f"https://1xbet.com/service-api/betslip/get/{user_code}?lng=en&country=201"
        r = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'}, timeout=15)
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
        await update.message.reply_text("⚠️ Server Connection Error")

def run_bot():
    # ApplicationBuilder အစား Application ကို တိုက်ရိုက်သုံးပါမယ် (Version 20+)
    application = Application.builder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, convert_logic))
    print("Bot is starting polling...")
    application.run_polling(drop_pending_updates=True)

if __name__ == '__main__':
    # ၁။ Bot ကို Thread နဲ့ နောက်ကွယ်မှာ Run မယ်
    t = threading.Thread(target=run_bot, daemon=True)
    t.start()
    # ၂။ Flask ကို Main မှာ Run မယ်
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
