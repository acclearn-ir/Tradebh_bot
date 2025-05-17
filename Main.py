import requests
import time
import os

TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")

def send_telegram_message(message: str):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message,
        "parse_mode": "HTML"
    }
    try:
        requests.post(url, data=payload)
    except Exception as e:
        print("Telegram error:", e)

def fetch_dexscreener_bsc():
    url = "https://api.dexscreener.com/latest/dex/pairs/bsc"
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            return response.json().get("pairs", [])
    except Exception as e:
        print("Dexscreener error:", e)
    return []

def check_tokens():
    tokens = fetch_dexscreener_bsc()
    if not tokens:
        return

    for pair in tokens[:20]:
        try:
            change = float(pair.get("priceChange", {}).get("m5", 0))
            if abs(change) > 50:
                name = pair.get("baseToken", {}).get("name", "Unknown")
                price = pair.get("priceUsd", "N/A")
                url = pair.get("url", "#")
                message = (f"🚀 <b>توکن نوسانی جدید روی BSC</b>\n"
                           f"📛 نام: {name}\n"
                           f"💲 قیمت: ${price}\n"
                           f"📈 تغییرات ۵ دقیقه‌ای: {change}%\n"
                           f"🔗 <a href='{url}'>مشاهده / خرید</a>")
                send_telegram_message(message)
                time.sleep(1)
        except:
            continue

if __name__ == "__main__":
    while True:
        check_tokens()
        time.sleep(300)
