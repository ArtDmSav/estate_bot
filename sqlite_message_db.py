import sqlite3 as sql


def write(date='2024-09-24 22:54:40+00:00', city='lim', price=1000, message_id=224491,
          chat_id=-1001261922335):  # (date, city, price, message_id, chat_id):

    connect = sql.connect("estate.db")

    cursor = connect.cursor()
    cursor.execute(
        f"INSERT INTO lots (city, price, date, message_id, chat_id) VALUES ('{city}', {price}, '{date}', {message_id}, {chat_id})")

    connect.commit()
    connect.close()


def table_view():
    connect = sql.connect("estate.db")

    date = connect.execute("SELECT * FROM lots")
    for row in date:
        print(row)

    connect.close()
