import configparser

from telethon.errors.rpcerrorlist import MessageIdInvalidError
from telethon.sync import TelegramClient

from database import sqlite_view_db, sqlite_commit_db
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


@time_count
def send_msgs_f_users(active_user_list, last_msg_id):
    # Считываем учетные данные
    config = configparser.ConfigParser()
    config.read("config/config.ini")

    # Присваиваем значения внутренним переменным
    api_id = config['Telegram']['api_id']
    api_hash = config['Telegram']['api_hash']
    phone = config['Telegram']['username']

    last_sent_msg_id = 0
    flag = True

    with TelegramClient(phone, int(api_id), api_hash) as client:
        for row in active_user_list:
            data = sqlite_view_db.request(row[0], row[1], row[2], row[4], int(row[3]))
            for line in data:
                # catch msg error (usually trigger msg from admin group)
                try:
                    if line[1] == -1:

                        client.forward_messages(entity=line[2], messages=line[0], from_peer=line[3])
                    else:
                        client.forward_messages(entity=line[2], messages=[_ for _ in range(line[0], line[1])],
                                                from_peer=line[3])
                except MessageIdInvalidError:
                    print("telethon.errors.rpcerrorlist.MessageIdInvalidError")

                print(line[0], line[1], line[2], line[3])
                if flag:
                    if line[1] != -1:
                        last_sent_msg_id = line[1]
                        flag = False
                    else:
                        last_sent_msg_id = line[0]
                        flag = False

            if flag:
                sqlite_commit_db.last_sent_msg_id(last_msg_id, row[3])
            else:
                sqlite_commit_db.last_sent_msg_id(last_sent_msg_id, row[3])
