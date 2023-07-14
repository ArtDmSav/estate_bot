import sqlite3 as sql

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
                        id INTEGER PRIMARY KEY AUTO_INCREMENT,
                        city VARCHAR(20),
                        price INTEGER,
                        date DATETIME
                        message_id INTEGER
                        chat_id BIGINTEGER 
                    );
                """)


def write(date='2023-03-25 22:54:40+00:00', city='lim', price=1000, message_id=224491,
          chat_id=-1001261922335):  # (date, city, price, message_id, chat_id):

    connect = sql.connect("estate.db")

    with connect.cursor() as cursor:
        cursor.execute("""show tables""")
        print(cursor.fetchall())
        cursor.execute(f"insert into tg_messages (city, price, date, message_id, chat_id)"
                       f"value('{city}', {price}, '{date}', {message_id}, {chat_id})")

    connect.commit()
    connect.close()


def table_view():
    connect = pymysql.connect(host='localhost',
                              user='root',
                              password='95706271Cy@',
                              db='tg_db',
                              charset='utf8mb4',
                              cursorclass=pymysql.cursors.DictCursor
                              )

    with connect.cursor() as cursor:
        cursor.execute("SELECT * FROM tg_messages")
        for row in cursor.fetchall():
            print(row)

    connect.close()
