import os
import requests
import telegram
from datetime import datetime, timedelta


# http status ex)404, 500
ERROR_CHECK_CODE = ['4', '5']


def lambda_handler(event, context):
    target_site_url = event['url']
    status_recive_channel = event['chat']
    now_tz_seoul = datetime.utcnow() + timedelta(seconds=32400)
    telegram_bot_token = os.environ['TELEGRAM_BOT_TOKEN_NUM'] + ':' + os.environ['TELEGRAM_BOT_TOKEN_KEY']
    try:
        website = requests.get(target_site_url)
        website_status_code = str(website.status_code)
        if website_status_code[0] in ERROR_CHECK_CODE:
            status_message = '%s status code is %s. \n%s\nstatus check time is %s' \
                             % (target_site_url, website_status_code, website.reason,
                                now_tz_seoul.strftime("%Y-%m-%d %H:%M:%S"))
            send_message(status_message, telegram_bot_token, status_recive_channel)
        else:
            return 'site status all green'
    except Exception:
        status_message = '%s site connect refused. now %s' % (target_site_url, now_tz_seoul.strftime("%Y-%m-%d %H:%M:%S"))
        send_message(status_message, telegram_bot_token, status_recive_channel)


def send_message(message, token, chat_id):
    bot = telegram.Bot(token=token)
    bot.send_message(chat_id=chat_id, text=message)

