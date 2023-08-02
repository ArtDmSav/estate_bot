import configparser
import logging

from telethon.sync import TelegramClient
from telethon.tl.functions.messages import GetHistoryRequest

from database import sqlite_message_db
from functions import city_parsing, price_parsing


def parsing_chat(last_msg_id):
    logging.basicConfig(level=logging.DEBUG, filename='logs/bot_telethon.log',
                        format='%(levelname)s (%(asctime)s): %(message)s (Line: %(lineno)d) [%(filename)s]',
                        datefmt='%d/%m/%Y %I:%M:%S', encoding='UTF-8', filemode='w'
                        )
    logging.warning('warning')
    logging.critical('critical')
    logging.debug('debug')
    logging.info('info')
    logging.error('error')

    # Read config file
    config = configparser.ConfigParser()
    config.read("config/config.ini")

    # Assign data from file
    api_id = int(config['Telegram']['api_id'])
    api_hash = config['Telegram']['api_hash']
    phone = config['Telegram']['username']

    # Start telegram client by telethon
    client = TelegramClient(phone, api_id, api_hash)
    client.start()

    # Set data
    offset_id = 0
    limit = 2000
    end_id = 0
    counter = 0
    clean_counter = 0
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
            sqlite_message_db.add_msg_end_id()
            client.disconnect()
            return
        messages = history.messages

        for message in messages:
            if message.id <= last_msg_id:
                sqlite_message_db.add_msg_end_id()
                client.disconnect()
                return

            if flag_1:  # save id first message. it's end id for next iteration
                end_id = message.id
                flag_1 = False
                flag_2 = True
                print('end_id_if = ', end_id)
            counter += 1
            if not message.message == '':  # skip message without text (skip photo, video message)
                clean_counter += 1

                # Print our count message number, and 'clean' message number (only message with text)
                print('________________________________________________ \n'
                      'counter = ', counter,
                      'clean_counter = ', clean_counter
                      )
                # Call find price func in message (use low register for all text)
                str_message = str(message.message).lower()
                price = price_parsing.f_price(str_message)
                # price = price_parsing.f_price(message.message.lower())
                if price == -1:  # If we can't find price, we move to the next message
                    continue

                print("price = ", price, "€")
                try:
                    city = city_parsing.parse(message.message.lower())
                except AttributeError:  # Catch transformation to low error (debug)
                    print(AttributeError)
                    continue

                # Add date to database
                if flag_2:
                    flag_2 = False
                    sqlite_message_db.write_lots(message.date, city, price, message.id, message.chat_id, end_id)
                else:
                    sqlite_message_db.write_lots(message.date, city, price, message.id, message.chat_id)

                # Print data for manual check (debug)
                print("city = ", city)
                print("data time = ", message.date)
                print(message.id)
                print(message.message)
