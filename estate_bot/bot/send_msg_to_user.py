from telethon.sync import TelegramClient

from estate_bot.config.data import API_ID, API_HASH, BOT_TOKEN
from estate_bot.database import sqlite_view_db, sqlite_commit_db
from estate_bot.functions.time_count_decorator import time_count


@time_count
def send_link_to_bot(active_user_list, last_msg_id):
    # We have to manually call "start" if we want an explicit bot token
    bot = TelegramClient('bot', int(API_ID), API_HASH, system_version="4.16.30-vxCUSTOM").start(bot_token=BOT_TOKEN)

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
