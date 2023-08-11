import configparser

from telethon.errors.rpcerrorlist import MessageIdInvalidError
from telethon.sync import TelegramClient

from functions.time_count_decorator import time_count


@time_count
def send_msg_f_user(msg_start=345210, msg_end=-1, user=474103257, chanel=-1001261922335):
    # Считываем учетные данные
    config = configparser.ConfigParser()
    config.read("config/config.ini")

    # Присваиваем значения внутренним переменным
    api_id = config['Telegram']['api_id']
    api_hash = config['Telegram']['api_hash']
    phone = config['Telegram']['username']

    with TelegramClient(phone, int(api_id), api_hash) as client:
        try:
            if msg_end == -1:

                client.forward_messages(entity=user, messages=msg_start, from_peer=chanel)
            else:
                client.forward_messages(entity=user, messages=[_ for _ in range(msg_start, msg_end)], from_peer=chanel)
        except MessageIdInvalidError:
            print("telethon.errors.rpcerrorlist.MessageIdInvalidError")
