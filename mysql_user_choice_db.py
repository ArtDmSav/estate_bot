# добавить проверку юзер ид на наличие в таблице
# при наличии заменить на новые входные параметры
# тк юзер ид = праймари кей
import pymysql.cursors


def write(city="Лимассол", low_price=1000, max_price=2500, user_id='+79372416727'):
    # connection = pymysql.connect(host='localhost',
    #                              user='root',
    #                              password='95706271Cy@',
    #                              db='tg_db',
    #                              charset='utf8mb4'
    #                              )
    #
    # create = """use tg_db;
    #        CREATE TABLE user_choice(`id` INT NOT NULL AUTO_INCREMENT,
    #                                 `city` VARCHAR(20) NOT NULL,
    #                                 `low_price` INT(10) NOT NULL,
    #                                 `max_price` INT(10) NOT NULL,
    #                                 `user_id` VARCHAR(20) NOT NULL,
    #                                 PRIMARY KEY (`user_id`));"""
    #
    #
    # connection.close()

    connect = pymysql.connect(host='localhost',
                              user='root',
                              password='95706271Cy@',
                              db='tg_db',
                              charset='utf8mb4',
                              cursorclass=pymysql.cursors.DictCursor
                              )
    with connect.cursor() as cursor:
        cursor.execute("""show tables""")
        print(cursor.fetchall())
        cursor.execute(f"insert into user_choice (city, low_price, max_price, user_id)"
                       f"value('{city}', {low_price}, {max_price}, '{user_id}')")
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
        cursor.execute("SELECT * FROM user_choice")
        for row in cursor.fetchall():
            print(row)
        # cursor.execute("""select * from user_choice;""")
        # print(cursor.fetchall())
    connect.close()


write()
table_view()
