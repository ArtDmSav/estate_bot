import configparser

import pymysql.cursors

# Считываем учетные данные
config = configparser.ConfigParser()
config.read("config.ini")
pas = config['SQL']['db_password']
name = config['SQL']['db_name']


def write(date='2023-03-25 22:54:40+00:00', city='lim', price=1000, message_id=224491,
          chat_id=-1001261922335):  # (date, city, price, message_id, chat_id):

    connect = pymysql.connect(host='localhost',
                              user='root',
                              password=pas,
                              db=name,
                              charset='utf8mb4',
                              cursorclass=pymysql.cursors.DictCursor
                              )

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
                              password=pas,
                              db=name,
                              charset='utf8mb4',
                              cursorclass=pymysql.cursors.DictCursor
                              )

    with connect.cursor() as cursor:
        cursor.execute("SELECT * FROM tg_messages")
        for row in cursor.fetchall():
            print(row)

    connect.close()
