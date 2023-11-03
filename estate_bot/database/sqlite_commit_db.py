import sqlite3 as sql
from datetime import datetime, timedelta
from pathlib import Path

from estate_bot.config.data import DEL_MSG_AFTER_DAY
from estate_bot.functions.time_count_decorator import time_count

dir_path = Path(__file__).parent.resolve()
path = dir_path / 'estate.db'
user_log_path = f"{Path.cwd()}/logs/user_history"



@time_count
def write_lots(date, city, price, message_id, chat_id, msg, msg_en=' ', msg_ru=' '):
    i = date
    date = i.date()
    print(f"GROUP_ID: {chat_id}/{message_id} CITY: {city} PRICE: {price}")
    connect = sql.connect(path)
    cursor = connect.cursor()

    cursor.execute(f"""SELECT message_id FROM lots WHERE message_id={message_id}""")

    # check to double UNIQUE constraint: lots.message_id
    # p.s. added after real case in production release
    if not any(cursor.fetchall()):
        try:
            cursor.execute(
                f"INSERT INTO lots (city, price, date, message_id, chat_id, msg, msg_en, msg_ru) "
                f"VALUES ('{city}', {price}, '{date}', {message_id}, '{chat_id}', "
                f"'{msg}', '{msg_en}', '{msg_ru}') "
            )
        except ValueError:
            print("sqlite3.OperationalError: ValueError")
        except SyntaxError:
            print("sqlite3.OperationalError: SyntaxError")

    else:
        print("double lots with id: ", message_id)
        print("sqlite3.IntegrityError: UNIQUE constraint failed: lots.message_id")

    connect.commit()
    connect.close()


@time_count
def write_user(city, min_price, max_price, msg_chat_id, active, last_msg_id=1, english=0, chat_username='o'):
    connect = sql.connect(path)

    cursor = connect.cursor()
    cursor.execute(f"""SELECT msg_chat_id FROM users WHERE msg_chat_id={msg_chat_id}""")
    if not any(cursor.fetchall()):
        cursor.execute(
            f"INSERT INTO users (city, min_price, max_price, msg_chat_id, active, last_msg_id, english) "
            f"VALUES ('{city}', {min_price}, {max_price}, {msg_chat_id}, {active}, '{last_msg_id}', {english}) "
        )
        connect.commit()
        with open(f"{user_log_path}/{msg_chat_id}.txt", 'w') as f:
            f.write(chat_username + '\n')
            f.write(str(datetime.now()) + '\n')
            f.write(f"{city}: {min_price} - {max_price}, user_active: {active}, english: {english}\n")
    else:
        cursor.execute(
            f"UPDATE users SET city=?, min_price=?, max_price=?, active=?, last_msg_id=?, english=? WHERE msg_chat_id=?"
            , (city, min_price, max_price, active, last_msg_id, english, msg_chat_id))
        connect.commit()
        with open(f"{user_log_path}/{msg_chat_id}.txt", 'a') as f:
            f.writelines(str(datetime.now())+'\n')
            f.writelines(f"{city}: {min_price} - {max_price} euro, user_active: {active}, english: {english}\n")

    connect.close()


@time_count
def stop_user(msg_chat_id):
    connect = sql.connect(path)
    cursor = connect.cursor()

    cursor.execute(f"UPDATE users SET active=0 WHERE msg_chat_id={msg_chat_id}")
    connect.commit()
    connect.close()

    with open(f"{user_log_path}/{msg_chat_id}.txt", 'a') as f:
        f.write(str(datetime.now()) + '\n')
        f.write(f"deactivation bot\n")


@time_count
def del_repeating_msg():
    connect = sql.connect(path)
    cursor = connect.cursor()

    cursor.execute(f"DELETE FROM lots "
                   f"WHERE id NOT IN ( "
                   f"   SELECT MIN(id) "
                   f"   FROM lots"
                   f"   GROUP BY message_id "
                   f"); "
                   )

    connect.commit()
    connect.close()


@time_count
def del_old_msg():
    time_del = (datetime.now() - timedelta(days=DEL_MSG_AFTER_DAY))

    connect = sql.connect(path)
    cursor = connect.cursor()

    data = cursor.execute(f"SELECT date, MAX(message_id) AS max_message_id "
                          f"FROM lots "
                          f"GROUP BY date; ").fetchall()
    for row in data:
        print(row[0], row[1])
        times = datetime.strptime(row[0], '%Y-%m-%d')
        if times < time_del:
            cursor.execute(f"DELETE FROM lots "
                           f"WHERE message_id <= {row[1]}; ")

    connect.commit()
    connect.close()


@time_count
def last_sent_msg_id(last_sent_msg_id, user_id):
    connect = sql.connect(path)
    cursor = connect.cursor()

    cursor.execute(f"UPDATE users SET last_msg_id={last_sent_msg_id} WHERE msg_chat_id={user_id}")

    connect.commit()
    connect.close()

    # @time_count
    # def add_msg_end_id():
    #     connect = sql.connect(path)
    #     cursor = connect.cursor()
    #
    #     cursor.execute(f"WITH sorted_lots AS ( "
    #                    f"   SELECT *, "
    #                    f"       LEAD(message_id, 1) OVER (ORDER BY message_id) as next_message_id "
    #                    f"   FROM lots "
    #                    f") "
    #                    f"UPDATE lots "
    #                    f"SET message_end_id = ( "
    #                    f"    SELECT CASE "
    #                    f"        WHEN sorted_lots.message_id = sorted_lots.next_message_id -1 THEN -1 "
    #                    f"        ELSE sorted_lots.next_message_id "
    #                    f"       END "
    #                    f"    FROM sorted_lots "
    #                    f"    WHERE sorted_lots.message_id = lots.message_id "
    #                    f") "
    #                    f"WHERE message_end_id IS NULL; "
    #                    )
    #
    #     connect.commit()
    #     connect.close()
