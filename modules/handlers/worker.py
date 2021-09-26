from aiogram import types
from main import dp
from modules import sqLite, workWF
from modules.dispatcher import bot, Worker
from modules.keyboards import confirm_kb, worker_first_kb
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
import datetime


# Start menu worker Callback feed fish
@dp.callback_query_handler(state=Worker.worker_start, text='i_feed_fish')
async def add_person_start(call: types.CallbackQuery):
    pools = sqLite.read_all_value_bu_name(name='oners', table='pools')
    date_keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    for i in range(0, len(pools)):
        i = KeyboardButton(f'Бассейн №{i + 1}')
        date_keyboard.add(i)
    await call.message.answer(text="Выберите в каком бассейне вы покормили рыбу",
                              reply_markup=date_keyboard)
    await Worker.feed_fish.set()


# Menu worker feed fish
@dp.message_handler(state=Worker.feed_fish)
async def add_person_start(message: types.Message):
    if ' №' in message.text:
        pool_id = str(message.text.split('№')[1])
        tg_id = message.from_user.id
        sqLite.insert_info(table_name='users', telegram_id=tg_id, name='data', date=pool_id)
        await message.answer('Сколько корма вы потратили на этот бассейн в кг?\n'
                             'Только цифры', reply_markup=types.ReplyKeyboardRemove())
        await Worker.feed_fish_food.set()
    else:
        await message.answer('Нажмите на кнопку')


# Menu worker feed fish
@dp.message_handler(state=Worker.feed_fish_food)
async def add_person_start(message: types.Message):
    if message.text.isdigit():
        tg_id = message.from_user.id
        sqLite.insert_info(table_name='users', telegram_id=tg_id, name='data_2', date=message.text)
        pool_id = sqLite.read_value_bu_name(name='data', table='users', telegram_id=tg_id)[0]
        await message.answer(f'Вы покормили рыбу в бассейне <b>№{pool_id}</b>, на это потрачено '
                             f'<b>{message.text} кг</b> корма. \nВсе верно?',
                             reply_markup=confirm_kb, parse_mode='html')
        await Worker.feed_fish_confirm.set()
    else:
        await message.answer('Введите только цифры')


# Start menu worker Callback feed fish
@dp.callback_query_handler(state=Worker.feed_fish_confirm, text='yes_all_good')
async def add_person_start(call: types.CallbackQuery):
    tg_id = call.from_user.id
    pool_number = sqLite.read_value_bu_name(name='data', table='users', telegram_id=tg_id)[0]
    food = sqLite.read_value_bu_name(name='data_2', table='users', telegram_id=tg_id)[0]
    pool = sqLite.read_values_in_db_by_phone(name='number', table='pools', data=f'{pool_number}')
    fish_ids = str(pool[2]).split('ID')
    start_fish_mass = str(pool[3]).split('KG')
    investor_tg_ids = str(pool[1]).split('TgID')
    all_fish_mass = int(pool[4])
    for i in range(0, (len(fish_ids) - 1)):
        investor_tg_id = investor_tg_ids[i]
        food_mass = round(float(start_fish_mass[i]) * float(food) / all_fish_mass, 2)
        old_balance = float(sqLite.read_value_bu_name(name='balance', table='users',
                                                      telegram_id=int(investor_tg_id))[0])
        food_price = float(sqLite.read_value_bu_name(name='food_price', table='users',
                                                     telegram_id=workWF.read_admin())[0])
        new_balance = round(old_balance - food_price * food_mass, 2)
        sqLite.insert_info(table_name='users', telegram_id=int(investor_tg_id), name='balance', date=str(new_balance))
        sqLite.insert_pool_db1(telegram_id=tg_id,
                               food_mass=str(food_mass),
                               fish_mass="None",
                               fish_id=fish_ids[i],
                               number=int(pool_number),
                               data=datetime.datetime.now(),
                               type='feed_fish')
        try:
            await bot.send_message(chat_id=investor_tg_ids[i],
                                   text=f'Вашу рыбку с ID - <b>{str(fish_ids[i])}</b> покормили. На эту ушло'
                                        f'<b>{str(food_mass)} кг</b> корма.',
                                   parse_mode='html', reply_markup=types.ReplyKeyboardRemove())
        except:
            await bot.send_message(chat_id=workWF.read_admin(),
                                   text=f'Телеграм ID <b>{investor_tg_ids[i]}</b> не действительный, '
                                        f'либо человек не подписан на бота.',
                                   parse_mode='html', reply_markup=types.ReplyKeyboardRemove())
    await call.message.answer(text="Данные сохранены")
    await call.message.answer(text='Добрый день. Чем могу помочь?', reply_markup=worker_first_kb)
    await Worker.worker_start.set()


