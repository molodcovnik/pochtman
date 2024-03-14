# import telepot
import requests
from django.conf import settings


def send_telegram(result_dict, chat_id, template_name):
    token = settings.TOKEN
    url = "https://api.telegram.org/bot"
    channel_id = chat_id
    url += token
    method = url + "/sendMessage"
    proxies = {
        'http': settings.PROXIES_HTTP
    }

    table = '\n'.join(f"{arr[0]} : {'Да' if arr[1] == 'True' else 'Нет' if arr[1] == 'False' else arr[1]}" for arr in result_dict)
    text = f'Получена новая заявка от <strong>{template_name.capitalize()}</strong>\n'
    message_text = text + '\n' + table


    r = requests.post(method, data={
         "chat_id": channel_id,
         "text": message_text,
         "parse_mode": "HTML"
          }, proxies=proxies)

    if r.status_code != 200:
        raise Exception("post_text error")
