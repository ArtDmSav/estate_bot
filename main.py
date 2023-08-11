import send_msg_to_user
from bot.bot_telethon import parsing_chat
from database import sqlite_message_db, sqlite_user_request
from functions.time_count_decorator import full_time

# Create database and tables
# sqlite_create_db.create_lots()
# sqlite_create_db.create_users()

# Delete old messages
del_msg_after_day = 30
sqlite_message_db.del_old_msg(del_msg_after_day)

last_msg_id = sqlite_message_db.last_msg_id()
parsing_chat(last_msg_id)

active_user_list = sqlite_user_request.active_user()
print(active_user_list)
last_sent_msg_id = 0
flag = True
for row in active_user_list:
    data = sqlite_user_request.request(row[0], row[1], row[2], row[4], int(row[3]))
    for line in data:
        send_msg_to_user.send_msg_f_user(line[0], line[1], line[2], line[3])
        print(line[0], line[1], line[2], line[3])
        if flag:
            if line[1] != -1:
                last_sent_msg_id = line[1]
                flag = False
            else:
                last_sent_msg_id = line[0]
                flag = False

    if flag:
        sqlite_message_db.last_sent_msg_id(last_msg_id, row[3])
    else:
        sqlite_message_db.last_sent_msg_id(last_sent_msg_id, row[3])

full_time()
