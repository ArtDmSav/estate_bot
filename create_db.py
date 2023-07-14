import sqlite3 as sql


def create_lots():
    connect = sql.connect("estate.db")

    with connect:
        # получаем количество таблиц с нужным нам именем
        data = connect.execute("select count(*) from sqlite_master where type='table' and name='lots'")
        for row in data:
            # если таких таблиц нет
            if row[0] == 0:
                # создаём таблицу для товаров
                with connect:
                    connect.execute("""
                        CREATE TABLE lots (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            city VARCHAR(20),
                            price INTEGER,
                            date DATETIME,
                            message_id INTEGER,
                            chat_id BIGINTEGER 
                        );
                    """)


def create_users():
    connect = sql.connect("estate.db")

    with connect:
        # получаем количество таблиц с нужным нам именем
        data = connect.execute("select count(*) from sqlite_master where type='table' and name='users'")
        for row in data:
            # если таких таблиц нет
            if row[0] == 0:
                # создаём таблицу для товаров
                with connect:
                    connect.execute("""
                        CREATE TABLE users (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            city VARCHAR(20),
                            min_price INTEGER,
                            max_price INTEGER,
                            user_id VARCHAR(20)
                        );
                    """)
