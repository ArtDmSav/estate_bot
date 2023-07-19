from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

restart_button = ReplyKeyboardMarkup(resize_keyboard=True,
                                     one_time_keyboard=True
                                     ).add(KeyboardButton('Ввести новые параметры'), KeyboardButton('Остановка бота'))

list_city_name = [['Лимассол', 'Никосия', 'Пафос'],
                  ['Ларнака', 'Весь Кипр']]
buttons_list_city = []
for item in list_city_name:
    l = []
    for i in item:
        l.append(KeyboardButton(i))
    buttons_list_city.append(l)

choose_city_button = ReplyKeyboardMarkup(buttons_list_city,
                                         resize_keyboard=True,
                                         one_time_keyboard=True,
                                         ).add(KeyboardButton('Ввести новые параметры'))

list_button_max_price = [[300, 500, 700, 1000, 1200],
                         [1200, 1400, 1600, 1800, 2000, 2200],
                         [2500, 3000, 5000, 8000, 999999]]
buttons_list_age = []
for item in list_button_max_price:
    l = []
    for i in item:
        l.append(KeyboardButton(i))
    buttons_list_age.append(l)
keyboard_max_price_buttons = ReplyKeyboardMarkup(buttons_list_age,
                                                 resize_keyboard=True,
                                                 one_time_keyboard=True,
                                                 ).add(KeyboardButton('Ввести новые параметры'))

list_button_min_price = [[100, 300, 500, 700, 1000],
                         [1200, 1400, 1600, 1800, 2000],
                         [2200, 2500, 3000, 5000, 8000]]
buttons_list_month = []
for item in list_button_min_price:
    l = []
    for i in item:
        l.append(KeyboardButton(i))
    buttons_list_month.append(l)
keyboard_min_price_buttons = ReplyKeyboardMarkup(buttons_list_month,
                                                 resize_keyboard=True,
                                                 one_time_keyboard=True,
                                                 ).add(KeyboardButton('Ввести новые параметры'))
