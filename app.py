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
    return "Bot is Running Successfully"

# သင့်ရဲ့ Token အသစ်
TOKEN = "8382398265:AAGdhv10bZvsHB-MZxIptP872P7rFjyfaiU"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🇲🇲 1xBet France to Myanmar Converter မှ ကြိုဆိုပါတယ်။\n\nပြင်သစ် Betslip Code ကို ပို့ပေးပါ။")

async def convert_logic(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_code = update.message.text.upper().strip()
    await update.message.reply_text(f"🔍 Checking Code: {user_code} ...")
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    try:
        # 1xBet API ကို ခေါ်ယူခြင်း
        api_url = f"https://1xbet.com/service-api/betslip/get/{user_code}?lng=en&country=201"
        response = requests.get(api_url, headers=headers, timeout=15)
        
        if response.status_code == 200:
            data = response.json()
            if data.get('success') and 'Value' in data:
                events = data['Value'].get('Events', [])
                if not events:
                    await update.message.reply_text("❌ ဤ Code ထဲတွင် ပွဲစဉ်များ မရှိတော့ပါ။")
                    return

                reply = f"✅ ပွဲစဉ်စာရင်း (Code: {user_code})\n"
                reply += "──────────────────\n"
                for i, event in enumerate(events, 1):
                    game = event.get('GameName', 'Unknown Game')
                    market = event.get('MarketName', 'Unknown Bet')
                    reply += f"{i}. ⚽ {game}\n🎯 {market}\n\n"
                reply += "──────────────────\n⚠️ ဤပွဲစဉ်များကို မြန်မာအကောင့်တွင် ကိုယ်တိုင်ပြန်ရွေးပါ။"
                await update.message.reply_text(reply)
            else:
                await update.message.reply_text("❌ Code မှားယွင်းနေပါသည်။ (သို့မဟုတ်) 1xBet က Block ထားပါသည်။")
        else:
            await update.message.reply_text("🌐 Server Error: ခဏနေမှ ပြန်စမ်းကြည့်ပါ။")
    except Exception as e:
        await update.message.reply_text(f"⚠️ Error: {str(e)}")

def run_bot():
    # Telegram Bot Version 20 Standard
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
