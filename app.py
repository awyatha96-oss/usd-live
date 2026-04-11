import os
import requests
from flask import Flask, render_template_string, request

app = Flask(__name__)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>1xBet All-in-One Converter</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        body { font-family: sans-serif; background: #f0f2f5; display: flex; justify-content: center; padding: 20px; }
        .container { width: 100%; max-width: 450px; background: white; padding: 25px; border-radius: 15px; box-shadow: 0 4px 12px rgba(0,0,0,0.15); }
        input { width: 100%; padding: 15px; margin: 15px 0; border: 2px solid #ddd; border-radius: 8px; box-sizing: border-box; font-size: 18px; text-transform: uppercase; }
        button { width: 100%; padding: 15px; background: #0056b3; color: white; border: none; border-radius: 8px; font-weight: bold; cursor: pointer; }
        .match-card { text-align: left; border-left: 5px solid #28a745; background: #fafafa; padding: 12px; margin-top: 12px; border-radius: 5px; }
        .live-tag { color: white; background: red; padding: 2px 5px; font-size: 12px; border-radius: 3px; font-weight: bold; float: right; }
        .error { color: #d93025; background: #fce8e6; padding: 10px; border-radius: 8px; margin-top: 15px; text-align: center; }
    </style>
</head>
<body>
    <div class="container">
        <h2 style="text-align: center;">🇲🇲 1xBet Converter</h2>
        <form method="POST">
            <input type="text" name="code" placeholder="Enter Code" value="{{ code }}" required>
            <button type="submit">Convert Matches</button>
        </form>

        {% if error %}<div class="error">{{ error }}</div>{% endif %}
        {% if result %}
            <div style="margin-top:20px;">
                {% for event in result %}
                    <div class="match-card">
                        {% if event.IsLive %}<span class="live-tag">LIVE</span>{% endif %}
                        <div style="font-weight:bold;">⚽ {{ event.GameName }}</div>
                        <div style="font-size:13px; color:#555;">{{ event.League }}</div>
                        <div style="margin-top:5px; color:#0056b3; font-weight:bold;">🎯 {{ event.MarketName }}</div>
                    </div>
                {% endfor %}
            </div>
        {% endif %}
    </div>
</body>
</html>
"""

def fetch_data(code):
    # API လမ်းကြောင်း (၂) မျိုးလုံးကို စမ်းစစ်မယ်
    urls = [
        f"https://1xbet.com/service-api/betslip/get/{code}?lng=en&country=201",
        f"https://1xbet.com/service-api/betslip/get/{code}?lng=en&partner=151"
    ]
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1',
        'Accept': 'application/json'
    }

    for url in urls:
        try:
            r = requests.get(url, headers=headers, timeout=10)
            data = r.json()
            if data.get('success') and 'Value' in data:
                return data['Value'].get('Events', []), None
        except:
            continue
    return None, "❌ Code မတွေ့ပါ (သို့) ပွဲစဉ်များ ပိတ်သွားပါပြီ။"

@app.route('/', methods=['GET', 'POST'])
def index():
    result, error, code = None, None, ""
    if request.method == 'POST':
        code = request.form.get('code', '').upper().strip()
        result, error = fetch_data(code)
    return render_template_string(HTML_TEMPLATE, result=result, error=error, code=code)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))
