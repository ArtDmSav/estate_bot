import configparser

from telethon.sync import TelegramClient
from telethon.tl.functions.messages import GetHistoryRequest

import city
import mysql_message_db
import price
import w_csv_data

# Считываем учетные данные
config = configparser.ConfigParser()
config.read("config.ini")

# Присваиваем значения внутренним переменным
api_id = config['Telegram']['api_id']
api_hash = config['Telegram']['api_hash']
phone = config['Telegram']['username']

# Запускаем клиента
client = TelegramClient(phone, api_id, api_hash)
client.start()

# Задаем переменные
all_messages = []
offset_id = 0
limit = 100
total_messages = 0
total_count_limit = 0
end_id = 0
counter = 0
clean_counter = 0
price_list = []
price_min = 5  # костыль
price_max = 999000  # костыль
find_city = 'Пафос'  # костыль
target_group = 'estatecyprus'  # костыль
flag_1 = True

while True:
    history = client(GetHistoryRequest(
        peer=target_group,
        offset_id=offset_id,
        offset_date=None,
        add_offset=0,
        limit=limit,
        max_id=0,
        min_id=end_id,
        hash=0
    ))
    if not history.messages:
        break
    messages = history.messages

    for message in messages:
        if flag_1:  # сохраняем ид 1го полученого сообщения что бы в
            end_id = message.id  # след итерации остановится на нем
            flag_1 = False
            print('end id = ', end_id)
        counter += 1
        if not message.message == '':  # отсееваем пустые сообщения (фото видео файлы)
            clean_counter += 1
            # Чекаем номер наш порядковый номер сообщения (из limit) и выводим наш реальный порядковый номер сообщения
            # исключая пустые/фото/видео сообщения
            print('________________________________________________ \n'
                  'counter = ', counter,
                  'clean_counter = ', clean_counter
                  )
            # Вызываем функцию поиска цены в сообщении (переводим в нижний регист для удобства)
            pric = price.f_price(message.message.lower())
            if pric == -1:  # Если цены нет то переходим к следующему сообщению
                continue

            if price_min <= pric <= price_max:  # Костыль Чек диапазона цены
                print("price = ", pric, "€")
                try:
                    citys = city.parse(message.message.lower())  # при закреплении сообщения в группе
                except AttributeError:  # ошибка преобразования к lower
                    continue
                # Записываем необходимые данные в таблицу SQL
                mysql_message_db.write(message.date, citys, pric, message.id, message.chat_id)

                # Выводим данные о сообщении для ручного чека
                print("city = ", citys)
                print("data time = ", message.date)
                print(message.id)
                print(message.message)

                # Косыль Записываем необходимые данные в CSV формате
                w_csv_data.write_csv(message.date, citys, pric, message.id, message.chat_id)
    # offset_id = messages[len(messages) - 1].id                 #берет ид предпоследнего сообщения хз зачем
    # print('\noffset_id = ', offset_id)
    # if total_count_limit != 0 and total_messages >= total_count_limit:
    # break
# Выводим таблицу SQL для ручного чека
mysql_message_db.table_view()
print("Парсинг сообщений группы успешно выполнен.")  # Сообщение об удачном парсинге чата.
