def send_message(message):
    import sqlite3
    import requests
    from dotenv import load_dotenv
    load_dotenv()
    import os

    BOT_TOKEN = os.getenv('BOT_TOKEN')
    CHAT_ID = -1002172856445
    conn = sqlite3.connect('userinfo.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM info_of_user")
    rows = cursor.fetchall()
    print(rows[-1])
    cursor.close()
    conn.close()

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": message
    }

    response = requests.post(url, data=payload)
    if response.status_code == 200:
        print("Message sent successfully!")
    else:
        print(f"Failed to send message: {response.text}")






