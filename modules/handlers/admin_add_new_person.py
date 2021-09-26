from aiogram import types
from main import dp
from modules import workWF, sqLite
from aiogram.dispatcher.filters import Text
from modules.dispatcher import bot, Admin_Form
from modules.keyboards import admin_kb_start, back_reply, add_person_reply, start_admin_kb


# Start menu admin
@dp.callback_query_handler(state=Admin_Form.phone_input, text='back')
@dp.callback_query_handler(state=Admin_Form.admin_first_menu, text='add_person')
async def add_person_start(call: types.CallbackQuery):
    await call.message.edit_text(text="Выберите меню ниже", reply_markup=admin_kb_start)
    await Admin_Form.name_input.set()


# Start menu admin
@dp.message_handler(Text(equals='⬅️ Назад', ignore_case=True), state=Admin_Form.type_input)
@dp.message_handler(Text(equals='⬅️ Назад', ignore_case=True), state=Admin_Form.phone_input_search)
@dp.message_handler(Text(equals='⬅️ Назад', ignore_case=True), state=Admin_Form.manual_input)
async def add_person_start(message: types.Message):
    await message.answer(text="Выберите меню ниже", reply_markup=admin_kb_start)
    await Admin_Form.name_input.set()


# Telegram_ID input Callback
@dp.callback_query_handler(state=Admin_Form.name_input, text='manual_input')
async def phone(call: types.CallbackQuery):
    await call.message.answer(text='Введите Телеграм ID. \nТолько цифры.\n'
                                   'Если вы не знаете телеграм id. '
                                   'Попросите инвестора зарегистрироваться и прислать вам заявку.',
                              reply_markup=back_reply)
    await Admin_Form.manual_input.set()


# Telegram_ID input
@dp.message_handler(Text(equals='⬅️ Назад', ignore_case=True), state=Admin_Form.phone_input)
@dp.message_handler(state=Admin_Form.name_input)
async def start_menu(message: types.Message):
    await message.answer(text='Введите Телеграм ID. \nТолько цифры.\n'
                              'Если вы не знаете телеграм id. '
                              'Попросите инвестора зарегистрироваться и прислать вам заявку.', reply_markup=back_reply)
    await Admin_Form.manual_input.set()


# Phone input callback
@dp.message_handler(Text(equals='⬅️ Назад', ignore_case=True), state=Admin_Form.surname_input)
@dp.message_handler(state=Admin_Form.manual_input)
async def start_menu(message: types.Message):
    telegram_id = int(workWF.read_admin())
    if message.text.isdigit() or message.text == '⬅️ Назад':
        await message.answer(text="Введите полный мобильный телефон пользователя \n"
                                  "пример: +7123456789", reply_markup=back_reply)
        if message.text.isdigit():
            sqLite.insert_info(table_name='users', name=f'data', date=f'{str(message.text)}', telegram_id=telegram_id)
            sqLite.insert_first_note(telegram_id=message.text)
        else:
            pass
        await Admin_Form.phone_input.set()
    else:
        await message.answer(text='Введите только цифры.', reply_markup=back_reply)


# Surname input
@dp.message_handler(Text(equals='⬅️ Назад', ignore_case=True), state=Admin_Form.telegram_id_input)
@dp.message_handler(state=Admin_Form.phone_input)
async def start_menu(message: types.Message):
    user_id = sqLite.read_value_bu_name(name='data', table='users', telegram_id=int(workWF.read_admin()))[0]
    sqLite.insert_info(table_name='users', name=f'phone_number', date=f'{str(message.text)}', telegram_id=int(user_id))
    await message.answer(text='Введите Фамилию.', reply_markup=back_reply)
    await Admin_Form.surname_input.set()


# Name input
@dp.message_handler(state=Admin_Form.surname_input)
async def start_menu(message: types.Message):
    user_id = sqLite.read_value_bu_name(name='data', table='users', telegram_id=int(workWF.read_admin()))[0]
    sqLite.insert_info(table_name='users', name=f'surname', date=f'{str(message.text)}', telegram_id=int(user_id))
    await message.answer(text='Введите Имя.', reply_markup=back_reply)
    await Admin_Form.telegram_id_input.set()


