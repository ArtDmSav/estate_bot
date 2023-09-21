from estate_bot.bot.bot_telethon import parsing_chat
from estate_bot.bot.send_msg_to_user import send_link_to_bot
from estate_bot.config.data import DEL_MSG_AFTER_DAY
from estate_bot.database.sqlite_commit_db import del_old_msg
from estate_bot.database.sqlite_view_db import last_msg_id
from estate_bot.functions.time_count_decorator import full_time


def do_it():
    # Create database and tables
    # sqlite_create_db.create_lots()
    # sqlite_create_db.create_users()

    lst_msg_id = last_msg_id()

    del_old_msg(DEL_MSG_AFTER_DAY)
    parsing_chat(lst_msg_id)
    send_link_to_bot(lst_msg_id)
    full_time()


do_it()
