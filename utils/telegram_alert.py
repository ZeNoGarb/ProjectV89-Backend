import cv2
import requests
from config import Config

TELEGRAM_TOKEN = Config.TELEGRAM_TOKEN
TELEGRAM_CHAT_ID = Config.TELEGRAM_CHAT_ID

def send_telegram_alert(image, message="Alert!"):
    url = f'https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendPhoto'
    _, img_encoded = cv2.imencode('.jpg', image)
    files = {'photo': ('frame.jpg', img_encoded.tobytes())}
    data = {'chat_id': TELEGRAM_CHAT_ID, 'caption': message}
    response = requests.post(url, data=data, files=files)
    return response.ok