# Pick a type of person
@dp.message_handler(Text(equals='⬅️ Назад', ignore_case=True), state=Admin_Form.set_balance_investor)
@dp.message_handler(state=Admin_Form.telegram_id_input)
async def start_menu(message: types.Message):
    user_id = sqLite.read_value_bu_name(name='data', table='users', telegram_id=int(workWF.read_admin()))[0]
    sqLite.insert_info(table_name='users', name=f'name', date=f'{str(message.text)}', telegram_id=int(user_id))
    await message.answer(text='Вы добавляете нового рабочего или инвестора?', reply_markup=add_person_reply)
    await Admin_Form.type_input.set()


# Add a New worker
@dp.message_handler(Text(equals='🛠 Рабочий', ignore_case=True), state=Admin_Form.type_input)
async def start_menu(message: types.Message):
    user_id = sqLite.read_value_bu_name(name='data', table='users', telegram_id=int(workWF.read_admin()))[0]
    sqLite.insert_info(table_name='users', name=f'user_type', date=f'worker', telegram_id=int(user_id))
    await message.answer(text='Данные сохранены.', reply_markup=types.ReplyKeyboardRemove())
    try:
        await bot.send_message(chat_id=user_id, text='Поздравляю администратор добавил вас в базу. '
                                                     'Вы зарегистрированы как новый рабочий. '
                                                     'Для того что бы зайти в бота нажмите /start ')
    except:
        await message.answer(text='Телеграм ID неверен либо пользователь не подписон на бот')
    await message.answer(text=f'Добрый день. Администратор чем тебе помочь', reply_markup=start_admin_kb)
    await Admin_Form.admin_first_menu.set()


# Set balance of investor
@dp.message_handler(Text(equals='⬅️ Назад', ignore_case=True), state=Admin_Form.set_pool_number)
@dp.message_handler(Text(equals='💵 Инвестор', ignore_case=True), state=Admin_Form.type_input)
async def start_menu(message: types.Message):
    user_id = sqLite.read_value_bu_name(name='data', table='users', telegram_id=int(workWF.read_admin()))[0]
    sqLite.insert_info(table_name='users', name=f'user_type', date=f'investor', telegram_id=int(user_id))
    await message.answer(text='Задайте баланс инвестора в RUR. \nТолько цифры.', reply_markup=back_reply)
    await Admin_Form.set_balance_investor.set()


# Set balance of investor
@dp.message_handler(state=Admin_Form.set_balance_investor)
async def start_menu(message: types.Message):
    user_id = sqLite.read_value_bu_name(name='data', table='users', telegram_id=int(workWF.read_admin()))[0]

    if message.text.isdigit():
        await message.answer(text=f'Данные сохранены.', reply_markup=types.ReplyKeyboardRemove())
        try:
            await bot.send_message(chat_id=user_id,
                                   text='Поздравляю администратор добавил вас в базу. '
                                        'Для того что бы зайти в бота нажмите /start',
                                   reply_markup=types.ReplyKeyboardRemove())
        except:
            await message.answer(text="Телеграм ID не верный либо человек отписался от бота")
        await message.answer(text=f'Добрый день. Администратор чем тебе помочь', reply_markup=start_admin_kb)
        await Admin_Form.admin_first_menu.set()
        sqLite.insert_info(table_name='users', name=f'balance', date=f'{str(message.text)}', telegram_id=int(user_id))
    else:
        await message.answer(text='Введите только цифры')


# Telegram_ID input phone
@dp.callback_query_handler(state=Admin_Form.name_input, text='input')
async def phone(call: types.CallbackQuery):
    await call.message.answer(text='Полный мобильный телефон пользователя \nпример: +7123456789',
                              reply_markup=back_reply)
    await Admin_Form.phone_input_search.set()


# Telegram_ID input phone
@dp.message_handler(state=Admin_Form.phone_input_search)
async def phone(message: types.Message):
    try:
        user_id = int(sqLite.read_values_in_db_by_phone(table='users', name='phone_number', data=message.text)[0])
        sqLite.insert_info(table_name='users', name=f'data', date=f'{user_id}', telegram_id=int(workWF.read_admin()))
        await message.answer(text='Вы добавляете нового рабочего или инвестора?',
                             reply_markup=add_person_reply)
        await Admin_Form.type_input.set()
    except:
        await message.answer(text='Данного номера нет в базе данных')
