import os
import requests
from flask import Flask, render_template_string, request

app = Flask(__name__)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>1xBet Official Converter</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        body { font-family: sans-serif; background: #f4f7f9; display: flex; justify-content: center; padding: 20px; }
        .container { width: 100%; max-width: 450px; background: white; padding: 25px; border-radius: 12px; box-shadow: 0 4px 10px rgba(0,0,0,0.1); text-align: center; }
        input { width: 100%; padding: 15px; margin: 15px 0; border: 2px solid #ddd; border-radius: 8px; box-sizing: border-box; font-size: 18px; text-transform: uppercase; }
        button { width: 100%; padding: 15px; background: #007bff; color: white; border: none; border-radius: 8px; font-weight: bold; cursor: pointer; }
        .match-card { text-align: left; background: #fff; border-left: 5px solid #28a745; padding: 15px; margin-top: 15px; border-radius: 8px; box-shadow: 0 2px 5px rgba(0,0,0,0.05); }
        .error { color: #d93025; background: #fce8e6; padding: 12px; border-radius: 8px; margin-top: 20px; font-weight: bold; }
    </style>
</head>
<body>
    <div class="container">
        <h2>🇲🇲 1xBet Converter</h2>
        <form method="POST">
            <input type="text" name="code" placeholder="ENTER CODE HERE" value="{{ code }}" required>
            <button type="submit">Convert Now</button>
        </form>

        {% if error %}<div class="error">{{ error }}</div>{% endif %}
        {% if result %}
            <div style="margin-top:20px;">
                {% for event in result %}
                    <div class="match-card">
                        <div style="font-weight:bold;">⚽ {{ event.GameName }}</div>
                        <div style="font-size:13px; color:#666;">{{ event.League }}</div>
                        <div style="color: #007bff; font-weight:bold; margin-top:5px;">🎯 {{ event.MarketName }}</div>
                    </div>
                {% endfor %}
            </div>
        {% endif %}
    </div>
</body>
</html>
"""

def get_1xbet_slip(code):
    # 1xBet ရဲ့ မတူညီတဲ့ Gateway ၃ ခုလုံးကို အလှည့်ကျ စစ်ဆေးမယ်
    gateways = [
        f"https://1xbet.com/service-api/betslip/get/{code}?lng=en&country=1",
        f"https://1xbet.com/service-api/betslip/get/{code}?lng=en&country=201",
        f"https://1xbet.com/service-api/betslip/get/{code}?lng=en&partner=151"
    ]
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'application/json'
    }

    for url in gateways:
        try:
            r = requests.get(url, headers=headers, timeout=10)
            if r.status_code == 200:
                data = r.json()
                if data.get('success') and 'Value' in data:
                    return data['Value'].get('Events', []), None
        except:
            continue
    return None, "❌ 1xBet က လမ်းကြောင်း ပိတ်ထားပါတယ်။ ခဏနေမှ ပြန်စမ်းပါ။"

@app.route('/', methods=['GET', 'POST'])
def index():
    result, error, code = None, None, ""
    if request.method == 'POST':
        code = request.form.get('code', '').upper().strip()
        result, error = get_1xbet_slip(code)
    return render_template_string(HTML_TEMPLATE, result=result, error=error, code=code)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))
