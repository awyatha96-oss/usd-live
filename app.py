import os
import requests
from flask import Flask, render_template_string, request

app = Flask(__name__)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>1xBet Live Converter</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        body { font-family: 'Segoe UI', sans-serif; background-color: #f0f2f5; padding: 15px; display: flex; justify-content: center; }
        .container { width: 100%; max-width: 480px; background: white; padding: 25px; border-radius: 15px; box-shadow: 0 4px 15px rgba(0,0,0,0.1); }
        h2 { text-align: center; color: #003366; }
        input { width: 100%; padding: 15px; margin: 15px 0; border: 2px solid #ddd; border-radius: 10px; font-size: 18px; text-transform: uppercase; box-sizing: border-box; }
        button { width: 100%; padding: 15px; background: #0056b3; color: white; border: none; border-radius: 10px; font-size: 16px; font-weight: bold; cursor: pointer; width: 100%; }
        .match-card { background: #fff; border-left: 6px solid #28a745; margin-top: 15px; padding: 15px; border-radius: 10px; box-shadow: 0 2px 5px rgba(0,0,0,0.05); position: relative; }
        .live-label { position: absolute; top: 10px; right: 10px; background: #e41e26; color: white; padding: 2px 8px; border-radius: 5px; font-size: 12px; font-weight: bold; animation: blinker 1.5s linear infinite; }
        @keyframes blinker { 50% { opacity: 0; } }
        .error { color: #721c24; background: #f8d7da; padding: 12px; border-radius: 10px; margin-top: 20px; text-align: center; }
    </style>
</head>
<body>
    <div class="container">
        <h2>⚽ 1xBet Live Converter</h2>
        <form method="POST">
            <input type="text" name="code" placeholder="Enter Code (e.g. H5R89)" value="{{ code }}" required>
            <button type="submit">Convert Matches</button>
        </form>

        {% if error %}
            <div class="error">{{ error }}</div>
        {% elif result %}
            <div style="margin-top: 20px;">
                <h4 style="text-align: left; margin-bottom: 10px;">✅ Results for: {{ code }}</h4>
                {% for event in result %}
                    <div class="match-card">
                        {% if event.IsLive %}<div class="live-label">LIVE</div>{% endif %}
                        <div style="font-weight: bold; font-size: 16px; margin-bottom: 5px;">{{ event.GameName }}</div>
                        <div style="font-size: 13px; color: #666; margin-bottom: 8px;">{{ event.League }}</div>
                        <div style="color: #0056b3; font-weight: bold; font-size: 15px; background: #e7f1ff; padding: 5px 10px; border-radius: 5px; display: inline-block;">
                            🎯 Bet: {{ event.MarketName }}
                        </div>
                    </div>
                {% endfor %}
            </div>
        {% endif %}
    </div>
</body>
</html>
"""

@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    error = None
    code = ""
    if request.method == 'POST':
        code = request.form.get('code', '').upper().strip()
        
        # 1xBet Mobile API လမ်းကြောင်း (Live ပွဲစဉ်များပါ ဖတ်နိုင်ရန်)
        # partner=151 နှင့် country=1 ကို သုံးထားခြင်းက Global Code တွေပါ ရစေပါတယ်
        url = f"https://1xbet.com/service-api/betslip/get/{code}?lng=en&country=1&partner=151"
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1',
            'Accept': 'application/json',
            'Referer': 'https://1xbet.com/'
        }

        try:
            # 1xBet က Block တာ သက်သာအောင် timeout ကို နည်းနည်း တိုးထားပါတယ်
            r = requests.get(url, headers=headers, timeout=20)
            if r.status_code == 200:
                data = r.json()
                if data.get('success') and 'Value' in data:
                    result = data['Value'].get('Events', [])
                    if not result:
                        error = "❌ ဤ Code မှာ ပွဲစဉ်များ မရှိတော့ပါ။"
                else:
                    error = "❌ Code သက်တမ်းကုန်သွားပါပြီ (သို့မဟုတ်) မှားနေပါသည်။"
            else:
                error = "⚠️ 1xBet ဘက်က လမ်းကြောင်း ပိတ်ထားပါတယ်။ ၁ မိနစ်လောက်နေမှ ပြန်စမ်းပါ။"
        except Exception:
            error = "⚠️ Connection Error. VPN ဖွင့်ထားရင် ပိတ်ပြီး ပြန်စမ်းကြည့်ပါ။"
            
    return render_template_string(HTML_TEMPLATE, result=result, error=error, code=code)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
