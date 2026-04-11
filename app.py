import os
import requests
import threading
from flask import Flask
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# ၁။ Render Live ဖြစ်စေရန် Web Server တည်ဆောက်ခြင်း
app = Flask(__name__)

@app.route('/')
def home():
    return "New Bot is Running Successfully", 200

# ၂။ သင်ပေးထားသော Token အသစ်
TOKEN = "8578954674:AAHBVc4nLld7lQFAF6jhTj4XC8JjICdpy7o"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🇲🇲 1xBet France Code Converter (New Bot)\n\nပြင်သစ် Code ပို့ပေးပါ။ ပွဲစဉ်အသေးစိတ်ကို ပြပေးပါမည်။")

async def convert_logic(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_code = update.message.text.upper().strip()
    await update.message.reply_text(f"🔍 စစ်ဆေးနေသည်: {user_code}...")
    
    try:
        url = f"https://1xbet.com/service-api/betslip/get/{user_code}?lng=en&country=201"
        r = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'}, timeout=15)
        data = r.json()
        
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
            reply += "──────────────────"
            await update.message.reply_text(reply)
        else:
            await update.message.reply_text("❌ Code မတွေ့ပါ။ (ပွဲပြီးသွားခြင်း သို့မဟုတ် မှားယွင်းခြင်း ဖြစ်နိုင်သည်)")
    except:
        await update.message.reply_text("⚠️ ချိတ်ဆက်မှု အဆင်မပြေပါ။ ခဏနေမှ ပြန်စမ်းပါ။")

# ၃။ Bot ကို Background တွင် Polling စနစ်ဖြင့် မောင်းနှင်ခြင်း
def run_bot():
    application = Application.builder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, convert_logic))
    print("Bot is starting polling...")
    application.run_polling(drop_pending_updates=True)

if __name__ == '__main__':
    # Bot ကို Thread တစ်ခုဖြင့် ခွဲမောင်းမည်
    t = threading.Thread(target=run_bot, daemon=True)
    t.start()
    
    # Render အတွက် Main Thread တွင် Flask ကို run မည်
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
