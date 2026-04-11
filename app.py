import os
import requests
from flask import Flask, render_template_string, request

app = Flask(__name__)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>3-in-1 Bet Converter</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        body { font-family: 'Segoe UI', sans-serif; background: #0b0e11; color: #eaecef; display: flex; justify-content: center; padding: 20px; }
        .container { width: 100%; max-width: 480px; background: #1e2329; padding: 25px; border-radius: 15px; box-shadow: 0 10px 30px rgba(0,0,0,0.5); text-align: center; }
        .brand-header { font-size: 24px; font-weight: bold; color: #f0b90b; margin-bottom: 20px; text-transform: uppercase; }
        .platform-tags { display: flex; justify-content: center; gap: 10px; margin-bottom: 15px; font-size: 12px; }
        .tag { padding: 3px 8px; border-radius: 4px; background: #333; color: #aaa; }
        input { width: 100%; padding: 15px; margin-bottom: 15px; border: 1px solid #474d57; border-radius: 10px; background: #2b3139; color: white; font-size: 18px; text-transform: uppercase; text-align: center; }
        button { width: 100%; padding: 15px; background: #f0b90b; color: black; border: none; border-radius: 10px; font-weight: bold; font-size: 16px; cursor: pointer; transition: 0.3s; }
        button:hover { background: #ffe066; }
        .match-card { text-align: left; background: #2b3139; border-left: 5px solid #f0b90b; padding: 15px; margin-top: 15px; border-radius: 10px; }
        .live-badge { float: right; background: #f6465d; color: white; padding: 2px 6px; border-radius: 4px; font-size: 11px; font-weight: bold; }
        .error { color: #f6465d; background: rgba(246, 70, 93, 0.1); padding: 12px; border-radius: 10px; margin-top: 20px; border: 1px solid #f6465d; }
    </style>
</head>
<body>
    <div class="container">
        <div class="brand-header">💎 Multi-Platform Converter</div>
        <div class="platform-tags">
            <span class="tag">1XBET</span>
            <span class="tag">MELBET</span>
            <span class="tag">MEGAPARI</span>
        </div>
        
        <form method="POST">
            <input type="text" name="code" placeholder="ENTER CODE (E.G. GQT88)" value="{{ code }}" required>
            <button type="submit">FIND MATCHES</button>
        </form>

        {% if error %}<div class="error">{{ error }}</div>{% endif %}
        {% if result %}
            <div style="margin-top:20px;">
                <h4 style="text-align: left; color: #f0b90b;">✅ Results Found:</h4>
                {% for event in result %}
                    <div class="match-card">
                        {% if event.IsLive %}<span class="live-badge">LIVE</span>{% endif %}
                        <div style="font-weight:bold; font-size: 16px;">⚽ {{ event.GameName }}</div>
                        <div style="font-size:13px; color:#848e9c; margin: 5px 0;">{{ event.League }}</div>
                        <div style="color: #02c076; font-weight:bold; background: rgba(2, 192, 118, 0.1); padding: 5px; border-radius: 5px; display: inline-block;">
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

def fetch_from_all(code):
    # စစ်ဆေးမည့် Platform များစာရင်း (1xbet, melbet, megapari)
    domains = [
        "1xbet.com",
        "melbet.com",
        "megapari.com"
    ]
    
    # France Code ရော Global Code ရော မိအောင် လမ်းကြောင်း ၂ ခုလုံး စစ်မယ်
    pathways = ["country=201", "country=1", "partner=151"]
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1',
        'Accept': 'application/json'
    }

    for domain in domains:
        for path in pathways:
            url = f"https://{domain}/service-api/betslip/get/{code}?lng=en&{path}"
            try:
                r = requests.get(url, headers=headers, timeout=8)
                if r.status_code == 200:
                    data = r.json()
                    if data.get('success') and 'Value' in data:
                        events = data['Value'].get('Events', [])
                        if events:
                            return events, None
            except:
                continue
                
    return None, "❌ Code not found on any platform (1x/Mel/Mega)."

@app.route('/', methods=['GET', 'POST'])
def index():
    result, error, code = None, None, ""
    if request.method == 'POST':
        code = request.form.get('code', '').upper().strip()
        result, error = fetch_from_all(code)
    return render_template_string(HTML_TEMPLATE, result=result, error=error, code=code)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))
