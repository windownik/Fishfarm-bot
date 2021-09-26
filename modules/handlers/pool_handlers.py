from aiogram import types
from main import dp
from modules import sqLite, workWF
from modules.dispatcher import bot, Admin_Form, Admin_Pool
from modules.keyboards import pool_kb, back_kb, work_with_fish, confirm_kb
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
import datetime


# Start menu pool Callback
@dp.callback_query_handler(state=Admin_Pool.sale_fish_in_pool, text='back')
@dp.callback_query_handler(state=Admin_Pool.delete_fish_in_pool, text='back')
@dp.callback_query_handler(state=Admin_Pool.save_fish, text='back')
@dp.callback_query_handler(state=Admin_Pool.create_pool, text='back')
@dp.callback_query_handler(state=Admin_Form.admin_first_menu, text='pool')
async def add_person_start(call: types.CallbackQuery):
    await call.message.edit_text(text="Здесь вы работаете с бассейнами. Выберите меню ниже.", reply_markup=pool_kb)
    await Admin_Pool.pool_start.set()


# Create pool Callback
@dp.callback_query_handler(state=Admin_Pool.confirm_new_pool, text='back')
@dp.callback_query_handler(state=Admin_Pool.pool_start, text='create_pools_btn')
async def add_person_start(call: types.CallbackQuery):
    admin_id = workWF.read_admin()
    all_pools = str(sqLite.read_value_bu_name(name='pool', table='users', telegram_id=admin_id)[0])
    all_pools = all_pools.split('Q')
    text = ''
    for i in all_pools:
        if i == '':
            pass
        else:
            text = text + i + ', '
    await call.message.edit_text(text=f"Введите номер нового бассейна.\n"
                                      f"Вот номера бассейнов которые уже есть в базе\n"
                                      f"<b>{text[:-2]}</b>\n\n"
                                      f"Только цифры", parse_mode='html',
                                 reply_markup=back_kb)
    await Admin_Pool.create_pool.set()


# Create pool confirm
@dp.message_handler(state=Admin_Pool.create_pool)
async def add_person_start(message: types.Message):
    if message.text.isdigit():
        admin_id = workWF.read_admin()
        all_pools = str(sqLite.read_value_bu_name(name='pool', table='users', telegram_id=admin_id)[0])
        if message.text in all_pools.split('Q'):
            await message.answer("Данный номер уже есть")
        else:
            await message.answer(text=f"Номер нового бассейна <b>№{message.text}</b>\n"
                                      f"Данные верны?", parse_mode='html',
                                 reply_markup=confirm_kb)
            await Admin_Pool.confirm_new_pool.set()
            sqLite.insert_info(table_name='users', name='data', date=message.text, telegram_id=admin_id)
    else:
        await message.answer('Введите только цифры')


# Create pool Callback
@dp.callback_query_handler(state=Admin_Pool.confirm_new_pool, text='yes_all_good')
async def add_person_start(call: types.CallbackQuery):
    admin_id = workWF.read_admin()
    all_pools = str(sqLite.read_value_bu_name(name='pool', table='users', telegram_id=admin_id)[0])

    number = str(sqLite.read_value_bu_name(table='users', name='data', telegram_id=admin_id)[0])
    if all_pools == 'None':
        text = f"{str(number)}Q"
    else:
        text = all_pools + str(number) + 'Q'
    sqLite.insert_info(table_name='users', name='pool', date=text, telegram_id=admin_id)
    sqLite.insert_first_pool(int(number))
    sqLite.new_user_table(int(number))
    await call.message.edit_text(text=f"Данные сохранены")
    await call.message.answer(text="Здесь вы работаете с бассейнами. Выберите меню ниже.", reply_markup=pool_kb)
    await Admin_Pool.pool_start.set()


