import os
import requests
from flask import Flask, render_template_string, request

app = Flask(__name__)

# Website ရဲ့ ပုံစံ (HTML)
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>1xBet Code Converter</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        body { font-family: sans-serif; background-color: #f4f4f9; padding: 20px; text-align: center; }
        .container { max-width: 500px; margin: auto; background: white; padding: 20px; border-radius: 10px; box-shadow: 0 0 10px rgba(0,0,0,0.1); }
        input { width: 80%; padding: 10px; margin: 10px 0; border: 1px solid #ddd; border-radius: 5px; text-transform: uppercase; }
        button { padding: 10px 20px; background: #007bff; color: white; border: none; border-radius: 5px; cursor: pointer; }
        .result { text-align: left; margin-top: 20px; padding: 10px; border-top: 1px solid #eee; }
        .event { margin-bottom: 10px; padding: 5px; border-bottom: 1px dashed #ccc; }
    </style>
</head>
<body>
    <div class="container">
        <h2>🇲🇲 1xBet Converter</h2>
        <form method="POST">
            <input type="text" name="code" placeholder="Enter France Code (e.g. GQT88)" required>
            <br>
            <button type="submit">Check Matches</button>
        </form>

        {% if result %}
            <div class="result">
                <h4>✅ Results for: {{ code }}</h4>
                {% if result.success %}
                    {% for event in result.Value.Events %}
                        <div class="event">
                            <strong>⚽ {{ event.GameName }}</strong><br>
                            🎯 Bet: <span style="color: blue;">{{ event.MarketName }}</span>
                        </div>
                    {% endfor %}
                {% else %}
                    <p style="color: red;">❌ Code not found or expired.</p>
                {% endif %}
            </div>
        {% endif %}
    </div>
</body>
</html>
"""

@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    code = ""
    if request.method == 'POST':
        code = request.form.get('code').upper().strip()
        url = f"https://1xbet.com/service-api/betslip/get/{code}?lng=en&country=201"
        try:
            r = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'}, timeout=10)
            result = r.json()
        except:
            result = {"success": False}
            
    return render_template_string(HTML_TEMPLATE, result=result, code=code)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
