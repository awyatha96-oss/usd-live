import os
import requests
import threading
from flask import Flask
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# ၁။ Render အတွက် Web Server Setup
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is Alive", 200

# ၂။ Bot Logic
TOKEN = "8382398265:AAGdhv10bZvsHB-MZxIptP872P7rFjyfaiU"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🇲🇲 1xBet France Code Converter\n\nပြင်သစ် Code ပို့ပေးပါ။")

async def convert_logic(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_code = update.message.text.upper().strip()
    await update.message.reply_text(f"🔍 စစ်ဆေးနေသည်: {user_code}...")
    
    try:
        url = f"https://1xbet.com/service-api/betslip/get/{user_code}?lng=en&country=201"
        r = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'}, timeout=15)
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

# ၃။ Bot ကို Background မှာ Run မည့် Function
def run_bot():
    # အသစ်ဆုံး Version 20 ပုံစံ
    application = Application.builder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, convert_logic))
    print("Bot is starting...")
    application.run_polling(drop_pending_updates=True)

if __name__ == '__main__':
    # Bot ကို Thread နှင့် ခွဲမောင်းမည်
    bot_thread = threading.Thread(target=run_bot, daemon=True)
    bot_thread.start()
    
    # Flask ကို Main Thread တွင် Run မည် (ဒါမှ Render က Live ပေးမှာပါ)
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
