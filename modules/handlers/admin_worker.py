from aiogram import types
from main import dp
from modules import sqLite, workWF
from aiogram.dispatcher.filters import Text
from modules.dispatcher import Admin_Form, Admin_Worker
from modules.keyboards import admin_worker, change_contact_kb, worker_kb, activity_kb, confirm_kb, back_kb
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


# Start menu admin Callback
@dp.callback_query_handler(state=Admin_Worker.correct_worker_data, text='back')
@dp.callback_query_handler(state=Admin_Worker.delete_worker, text='back')
@dp.callback_query_handler(state=Admin_Worker.confirm_correct_tg_id, text='back')
@dp.callback_query_handler(state=Admin_Worker.confirm_status, text='back')
@dp.callback_query_handler(state=Admin_Worker.confirm_correct_phone, text='back')
@dp.callback_query_handler(state=Admin_Form.phone_input, text='back')
@dp.callback_query_handler(state=Admin_Form.admin_first_menu, text='staff')
async def add_person_start(call: types.CallbackQuery):
    await call.message.edit_text(text="Здесь вы управляете рабочими.", reply_markup=admin_worker)
    await Admin_Worker.admin_all_worker.set()


# Start menu admin reply
@dp.message_handler(Text(equals='⬅️ Назад', ignore_case=True), state=Admin_Form.surname_input)
async def add_person_start(message: types.Message):
    await message.edit_text(text="Здесь вы управляете рабочими.", reply_markup=admin_worker)
    await Admin_Worker.admin_all_worker.set()


# Show all staff personal
@dp.callback_query_handler(state=Admin_Worker.worker_data, text='back')
@dp.callback_query_handler(state=Admin_Worker.admin_all_worker, text='all_staff')
async def phone(call: types.CallbackQuery):
    date_keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    all_users = sqLite.read_all_value_bu_name(name='*', table=f'users')
    for i in range(0, len(all_users)):
        if 'worker' in str(all_users[i][4]):
            worker = all_users[i]
            show_data = f'{str(worker[3])} {str(worker[2])} TgID {str(worker[0])}'
            i = KeyboardButton(show_data)
            date_keyboard.add(i)
        else:
            pass
    await call.message.answer(text="Вот все ваши рабочие", reply_markup=date_keyboard)
    await Admin_Worker.worker_data.set()


# Start menu admin reply
@dp.message_handler(state=Admin_Worker.worker_data)
async def add_person_start(message: types.Message):
    if 'TgID' in str(message.text):
        input_data = str(message.text).split('TgID ')[1]
        sqLite.insert_info(table_name='users', name=f'data', date=f'{input_data}', telegram_id=workWF.read_admin())
        worker_data = sqLite.read_value_bu_name(name='*', table='users', telegram_id=int(input_data))
        if worker_data[8] is True or str(worker_data[8]) == 'True':
            status = 'Работает'
        else:
            status = 'Отключен'
        await message.answer(text=f"Имя - {worker_data[3]}\n"
                                  f"Фамилия - {worker_data[2]}\n"
                                  f"Телефон - {worker_data[1]}\n"
                                  f"Телеграм ID - {worker_data[0]}\n"
                                  f"Тип аккаунта - {worker_data[4]}\n"
                                  f"Статус - {status}", reply_markup=worker_kb)
        await Admin_Worker.correct_worker_data.set()
    else:
        await message.answer(text="Нажмите кнопку ниже")


# Correct data
@dp.callback_query_handler(state=Admin_Worker.correct_worker_data, text='change')
async def add_person_start(call: types.CallbackQuery):
    await call.message.answer(text='Выберите что изменить', reply_markup=change_contact_kb)
    await Admin_Worker.pick_data.set()


# Phone input callback
@dp.message_handler(state=Admin_Worker.pick_data)
async def start_menu(message: types.Message):
    if message.text == '📞 Телефон':
        await message.answer('Введите новый телефонный номер \n'
                             'пример: +7123456789')
        await Admin_Worker.correct_phone.set()
    elif message.text == '🧭 Телеграм ID':
        sqLite.insert_info(table_name='users', name=f'data_2', date=f'telegram_id', telegram_id=workWF.read_admin())
        await message.answer('Введите новый Telegram ID')
        await Admin_Worker.correct_tg_id.set()
    elif message.text == '⚙️ Статус':
        sqLite.insert_info(table_name='users', name=f'data_2', date=f'activ', telegram_id=workWF.read_admin())
        await message.answer('Выберите новый статус', reply_markup=activity_kb)
        await Admin_Worker.correct_status.set()
    else:
        await message.answer(text='Нажмите кнопку')


