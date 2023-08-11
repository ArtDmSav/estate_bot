import pathlib
import sqlite3 as sql
from datetime import datetime, timedelta
from pathlib import Path

from functions.time_count_decorator import time_count

dir_path = pathlib.Path.cwd()
path = Path(dir_path, 'database', 'estate.db')
print(str(path))


@time_count
def write_lots(date, city='lim', price=1000, message_id=224491,
               chat_id=-1001261922335, end_id='NULL'):  # (date, city, price, message_id, chat_id):
    i = date
    date = i.date()
    if end_id == message_id:
        end_id = -1
    connect = sql.connect("database/estate.db")
    cursor = connect.cursor()
    cursor.execute(
        f"INSERT INTO lots (city, price, date, message_id, message_end_id, chat_id) VALUES ('{city}', {price}, '{date}'"
        f", {message_id}, {end_id}, {chat_id})")

    connect.commit()
    connect.close()


@time_count
def write_user(city='Лимассол', min_price=1000, max_price=2000,
               msg_chat_id=474103257, active=1, last_msg_id=1):
    print("kgdjsnjsfnvksjdnbvksdjnfbkdsnb= ", last_msg_id)
    connect = sql.connect("database/estate.db")

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
def stop_user(msg_chat_id=474103257):
    print('write_user start')
    connect = sql.connect("database/estate.db")

    cursor = connect.cursor()
    cursor.execute(f"UPDATE users SET active=0 WHERE msg_chat_id={msg_chat_id}")
    print('sql update ok')
    connect.commit()
    connect.close()


@time_count
def table_view_lots():
    connect = sql.connect("database/estate.db")

    data = connect.execute("SELECT * FROM lots")
    for row in data:
        print(row)

    connect.close()


@time_count
def table_view_users():
    connect = sql.connect("database/estate.db")

    date = connect.execute("SELECT * FROM users")
    for row in date:
        print(row)

    connect.close()


@time_count
def last_msg_id():
    connect = sql.connect("database/estate.db")

    cursor = connect.cursor()
    result = cursor.execute(f"SELECT "
                            f"CASE "
                            f"WHEN message_end_id = -1 THEN MAX(message_id) "
                            f"ELSE message_end_id "
                            f"END AS result "
                            f"FROM lots; "
                            ).fetchall()[0][0]
    # Old version
    # result = cursor.execute(f"SElECT MAX(message_id) "
    #                         f"FROM lots").fetchall()[0][0]
    connect.close()

    try:
        print('last_msg_id = ', result)
        return result
    except IndexError:
        return None


@time_count
def del_repeating_msg():
    connect = sql.connect("database/estate.db")

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
def del_old_msg(day):
    # start_count = time.time()
    connect = sql.connect("database/estate.db")

    cursor = connect.cursor()
    date = cursor.execute(f"SElECT date, message_id "
                          f"FROM lots ").fetchall()

    for row in date:
        times = datetime.strptime(row[0], '%Y-%m-%d')
        if (datetime.now() - times) > timedelta(days=day):
            cursor.execute(f"DELETE FROM lots "
                           f"WHERE message_id = {row[1]}; ")

    connect.commit()
    connect.close()
    # end_count = time.time()
    # print(round(end_count-start_count, 3), ' sec')


@time_count
def add_msg_end_id():
    connect = sql.connect("database/estate.db")

    cursor = connect.cursor()
    # cursor.execute(f"UPDATE lots "
    #                f"SET message_end_id = NULL;")

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
                   f"    WHERE sorted_lots.id = lots.id "
                   f") "
                   f"WHERE message_end_id IS NULL; "
                   )

    connect.commit()
    connect.close()


@time_count
def last_sent_msg_id(last_sent_msg_id, user_id):
    print(f'write_last_sent_msg_id = {last_sent_msg_id}, user_id = {user_id}')
    connect = sql.connect("database/estate.db")

    cursor = connect.cursor()
    cursor.execute(f"UPDATE users SET last_msg_id={last_sent_msg_id} WHERE msg_chat_id={user_id}")

    connect.commit()
    connect.close()
