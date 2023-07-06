import pymysql.cursors


def request(city='Лимассол', min_price=1000, max_price=2000, user_id='+79372416727'):
    connect = pymysql.connect(host='localhost',
                              user='root',
                              password='95706271Cy@',
                              db='tg_db',
                              charset='utf8mb4',
                              cursorclass=pymysql.cursors.DictCursor
                              )

    with connect.cursor() as cursor:
        cursor.execute(f"SELECT * FROM tg_messages "
                       f"WHERE city = '{city}' AND price BETWEEN {min_price} AND {max_price};")

        for row in cursor.fetchall():
            print(row)
            print('\n', row['city'])

    connect.close()


request()
