import sqlite3 as sql


def request():
    connect = sql.connect('estate.db')
    cursor = connect.cursor()
    # user_active = cursor.execute(f"SELECT city, min_price, max_price, msg_chat_id, last_datetime "
    #                              f"FROM users "
    #                              f"WHERE active=1 "
    #                              )
    # print(type(user_active))
    # print(user_active[0])
    # for row in user_active:
    #     print(row[0])

    data = cursor.execute(f"SELECT DISTINCT lots.date, lots.message_id, lots.chat_id, users.msg_chat_id "
                          f"FROM lots "
                          f"JOIN users ON lots.city = users.city "
                          f"WHERE users.active = 1 "
                          f"AND users.msg_chat_id IN ( "
                          f"    SELECT DISTINCT msg_chat_id "
                          f"    FROM users "
                          f"    WHERE active = 1 "
                          f"    AND city = lots.city "
                          f"    AND min_price <= lots.price "
                          f"    AND max_price >= lots.price) "
                          f"ORDER BY lots.date; "
                          )

    connect.close()
    return data
