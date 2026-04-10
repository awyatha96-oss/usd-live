import os
import requests
from flask import Flask
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import threading

# Flask Setup
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is Running"

# Telegram Bot Token
TOKEN = "8382398265:AAF92uZPHGmB6APcl3G3yhh0oFWw39nBm8A"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🇲🇲 1xBet Converter Bot မှ ကြိုဆိုပါတယ်။\nပြင်သစ် Code ပေးပို့ပါ။")

async def convert_logic(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_code = update.message.text.upper().strip()
    await update.message.reply_text(f"🔍 ပြင်သစ် Code: {user_code} ကို စစ်ဆေးနေပါတယ်...")
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    try:
        api_url = f"https://1xbet.com/service-api/betslip/get/{user_code}?lng=en&country=201"
        response = requests.get(api_url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            if data.get('success') and 'Value' in data:
                events = data['Value'].get('Events', [])
                if not events:
                    await update.message.reply_text("❌ ပွဲစဉ်များ မရှိတော့ပါ။")
                    return

                reply = f"✅ ပွဲစဉ်များ (Code: {user_code})\n"
                reply += "──────────────────\n"
                for i, event in enumerate(events, 1):
                    game = event.get('GameName', 'Unknown Game')
                    market = event.get('MarketName', 'Unknown Bet')
                    reply += f"{i}. ⚽ {game}\n🎯 လောင်းရန်: {market}\n\n"
                reply += "──────────────────"
                await update.message.reply_text(reply)
            else:
                await update.message.reply_text("❌ Code မှားနေသည် သို့မဟုတ် ပိတ်သွားပါပြီ။")
        else:
            await update.message.reply_text("🌐 Server Error (1xBet)")
    except Exception as e:
        await update.message.reply_text(f"⚠️ Error: {str(e)}")

def run_flask():
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)

def main():
    # Flask ကို နောက်ကွယ်မှာ Run မယ်
    flask_thread = threading.Thread(target=run_flask)
    flask_thread.daemon = True
    flask_thread.start()

    # Telegram Bot ကို Run မယ်
    application = Application.builder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, convert_logic))
    
    print("Bot is starting...")
    application.run_polling()

if __name__ == '__main__':
    main()
