import os
import asyncio
import requests
import threading
from flask import Flask
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Flask setup for Render
app = Flask(__name__)

@app.route('/')
def home():
    return "1xBet Converter Bot is Live!"

# Telegram Bot Token
TOKEN = "8382398265:AAF92uZPHGmB6APcl3G3yhh0oFWw39nBm8A"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    welcome_msg = (
        "🇲🇲 1xBet France to Myanmar Converter မှ ကြိုဆိုပါတယ်။\n\n"
        "ပြင်သစ် Tipster တွေဆီကရတဲ့ Code ကို ပို့ပေးပါ။\n"
        "ကျွန်တော်က အဲဒီ code ထဲမှာပါတဲ့ ပွဲစဉ်တွေကို ဖတ်ပြပေးပါမယ်။"
    )
    await update.message.reply_text(welcome_msg)

async def convert_logic(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_code = update.message.text.upper().strip()
    await update.message.reply_text(f"🔍 ပြင်သစ် Code: {user_code} ကို စစ်ဆေးနေပါတယ်...")

    # 1xBet API Headers (Browser အစစ်လို ဖြစ်အောင် လုပ်ခြင်း)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept': 'application/json',
        'Referer': 'https://1xbet.com/fr/'
    }

    try:
        # ပြင်သစ်ဆာဗာကနေ ဒေတာယူရန် (lng=en က အင်္ဂလိပ်လို ပြခိုင်းတာပါ)
        api_url = f"https://1xbet.com/service-api/betslip/get/{user_code}?lng=en&country=201"
        
        response = requests.get(api_url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            
            if data.get('success') and 'Value' in data:
                events = data['Value'].get('Events', [])
                
                if not events:
                    await update.message.reply_text("❌ ဒီ code ထဲမှာ ပွဲစဉ်များ မရှိတော့ပါ။ (သို့မဟုတ်) ပွဲပြီးသွားပါပြီ။")
                    return

                reply = f"✅ ပွဲစဉ်များ ရှာတွေ့ပါပြီ (Code: {user_code})\n"
                reply += "──────────────────\n"
                
                for i, event in enumerate(events, 1):
                    game = event.get('GameName', 'Unknown Game')
                    market = event.get('MarketName', 'Unknown Bet')
                    # အချိန်ကိုပါ ထည့်ချင်ရင် event.get('Start') ကို သုံးနိုင်ပါတယ်
                    reply += f"{i}. ⚽ {game}\n🎯 လောင်းရန်: {market}\n\n"
                
                reply += "──────────────────\n"
                reply += "⚠️ မှတ်ချက်: မြန်မာအကောင့်ထဲတွင် ဤပွဲစဉ်များကို ကိုယ်တိုင်ပြန်ရွေးပြီး Code အသစ်ထုတ်ယူပါ။"
                
                await update.message.reply_text(reply)
            else:
                await update.message.reply_text("❌ Code မှားနေသည် (သို့မဟုတ်) 1xBet ဘက်က ပိတ်ထားသည်။")
        else:
            await update.message.reply_text("🌐 Server Error: 1xBet Website ကို ဆက်သွယ်၍မရပါ။")

    except Exception as e:
        await update.message.reply_text(f"⚠️ Error ဖြစ်သွားပါသည်: {str(e)}")

async def main():
    # Application setup
    application = Application.builder().token(TOKEN).build()

    # Handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, convert_logic))

    # Bot Start
    async with application:
        await application.initialize()
        await application.start()
        await application.updater.start_polling()
        while True:
            await asyncio.sleep(1)

if __name__ == '__main__':
    # Flask ကို Thread နဲ့ Run ရန် (Render PORT check အတွက်)
    port = int(os.environ.get("PORT", 5000))
    t = threading.Thread(target=lambda: app.run(host='0.0.0.0', port=port, use_reloader=False))
    t.daemon = True
    t.start()
    
    # Bot Run ရန်
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        pass
