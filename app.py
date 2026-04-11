import os
import requests
from flask import Flask, render_template_string, request

app = Flask(__name__)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>France Slip Converter</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        body { font-family: sans-serif; background: #0b0e11; color: #eaecef; display: flex; justify-content: center; padding: 20px; }
        .container { width: 100%; max-width: 450px; background: #1e2329; padding: 25px; border-radius: 12px; box-shadow: 0 8px 32px rgba(0,0,0,0.3); text-align: center; }
        h2 { color: #f0b90b; margin-bottom: 20px; }
        input { width: 100%; padding: 15px; margin-bottom: 15px; border: 1px solid #474d57; border-radius: 8px; background: #2b3139; color: white; font-size: 18px; text-transform: uppercase; box-sizing: border-box; }
        button { width: 100%; padding: 15px; background: #f0b90b; color: black; border: none; border-radius: 8px; font-weight: bold; font-size: 16px; cursor: pointer; }
        button:hover { background: #dca009; }
        .match-card { text-align: left; background: #2b3139; border-left: 4px solid #f0b90b; padding: 15px; margin-top: 15px; border-radius: 8px; }
        .error { color: #f6465d; background: rgba(246, 70, 93, 0.1); padding: 12px; border-radius: 8px; margin-top: 20px; font-weight: bold; border: 1px solid #f6465d; }
    </style>
</head>
<body>
    <div class="container">
        <h2>🇫🇷 France Code Converter</h2>
        <form method="POST">
            <input type="text" name="code" placeholder="ENTER CODE (E.G. L82C1)" value="{{ code }}" required>
            <button type="submit">CHECK SLIP</button>
        </form>

        {% if error %}<div class="error">{{ error }}</div>{% endif %}
        {% if result %}
            <div style="margin-top:20px;">
                {% for event in result %}
                    <div class="match-card">
                        <div style="font-weight:bold; color:#f0b90b; margin-bottom:5px;">⚽ {{ event.GameName }}</div>
                        <div style="font-size:13px; color:#848e9c; margin-bottom:8px;">{{ event.League }}</div>
                        <div style="color: #02c076; font-weight:bold;">🎯 Bet: {{ event.MarketName }}</div>
                    </div>
                {% endfor %}
            </div>
        {% endif %}
    </div>
</body>
</html>
"""

def fetch_data(code):
    # အဓိက France Gateway ကို ဦးစားပေးခေါ်မယ်
    url = f"https://1xbet.com/service-api/betslip/get/{code}?lng=en&country=201&partner=151"
    
    # 1xBet က ပိတ်ရခက်အောင် Mobile Safari ပုံစံသွင်းမယ်
    headers = {
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1',
        'Accept': 'application/json',
        'Referer': 'https://m.1xbet.com/'
    }

    try:
        # Timeout ကို တိုးထားပြီး Connection ကို အကြိမ်ကြိမ်စမ်းမယ်
        session = requests.Session()
        r = session.get(url, headers=headers, timeout=20)
        
        if r.status_code == 200:
            data = r.json()
            if data.get('success') and 'Value' in data:
                return data['Value'].get('Events', []), None
            else:
                return None, "❌ Code Expired (သို့) ရှာမတွေ့ပါ။"
        else:
            return None, "⚠️ 1xBet က ပိတ်ထားဆဲပါ။ 1 မိနစ်နေမှ ပြန်စမ်းပါ။"
    except:
        return None, "⚠️ Connection Error. VPN (France) ချိတ်ပြီး Refresh လုပ်ကြည့်ပါ။"

@app.route('/', methods=['GET', 'POST'])
def index():
    result, error, code = None, None, ""
    if request.method == 'POST':
        code = request.form.get('code', '').upper().strip()
        result, error = fetch_data(code)
    return render_template_string(HTML_TEMPLATE, result=result, error=error, code=code)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))
