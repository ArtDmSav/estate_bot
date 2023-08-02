import sqlite3 as sql


def active_user():
    active_user_base = []
    connect = sql.connect('database/estate.db')
    cursor = connect.cursor()
    data = cursor.execute("SELECT city, min_price, max_price, msg_chat_id, last_msg_id "
                          "FROM users "
                          "WHERE active = 1 ")
    for row in data:
        active_user_base.append(row)
    connect.close()
    return active_user_base


def request(city="Лимассол", min_price=1000, max_price=2000, last_msg_id=1, user_id=474103257):
    data_user = []
    connect = sql.connect('database/estate.db')
    cursor = connect.cursor()
    data = cursor.execute(f"SELECT message_id, message_end_id, {user_id}, chat_id "
                          f"FROM lots "
                          f"WHERE message_id > {last_msg_id} "
                          f"    AND city = '{city}' "
                          f"    AND price BETWEEN {min_price} AND {max_price} "
                          f"ORDER BY message_id DESC; "
                          #
                          # f"SELECT DISTINCT lots.date, lots.message_id, lots.message_end_id, lots.chat_id, "
                          # f"users.msg_chat_id "
                          # f"FROM lots "
                          # f"JOIN users ON lots.city = users.city "
                          # f"WHERE users.active = 1 "
                          # f"AND users.msg_chat_id IN ( "
                          # f"    SELECT DISTINCT msg_chat_id "
                          # f"    FROM users "
                          # f"    WHERE active = 1 "
                          # f"    AND city = lots.city "
                          # f"    AND min_price <= lots.price "
                          # f"    AND max_price >= lots.price) "
                          # f"ORDER BY lots.date; "
                          )
    for row in data:
        data_user.append(row)
    connect.close()
    return data_user
