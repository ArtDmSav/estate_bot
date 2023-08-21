import pathlib
import sqlite3 as sql

from functions.time_count_decorator import time_count

# Write path to work directory
dir_path = pathlib.Path.cwd()
path = pathlib.Path(dir_path, 'database', 'estate.db')


@time_count
def create_lots():
    connect = sql.connect(path)

    with connect:
        data = connect.execute("select count(*) from sqlite_master where type='table' and name='lots'")
        for row in data:
            if row[0] == 0:
                with connect:
                    connect.execute("""
                        CREATE TABLE lots (
                            city VARCHAR(20),
                            price INTEGER(7),
                            date DATETIME,
                            message_id INTEGER(7) NOT NULL UNIQUE,
                            message_end_id INTEGER(7),
                            chat_id TEXT,
                            msg TEXT(33),
                            PRIMARY KEY(message_id)
                        );
                    """)


@time_count
def create_users():
    connect = sql.connect(path)
    with connect:
        data = connect.execute("select count(*) from sqlite_master where type='table' and name='users'")
        for row in data:
            if row[0] == 0:
                with connect:
                    connect.execute("""
                        CREATE TABLE users (
                            city VARCHAR(20),
                            min_price INTEGER(7),
                            max_price INTEGER(7),
                            msg_chat_id VARCHAR(20) UNIQUE,
                            active INTEGER(1),
                            last_msg_id INTEGER(7),
                            PRIMARY KEY(msg_chat_id)
                        );
                    """)