# Check fish size
@dp.callback_query_handler(state=Worker.worker_start, text='send_text_msg')
async def add_person_start(call: types.CallbackQuery):
    pools = sqLite.read_all_value_bu_name(name='oners', table='pools')
    date_keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    for i in range(0, len(pools)):
        i = KeyboardButton(f'Бассейн №{i + 1}')
        date_keyboard.add(i)
    await call.message.answer(text="Выберите в каком бассейне вы <b>произвели замер</b> рыбы",
                              reply_markup=date_keyboard, parse_mode='html')
    await Worker.size_fish.set()


# Pick a pool
@dp.message_handler(state=Worker.size_fish)
async def add_person_start(message: types.Message):
    if ' №' in message.text:
        pool_id = str(message.text.split('№')[1])
        tg_id = message.from_user.id
        sqLite.insert_info(table_name='users', telegram_id=tg_id, name='data', date=pool_id)
        await message.answer('Какой вес рыбы в этом бассейне в кг?\n'
                             'Только цифры', reply_markup=types.ReplyKeyboardRemove())
        await Worker.size_fish_food.set()
    else:
        await message.answer('Нажмите на кнопку')


# Menu worker feed fish
@dp.message_handler(state=Worker.size_fish_food)
async def add_person_start(message: types.Message):
    tg_id = message.from_user.id
    sqLite.insert_info(table_name='users', telegram_id=tg_id, name='data_2', date=message.text)
    pool_id = sqLite.read_value_bu_name(name='data', table='users', telegram_id=tg_id)[0]
    await message.answer(f'Вы измеряли рыбу в бассейне <b>№{pool_id}</b>, и ее вес составил '
                         f'<b>{message.text} кг</b> корма. \n'
                         f'Все верно?', reply_markup=confirm_kb, parse_mode='html')
    await Worker.size_fish_confirm.set()


# Start menu worker Callback check fish size
@dp.callback_query_handler(state=Worker.size_fish_confirm, text='yes_all_good')
async def add_person_start(call: types.CallbackQuery):
    tg_id = call.from_user.id
    pool_number = sqLite.read_value_bu_name(name='data', table='users', telegram_id=tg_id)[0]
    size = sqLite.read_value_bu_name(name='data_2', table='users', telegram_id=tg_id)[0]
    pool = sqLite.read_values_in_db_by_phone(name='number', table='pools', data=f'{pool_number}')
    user_ids = str(pool[1]).split('TgID')
    fish_ids = str(pool[2]).split('ID')
    for i in range(0, (len(fish_ids) - 1)):
        sqLite.insert_pool_db1(telegram_id=tg_id,
                               food_mass="None",
                               fish_mass=str(size),
                               fish_id=fish_ids[i],
                               number=int(pool_number),
                               data=datetime.datetime.now(),
                               type='size_fish')
        try:
            await bot.send_message(chat_id=user_ids[i],
                                   text=f'Вашу рыбку с ID - <b>{str(fish_ids[i])}</b> измеряли. Ее вес составил'
                                        f'<b>{str(size)} кг</b>.',
                                   parse_mode='html', reply_markup=types.ReplyKeyboardRemove())
        except:
            await bot.send_message(chat_id=workWF.read_admin(),
                                   text=f'Телеграм ID <b>{user_ids[i]}</b> не действительный, '
                                        f'либо человек не подписан на бота.',
                                   parse_mode='html', reply_markup=types.ReplyKeyboardRemove())
    sqLite.insert_info_pool(number=int(pool_number), name='fish_size', date=size)
    await call.message.answer(text="Данные сохранены")
    await call.message.answer(text='Добрый день. Чем могу помочь?', reply_markup=worker_first_kb)
    await Worker.worker_start.set()


