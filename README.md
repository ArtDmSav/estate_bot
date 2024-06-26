My first study project.
Legacy

# Telegram Real Estate Message Parser (EN/RU)

<!DOCTYPE html>
<html>

<body>
    <h2>Problem:</h2>
    <p>While on Cyprus, I encountered an issue with searching for rental housing, as local realtors prioritize posting
        information about real estate in Telegram chats. Each day, thousands of messages arrive in a single chat, without
        the ability to sort them by relevant parameters, making the search more laborious and time-consuming.</p>
    <h2>What the bot does:</h2>
    <p>Users provide parameters such as minimum price, maximum price, and city. The bot sends sorted messages to the user
        based on their request.</p>
    <h2>How the bot works:</h2>
    <ul>
        <li><strong>bot_aiogram.py </strong> <br>
			This is a separate script that constantly interacts with users and records/updates
            entered parameters in an SQLite database using the "users" table. The aiogram library is used for this purpose,
            specifically its packages ReplyKeyboardMarkup, FSMContext, StatesGroup, and MemoryStorage. The logging library
            is also present for logging and debugging purposes.<br><br></li>
        <li><strong>main.py</strong> <br>
			This script is responsible for parsing messages, recording them in the database, and
            then forwarding messages to users. This file is periodically launched, for example, every 10 minutes using
            crontab. If necessary, a database is created using sqlite_create_db.py. Obsolete messages are deleted using
            the del_old_msg(del_msg_after_day) function. The last_msg_id() function extracts the ID of the last message
            from the database and passes it to the parsing_chat(last_msg_id) function, which records all messages in
            the database. Then, all active users (to whom messages need to be sent) are selected using the active_user()
            function, and the result is passed as a list to the send_msgs_f_users(active_user_list, last_msg_id) function
            for message distribution. The last step is to call the full_time() function, which calculates the execution
            time of all functions wrapped in decorators and provides the final program execution time.<br><br></li>
        <li><strong>bot_telethon.py</strong> <br> 
			In this file, the Telethon library (API) is used. A session is created and the
            message history from the required chat is retrieved. Then, each message is parsed using price_parsing.py and
            city_parsing.py, and the results are recorded in the database in the "lots" table.<br><br></li>
    </ul>
    <h1>Telegram-парсер сообщений недвижимости</h1>
    <h2>Проблема:</h2>
    <p>Находясь на Кипре, столкнулся с проблемой поиска аренды жилья, так как местные риэлторы приоритетно размещают
    информацию о недвижимости в Telegram-чатах. Ежедневно в одном чате поступает до нескольких тысяч сообщений, без
    возможности сортировки по нужным параметрам, что делает поиск более трудоемким, и на это уходит много времени.</p>
    <h2>Что делает бот:</h2>
    <p>Пользователь задает такие параметры, как минимальная цена, максимальная цена, город.
    Бот присылает отсортированные по его запросу сообщения пользователю.</p>
    <h2>Как работает бот:</h2>
    <ul>
        <li><strong>bot_aiogram.py </strong> <br>
			отдельный скрипт, который постоянно взаимодействует с пользователем и записывает/перезаписывает
    введенные параметры в БД SQLite, используя таблицу "users". Для этого используется библиотека aiogram, в частности
    ее пакеты ReplyKeyboardMarkup, FSMContext, StatesGroup, MemoryStorage.<br><br></li>
        <li><strong>main.py</strong> <br>
			является скриптом для парсинга сообщений, записи их в БД, а затем пересылки сообщений пользователям.
    Данный файл запускается периодически, раз в 10 минут. При необходимости создается БД с
    помощью sqlite_create_db.py. Затем устаревшие сообщения удаляются с помощью функции del_old_msg().
    С помощью last_msg_id() извлекается ID последнего сообщения из БД и передается в функцию парсинга сообщений
    parsing_chat(), которая записывает все сообщения в БД. Затем выбираются все активные пользователи
    (которым необходимо рассылать сообщения) с помощью функции active_user(), и результат в виде списка передается
    в функцию рассылки сообщений пользователям send_msgs_f_users(active_user_list, last_msg_id). Последним шагом
    вызывается функция full_time(), которая суммирует время выполнения всех функций, обернутых декоратором, и выдает
    итоговое время выполнения программы.<br><br></li>
        <li><strong>bot_telethon.py</strong> <br> 
			здесь используется библиотека Telethon (API). Создается сессия и загружается история сообщений из
    нужного чата. Затем каждое сообщение парсится с помощью price_parsing.py и city_parsing.py, и результат записывается
    в БД в таблицу "lots".<br><br></li>
	    	<p>Ссылка на телеграм бота: <a href="https://t.me/estatecyprus_bot">@estatecyprus_bot</a></p>
		<p>По всем вопросам пишите мне в телеграм: <a href="https://t.me/artdmsav">@artdmsav</a></p>
</body>

</html>
