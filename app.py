import os
import requests
from flask import Flask, render_template_string, request

app = Flask(__name__)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>France Code Converter</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        body { font-family: sans-serif; background: #121212; color: white; display: flex; justify-content: center; padding: 20px; }
        .container { width: 100%; max-width: 450px; background: #1e1e1e; padding: 25px; border-radius: 15px; box-shadow: 0 0 20px rgba(0,0,0,0.5); text-align: center; }
        input { width: 100%; padding: 15px; margin: 15px 0; border: 1px solid #333; border-radius: 8px; background: #2d2d2d; color: white; font-size: 18px; text-transform: uppercase; }
        button { width: 100%; padding: 15px; background: #007bff; color: white; border: none; border-radius: 8px; font-weight: bold; cursor: pointer; }
        .match-card { text-align: left; background: #2d2d2d; border-left: 5px solid #ffcc00; padding: 15px; margin-top: 15px; border-radius: 8px; }
        .error { color: #ff4444; background: #3d1a1a; padding: 12px; border-radius: 8px; margin-top: 20px; }
    </style>
</head>
<body>
    <div class="container">
        <h2>🇫🇷 France Code Special</h2>
        <form method="POST">
            <input type="text" name="code" placeholder="ENTER FRANCE CODE" value="{{ code }}" required>
            <button type="submit">Check France Data</button>
        </form>

        {% if error %}<div class="error">{{ error }}</div>{% endif %}
        {% if result %}
            <div style="margin-top:20px;">
                {% for event in result %}
                    <div class="match-card">
                        <div style="font-weight:bold; color: #ffcc00;">⚽ {{ event.GameName }}</div>
                        <div style="font-size:13px; color:#aaa;">{{ event.League }}</div>
                        <div style="color: #00ff00; font-weight:bold; margin-top:5px;">🎯 {{ event.MarketName }}</div>
                    </div>
                {% endfor %}
            </div>
        {% endif %}
    </div>
</body>
</html>
"""

def get_france_data(code):
    # France Code တွေအတွက် သီးသန့် API Gateway (Country 201 = France)
    url = f"https://1xbet.com/service-api/betslip/get/{code}?lng=en&country=201&partner=151"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0 Safari/537.36',
        'Referer': 'https://1xbet.fr/',
        'Accept': 'application/json'
    }

    try:
        r = requests.get(url, headers=headers, timeout=15)
        data = r.json()
        if data.get('success') and 'Value' in data:
            return data['Value'].get('Events', []), None
        else:
            return None, "❌ France Code မတွေ့ပါ။ သက်တမ်းကုန်သွားတာ ဖြစ်နိုင်ပါတယ်။"
    except:
        return None, "⚠️ Connection Error. VPN ခံပြီး ပြန်စမ်းကြည့်ပါ။"

@app.route('/', methods=['GET', 'POST'])
def index():
    result, error, code = None, None, ""
    if request.method == 'POST':
        code = request.form.get('code', '').upper().strip()
        result, error = get_france_data(code)
    return render_template_string(HTML_TEMPLATE, result=result, error=error, code=code)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))
