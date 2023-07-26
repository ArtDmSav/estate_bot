import sqlite3 as sql
from datetime import datetime, timedelta


# import time


def write_lots(date, city='lim', price=1000, message_id=224491,
               chat_id=-1001261922335, end_id='NULL'):  # (date, city, price, message_id, chat_id):
    i = date
    date = i.date()
    if end_id == message_id:
        end_id = -1
    connect = sql.connect("estate.db")
    cursor = connect.cursor()
    cursor.execute(
        f"INSERT INTO lots (city, price, date, message_id, message_end_id, chat_id) VALUES ('{city}', {price}, '{date}'"
        f", {message_id}, {end_id}, {chat_id})")

    connect.commit()
    connect.close()


def write_user(city='Лимассол', min_price=1000, max_price=2000,
               msg_chat_id=474103257, active=1,
               last_datetime='2024-09-24 22:54:40+00:00'):  # (date, city, price, msg_message_id, chat_id):
    connect = sql.connect("estate.db")

    cursor = connect.cursor()
    cursor.execute(f"""SELECT msg_chat_id FROM users WHERE msg_chat_id={msg_chat_id}""")
    try:
        cursor.fetchall()[0][0]
    except IndexError:
        cursor.execute(
            f"INSERT INTO users (city, min_price, max_price, msg_chat_id, active, last_datetime) "
            f"VALUES ('{city}', {min_price}, {max_price}, {msg_chat_id}, {active}, '{last_datetime}')")
        connect.commit()
    else:
        cursor.execute(
            f" UPDATE users SET city=?, min_price=?, max_price=?, active=1 WHERE msg_chat_id=?",
            (city, min_price, max_price, msg_chat_id))
        connect.commit()
    connect.close()


def stop_user(msg_chat_id=474103257):
    print('write_user start')
    connect = sql.connect("estate.db")

    cursor = connect.cursor()
    cursor.execute(f"UPDATE users SET active=0 WHERE msg_chat_id={msg_chat_id}")
    print('sql update ok')
    connect.commit()
    connect.close()


def table_view_lots():
    connect = sql.connect("estate.db")

    data = connect.execute("SELECT * FROM lots")
    for row in data:
        print(row)

    connect.close()


def table_view_users():
    connect = sql.connect("estate.db")

    date = connect.execute("SELECT * FROM users")
    for row in date:
        print(row)

    connect.close()


def last_msg_id():
    connect = sql.connect("estate.db")

    cursor = connect.cursor()
    result = cursor.execute(f"SElECT MAX(message_id) "
                            f"FROM lots").fetchall()[0][0]
    connect.close()

    try:
        print('last_msg_id = ', result)
        return result
    except IndexError:
        return None


def del_repeating_msg():
    connect = sql.connect("estate.db")

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


def del_old_msg(day):
    # start_count = time.time()
    connect = sql.connect("estate.db")

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


def add_msg_end_id():
    connect = sql.connect("estate.db")

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


add_msg_end_id()
