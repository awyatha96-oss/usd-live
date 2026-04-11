import os
import requests
from flask import Flask, render_template_string, request

app = Flask(__name__)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>1xBet Converter Pro</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        body { font-family: sans-serif; background: #e9ecef; display: flex; justify-content: center; padding: 20px; }
        .container { width: 100%; max-width: 450px; background: white; padding: 25px; border-radius: 15px; box-shadow: 0 5px 15px rgba(0,0,0,0.2); }
        h2 { text-align: center; color: #003366; }
        input { width: 100%; padding: 15px; margin: 15px 0; border: 2px solid #ced4da; border-radius: 8px; box-sizing: border-box; font-size: 18px; text-transform: uppercase; }
        button { width: 100%; padding: 15px; background: #28a745; color: white; border: none; border-radius: 8px; font-weight: bold; font-size: 16px; cursor: pointer; }
        .match-card { text-align: left; border-left: 5px solid #007bff; background: #f8f9fa; padding: 15px; margin-top: 15px; border-radius: 8px; }
        .error { color: #721c24; background: #f8d7da; padding: 12px; border-radius: 8px; margin-top: 20px; text-align: center; font-weight: bold; }
    </style>
</head>
<body>
    <div class="container">
        <h2>🇲🇲 1xBet Converter</h2>
        <form method="POST">
            <input type="text" name="code" placeholder="Enter Bet Code" value="{{ code }}" required>
            <button type="submit">Convert Matches</button>
        </form>

        {% if error %}<div class="error">{{ error }}</div>{% endif %}
        {% if result %}
            <div style="margin-top:20px;">
                <h4 style="margin-bottom:10px;">✅ Found {{ result|length }} Matches</h4>
                {% for event in result %}
                    <div class="match-card">
                        <div style="font-weight:bold; color:#333;">⚽ {{ event.GameName }}</div>
                        <div style="font-size:13px; color:#666; margin: 5px 0;">{{ event.League }}</div>
                        <div style="color: #d93025; font-weight:bold;">🎯 Bet: {{ event.MarketName }}</div>
                    </div>
                {% endfor %}
            </div>
        {% endif %}
    </div>
</body>
</html>
"""

def fetch_1xbet(code):
    # API လမ်းကြောင်း (၃) မျိုးစလုံးကို တစ်ခုပြီးတစ်ခု စမ်းမယ်
    # 1. Global, 2. France, 3. Mobile API
    api_endpoints = [
        f"https://1xbet.com/service-api/betslip/get/{code}?lng=en&country=1",
        f"https://1xbet.com/service-api/betslip/get/{code}?lng=en&country=201",
        f"https://1xbet.com/service-api/betslip/get/{code}?lng=en&partner=151"
    ]
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
        'Accept': 'application/json',
        'Referer': 'https://1xbet.com/'
    }

    for url in api_endpoints:
        try:
            response = requests.get(url, headers=headers, timeout=10)
            if response.status_code == 200:
                data = response.json()
                if data.get('success') and 'Value' in data:
                    events = data['Value'].get('Events', [])
                    if events:
                        return events, None
        except:
            continue
            
    return None, "❌ Code မတွေ့ပါ (သို့မဟုတ်) 1xBet မှ ပိတ်ထားပါသည်။"

@app.route('/', methods=['GET', 'POST'])
def index():
    result, error, code = None, None, ""
    if request.method == 'POST':
        code = request.form.get('code', '').upper().strip()
        result, error = fetch_1xbet(code)
    return render_template_string(HTML_TEMPLATE, result=result, error=error, code=code)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))
