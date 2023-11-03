from telethon.sync import TelegramClient
from estate_bot.config.data import API_ID, API_HASH, BOT_TOKEN, INACTIVE, ACTIVE
from estate_bot.database import sqlite_view_db, sqlite_commit_db
from estate_bot.functions.time_count_decorator import time_count


@time_count
def send_link_to_bot(last_msg_id):
    active_user_list_ru = sqlite_view_db.active_user(INACTIVE)
    active_user_list_en = sqlite_view_db.active_user(ACTIVE)
    # We have to manually call "start" if we want an explicit bot token
    bot = TelegramClient('bot', int(API_ID), API_HASH, system_version="4.16.30-vxCUSTOM").start(bot_token=BOT_TOKEN)

    with bot:
        for row in active_user_list_ru:
            #                             (city, min_pri, max_pr, lst_msg, user_id)
            data = sqlite_view_db.request(row[0], row[1], row[2], row[4], int(row[3]))
            flag = True
            # line[message_id, {user_id}, chat_id, msg_ru, msg_en]
            for line in data:
                text = f"\n\n{line[3]}\nДанное бъявление доступно по ссылке ->>>  {line[2]}/{line[0]} "
                print(f"USER_ID: {line[1]} DROUP_ID: {line[2]}/{line[0]}")
                bot.send_message(line[1], text)
                if flag:
                    last_sent_msg_id = line[0]
                flag = False

            if flag:
                sqlite_commit_db.last_sent_msg_id(last_msg_id, row[3])
            else:
                sqlite_commit_db.last_sent_msg_id(last_sent_msg_id, row[3])

        for row in active_user_list_en:
            #                             (city, min_pri, max_pr, lst_msg, user_id)
            data = sqlite_view_db.request(row[0], row[1], row[2], row[4], int(row[3]))
            flag = True
            # line[message_id, {user_id}, chat_id, msg]
            for line in data:
                text = f"\n\n{line[4]}\nThis announcement is available at this link ->>>  {line[2]}/{line[0]} "
                print(f"EN_USER_ID: {line[1]} DROUP_ID: {line[2]}/{line[0]}")
                bot.send_message(line[1], text)
                if flag:
                    last_sent_msg_id = line[0]
                flag = False

            if flag:
                sqlite_commit_db.last_sent_msg_id(last_msg_id, row[3])
            else:
                sqlite_commit_db.last_sent_msg_id(last_sent_msg_id, row[3])
