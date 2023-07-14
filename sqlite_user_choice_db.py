# добавить проверку юзер ид на наличие в таблице
# при наличии заменить на новые входные параметры
# тк юзер ид = праймари кей
import sqlite3 as sql


def write(city="Лимассол", min_price=1000, max_price=2500, user_id='+79372416727'):
    connect = sql.connect('estate.db')
    cursor = connect.cursor()
    cursor.execute(f"INSERT INTO users (city, min_price, max_price, user_id)"
                   f"VALUES ('{city}', {min_price}, {max_price}, '{user_id}')")
    connect.commit()
    connect.close()


def table_view():
    connect = sql.connect('estate.db')
    cursor = connect.cursor()
    data = cursor.execute("SELECT * FROM users")
    for row in data:
        print(row)
    connect.close()
