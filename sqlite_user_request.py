import sqlite3 as sql


def request(city='Лимассол', min_price=1000, max_price=2000, user_id='+79372416727'):
    connect = sql.connect('estate.db')
    cursor = connect.cursor()

    data = cursor.execute(f"SELECT * FROM lots WHERE city = '{city}' AND price BETWEEN {min_price} AND {max_price};")

    for row in data:
        print(row)

    connect.close()
