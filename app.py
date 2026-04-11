import os
import requests
from flask import Flask, render_template_string, request

app = Flask(__name__)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>1xBet Live/Pre-match Converter</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        body { font-family: 'Segoe UI', sans-serif; background-color: #f0f2f5; padding: 20px; display: flex; justify-content: center; }
        .container { width: 100%; max-width: 480px; background: white; padding: 25px; border-radius: 15px; box-shadow: 0 4px 15px rgba(0,0,0,0.1); text-align: center; }
        h2 { color: #003366; }
        input { width: 100%; padding: 15px; margin: 15px 0; border: 2px solid #ddd; border-radius: 10px; font-size: 18px; text-transform: uppercase; box-sizing: border-box; }
        button { width: 100%; padding: 15px; background: #0056b3; color: white; border: none; border-radius: 10px; font-size: 16px; font-weight: bold; cursor: pointer; }
        .match-card { text-align: left; background: #fff; border-left: 6px solid #28a745; margin-top: 15px; padding: 15px; border-radius: 8px; box-shadow: 0 2px 5px rgba(0,0,0,0.05); }
        .live-tag { background: red; color: white; padding: 2px 6px; border-radius: 4px; font-size: 12px; font-weight: bold; }
        .error { color: #721c24; background: #f8d7da; padding: 10px; border-radius: 8px; margin-top: 20px; }
    </style>
</head>
<body>
    <div class="container">
        <h2>⚽ 1xBet Live/Pre-match</h2>
        <form method="POST">
            <input type="text" name="code" placeholder="Enter Code (e.g. GQT88)" value="{{ code }}" required>
            <button type="submit">Convert Matches</button>
        </form>

        {% if error %}
            <div class="error">{{ error }}</div>
        {% elif result %}
            <div style="margin-top: 20px;">
                <h4 style="text-align: left;">✅ Results for: {{ code }}</h4>
                {% for event in result %}
                    <div class="match-card">
                        <div style="font-weight: bold;">
                            {{ event.GameName }} 
                            {% if event.IsLive %}<span class="live-tag">LIVE</span>{% endif %}
                        </div>
                        <div style="font-size: 14px; color: #666; margin: 5px 0;">{{ event.League }}</div>
                        <div style="color: #0056b3; font-weight: bold;">🎯 Bet: {{ event.MarketName }}</div>
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
        
        # Live တွေရော Pre-match တွေရော ဖတ်နိုင်တဲ့ API URL
        # 1xBet ရဲ့ Sharing API ကို တိုက်ရိုက်ခေါ်ခြင်း
        url = f"https://1xbet.com/service-api/betslip/get/{code}?lng=en"
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36',
            'Referer': 'https://1xbet.com/'
        }

        try:
            r = requests.get(url, headers=headers, timeout=15)
            data = r.json()
            if data.get('success') and 'Value' in data:
                result = data['Value'].get('Events', [])
                if not result:
                    error = "❌ No matches found."
            else:
                error = "❌ Code incorrect or data not found."
        except:
            error = "⚠️ Connection Error. Please try again."
            
    return render_template_string(HTML_TEMPLATE, result=result, error=error, code=code)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
