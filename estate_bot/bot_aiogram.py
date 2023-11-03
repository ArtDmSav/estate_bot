import logging

from aiogram import Bot, types, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import Dispatcher, FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

from estate_bot.bot.keyboards.tg_keyboards_aiogram import city_name_bt, max_price_bt, min_price_bt, restart_bt, ch_lang
from estate_bot.bot.keyboards.tg_keyboards_aiogram import city_name_bt_en, max_price_bt_en, min_price_bt_en, \
    restart_bt_en
from estate_bot.config.data import BOT_TOKEN, ACTIVE, INACTIVE
from estate_bot.database.sqlite_commit_db import write_user, stop_user
from estate_bot.database.sqlite_view_db import last_msg_id

logging.basicConfig(level=logging.DEBUG, filename='logs/bot_aiogram.log',
                    format='%(levelname)s (%(asctime)s): %(message)s (Line: %(lineno)d) [%(filename)s]',
                    datefmt='%d/%m/%Y %I:%M:%S', encoding='UTF-8', filemode='w'
                    )
logging.warning('warning')
logging.critical('critical')
logging.debug('debug')
logging.info('info')
logging.error('error')


class ClientStatesGroup(StatesGroup):
    language = State()
    city = State()
    min_price = State()
    max_price = State()


bot = Bot(token=BOT_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


@dp.message_handler(commands=['start'], state='*')
async def start_bot(message: types.Message):
    await ClientStatesGroup.language.set()
    print("msd.msg_id = ", message.message_id)
    await message.reply("""Доброго времени суток! Данный бот создан для помощи в подборе недвижимости по вашим 
        параметрам, таким как стоимость и город!
        Вы можете задать диапозон цен от 100 до 999 999 у.е.\n
        А так же выбрать локацию из предложенных: Лимассол, Пафос, Ларнака, Никосия или весь Кипр
        (список локаций постоянно расширяется и вы можете оставить запрос на
        добавления нового города или деревни/ написав сюда @artdmsav)
        Бот находится на этапе альфа тестирования и возможны следующие нюансы: 
        - Возможно выбрать только один населеный пункт для поиска
        - Нет возможности сортировки по типу Аренда, Продажа, Покупка
        - Сумма ограничена от 3-х до 6-ти цифр\n
        Мы работаем над устранением данных неудобств для Вашего комфортного пользования.\nGood day! This bot was created to help you select real estate according to your needs.
         parameters such as cost and city!
         You can set a price range from 100 to 999,999 USD\n
         And also choose a location from the proposed ones: Limassol, Paphos, Larnaca, Nicosia or all of Cyprus
         (the list of locations is constantly expanding and you can leave a request for
         adding a new city or village / by writing here @artdmsav)
         The bot is at the alpha testing stage and the following nuances are possible:
         - It is possible to select only one locality for search
         - It is not possible to sort by type Rent, Sale, Purchase
         - The amount is limited from 3 to 6 digits\n
         We are working to eliminate these inconveniences for your comfortable use.\n\n 
        Выберите язык. Choose language.""",
                        reply_markup=ch_lang()
                        )


@dp.message_handler(text='Ввести новые параметры', state='*')
async def restat_bot(message: types.Message):
    await ClientStatesGroup.language.set()
    await message.reply("Выберите язык", reply_markup=ch_lang())


@dp.message_handler(text='Enter new parameters', state='*')
async def restat_bot_en(message: types.Message):
    await ClientStatesGroup.language.set()
    await message.reply("Choose language", reply_markup=ch_lang())


@dp.message_handler(text='Остановка бота', state='*')
async def stop_bot(message: types.Message):
    stop_user(message.chat.id)
    await message.reply("Бот остановлен!\n Для нового поиска нажмите кнопку 'Ввести новые параметры'",
                        reply_markup=restart_bt()
                        )


@dp.message_handler(text='Stopping the bot', state='*')
async def stop_bot_en(message: types.Message):
    stop_user(message.chat.id)
    await message.reply("The bot has stopped!\nFor a new search, click the 'Enter new parameters' button",
                        reply_markup=restart_bt_en()
                        )


@dp.message_handler(text='Русский', state=ClientStatesGroup.language)
async def ru_lang(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['language'] = message.text
    await ClientStatesGroup.next()
    await message.reply('Выберите город:  \n',
                        reply_markup=city_name_bt()
                        )


@dp.message_handler(text='English', state=ClientStatesGroup.language)
async def en_lang(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['language'] = message.text
    await ClientStatesGroup.next()
    await message.reply('Choose your city:  \n',
                        reply_markup=city_name_bt_en()
                        )


@dp.message_handler(text=('Лимассол', 'Никосия', 'Пафос', 'Ларнака', 'Весь Кипр'), state=ClientStatesGroup.city)
async def city(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['city'] = message.text
    await ClientStatesGroup.next()
    await message.reply('Укажите минимальную стоимость аренды:  \n',
                        reply_markup=min_price_bt()
                        )


@dp.message_handler(text=('Limassol', 'Nicosia', 'Paphos', 'Larnaca', 'All Cyprus'), state=ClientStatesGroup.city)
async def city_en(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['city'] = message.text
    await ClientStatesGroup.next()
    await message.reply('Specify the minimum rental price:  \n',
                        reply_markup=min_price_bt_en()
                        )


@dp.message_handler(regexp='\d{3,6}', state=ClientStatesGroup.min_price)
async def min_price(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['min_price'] = message.text
    await ClientStatesGroup.next()

    if data['language'] == 'Русский':
        await message.reply('Укажите максимальную стоимость аренды:  \n',
                            reply_markup=max_price_bt()
                            )
    else:
        await message.reply('Specify the maximum rental price:  \n',
                            reply_markup=max_price_bt_en()
                            )


@dp.message_handler(regexp="\d{3,6}", state=ClientStatesGroup.max_price)
async def max_price(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['max_price'] = message.text
        if int(data['min_price']) > int(data['max_price']):
            data['min_price'], data['max_price'] = data['max_price'], data['min_price']

    if data['language'] == 'Русский':
        await message.reply(f'Вы хотите найти арендовать недвижемость в {data["city"]}, со стоимостью аренды от '
                            f'{data["min_price"]} евро, до {data["max_price"]} евро.\nПодходящие предложения будут '
                            f'поступать в этот чат')

        write_user(data['city'], int(data['min_price']), int(data['max_price']),
                   message.chat.id, ACTIVE, last_msg_id(), INACTIVE, message.chat.username)

        await message.answer('\n\n\n\nДля ввода новых параметров, нажмите "Ввести новые параметры"',
                             reply_markup=restart_bt())
    else:
        await message.reply(f'You want to find a property for rent in {data["city"]}, with rental prices from '
                            f'{data["min_price"]} euros, up to {data["max_price"]} euros.\nSuitable offers will be '
                            f'enter this chat')

        city_ru = await change_city_name(data['city'])

        write_user(city_ru, int(data['min_price']), int(data['max_price']),
                   message.chat.id, ACTIVE, last_msg_id(), ACTIVE, message.chat.username)

        await message.answer('\n\n\n\nTo enter new parameters, click "Enter new parameters"',
                             reply_markup=restart_bt_en())

    await state.finish()


async def change_city_name(data):
    if data == 'Limassol':
        city_ru = 'Лимассол'
    elif data == 'Nicosia':
        city_ru = 'Никосия'
    elif data == 'Paphos':
        city_ru = 'Пафос'
    elif data == 'Larnaca':
        city_ru = 'Ларнака'
    elif data == 'Rest of Cyprus':
        city_ru = 'Остальной Кипр'
    else:
        city_ru = 'Кипр'
    return city_ru


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
