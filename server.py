from flask import Flask, request
import telegram_bot_2

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json()
    telegram_bot_2.handle_update(data)
    return "OK", 200

@app.route('/')
def home():
    return "Hello, your bot server is running!", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
