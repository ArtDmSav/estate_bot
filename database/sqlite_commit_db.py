import pathlib
import sqlite3 as sql
from datetime import datetime, timedelta

from functions.time_count_decorator import time_count

dir_path = pathlib.Path.cwd()
path = pathlib.Path(dir_path, 'database', 'estate.db')


@time_count
def write_lots(date, city, price, message_id, chat_id, end_id='NULL'):
    i = date
    date = i.date()
    if end_id == message_id:
        end_id = -1
    connect = sql.connect(path)
    cursor = connect.cursor()

    cursor.execute(
        f"INSERT INTO lots (city, price, date, message_id, message_end_id, chat_id) VALUES ('{city}', {price}, '{date}'"
        f", {message_id}, {end_id}, {chat_id})")

    connect.commit()
    connect.close()


@time_count
def write_user(city, min_price, max_price, msg_chat_id, active, last_msg_id=1):
    connect = sql.connect(path)

    cursor = connect.cursor()

    cursor.execute(f"""SELECT msg_chat_id FROM users WHERE msg_chat_id={msg_chat_id}""")
    try:
        cursor.fetchall()[0][0]
    except IndexError:

        cursor.execute(
            f"INSERT INTO users (city, min_price, max_price, msg_chat_id, active, last_msg_id) "
            f"VALUES ('{city}', {min_price}, {max_price}, {msg_chat_id}, {active}, '{last_msg_id}')")

        connect.commit()
    else:

        cursor.execute(
            f" UPDATE users SET city=?, min_price=?, max_price=?, active=?, last_msg_id=? WHERE msg_chat_id=?",
            (city, min_price, max_price, 1, last_msg_id, msg_chat_id))

        connect.commit()
    connect.close()


@time_count
def stop_user(msg_chat_id):
    connect = sql.connect(path)
    cursor = connect.cursor()

    cursor.execute(f"UPDATE users SET active=0 WHERE msg_chat_id={msg_chat_id}")

    connect.commit()
    connect.close()



@time_count
def del_repeating_msg():
    connect = sql.connect(path)
    cursor = connect.cursor()

    cursor.execute(f"DELETE FROM lots "
                   f"WHERE id NOT IN ( "
                   f"   SELECT MIN(id) "
                   f"   FROM lots"
                   f"   GROUP BY message_id "
                   f"); "
                   )

    connect.commit()
    connect.close()


@time_count
def del_old_msg(days):
    connect = sql.connect(path)
    cursor = connect.cursor()

    date = cursor.execute(f"SElECT date, message_id "
                          f"FROM lots ").fetchall()

    for row in date:
        times = datetime.strptime(row[0], '%Y-%m-%d')
        if (datetime.now() - times) > timedelta(days=days):
            cursor.execute(f"DELETE FROM lots "
                           f"WHERE message_id = {row[1]}; ")

    connect.commit()
    connect.close()


@time_count
def add_msg_end_id():
    connect = sql.connect(path)
    cursor = connect.cursor()

    cursor.execute(f"WITH sorted_lots AS ( "
                   f"   SELECT *, "
                   f"       LEAD(message_id, 1) OVER (ORDER BY message_id) as next_message_id "
                   f"   FROM lots "
                   f") "
                   f"UPDATE lots "
                   f"SET message_end_id = ( "
                   f"    SELECT CASE "
                   f"        WHEN sorted_lots.message_id = sorted_lots.next_message_id -1 THEN -1 "
                   f"        ELSE sorted_lots.next_message_id "
                   f"       END "
                   f"    FROM sorted_lots "
                   f"    WHERE sorted_lots.message_id = lots.message_id "
                   f") "
                   f"WHERE message_end_id IS NULL; "
                   )

    connect.commit()
    connect.close()


@time_count
def last_sent_msg_id(last_sent_msg_id, user_id):
    connect = sql.connect(path)
    cursor = connect.cursor()

    cursor.execute(f"UPDATE users SET last_msg_id={last_sent_msg_id} WHERE msg_chat_id={user_id}")

    connect.commit()
    connect.close()
