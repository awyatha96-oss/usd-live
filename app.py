import os
import requests
from flask import Flask
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# Flask setup (Render အတွက် လိုအပ်သည်)
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is running!"

# Telegram Bot Token
TOKEN = "8382398265:AAF92uZPHGmB6APcl3G3yhh0oFWw39nBm8A"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("မင်္ဂလာပါ။ 1xBet ပြင်သစ် Betslip Code ကို ပေးပို့ပါ။ မြန်မာ Code အဖြစ် ပြောင်းလဲပေးပါမည်။")

async def convert_code(update: Update, context: ContextTypes.DEFAULT_TYPE):
    france_code = update.message.text.upper().strip()
    await update.message.reply_text(f"ပြင်သစ် Code '{france_code}' ကို စစ်ဆေးနေပါသည်...")

    # --- ဒီနေရာမှာ 1xBet API Logic ထည့်ရပါမယ် ---
    # မှတ်ချက် - 1xBet က ပွဲစဉ်ဒေတာယူဖို့ Proxy သို့မဟုတ် Session လိုအပ်ပါတယ်။
    # လောလောဆယ်တွင် ပုံစံတူ Response ကို ပြသပေးပါမည်။
    
    try:
        # 1xBet (France) ရဲ့ API ကို လှမ်းခေါ်တဲ့ပုံစံ (ဥပမာသာဖြစ်သည်)
        # တကယ့်စနစ်မှာ 1xbet.com/test-api/v1/get-betslip သို့မဟုတ် scraping သုံးရမည်
        
        result_message = (
            f"✅ ပြောင်းလဲပြီးပါပြီ!\n\n"
            f"🇫🇷 France Code: {france_code}\n"
            f"🇲🇲 Myanmar Code: (MM-REPLACEMENT)\n\n"
            f"⚠️ မှတ်ချက်: 1xBet Server များ မတူညီသဖြင့် ပွဲစဉ်အချို့ ကွဲလွဲနိုင်ပါသည်။"
        )
        await update.message.reply_text(result_message)
        
    except Exception as e:
        await update.message.reply_text("Error: စနစ်အတွင်း အမှားအယွင်းတစ်ခု ရှိနေပါသည်။")

if __name__ == "__main__":
    # Bot Application ဆောက်ခြင်း
    application = ApplicationBuilder().token(TOKEN).build()
    
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), convert_code))
    
    # Render အတွက် Port ပေးခြင်း
    port = int(os.environ.get("PORT", 5000))
    
    print("Bot is starting...")
    application.run_polling()
