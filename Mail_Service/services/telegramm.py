# import telepot
import requests
from django.conf import settings


def send_telegram(text: str):
    token = settings.TOKEN
    url = "https://api.telegram.org/bot"
    channel_id = settings.CHANNEL_ID
    url += token
    method = url + "/sendMessage"
    proxies = {
        'http': settings.PROXIES_HTTP
    }


    r = requests.post(method, data={
         "chat_id": channel_id,
         "text": text
          }, proxies=proxies)

    if r.status_code != 200:
        raise Exception("post_text error")
