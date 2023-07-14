import configparser
import logging

from telethon.sync import TelegramClient
from telethon.tl.functions.messages import GetHistoryRequest

import city_parsing
import create_db
import price_parsing
import sqlite_message_db

# Write logs
logging.basicConfig(level=logging.DEBUG, filename='main_estate.log',
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
config.read("config.ini")

# Assign data from file
api_id = int(config['Telegram']['api_id'])
api_hash = config['Telegram']['api_hash']
phone = config['Telegram']['username']

# Start telegram client by telethon
client = TelegramClient(phone, api_id, api_hash)
client.start()

# Set data
offset_id = 0
limit = 100
total_messages = 0  # what is it param?
total_count_limit = 0  # what is it param?
end_id = 0
counter = 0
clean_counter = 0
target_group = 't.me/estatecyprus'
flag_1 = True

# Create database and tables
create_db.create_lots()
create_db.create_users()

# Start telethon body
while True:
    history = client(GetHistoryRequest(
        peer=target_group,  # Don't warn ing, it's OK
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
        if flag_1:  # save id first message. it's end id for next iteration
            end_id = message.id
            flag_1 = False
            print('end id = ', end_id)
        counter += 1
        if not message.message == '':  # skip message without text (skip photo, video message)
            clean_counter += 1
            # Print our count message number, and 'clean' message number (only message with text)
            print('________________________________________________ \n'
                  'counter = ', counter,
                  'clean_counter = ', clean_counter
                  )
            # Call find price func in message (use low register for all text)
            price = price_parsing.f_price(message.message.lower())
            if price == -1:  # If we can't find price, we move to the next message
                continue

            print("price = ", price, "€")
            try:
                city = city_parsing.parse(message.message.lower())
            except AttributeError:  # Catch transformation to low error (debug)
                print(AttributeError)
                continue
            # Add date to database
            sqlite_message_db.write(message.date, city, price, message.id, message.chat_id)
            # Print date for manual check (debug)
            print("city = ", city)
            print("data time = ", message.date)
            print(message.id)
            print(message.message)

    # WHAT IS IT? HOW IT WORK? I MUST UNDERSTAND WHAT I WRITE =), BUT IT LATER
    offset_id = messages[len(messages) - 1].id
    print('\noffset_id = ', offset_id)
    if total_count_limit != 0 and total_messages >= total_count_limit:
        break

# Print table for manual check (debug)
sqlite_message_db.table_view()

print("Парсинг сообщений группы успешно выполнен.")  # Message for good parsing!
