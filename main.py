import configparser
import logging
import time

from telethon.sync import TelegramClient
from telethon.tl.functions.messages import GetHistoryRequest

import city_parsing
import price_parsing
import sqlite_create_db
import sqlite_message_db

start_time = time.time()
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
limit = 2000
end_id = 0
counter = 0
del_msg_after_day = 30
clean_counter = 0
target_group = 't.me/estatecyprus'
flag_1 = True

# Create database and tables
sqlite_create_db.create_lots()
sqlite_create_db.create_users()
last_msg_id = sqlite_message_db.last_msg_id()
sqlite_message_db.del_old_msg(del_msg_after_day)
# sqlite_message_db.del_repeating_msg()


# Start telethon body
while True:
    history = client(GetHistoryRequest(
        peer=target_group,  # Don't warn ing, it's OK
        offset_id=offset_id,  # Offset message ID (only messages previous to the given ID will be retrieved).Exclusive
        offset_date=None,  # (datetime): Offset date (messages previous to this date will be retrieved). Exclusive
        add_offset=0,  # (int): Additional message offset (all of the specified offsets + this offset = older messages)
        limit=limit,  # (int | None, optional): Number of messages to be retrieved. Due to limitations with the API
        # retrieving more than 3000 messages will take longer than half a minute (or even more based on
        # previous calls).
        max_id=0,
        min_id=end_id,  # (int): All the messages with a lower (older) ID or equal to this will be excluded.
        hash=0
    ))

    if not history.messages:
        break
    messages = history.messages

    for message in messages:
        if message.id <= last_msg_id:
            break

        if flag_1:  # save id first message. it's end id for next iteration
            end_id = message.id
            flag_1 = False
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

            # chanPeer = PeerChannel(channel_id=message.chat_id)
            # channel_entity = client.get_entity(chanPeer)
            # print("dgfchfgvjhghjhbhvbgjvhb", message)
            # Add date to database
            sqlite_message_db.write_lots(message.date, city, price, message.id, message.chat_id)
            # Print data for manual check (debug)
            print("city = ", city)
            print("data time = ", message.date)
            print(message.id)
            print(message.message)

end_time = time.time()
total_time = round(end_time - start_time, 3)
print('\n\nProgram takes = ', total_time, 'sec')

# Print table for manual check (debug)
# sqlite_message_db.table_view_lots()
