import configparser

from telethon import Button
from telethon import TelegramClient, events

# Считываем учетные данные
config = configparser.ConfigParser()
config.read("config.ini")

# Присваиваем значения внутренним переменным
api_id = config['Telegram']['api_id']
api_hash = config['Telegram']['api_hash']
bot_token = config['Telegram']['bot_token']

# async def handler(event):
#     # Good
#     chat = await event.get_chat()
#     sender = await event.get_sender()
#     chat_id = event.chat_id
#     sender_id = event.sender_id

# Создаем объект клиента
client = TelegramClient('estate_cyprus_bot', api_id, api_hash)

client.start(bot_token=bot_token)


# Обработчик события при запуске бота
@client.on(events.NewMessage(pattern='/start'))
async def start(event):
    await event.respond("""Доброго времени суток! Данный бот создан для помощи в бодборе недвижимости по вашим параметрам, таким
как стоимость и город!\n\n
Вы можете задать диапозон цен от 100 до 999 999 у.е.\n
А так же выбрать локацию из предложенных: Лимассол, Пафос, Ларнака, Айя напа, Никосия или весь Кипр
(список локаций постоянно расширяется и вы можете оставить запрос на
добавления нового города или деревни/ написав сюда @artdmsav)\n
Бот находится на этапе альфа тестирования и возможны следующие нюансы:\n
- Дублирование объявлений (когда одно объявление выложенно на нескольких площадкках\n
- Возможно выбрать только один населеный пункт для поиска\n
- Нет возможности сортировки по типу Аренда, Продажа, Покупка\n
- Максимальная сумма ограничена 6-ю цифрами\n\n
Мы работаем над устранением данных неудобств для Вашего комфортного пользования.\n\n
Если Вы обнаружили ошибку или хотите предложить новую функцию, прошу написать мне @artdmsav\n\n
P.S. От себя, желаю Вам найти квартиру или дом Вашей мечты на этом прекрасном острове!\n\n""")


@client.on(events.CallbackQuery)
async def handle_callback_query(event):
    # Извлекаем данные из callback-кнопки
    button_data = event.data.decode('utf-8')
    print(button_data)
    # # Отправляем пользователю сообщение с выбранным вариантом ответа
    # await event.answer(f'Вы выбрали: {button_data}')
    # Изменяем сообщение с кнопками на сообщение без кнопок
    message = await event.edit(f'Вы выбрали: {button_data}', buttons=None)


# Определяем обработчик события NewMessage
@client.on(events.NewMessage)
async def handle_first_message(event):
    # Отправляем пользователю сообщение с вариантами ответов
    message = await event.respond('\n\nВыберите один из вариантов:', buttons=[
        # Определяем четыре inline-кнопки с текстом и уникальными callback-данными
        [Button.inline('Limassol', b'Limassol'), Button.inline('Nicosia', b'Nicosia')],
        [Button.inline('Larnaka', b'Larnaka'), Button.inline('Pafos', b'Pafos')],
    ])
    # response = await client.wait_for_event(events.CallbackQuery)


@client.on(events.NewMessage)
async def handle_second_message(event):
    # Отправляем пользователю запрос на ввод данных.
    await event.respond('Укажите минимальную стоимость:')
    text = event.message.message
    chat_id = event.chat_id

    # Проверяем, что введено число.
    if text.isdigit():
        pass
    else:
        await event.respond('Введите только число (от 100 до 999999)!')

    # Отправляем пользователю сообщение с ответом.
    await event.respond(f'Минимальная стоимость = , {text}')


# Запускаем клиента
client.run_until_disconnected()