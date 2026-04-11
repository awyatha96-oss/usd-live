import os
import requests
import random
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
        .container { width: 100%; max-width: 480px; background: white; padding: 20px; border-radius: 15px; box-shadow: 0 4px 15px rgba(0,0,0,0.1); }
        h2 { text-align: center; color: #003366; font-size: 22px; }
        input { width: 100%; padding: 12px; margin: 10px 0; border: 2px solid #ddd; border-radius: 8px; font-size: 16px; text-transform: uppercase; box-sizing: border-box; }
        button { width: 100%; padding: 12px; background: #0056b3; color: white; border: none; border-radius: 8px; font-size: 16px; font-weight: bold; cursor: pointer; width: 100%; }
        .match-card { background: #fff; border-left: 5px solid #007bff; margin-top: 12px; padding: 12px; border-radius: 8px; box-shadow: 0 2px 5px rgba(0,0,0,0.05); position: relative; }
        .live-badge { position: absolute; top: 10px; right: 10px; background: #dc3545; color: white; padding: 2px 6px; border-radius: 4px; font-size: 11px; font-weight: bold; }
        .error { color: #721c24; background: #f8d7da; padding: 10px; border-radius: 8px; margin-top: 15px; font-size: 14px; text-align: center; }
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
            <div style="margin-top: 15px;">
                <h4 style="margin: 0 0 10px 5px;">✅ Results for: {{ code }}</h4>
                {% for event in result %}
                    <div class="match-card">
                        {% if event.IsLive %}<span class="live-badge">LIVE</span>{% endif %}
                        <div style="font-weight: bold; padding-right: 50px;">{{ event.GameName }}</div>
                        <div style="font-size: 13px; color: #666; margin: 4px 0;">{{ event.League }}</div>
                        <div style="color: #28a745; font-weight: bold; font-size: 15px;">🎯 {{ event.MarketName }}</div>
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
        
        # 1xBet Mobile API လမ်းကြောင်းများစွာကို အလှည့်ကျ သုံးခြင်း (Proxy သဘောမျိုး)
        domains = ["1xbet.com", "1xbet.org", "1xbet-new.com"]
        target_domain = random.choice(domains)
        url = f"https://{target_domain}/service-api/betslip/get/{code}?lng=en&country=1"
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1',
            'Accept': 'application/json',
            'X-Requested-With': 'XMLHttpRequest',
            'Referer': f'https://{target_domain}/'
        }

        try:
            r = requests.get(url, headers=headers, timeout=15)
            data = r.json()
            if data.get('success') and 'Value' in data:
                result = data['Value'].get('Events', [])
                if not result:
                    error = "❌ ဤ Code မှာ ပွဲစဉ်များ မရှိတော့ပါ။"
            else:
                error = "❌ Code သက်တမ်းကုန်သွားပြီ သို့မဟုတ် မှားနေပါသည်။"
        except Exception:
            # တိုက်ရိုက်မရလျှင် အခြားနည်းလမ်းဖြင့် ထပ်စမ်းခြင်း
            error = "⚠️ Connection Error. ပွဲကန်နေချိန်မို့ 1xBet က ပိတ်ထားနိုင်ပါတယ်။ ခဏနေမှ ထပ်စမ်းပါ။"
            
    return render_template_string(HTML_TEMPLATE, result=result, error=error, code=code)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
