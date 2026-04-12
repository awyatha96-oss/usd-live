import os
import requests
from flask import Flask, render_template_string, request

app = Flask(__name__)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Ultimate Slip Converter</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        body { font-family: sans-serif; background: #0b0e11; color: #fff; display: flex; justify-content: center; padding: 20px; }
        .container { width: 100%; max-width: 450px; background: #1e2329; padding: 25px; border-radius: 12px; box-shadow: 0 5px 20px rgba(0,0,0,0.5); text-align: center; }
        input { width: 100%; padding: 15px; margin-bottom: 15px; border: 1px solid #444; border-radius: 8px; background: #2b3139; color: white; font-size: 18px; text-transform: uppercase; }
        button { width: 100%; padding: 15px; background: #f0b90b; color: black; border: none; border-radius: 8px; font-weight: bold; cursor: pointer; }
        .match-card { text-align: left; background: #2b3139; border-left: 4px solid #f0b90b; padding: 12px; margin-top: 12px; border-radius: 5px; }
        .error { color: #f6465d; background: rgba(246,70,93,0.1); padding: 10px; border-radius: 8px; margin-top: 15px; border: 1px solid #f6465d; }
    </style>
</head>
<body>
    <div class="container">
        <h2 style="color:#f0b90b;">🚀 Pro Converter</h2>
        <form method="POST">
            <input type="text" name="code" placeholder="ENTER CODE" value="{{ code }}" required>
            <button type="submit">FIND NOW</button>
        </form>

        {% if error %}<div class="error">{{ error }}</div>{% endif %}
        {% if result %}
            <div style="margin-top:20px;">
                {% for event in result %}
                    <div class="match-card">
                        <div style="font-weight:bold;">⚽ {{ event.GameName }}</div>
                        <div style="font-size:12px; color:#aaa;">{{ event.League }}</div>
                        <div style="color:#02c076; font-weight:bold; margin-top:5px;">🎯 {{ event.MarketName }}</div>
                    </div>
                {% endfor %}
            </div>
        {% endif %}
    </div>
</body>
</html>
"""

def fetch_data(code):
    # API ပိတ်တာ ကျော်ဖို့ Gateway မျိုးစုံကို အပြင်းအထန် စမ်းမယ်
    # 1xbet, melbet, megapari, linebet အကုန်ပါတယ်။
    targets = [
        f"https://1xbet.com/service-api/betslip/get/{code}?lng=en&country=201",
        f"https://melbet.com/service-api/betslip/get/{code}?lng=en&country=201",
        f"https://megapari.com/service-api/betslip/get/{code}?lng=en&country=201"
    ]
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
        'Accept': 'application/json',
        'X-Requested-With': 'XMLHttpRequest'
    }

    for url in targets:
        try:
            # 1xBet ရဲ့ firewall ကို ကျော်ဖို့ timeout ကို ချိန်ညှိထားတယ်
            r = requests.get(url, headers=headers, timeout=12)
            if r.status_code == 200:
                data = r.json()
                if data.get('success') and 'Value' in data:
                    return data['Value'].get('Events', []), None
        except:
            continue
    return None, "❌ အခုချိန်မှာ 1xBet က လမ်းကြောင်းအကုန် ပိတ်ထားပါတယ်။ ၁ မိနစ်လောက်နေမှ ပြန်စမ်းပါ။"

@app.route('/', methods=['GET', 'POST'])
def index():
    result, error, code = None, None, ""
    if request.method == 'POST':
        code = request.form.get('code', '').upper().strip()
        result, error = fetch_data(code)
    return render_template_string(HTML_TEMPLATE, result=result, error=error, code=code)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))