# Phone input
@dp.message_handler(state=Admin_Worker.correct_phone)
async def start_menu(message: types.Message):
    sqLite.insert_info(table_name='users', name=f'data_2', date=message.text, telegram_id=workWF.read_admin())
    user_id = sqLite.read_value_bu_name(name='data', table='users', telegram_id=workWF.read_admin())[0]
    old_phone = sqLite.read_value_bu_name(name='phone_number', table='users', telegram_id=int(user_id))[0]
    name = sqLite.read_value_bu_name(name='name', table='users', telegram_id=int(user_id))[0]
    surname = sqLite.read_value_bu_name(name='surname', table='users', telegram_id=int(user_id))[0]
    await message.answer(text=f'Вы уверены что хотите заменить телефонный номер <b>{old_phone}</b> у рабочего\n'
                              f'<b>{name} {surname}</b> на новый телефонный номер <b>{message.text}</b>',
                         reply_markup=confirm_kb, parse_mode='html')
    await Admin_Worker.confirm_correct_phone.set()


# Confirm new phone
@dp.callback_query_handler(state=Admin_Worker.confirm_correct_phone, text='yes_all_good')
async def add_person_start(call: types.CallbackQuery):
    user_id = sqLite.read_value_bu_name(name='data', table='users', telegram_id=workWF.read_admin())[0]
    phone_numb = sqLite.read_value_bu_name(name='data_2', table='users', telegram_id=workWF.read_admin())[0]
    sqLite.insert_info(table_name='users', name=f'phone_number', date=phone_numb, telegram_id=int(user_id))
    await call.message.answer(text='Данные сохранены', reply_markup=types.ReplyKeyboardRemove())
    await call.message.answer(text="Здесь вы управляете рабочими.", reply_markup=admin_worker)
    await Admin_Worker.admin_all_worker.set()


# Tg ID input
@dp.message_handler(state=Admin_Worker.correct_tg_id)
async def start_menu(message: types.Message):
    sqLite.insert_info(table_name='users', name=f'data_2', date=message.text, telegram_id=workWF.read_admin())
    user_id = sqLite.read_value_bu_name(name='data', table='users', telegram_id=workWF.read_admin())[0]
    old_phone = sqLite.read_value_bu_name(name='telegram_id', table='users', telegram_id=int(user_id))[0]
    name = sqLite.read_value_bu_name(name='name', table='users', telegram_id=int(user_id))[0]
    surname = sqLite.read_value_bu_name(name='surname', table='users', telegram_id=int(user_id))[0]
    await message.answer(text=f'Вы уверены что хотите заменить Telegram ID <b>{old_phone}</b> у рабочего\n'
                              f'<b>{name} {surname}</b> на новый Telegram ID <b>{message.text}</b>',
                         reply_markup=confirm_kb, parse_mode='html')
    await Admin_Worker.confirm_correct_tg_id.set()


# Confirm new telegram id
@dp.callback_query_handler(state=Admin_Worker.confirm_correct_tg_id, text='yes_all_good')
async def add_person_start(call: types.CallbackQuery):
    user_id = sqLite.read_value_bu_name(name='data', table='users', telegram_id=workWF.read_admin())[0]
    phone_numb = sqLite.read_value_bu_name(name='data_2', table='users', telegram_id=workWF.read_admin())[0]
    sqLite.insert_info(table_name='users', name=f'telegram_id', date=phone_numb, telegram_id=int(user_id))
    await call.message.answer(text='Данные сохранены', reply_markup=types.ReplyKeyboardRemove())
    await call.message.answer(text="Здесь вы управляете рабочими.", reply_markup=admin_worker)
    await Admin_Worker.admin_all_worker.set()


# Status input
@dp.message_handler(state=Admin_Worker.correct_status)
async def start_menu(message: types.Message):
    if '⚙️' in message.text:
        if message.text == '⚙️ Отключить аккаунт':
            text = 'отключен'
        elif message.text == '⚙️ Включить аккаунт':
            text = 'работает'
        else:
            pass
        sqLite.insert_info(table_name='users', name=f'data_2', date=text, telegram_id=workWF.read_admin())
        user_id = sqLite.read_value_bu_name(name='data', table='users', telegram_id=workWF.read_admin())[0]
        old_status = sqLite.read_value_bu_name(name='activ', table='users', telegram_id=int(user_id))[0]
        old_text = 'blank'
        if old_status == False or str(old_status) == 'False':
            old_text = 'отключен'
        elif old_status == True or str(old_status) == 'True':
            old_text = 'работает'
        name = sqLite.read_value_bu_name(name='name', table='users', telegram_id=int(user_id))[0]
        surname = sqLite.read_value_bu_name(name='surname', table='users', telegram_id=int(user_id))[0]
        await message.answer(text=f'Вы уверены что хотите изменить старый статус <b>{old_text}</b> у рабочего\n'
                                  f'<b>{name} {surname}</b> на новый статус <b>{text}</b>',
                             reply_markup=confirm_kb, parse_mode='html')
        await Admin_Worker.confirm_status.set()
    else:
        await message.answer('Нажмите кнопку')


