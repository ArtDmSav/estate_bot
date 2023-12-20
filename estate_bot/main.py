from bot.bot_telethon import parsing_chat
from bot.send_msg_to_user import send_link_to_bot
from database.sqlite_commit_db import del_old_msg
from database.sqlite_view_db import last_msg_id, view_user
from functions.time_count_decorator import full_time
from schedule import every, repeat, run_pending
import time
import sys
from datetime import datetime


@repeat(every(9).minutes)
def do_it():
    global count
    print(count)
    count += 1
    # Create database and tables
    # sqlite_create_db.create_lots()
    # sqlite_create_db.create_users()

    print(datetime.now())
    view_user()

    lst_msg_id = last_msg_id()
    del_old_msg()
    parsing_chat(lst_msg_id)
    send_link_to_bot(lst_msg_id)
    full_time()
    if count>5:
        sys.exit()


count = 0
#def loop_do_it()
while True:
    run_pending()
    time.sleep(10)

