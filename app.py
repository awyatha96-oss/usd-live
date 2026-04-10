import os
import asyncio
from flask import Flask
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Flask setup (Render keep-alive အတွက်)
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is alive!"

# Telegram Bot Token
TOKEN = "8382398265:AAF92uZPHGmB6APcl3G3yhh0oFWw39nBm8A"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("မင်္ဂလာပါ။ 1xBet ပြင်သစ် Betslip Code ပို့ပေးပါ။")

async def convert(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_code = update.message.text.upper().strip()
    await update.message.reply_text(f"ပြင်သစ် Code: {user_code} ကို လက်ခံရရှိပါပြီ။ မြန်မာ Code ပြောင်းလဲရန် ကြိုးစားနေဆဲ ဖြစ်ပါသည်။")

async def main():
    # Application တည်ဆောက်ခြင်း
    application = Application.builder().token(TOKEN).build()

    # Handler များ ထည့်ခြင်း
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, convert))

    # Bot ကို စတင်ခြင်း
    async with application:
        await application.initialize()
        await application.start()
        await application.updater.start_polling()
        
        # Render အတွက် Flask ကိုပါ တစ်ခါတည်း run ရန် (Thread သုံးရမည် သို့မဟုတ် ရိုးရိုး run မည်)
        # လောလောဆယ် bot သီးသန့် run ဖို့ပဲ အာရုံစိုက်ပါမယ်
        while True:
            await asyncio.sleep(1)

if __name__ == '__main__':
    # Render က PORT တောင်းတာကို ဖြေရှင်းရန်
    import threading
    port = int(os.environ.get("PORT", 5000))
    threading.Thread(target=lambda: app.run(host='0.0.0.0', port=port, use_reloader=False)).start()
    
    # Bot ကို Run ရန်
    asyncio.run(main())
