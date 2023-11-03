from telethon.sync import TelegramClient
from telethon.tl.functions.messages import GetHistoryRequest

from estate_bot.config.data import API_ID, API_HASH, USERNAME
from estate_bot.database import sqlite_commit_db
from estate_bot.functions import city_parsing, price_parsing
from estate_bot.functions.time_count_decorator import time_count
from estate_bot.functions.translate import to_en, to_ru, to_el


@time_count
def parsing_chat(last_msg_id):

    # Start telegram client by telethon
    client = TelegramClient(USERNAME, API_ID, API_HASH, system_version="4.16.30-vxCUSTOM")
    client.start()

    # Set data
    offset_id = 0
    limit = 500
    target_group = 't.me/estatecyprus'

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
            min_id=last_msg_id,  # (int): All the messages with a lower (older) ID or equal to this will be excluded.
            hash=0
        ))

        if not history.messages:
            client.disconnect()
            return
        messages = history.messages

        for message in messages:
            if message.id <= last_msg_id:
                client.disconnect()
                return

            if any(message.message):  # skip message without text (skip photo, video message)

                # Call find price func in message (use low register for all text)
                str_message = str(message.message).lower()
                price = price_parsing.f_price(str_message)
                if price == -1:  # If we can't find price, we move to the next message
                    continue

                msg_en = to_en(message.message)
                msg_ru = to_ru(message.message)

                try:
                    city = city_parsing.parse(message.message.lower())
                except AttributeError:  # Catch transformation to low error (debug)
                    print(AttributeError)
                    continue

                # Add lot to database
                sqlite_commit_db.write_lots(message.date, city, price, message.id, target_group, message.message,
                                            msg_ru, msg_en)

        client.disconnect()
        return
