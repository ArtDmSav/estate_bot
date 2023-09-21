import sqlite3 as sql
from pathlib import Path

from estate_bot.functions.time_count_decorator import time_count

dir_path = Path(__file__).parent.resolve()
path = dir_path / 'estate.db'


def view_user():
    connect = sql.connect(path)
    cursor = connect.cursor()

    data = cursor.execute("SELECT city, min_price, max_price, msg_chat_id "
                          "FROM users "
                          "WHERE active = 1 ")

    for row in data:
        print(row)

    connect.close()


@time_count
def active_user():
    active_user_base = []
    connect = sql.connect(path)
    cursor = connect.cursor()

    data = cursor.execute("SELECT city, min_price, max_price, msg_chat_id, last_msg_id "
                          "FROM users "
                          "WHERE active = 1 ")

    for row in data:
        active_user_base.append(row)
        print(row)

    connect.close()
    return active_user_base


@time_count
def request(city, min_price, max_price, last_msg, user_id):
    data_user = []
    connect = sql.connect(path)
    cursor = connect.cursor()

    data = cursor.execute(f"SELECT message_id, message_end_id, {user_id}, chat_id, msg "
                          f"FROM lots "
                          f"WHERE message_id > {last_msg} "
                          f"    AND city = '{city}' "
                          f"    AND price BETWEEN {min_price} AND {max_price} "
                          f"ORDER BY message_id DESC; "
                          )

    for row in data:
        data_user.append(row)
    connect.close()
    return data_user


@time_count
def last_msg_id():
    connect = sql.connect(path)
    cursor = connect.cursor()

    result = cursor.execute(f"SELECT MAX(message_id) "
                            f"FROM lots; "
                            ).fetchall()[0][0]

    connect.close()
    try:
        if result is None:
            return 1
        else:
            return result
    except IndexError:
        return 1