# Create pool Callback
@dp.callback_query_handler(state=Admin_Pool.pool_start, text='check_all_pools')
async def add_person_start(call: types.CallbackQuery):
    admin_id = workWF.read_admin()
    all_pools = str(sqLite.read_value_bu_name(name='pool', table='users', telegram_id=admin_id)[0])
    all_pools = all_pools.split('Q')
    date_keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    for i in range(0, len(all_pools) - 1):
        k = i
        i = KeyboardButton(f'Бассейн №{str(all_pools[k])}', )
        date_keyboard.insert(i)
    await call.message.answer(text=f"Вот все ваши бассейны. \nВыберите бассейн", parse_mode='html',
                              reply_markup=date_keyboard)
    await Admin_Pool.check_poll_data.set()


# Show pool data
@dp.message_handler(state=Admin_Pool.check_poll_data)
async def add_person_start(message: types.Message):
    if 'Бассейн №' in message.text:
        pool_number = message.text[9:]
        sqLite.insert_info(table_name='users', name='data', date=pool_number, telegram_id=workWF.read_admin())
        pool_data = sqLite.read_values_in_db_by_phone(name='number', table='pools', data=f'{pool_number}')
        all_investors = str(pool_data[1]).split('TgID')
        all_fish_id = str(pool_data[2]).split('ID')
        all_fish_mass = str(pool_data[3]).split('KG')
        pool_all_fish = sqLite.read_values_in_db_by_phone(table='pools', name='number', data=int(pool_number))[4]
        await message.answer(f"В бассейне №{pool_number} сейчас <b>{pool_all_fish} кг</b> рыбы", parse_mode='html')
        for i in range(len(all_investors) - 1):
            inv_name = sqLite.read_value_bu_name(table='users', name='*', telegram_id=int(all_investors[i]))
            await message.answer(f'Инвестор - <b>{inv_name[2]} {inv_name[3]}</b>\n'
                                 f'Владеет рыбой с ID <b>{all_fish_id[i]}</b>\n'
                                 f'Масса рыбы <b>{all_fish_mass[i]} кг</b>\n'
                                 f'Процент рыбы в бассейне '
                                 f'<b>{round(float((float(all_fish_mass[i]) * 100) / float(pool_all_fish)), 0)} %</b>',
                                 parse_mode='html')
        await message.answer('Что вы хотите сделать с рыбой?', reply_markup=work_with_fish)
        await Admin_Pool.sale_fish_in_pool.set()
    else:
        await message.answer('Нажмите кнопку')


# Delete pool
@dp.callback_query_handler(state=Admin_Pool.sale_fish_in_pool, text='delete_pool')
async def add_person_start(call: types.CallbackQuery):
    pool_data = sqLite.read_values_in_db_by_phone(name='telegram_id', table='users', data=workWF.read_admin())[10]
    await call.message.edit_text(text=f"Вы уверены что хотите удалить бассейн №{pool_data}", parse_mode='html',
                                 reply_markup=confirm_kb)
    await Admin_Pool.delete_fish_in_pool.set()


# Delete pool
@dp.callback_query_handler(state=Admin_Pool.delete_fish_in_pool, text='yes_all_good')
async def add_person_start(call: types.CallbackQuery):
    pool_data = sqLite.read_values_in_db_by_phone(name='telegram_id', table='users', data=workWF.read_admin())[10]
    sqLite.delete_str(table='pools', name='number', data=int(pool_data))
    numb_pool = sqLite.read_value_bu_name(name='pool', table='users', telegram_id=workWF.read_admin())[0]
    numb_pool = str(numb_pool).split('Q')
    pools = ''
    for i in numb_pool:
        if i == str(pool_data):
            pass
        else:
            pools = pools + i + 'Q'
    pools = pools[:-1]
    sqLite.insert_info(table_name='users', name='pool', date=pools, telegram_id=workWF.read_admin())
    await call.message.edit_text(text=f"Данные удалены")
    await call.message.answer(text="Здесь вы работаете с бассейнами. Выберите меню ниже.", reply_markup=pool_kb)
    await Admin_Pool.pool_start.set()


