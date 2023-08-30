import configparser
import pathlib

from telethon.sync import TelegramClient
from telethon.tl.functions.messages import GetHistoryRequest

from database import sqlite_commit_db
from functions import city_parsing, price_parsing
from functions.time_count_decorator import time_count


@time_count
def parsing_chat(last_msg_id):
    # Write path to work directory
    dir_path = pathlib.Path.cwd()
    path = pathlib.Path(dir_path, 'config', 'config.ini')

    # # Write path to work directory
    # dir_path = Path.home()
    # path = dir_path/'estate_bot/config/config.ini'

    # Read config file
    config = configparser.ConfigParser()
    config.read(path)

    # Assign data from file
    api_id = int(config['Telegram']['api_id'])
    api_hash = config['Telegram']['api_hash']
    # phone = config['Telegram']['username']

    # Start telegram client by telethon
    client = TelegramClient("6660980557", api_id, api_hash, system_version="4.16.30-vxCUSTOM")
    client.start()

    # Set data
    offset_id = 0
    limit = 500
    end_id = 0
    counter = 0
    target_group = 't.me/estatecyprus'
    flag_1 = True
    flag_2 = True

    while True:
        # noinspection PyTypeChecker
        history = client(GetHistoryRequest(
            peer=target_group,  # Don't warn ing, it's OK
            offset_id=offset_id,  # Offset message ID (only messages previous to the given ID will be retrieved).
            offset_date=None,  # (datetime): Offset date (messages previous to this date will be retrieved). Exclusive
            add_offset=0,  # (int): Additional message offset (all the specified offsets + this offset = older messages)
            limit=limit,  # (int | None, optional): Number of messages to be retrieved. Due to limitations with the API
            # retrieving more than 3000 messages will take longer than half a minute (or even more based on
            # previous calls).
            max_id=0,
            min_id=end_id,  # (int): All the messages with a lower (older) ID or equal to this will be excluded.
            hash=0
        ))

        if not history.messages:
            sqlite_commit_db.add_msg_end_id()
            client.disconnect()
            return
        messages = history.messages

        for message in messages:
            if message.id <= last_msg_id:
                sqlite_commit_db.add_msg_end_id()
                client.disconnect()
                return

            if flag_1:  # save id first message. it's end id for next iteration
                end_id = message.id
                flag_1 = False
                flag_2 = True

            if message.message != '':  # skip message without text (skip photo, video message)

                # Call find price func in message (use low register for all text)
                str_message = str(message.message).lower()
                price = price_parsing.f_price(str_message)
                if price == -1:  # If we can't find price, we move to the next message
                    continue

                try:
                    city = city_parsing.parse(message.message.lower())
                except AttributeError:  # Catch transformation to low error (debug)
                    print(AttributeError)
                    continue

                # Add lot to database
                if flag_2:
                    flag_2 = False
                    sqlite_commit_db.write_lots(message.date, city, price, message.id, target_group,
                                                message.message, end_id)
                    counter += 1
                else:
                    sqlite_commit_db.write_lots(message.date, city, price, message.id, target_group, message.message)
                    counter += 1

                # Print data for manual check (debug)
                # print("price = ", price, "€")
                # print("city = ", city)
                # print(message.id)
                # print(message.message)
