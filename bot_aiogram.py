import configparser
import logging
import pathlib
from pathlib import Path

from aiogram import Bot, types, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import Dispatcher, FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

from bot.keyboards.tg_keyboards_aiogram import city_name_bt, max_price_bt, min_price_bt, restart_bt
from database.sqlite_commit_db import write_user, stop_user
from database.sqlite_view_db import last_msg_id

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
    city = State()
    min_price = State()
    max_price = State()


dir_path = pathlib.Path.cwd()
path = Path(dir_path, 'config', 'config.ini')

config = configparser.ConfigParser()
config.read(path)

token = config['Telegram']['bot_token']

bot = Bot(token=token)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


@dp.message_handler(commands=['start'], state='*')
async def start_bot(message: types.Message):
    await ClientStatesGroup.city.set()
    print(message.message_id)
    await message.reply("""Доброго времени суток! Данный бот создан для помощи в подборе недвижимости по вашим 
        параметрам, таким как стоимость и город!
        Вы можете задать диапозон цен от 100 до 999 999 у.е.\n
        А так же выбрать локацию из предложенных: Лимассол, Пафос, Ларнака, Никосия или весь Кипр
        (список локаций постоянно расширяется и вы можете оставить запрос на
        добавления нового города или деревни/ написав сюда @artdmsav)
        Бот находится на этапе альфа тестирования и возможны следующие нюансы: 
        - Возможно выбрать только один населеный пункт для поиска
        - Нет возможности сортировки по типу Аренда, Продажа, Покупка
        - Сумма ограничена от 3-х до 6-ти цифрами\n
        Мы работаем над устранением данных неудобств для Вашего комфортного пользования.\n\n\n
                         >>>>ВАЖНО<<<<\n
Все сообщения будут приходить от @estatecyprus_msg 
Если у Вас закрытый аккаунт, напишите @estatecyprus_msg  любое сообщение для дальнейшего функционирования
бота \n\n\n\n""",
                        reply_markup=city_name_bt()
                        )


@dp.message_handler(text='Ввести новые параметры', state='*')
async def restat_bot(message: types.Message):
    await ClientStatesGroup.city.set()
    await message.reply("Введите новые параметры",
                        reply_markup=city_name_bt()
                        )


@dp.message_handler(text='Остановка бота', state='*')
async def stop_bot(message: types.Message):
    stop_user(message.chat.id)
    print('stop bot, id user = ', message.chat.id)
    await message.reply("Bot stopped",
                        reply_markup=restart_bt()
                        )


@dp.message_handler(text=('Лимассол', 'Никосия', 'Пафос', 'Ларнака', 'Весь Кипр'), state=ClientStatesGroup.city)
async def city(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['city'] = message.text
    await ClientStatesGroup.next()
    await message.reply('Укажите минимальную стоимость аренды:  \n',
                        reply_markup=min_price_bt()
                        )
    print(data['gender'])


@dp.message_handler(regexp="\d{3,6}",
                    state=ClientStatesGroup.min_price)
async def min_price(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['min_price'] = message.text
    await ClientStatesGroup.next()
    print('min_price = ', data['min_price'])
    await message.reply('Укажите максимальную стоимость аренды:  \n',
                        reply_markup=max_price_bt()
                        )


@dp.message_handler(regexp="\d{3,6}",
                    state=ClientStatesGroup.max_price)
async def max_price(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['max_price'] = message.text
    print('max_price = ', data['max_price'])
    await message.reply(f'Вы хотите найти арендовать недвижемость в {data["city"]}, со стоимостью аренды от '
                        f'{data["min_price"]} евро, до {data["max_price"]} евро.\nПодходящие предложения будут '
                        f'поступать в этот чат')
    # Check that min < max, else  change place
    if int(data['min_price']) <= int(data['max_price']):
        write_user(data['city'], int(data['min_price']), int(data['max_price']), message.chat.id,
                   1, last_msg_id())
    else:
        write_user(data['city'], data['max_price'], data['min_price'], message.chat.id,
                   1, last_msg_id())

    await message.answer('\n\n\n\nДля ввода новых параметров, нажмите "Ввести новые параметры"',
                         reply_markup=restart_bt())
    await state.finish()


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