# Sale fish in pool
@dp.callback_query_handler(state=Admin_Pool.sale_fish_in_pool, text='sail_all')
async def add_person_start(call: types.CallbackQuery):
    await call.message.answer(text=f"Введите стоимость сумму за какую была продана вся рыба в бассейне")
    await Admin_Pool.sale_fish_in_pool_confirm.set()


# Sale fish in pool
@dp.message_handler(state=Admin_Pool.sale_fish_in_pool_confirm)
async def add_person_start(message: types.Message):
    pool_data = sqLite.read_values_in_db_by_phone(name='telegram_id', table='users', data=workWF.read_admin())[10]
    check = sqLite.read_values_in_db_by_phone(table='pools', name='number', data=int(pool_data))[2]
    if check is None or check == '':
        await message.answer('В бассейне нет рыбы')
        await message.answer(text="Здесь вы работаете с бассейнами. Выберите меню ниже.", reply_markup=pool_kb)
        await Admin_Pool.pool_start.set()
    else:
        if message.text.isdigit():
            sqLite.insert_info(table_name='users', name='data_2', date=message.text, telegram_id=workWF.read_admin())
            await message.answer(text=f"Вы точно хотите продать всю рыбу из этого бассейна?", reply_markup=confirm_kb)
            await Admin_Pool.money_from_fish.set()
        else:
            await message.answer('Введите только цифры')


# Pick a price
@dp.callback_query_handler(state=Admin_Pool.money_from_fish, text='yes_all_good')
async def add_person_start(call: types.CallbackQuery):
    money = sqLite.read_value_bu_name(name='data_2', table='users', telegram_id=workWF.read_admin())[0]
    pool_number = sqLite.read_value_bu_name(name='data', table='users', telegram_id=workWF.read_admin())[0]
    pool_data = sqLite.read_values_in_db_by_phone(name='number', table='pools', data=f'{pool_number}')
    all_investors = str(pool_data[1]).split('TgID')
    all_fish_id = str(pool_data[2]).split('ID')
    investor_fish_mass = str(pool_data[3]).split('KG')
    pool_all_fish = int(pool_data[4])
    for i in range(len(all_investors) - 1):
        inv_name = sqLite.read_value_bu_name(table='users', name='*', telegram_id=int(all_investors[i]))
        money_for_investor = int((int(investor_fish_mass[i]) * int(money)) / pool_all_fish)
        balance = inv_name[6]
        if balance is not None:
            balance = float(balance) + float(money_for_investor)
            sqLite.insert_info(table_name='users', name='balance',
                               date=str(balance), telegram_id=int(all_investors[i]))
        else:
            sqLite.insert_info(table_name='users', name='balance',
                               date=str(money_for_investor), telegram_id=int(all_investors[i]))
        sqLite.insert_info_pool(name='oners', date='', number=pool_number)
        sqLite.insert_info_pool(name='fish_id', date='', number=pool_number)
        sqLite.insert_info_pool(name='start_fish_mass', date='', number=pool_number)
        sqLite.insert_info_pool(name='fish_mass', date='', number=pool_number)
        try:
            await call.message.answer(f'Инвестор - <b>{inv_name[2]} {inv_name[3]}</b>\n'
                                      f'Процент рыбы в бассейне '
                                      f'<b>{int((int(investor_fish_mass[i]) * 100) / pool_all_fish)} %</b>\n'
                                      f'Получил на баланс - <b>{money_for_investor} RUR</b>',
                                      parse_mode='html')
            await bot.send_message(chat_id=int(all_investors[i]),
                                   text=f'Инвестор - <b>{inv_name[2]} {inv_name[3]}</b>\n'
                                        f'Ваша рыба с ID <b>{all_fish_id[i]}</b> была продана за '
                                        f'{money_for_investor} RUR\n',
                                   parse_mode='html')
        except:
            print(f'Ошибка продажи всего бассейна {money_for_investor}')
    await call.message.answer(text="Здесь вы работаете с бассейнами. Выберите меню ниже.", reply_markup=pool_kb)
    await Admin_Pool.pool_start.set()


