from bot.bot_telethon import parsing_chat
from bot.send_msg_to_user import send_link_to_bot
from database import sqlite_commit_db, sqlite_view_db
from functions.time_count_decorator import full_time


# @repeat(every(9).minutes)
def do_it():
    # Create database and tables
    # sqlite_create_db.create_lots()
    # sqlite_create_db.create_users()

    # Delete old messages
    del_msg_after_day = 7
    sqlite_commit_db.del_old_msg(del_msg_after_day)

    last_msg_id = sqlite_view_db.last_msg_id()
    parsing_chat(last_msg_id)

    active_user_list = sqlite_view_db.active_user()
    send_link_to_bot(active_user_list, last_msg_id)
    full_time()


do_it()
# while True:
#     run_pending()
#     time.sleep(5)