# Start menu worker Callback feed fish
@dp.callback_query_handler(state=Worker.worker_start, text='send_photo_msg')
async def add_person_start(call: types.CallbackQuery):
    pools = sqLite.read_all_value_bu_name(name='oners', table='pools')
    date_keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    for i in range(0, len(pools)):
        i = KeyboardButton(f'Бассейн №{i + 1}')
        date_keyboard.add(i)
    await call.message.answer(text="Вы сделали фотографию рыбы. Из какого бассейна рыба на фотографии?",
                              reply_markup=date_keyboard)
    await Worker.send_photo.set()


# Pick a pool
@dp.message_handler(state=Worker.send_photo)
async def add_person_start(message: types.Message):
    if ' №' in message.text:
        pool_id = str(message.text.split('№')[1])
        tg_id = message.from_user.id
        sqLite.insert_info(table_name='users', telegram_id=tg_id, name='data', date=pool_id)
        await message.answer('Отправьте мне фотографию', reply_markup=types.ReplyKeyboardRemove())
        await Worker.pick_photo.set()
    else:
        await message.answer('Нажмите на кнопку')


# Write a text of msg
@dp.message_handler(content_types=['photo'], state=Worker.pick_photo)
async def photo_handler(message: types.Message):
    tg_id = message.from_user.id
    pool_number = sqLite.read_value_bu_name(name='data', table='users', telegram_id=tg_id)[0]
    await message.photo[-1].download(f'jpg/{str(message.from_user.id)}test.jpg')
    with open(f'jpg/{str(message.from_user.id)}test.jpg', 'rb') as photo:
        await bot.send_photo(chat_id=message.from_user.id, photo=photo)
    await message.answer(f'Вы видите сообщение которое будет отправлено владельцам рыбы бассейна '
                         f'<b>№{pool_number}</b>. Если все хорошо нажмите отправить.',
                         reply_markup=confirm_kb, parse_mode='html')
    photo.close()
    await Worker.confirm_send_photo.set()


# Yes send the msg
@dp.callback_query_handler(state=Worker.confirm_send_photo, text='yes_all_good')
async def add_person_start(call: types.CallbackQuery):
    tg_id = call.from_user.id
    pool_number = sqLite.read_value_bu_name(name='data', table='users', telegram_id=tg_id)[0]
    pool = sqLite.read_values_in_db_by_phone(name='number', table='pools', data=f'{pool_number}')
    investor_tg_ids = str(pool[1]).split('TgID')
    for i in range(0, len(investor_tg_ids) - 1):
        user_id = int(investor_tg_ids[i])
        try:
            with open(f'jpg/{str(call.from_user.id)}test.jpg', 'rb') as photo:
                await bot.send_photo(chat_id=user_id, photo=photo)
            photo.close()
        except:
            bot.send_message(text=f"Телеграм ID {user_id} пользователя не действительный. Отправка фото",
                             chat_id=workWF.read_admin())
            print(f"Телеграм ID {user_id} пользователя не действительный, либо пользователь не подписан на бота")
            photo.close()
    await call.message.answer('Сообщение отправлено', reply_markup=types.ReplyKeyboardRemove())
    await call.message.answer(text='Добрый день. Чем могу помочь?', reply_markup=worker_first_kb)
    await Worker.worker_start.set()