# Confirm new telegram id
@dp.callback_query_handler(state=Admin_Worker.confirm_status, text='yes_all_good')
async def add_person_start(call: types.CallbackQuery):
    user_id = sqLite.read_value_bu_name(name='data', table='users', telegram_id=workWF.read_admin())[0]
    status = sqLite.read_value_bu_name(name='data_2', table='users', telegram_id=workWF.read_admin())[0]
    if status == 'отключен':
        data = False
    elif status == 'работает':
        data = True
    else:
        pass
    sqLite.insert_info(table_name='users', name=f'activ', date=data, telegram_id=int(user_id))
    await call.message.answer(text='Данные сохранены', reply_markup=types.ReplyKeyboardRemove())
    await call.message.answer(text="Здесь вы управляете рабочими.", reply_markup=admin_worker)
    await Admin_Worker.admin_all_worker.set()


# Delete worker
@dp.callback_query_handler(state=Admin_Worker.correct_worker_data, text='delete')
async def add_person_start(call: types.CallbackQuery):
    await call.message.answer(text='Вы точно хотите удалить рабочего?', reply_markup=confirm_kb)
    await Admin_Worker.delete_worker.set()


# Delete worker
@dp.callback_query_handler(state=Admin_Worker.delete_worker, text='yes_all_good')
async def add_person_start(call: types.CallbackQuery):
    user_id = sqLite.read_value_bu_name(name='data', table='users', telegram_id=workWF.read_admin())[0]
    print(user_id)
    sqLite.delete_str(table='users', name='telegram_id', data=int(user_id))
    await call.message.answer(text='Данные удалены', reply_markup=types.ReplyKeyboardRemove())
    await call.message.answer(text="Здесь вы управляете рабочими.", reply_markup=admin_worker)
    await Admin_Worker.admin_all_worker.set()


# Show all staff journal notes
@dp.callback_query_handler(state=Admin_Worker.correct_worker_data, text='jornal')
async def phone(call: types.CallbackQuery):
    user_id = sqLite.read_value_bu_name(name='data', table='users', telegram_id=workWF.read_admin())[0]
    date_keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    all_pools = sqLite.read_all_value_bu_name(name='*', table=f'pools')
    month = ''
    for i in range(0, len(all_pools)):
        one_pool = sqLite.read_all_value_bu_name(name='*', table=f'pool{str(i + 1)}')
        for k in range(0, (len(one_pool))):
            deal_tg_id = str(one_pool[k][0])
            data = str(one_pool[k][5]).split(' ')[0][:-3]
            if str(data) in month:
                pass
            else:
                if str(user_id) in deal_tg_id:
                    month = month + ' ' + data
                    k = KeyboardButton(data)
                    date_keyboard.add(k)
                else:
                    pass
    if month == '':
        await call.message.edit_text(text="У этого рабочего пока нет записей в журнале", reply_markup=back_kb)
    else:
        await call.message.answer(text='Вот все месяцы в которых есть записи от этого рабочего.\nВыберите месяц.',
                                  reply_markup=date_keyboard)
    await Admin_Worker.journal.set()


# Status input
@dp.message_handler(state=Admin_Worker.journal)
async def start_menu(message: types.Message):
    month = message.text
    user_id = sqLite.read_value_bu_name(name='data', table='users', telegram_id=workWF.read_admin())[0]
    all_pools = sqLite.read_all_value_bu_name(name='*', table=f'pools')
    for i in range(0, len(all_pools)):
        one_pool = sqLite.read_all_value_bu_name(name='*', table=f'pool{str(i + 1)}')
        for k in range(0, (len(one_pool))):
            deal_tg_id = str(one_pool[k][0])
            data = str(one_pool[k][5]).split(' ')[0][:-3]
            if str(data) == month:
                if str(user_id) in deal_tg_id:
                    if str(one_pool[k][4]) == 'feed_fish':
                        await message.answer(f'ID рыбы - <b>{one_pool[k][3]}</b>, масса - <b>{one_pool[k][2]} кг</b>\n'
                                             f'Тип записи - <b>Рыба покормлена</b>, масса корма - '
                                             f'<b>{one_pool[k][1]} кг</b>\n Время записи '
                                             f'{str(one_pool[k][5]).split(".")[0]}',
                                             parse_mode='html')
                    elif str(one_pool[k][4]) == 'size_fish':
                        await message.answer(f'ID рыбы - <b>{one_pool[k][3]}</b>, масса - <b>{one_pool[k][2]} кг</b>\n'
                                             f'Тип записи - <b>Замер размеров</b>,\n Время записи '
                                             f'<b>{str(one_pool[k][5]).split(".")[0]}</b>',
                                             parse_mode='html')
                    else:
                        await message.answer(f'ID рыбы - <b>{one_pool[k][3]}</b>, масса - <b>{one_pool[k][2]} кг</b>\n'
                                             f'Тип записи - <b>{str(one_pool[k][4])}</b>,\n Время записи '
                                             f'<b>{str(one_pool[k][5]).split(".")[0]}</b>',
                                             parse_mode='html')
                else:
                    pass
            else:
                pass
    await message.answer(text="Здесь вы управляете рабочими.", reply_markup=admin_worker)
    await Admin_Worker.admin_all_worker.set()
