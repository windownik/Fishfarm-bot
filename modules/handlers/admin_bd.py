from aiogram import types
from main import dp
from modules import sqLite, workWF
from modules.dispatcher import Admin_db, Admin_Form
from modules.keyboards import start_admin_kb
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


# Start menu admin work with BD
@dp.callback_query_handler(state=Admin_Form.admin_first_menu, text='db')
async def add_person_start(call: types.CallbackQuery):
    pools = sqLite.read_all_value_bu_name(name='oners', table='pools')
    date_keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    for i in range(0, len(pools)):
        i = KeyboardButton(f'Бассейн №{i+1}')
        date_keyboard.add(i)
    await call.message.answer(text="Выберите бассейн в котором вы хотите посмотреть журнал событий",
                              reply_markup=date_keyboard)
    await Admin_db.db_start.set()


# Menu admin pick ID
@dp.message_handler(state=Admin_db.db_start)
async def add_person_start(message: types.Message):
    if ' №' in message.text:
        pool_id = str(message.text.split('№')[1])
        tg_id = int(workWF.read_admin())

        sqLite.insert_info(table_name='users', telegram_id=tg_id, name='data', date=pool_id)
        fish_id = sqLite.read_all_value_bu_name(name='*', table=f'pool{pool_id}')
        date_keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        id_s = ''
        for i in range(0, len(fish_id)):
            if str(fish_id[i][3]) in id_s:
                pass
            else:
                id_s = id_s + str(fish_id[i][3]) + ' '
                i = KeyboardButton(f'ID № {str(fish_id[i][3])}')
                date_keyboard.insert(i)
        await message.answer('Выберите ID рыбы которой вы хотите посмотреть журнал событий',
                             reply_markup=date_keyboard)
        await Admin_db.db_pick_pool.set()
    else:
        await message.answer('Нажмите на кнопку')


# Menu admin pick month
@dp.message_handler(state=Admin_db.db_pick_pool)
async def add_person_start(message: types.Message):
    if 'ID № ' in message.text:
        fish_id = str(message.text.split('ID № ')[1])
        tg_id = int(workWF.read_admin())
        pool_id = sqLite.read_value_bu_name(name='data', table='users', telegram_id=tg_id)[0]
        sqLite.insert_info(table_name='users', telegram_id=tg_id, name='data_2', date=fish_id)
        data = sqLite.read_all_value_bu_name(name='*', table=f'pool{pool_id}')
        date_keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        month = ''
        for i in range(0, len(data)):
            month_data = str(str(data[i][5]).split(' ')[0])[:-3]
            if str(month_data) in month:
                pass
            else:
                month = month + str(month_data) + ' '
                i = KeyboardButton(f'{month_data}')
                date_keyboard.add(i)
        await message.answer('Выберите месяц за который вы хотите просмотреть журнал',
                             reply_markup=date_keyboard)
        await Admin_db.show_data.set()
    else:
        await message.answer('Нажмите на кнопку')


# Show investor journal by fish ID in one month
@dp.message_handler(state=Admin_db.show_data)
async def add_person_start(message: types.Message):
    tg_id = int(workWF.read_admin())
    pool_id = sqLite.read_value_bu_name(name='data', table='users', telegram_id=tg_id)[0]
    fish_id = sqLite.read_value_bu_name(name='data_2', table='users', telegram_id=tg_id)[0]
    data = sqLite.read_all_value_bu_name(name='*', table=f'pool{str(pool_id)}')
    month = str(message.text)
    for i in range(0, len(data)):
        fish_id_in_bd = data[i][3]
        if str(fish_id) in str(fish_id_in_bd):
            if month in str(data[i][5]):
                line_type = str(data[i][4])
                if line_type == 'admin_add_fish':
                    await message.answer(text=f'Вы купили новую рыбу начальной общей массой - '
                                              f'<b>{str(data[i][2])} кг</b>, её ID <b>{str(data[i][3])}</b>. '
                                              f'Дата записи - <b>{str(data[i][5]).split(".")[0]}</b>',
                                         parse_mode='html', reply_markup=types.ReplyKeyboardRemove())
                elif line_type == 'feed_fish':
                    await message.answer(text=f'Вашу рыбку с ID - <b>{str(data[i][3])}</b> покормили. На эту ушло '
                                              f'<b>{str(data[i][1])} кг</b> корма. '
                                              f'Дата записи - <b>{str(data[i][5]).split(".")[0]}</b>',
                                         parse_mode='html', reply_markup=types.ReplyKeyboardRemove())
                elif line_type == 'size_fish':
                    await message.answer(text=f'Вашу рыбку с ID - <b>{str(data[i][3])}</b> измеряли. Ее вес составил '
                                              f'<b>{str(data[i][2])} кг</b>. '
                                              f'Дата записи - <b>{str(data[i][5]).split(".")[0]}</b>',
                                         parse_mode='html', reply_markup=types.ReplyKeyboardRemove())
                elif line_type == 'service_pay':
                    await message.answer(text=f'С вашего счета списана сумма <b>{str(data[i][1])} RUR</b> '
                                              f'pа обслуживание вашей рыбы с ID - <b>{str(data[i][3])}</b>. '
                                              f'Дата записи - <b>{str(data[i][5]).split(".")[0]}</b>',
                                         parse_mode='html', reply_markup=types.ReplyKeyboardRemove())
                elif line_type == 'admin_sell_fish':
                    await message.answer(text=f'Вашу рыбу с ID <b>{str(data[i][3])}</b> продали за <b>{str(data[i][1])}'
                                              f'RUR</b>. Дата записи - <b>{str(data[i][5]).split(".")[0]}</b>',
                                         parse_mode='html', reply_markup=types.ReplyKeyboardRemove())
                else:
                    await message.answer(
                        text=f"Запись не определена -{line_type}- Дата и время записи - "
                             f"{str(data[i][5]).split('.')[0]}", reply_markup=types.ReplyKeyboardRemove())
    await message.answer(text=f'Добрый день. Администратор чем тебе помочь', reply_markup=start_admin_kb)
    await Admin_Form.admin_first_menu.set()
