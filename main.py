import telebot
import requests
import time
from datetime import datetime

# --- CONFIGURATION ---
API_TOKEN = '8382398265:AAF92uZPHGmB6APcl3G3yhh0oFWw39nBm8A' # BotFather ဆီကရတဲ့ Token
CHANNEL_ID = '@usd_live_mm' # သင့် Channel နာမည် (@ ပါရမည်)

bot = telebot.TeleBot(API_TOKEN)
last_price = 0 

def get_usd_price():
    try:
        # ကမ္ဘာ့ဒေါ်လာဈေး API
        url = "https://api.exchangerate-api.com/v4/latest/USD"
        response = requests.get(url, timeout=10)
        data = response.json()
        return data['rates']['MMK']
    except Exception as e:
        print(f"API Error: {e}")
        return None

def send_update(current, previous):
    now = datetime.now()
    date_str = now.strftime("%d %B %Y")
    time_str = now.strftime("%I:%M %p")
    
    # ဈေးတက်/ကျ အလိုက် Emoji နှင့် စာသား ရွေးချယ်ခြင်း
    if current > previous:
        status_icon = "🟢"
        trend_text = "BULLISH 🔺 (**MARKET UP**)"
        status_msg = "ဝယ်လိုအား မြင့်တက်နေပါသည်။"
    else:
        status_icon = "🔴"
        trend_text = "BEARISH 🔻 (**MARKET LOW**)"
        status_msg = "စျေးနှုန်း ပြန်လည်ကျဆင်းနေပါသည်။"

    message = (
        "💎 **USD/MMK PREMIUM UPDATE**\n\n"
        f"{status_icon} CURRENT RATE: 1 USD ➡️ **{current:,.0f} MMK**\n"
        f"📈 TREND: {trend_text}\n\n"
        f"📊 STATUS: {status_msg}\n"
        f"🗓 DATE: {date_str}\n"
        f"🕒 TIME: {time_str} (Yangon)\n\n"
        "---\n"
        f"🔔 Stay Updated with {CHANNEL_ID}"
    )
    
    try:
        bot.send_message(CHANNEL_ID, message, parse_mode="Markdown")
        print(f"Success: {current} MMK posted to Channel.")
    except Exception as e:
        print(f"Telegram Error: {e}")

print("--- USD Price Monitor Bot Started ---")

while True:
    current_price = get_usd_price()
    
    if current_price and current_price != last_price:
        send_update(current_price, last_price)
        last_price = current_price
    
    # ၅ မိနစ်တစ်ခါ စစ်ဆေးရန် (အရမ်းမြန်ရင် Telegram က Block တတ်လို့ပါ)
    time.sleep(300)
