from flask import Flask, request
import telegram_bot_2
import asyncio

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json()
    # Use asyncio.run() to call the async function in a synchronous context
    asyncio.run(telegram_bot_2.handle_update(data))
    return "OK", 200

@app.route('/')
def home():
    return "Hello, your bot server is running!", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
