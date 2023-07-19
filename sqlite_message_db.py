import sqlite3 as sql


def write_lots(date='2024-09-24 22:54:40+00:00', city='lim', price=1000, message_id=224491,
               chat_id=-1001261922335):  # (date, city, price, message_id, chat_id):

    connect = sql.connect("estate.db")

    cursor = connect.cursor()
    cursor.execute(
        f"INSERT INTO lots (city, price, date, message_id, chat_id) VALUES ('{city}', {price}, '{date}', {message_id}, {chat_id})")

    connect.commit()
    connect.close()


def write_user(city='Лимассол', min_price=1000, max_price=2000,
               chat_id=474103257, active=1,
               last_datetime='2024-09-24 22:54:40+00:00'):  # (date, city, price, message_id, chat_id):
    connect = sql.connect("estate.db")

    cursor = connect.cursor()
    cursor.execute(f"""SELECT chat_id FROM users WHERE chat_id={chat_id}""")
    try:
        cursor.fetchall()[0][0]
    except IndexError:
        cursor.execute(
            f"INSERT INTO users (city, min_price, max_price, chat_id, active, last_datetime) "
            f"VALUES ('{city}', {min_price}, {max_price}, {chat_id}, {active}, '{last_datetime}')")
        connect.commit()
    else:
        cursor.execute(
            f" UPDATE users SET city=?, min_price=?, max_price=?, active=1 WHERE chat_id=?",
            (city, min_price, max_price, chat_id))
        connect.commit()
    connect.close()


def stop_user(chat_id=474103257):
    print('write_user start')
    connect = sql.connect("estate.db")

    cursor = connect.cursor()
    cursor.execute(f"UPDATE users SET active=0 WHERE chat_id={chat_id}")
    print('sql update ok')
    connect.commit()
    connect.close()


def table_view_lots():
    connect = sql.connect("estate.db")

    date = connect.execute("SELECT * FROM lots")
    for row in date:
        print(row)

    connect.close()


def table_view_users():
    connect = sql.connect("estate.db")

    date = connect.execute("SELECT * FROM users")
    for row in date:
        print(row)

    connect.close()
