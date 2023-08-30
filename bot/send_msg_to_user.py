import configparser

from telethon.sync import TelegramClient

from database import sqlite_view_db, sqlite_commit_db
from functions.time_count_decorator import time_count


@time_count
def send_link_to_bot(active_user_list, last_msg_id):
    # Считываем учетные данные
    config = configparser.ConfigParser()
    config.read("config/config.ini")

    # Присваиваем значения внутренним переменным
    api_id = config['Telegram']['api_id']
    api_hash = config['Telegram']['api_hash']
    bot_token = config['Telegram']['bot_token']

    # We have to manually call "start" if we want an explicit bot token
    bot = TelegramClient('bot', int(api_id), api_hash, system_version="4.16.30-vxCUSTOM").start(bot_token=bot_token)

    with bot:
        # bot.send_message(474103257, 'Thanks for the Telethon library!')
        for row in active_user_list:
            data = sqlite_view_db.request(row[0], row[1], row[2], row[4], int(row[3]))
            flag = True
            for line in data:
                text = f"\n\n{line[4]}\nДанное бъявление доступно по ссылке ->>>  {line[3]}/{line[0]} "
                print(f"USER_ID: {line[2]} DROUP_ID: {line[3]} MSG_ID: {line[0]}")
                bot.send_message(line[2], text)
                last_sent_msg_id = line[0]
                flag = False

            if flag:
                sqlite_commit_db.last_sent_msg_id(last_msg_id, row[3])
            else:
                sqlite_commit_db.last_sent_msg_id(last_sent_msg_id, row[3])