# Create pool Callback
@dp.callback_query_handler(state=Admin_Pool.confirm_new_pool, text='back')
@dp.callback_query_handler(state=Admin_Pool.pool_start, text='add_fish_btn')
async def add_person_start(call: types.CallbackQuery):
    admin_id = workWF.read_admin()
    all_pools = str(sqLite.read_value_bu_name(name='pool', table='users', telegram_id=admin_id)[0])
    all_pools = all_pools.split('Q')
    date_keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    for i in range(0, len(all_pools) - 1):
        k = i
        i = KeyboardButton(f'Бассейн №{str(all_pools[k])}', )
        date_keyboard.insert(i)
    await call.message.answer(text=f"Вот все ваши бассейны. \nВыберите бассейн", parse_mode='html',
                              reply_markup=date_keyboard)
    await Admin_Pool.add_fish.set()


# Show pool data
@dp.message_handler(state=Admin_Pool.add_fish)
async def add_person_start(message: types.Message):
    if 'Бассейн №' in message.text:
        pool_number = message.text[9:]
        sqLite.insert_info(name='data', table_name='users', date=f'{pool_number}', telegram_id=workWF.read_admin())
        date_keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        all_users = sqLite.read_all_value_bu_name(name='*', table=f'users')
        for i in range(0, len(all_users)):
            if 'investor' in all_users[i]:
                investor = all_users[i]
                show_data = f'{str(investor[3])} {str(investor[2])} TgID {str(investor[0])}'
                i = KeyboardButton(show_data)
                date_keyboard.add(i)
            else:
                pass
        await message.answer(text="Выберите инвестора", reply_markup=date_keyboard)
        await Admin_Pool.pick_investor.set()
    else:
        await message.answer('Нажмите кнопку')


# Start menu admin reply
@dp.message_handler(state=Admin_Pool.pick_investor)
async def add_person_start(message: types.Message):
    if 'TgID' in str(message.text):
        sqLite.insert_info(name='data_2', table_name='users', date=f'{message.text}', telegram_id=workWF.read_admin())
        await message.answer(text=f"Введите начальную массу добавляемой рыбы в кг.\n\n"
                                  f"Только цифры.")
        await Admin_Pool.pick_fish_mass.set()
    else:
        await message.answer(text="Нажмите кнопку")


# Start menu admin reply
@dp.message_handler(state=Admin_Pool.pick_fish_mass)
async def add_person_start(message: types.Message):
    if message.text.isdigit():
        sqLite.insert_info(name='fish_mass', table_name='users', date=f'{message.text}',
                           telegram_id=workWF.read_admin())
        fish_id = str(sqLite.read_value_bu_name(name='last_id', table='users', telegram_id=workWF.read_admin())[0])
        await message.answer(text=f"Введите ID сделки. Последний ID сделки в базе данных - <b>{fish_id}</b>\n\n"
                                  f"Только цифры.", parse_mode='html')
        await Admin_Pool.confirm_fish.set()

    else:
        await message.answer(text="Введите только цифры")


# Start menu admin reply
@dp.message_handler(state=Admin_Pool.confirm_fish)
async def add_person_start(message: types.Message):
    if message.text.isdigit():
        sqLite.insert_info(name='fish_number', table_name='users', date=f'{message.text}',
                           telegram_id=workWF.read_admin())
        data = sqLite.read_values_in_db_by_phone(table='users', name='telegram_id', data=workWF.read_admin())
        name = str(data[11]).split('TgID ')[0]
        all_fish_in_pool = sqLite.read_values_in_db_by_phone(table='pools', name='number', data=int(data[10]))[4]
        await message.answer(text=f"Инвестор - <b>{name}</b>\n"
                                  f"Купил - <b>{data[12]}</b> кг рыбы\n"
                                  f"В бассейн - <b>№ {data[10]}</b>\n"
                                  f"ID сделки - <b>№ {message.text}</b>\n"
                                  f"В бассейне сейчас - <b>{str(all_fish_in_pool)} кг</b> рыбы", parse_mode='html',
                             reply_markup=confirm_kb)
        await Admin_Pool.save_fish.set()

    else:
        await message.answer(text="Введите только цифры")


