import sqlite3 as sql


def create_lots():
    connect = sql.connect("database/estate.db")

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
                            price INTEGER(7),
                            date DATETIME,
                            message_id INTEGER(7),
                            message_end_id INTEGER(7),
                            chat_id BIGINTEGER(14) 
                        );
                    """)


def create_users():
    connect = sql.connect("database/estate.db")

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
                            min_price INTEGER(7),
                            max_price INTEGER(7),
                            msg_chat_id VARCHAR(20),
                            active INTEGER(1),
                            last_msg_id INTEGER(7)
                        );
                    """)