# Start menu admin reply
@dp.callback_query_handler(state=Admin_Pool.save_fish, text='yes_all_good')
async def add_person_start(call: types.CallbackQuery):
    await call.message.answer('Данные сохранены')
    data = sqLite.read_values_in_db_by_phone(table='users', name='telegram_id', data=workWF.read_admin())
    pool_old_data = sqLite.read_values_in_db_by_phone(table='pools', name='number', data=int(data[10]))
    oner = str(data[11]).split('TgID ')[1]
    old_oners = pool_old_data[1]
    if old_oners is None:
        sqLite.insert_info_pool(number=int(data[10]), name='oners', date=f'{oner}TgID')
    else:
        sqLite.insert_info_pool(number=int(data[10]), name='oners', date=f'{old_oners}{oner}TgID')

    fish_id = str(data[13])
    old_fish_id = pool_old_data[2]
    if old_fish_id is None:
        sqLite.insert_info_pool(number=int(data[10]), name='fish_id', date=f'{fish_id}ID')
    else:
        sqLite.insert_info_pool(number=int(data[10]), name='fish_id', date=f'{old_fish_id}{fish_id}ID')

    start_fish_mass = str(data[12])
    ols_start_fish_mass = pool_old_data[3]
    if ols_start_fish_mass is None:
        sqLite.insert_info_pool(number=int(data[10]), name='start_fish_mass', date=f'{start_fish_mass}KG')
    else:
        sqLite.insert_info_pool(number=int(data[10]), name='start_fish_mass',
                                date=f'{ols_start_fish_mass}{start_fish_mass}KG')

    all_fish_mass = pool_old_data[4]

    if all_fish_mass is None or all_fish_mass == '':
        sqLite.insert_info_pool(number=int(data[10]), name='fish_mass', date=f'{start_fish_mass}')
    else:
        all_fish_mass = int(all_fish_mass)
        sqLite.insert_info_pool(number=int(data[10]), name='fish_mass',
                                date=(all_fish_mass + int(start_fish_mass)))
    sqLite.insert_pool_db1(telegram_id=oner,
                           food_mass='None',
                           fish_mass=start_fish_mass,
                           fish_id=fish_id,
                           number=int(data[10]),
                           data=datetime.datetime.now(),
                           type='admin_add_fish')

    old_balance = sqLite.read_values_in_db_by_phone(table='users', name='telegram_id', data=int(oner))[6]
    sqLite.insert_info(table_name='users', telegram_id=workWF.read_admin(), date=int(fish_id), name='last_id')
    new_balance = float(old_balance) - float(start_fish_mass)*float(data[15])
    sqLite.insert_info(table_name='users', telegram_id=int(oner), date=new_balance, name='balance')
    try:
        await bot.send_message(chat_id=oner, text=f'Поздравляем администратор добавил вам рыбу с ID <b>{fish_id}</b>. '
                                                  f'Рыба находится в бассейне №{data[10]} '
                                                  f'Масса рыбы <b>{start_fish_mass} кг</b>', parse_mode='html')
    except:
        try:
            await bot.send_message(chat_id=workWF.read_admin(), text=f'Телеграм ID {oner} '
                                                                     f'недействительный либо юзер не подписан на бота')
        except:
            print(oner, 'добавление рыбы')
    await call.message.answer(text="Здесь вы работаете с бассейнами. Выберите меню ниже.", reply_markup=pool_kb)
    await Admin_Pool.pool_start.set()
