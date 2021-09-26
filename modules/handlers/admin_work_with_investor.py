from aiogram import types
from main import dp
from modules import sqLite, workWF
from aiogram.dispatcher.filters import Text
from modules.dispatcher import bot, Admin_Form, Admin_Investor
from modules.keyboards import admin_investor, back_kb, confirm_kb, prices, change_prices, \
    send_msg_img, admin_msg_investor, yes_sen_msg_kb, search_investor, work_with_investors, change_inv_contact_kb
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
import datetime


# Start menu admin Callback
@dp.callback_query_handler(state=Admin_Investor.admin_confirm_delete_inv, text='back')
@dp.callback_query_handler(state=Admin_Investor.admin_set_services, text='back')
@dp.callback_query_handler(state=Admin_Investor.admin_set_new_balance, text='back')
@dp.callback_query_handler(state=Admin_Investor.msg_for_one_img, text='back')
@dp.callback_query_handler(state=Admin_Investor.admin_check_investors, text='back')
@dp.callback_query_handler(state=Admin_Investor.end_msg, text='back')
@dp.callback_query_handler(state=Admin_Investor.send_msg, text='back')
@dp.callback_query_handler(state=Admin_Form.admin_first_menu, text='client')
async def add_person_start(call: types.CallbackQuery):
    await call.message.edit_text(text="Здесь вы работаете с инвесторами", reply_markup=admin_investor)
    await Admin_Investor.admin_start_investor.set()


# Start menu admin send msg
@dp.callback_query_handler(state=Admin_Investor.msg_for_one, text='back')
@dp.callback_query_handler(state=Admin_Investor.write_msg_text, text='back')
@dp.callback_query_handler(state=Admin_Investor.send_msg_for_all, text='back')
@dp.callback_query_handler(state=Admin_Investor.admin_start_investor, text='send_message')
async def add_person_start(call: types.CallbackQuery):
    await call.message.edit_text(text="Кому вы хотите отправить сообщение?", reply_markup=admin_msg_investor)
    await Admin_Investor.send_msg.set()


# Send for all
@dp.callback_query_handler(state=Admin_Investor.write_msg_text, text='back')
@dp.callback_query_handler(state=Admin_Investor.send_msg, text='for_all')
async def add_person_start(call: types.CallbackQuery):
    await call.message.edit_text(text="Введите текст сообщения.", reply_markup=back_kb)
    await Admin_Investor.send_msg_for_all.set()


# Send for all
@dp.message_handler(Text(equals='⬅️ Назад', ignore_case=True), state=Admin_Investor.write_msg_text)
async def add_person_start(message: types.Message):
    await message.answer(text="Введите текст сообщения.", reply_markup=back_kb)
    await Admin_Investor.send_msg_for_all.set()


# Write a text of msg
@dp.message_handler(state=Admin_Investor.send_msg_for_all)
async def add_person_start(message: types.Message):
    sqLite.insert_info(table_name='users', name=f'data', date=f'{str(message.text)}',
                       telegram_id=int(workWF.read_admin()))
    await message.answer(text="Добавьте изображение.", reply_markup=send_msg_img)
    await Admin_Investor.write_msg_text.set()


# Yes send the msg without img
@dp.callback_query_handler(state=Admin_Investor.write_msg_text, text='without_img')
async def add_person_start(call: types.CallbackQuery):
    text = sqLite.read_value_bu_name(name='data', table='users', telegram_id=int(workWF.read_admin()))[0]
    await call.message.answer(text=f'{text}')
    await call.message.answer('Вы видите сообщение которое будет отправлено. Если все хорошо нажмите отправить.',
                              reply_markup=yes_sen_msg_kb)
    await Admin_Investor.send_msg_for_all_without_img.set()


# Yes send the msg without img
@dp.callback_query_handler(state=Admin_Investor.send_msg_for_all_without_img, text='yes_sen_msg')
async def add_person_start(call: types.CallbackQuery):
    all_users = sqLite.read_all_value_bu_name(name='*', table=f'users')
    text = sqLite.read_value_bu_name(name='data', table='users', telegram_id=int(workWF.read_admin()))[0]
    for i in range(0, len(all_users)):
        if 'investor' in all_users[i]:
            investor = all_users[i]
            user_id = int(investor[0])
            try:
                await bot.send_message(chat_id=user_id, text=f'{text}')
            except:
                print("Телеграм ID пользователя не действительный, либо пользователь не подписан на бота")
        else:
            pass
    await call.message.answer('Сообщение отправлено', reply_markup=types.ReplyKeyboardRemove())
    await call.message.edit_text(text="Здесь вы работаете с инвесторами", reply_markup=admin_investor)
    await Admin_Investor.admin_start_investor.set()


# Write a text of msg
@dp.message_handler(content_types=['photo'], state=Admin_Investor.write_msg_text)
async def photo_handler(message: types.Message):
    text = sqLite.read_value_bu_name(name='data', table='users', telegram_id=int(workWF.read_admin()))[0]
    await message.photo[-1].download(f'jpg/{str(message.from_user.id)}test.jpg')
    with open(f'jpg/{str(message.from_user.id)}test.jpg', 'rb') as photo:
        await bot.send_photo(chat_id=message.from_user.id, photo=photo, caption=f'{text}', )
    await message.answer('Вы видите сообщение которое будет отправлено. Если все хорошо нажмите отправить.',
                         reply_markup=yes_sen_msg_kb)
    photo.close()
    await Admin_Investor.send_photo_msg_text.set()


# Yes send the msg
@dp.callback_query_handler(state=Admin_Investor.send_photo_msg_text, text='yes_sen_msg')
async def add_person_start(call: types.CallbackQuery):
    all_users = sqLite.read_all_value_bu_name(name='*', table=f'users')
    for i in range(0, len(all_users)):
        if 'investor' in all_users[i]:
            investor = all_users[i]
            user_id = int(investor[0])
            try:
                text = sqLite.read_value_bu_name(name='data', table='users', telegram_id=int(workWF.read_admin()))[0]
                with open(f'jpg/{str(call.from_user.id)}test.jpg', 'rb') as photo:
                    await bot.send_photo(chat_id=user_id, photo=photo, caption=f'{text}')
                photo.close()
            except:
                print("Телеграм ID пользователя не действительный, либо пользователь не подписан на бота")
                photo.close()
        else:
            pass
    await call.message.answer('Сообщение отправлено', reply_markup=types.ReplyKeyboardRemove())
    await call.message.edit_text(text="Здесь вы работаете с инвесторами", reply_markup=admin_investor)
    await Admin_Investor.admin_start_investor.set()


# Send msg for one investor
@dp.callback_query_handler(state=Admin_Investor.msg_for_one_without_img, text='back')
@dp.callback_query_handler(state=Admin_Investor.msg_for_one_by_name, text='back')
@dp.callback_query_handler(state=Admin_Investor.send_msg, text='for_one')
async def add_person_start(call: types.CallbackQuery):
    await call.message.edit_text(text="Выберите как найти человека", reply_markup=search_investor)
    await Admin_Investor.msg_for_one.set()


# Send msg for one investor
@dp.message_handler(Text(equals='⬅️ Назад', ignore_case=True), state=Admin_Investor.msg_for_one_by_name)
async def add_person_start(message: types.Message):
    await message.edit_text(text="Выберите как найти человека", reply_markup=search_investor)
    await Admin_Investor.msg_for_one.set()


# Send msg for one investor search by name
@dp.callback_query_handler(state=Admin_Investor.msg_for_one_photo, text='back')
@dp.callback_query_handler(state=Admin_Investor.write_msg_text, text='back')
@dp.callback_query_handler(state=Admin_Investor.msg_for_one, text='by_name')
async def add_person_start(call: types.CallbackQuery):
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
    await call.message.answer(text="Выберите кому хотите отправить данные", reply_markup=date_keyboard)
    await Admin_Investor.msg_for_one_by_name.set()


# Send msg for one investor search by name
@dp.callback_query_handler(state=Admin_Investor.msg_for_one, text='search_poll_number')
async def add_person_start(call: types.CallbackQuery):
    date_keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    all_users = sqLite.read_all_value_bu_name(name='*', table=f'pools')
    for i in range(len(all_users)):
        show_data = f'Бассейн №{str(i + 1)}'
        i = KeyboardButton(show_data)
        date_keyboard.insert(i)
    await call.message.answer(text="Выберите бассейн в рыба в котором принадлежит инвестору",
                              reply_markup=date_keyboard)
    await Admin_Investor.msg_for_one_by_pool.set()


# Start menu admin reply
@dp.message_handler(state=Admin_Investor.msg_for_one_by_pool)
async def add_person_start(message: types.Message):
    if ' №' in str(message.text):
        date_keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        input_data = str(message.text).split('№')[1]
        users_tg_id = sqLite.read_values_in_db_by_phone(table='pools', name='number', data=str(input_data))[1]
        input_data = str(users_tg_id).split('TgID')
        for i in range(len(input_data) - 1):
            user_id = str(input_data[i])
            investor_name = sqLite.read_values_in_db_by_phone(name='telegram_id', table='users', data=int(user_id))[2]
            investor_surname = sqLite.read_value_bu_name(name='surname', table='users', telegram_id=int(user_id))[0]
            show_data = f'{investor_name} {investor_surname} TgID {input_data[i]}'
            i = KeyboardButton(show_data)
            date_keyboard.insert(i)
        await message.answer(text=f"Выберите инвестора который владеет рыбой в этом бассейне",
                             reply_markup=date_keyboard)
        await Admin_Investor.msg_for_one_by_name.set()
    else:
        await message.answer(text="Нажмите кнопку ниже")


# Start menu admin reply
@dp.message_handler(state=Admin_Investor.msg_for_one_by_name)
async def add_person_start(message: types.Message):
    if 'TgID' in str(message.text):
        input_data = str(message.text).split('TgID ')[1]
        sqLite.insert_info(table_name='users', name=f'data', date=f'{input_data}', telegram_id=int(workWF.read_admin()))
        await message.answer(text=f"Введите текст сообщения")
        await Admin_Investor.msg_for_one_text.set()
    else:
        await message.answer(text="Нажмите кнопку ниже")


# Text from user
# Write a text of msg
@dp.message_handler(state=Admin_Investor.msg_for_one_text)
async def add_person_start(message: types.Message):
    sqLite.insert_info(table_name='users', name=f'data_2', date=f'{str(message.text)}',
                       telegram_id=message.from_user.id)
    await message.answer(text="Добавьте изображение.", reply_markup=send_msg_img)
    await Admin_Investor.msg_for_one_img.set()


# Yes send the msg without img
@dp.callback_query_handler(state=Admin_Investor.msg_for_one_img, text='without_img')
async def add_person_start(call: types.CallbackQuery):
    text = sqLite.read_value_bu_name(name='data_2', table='users', telegram_id=int(workWF.read_admin()))[0]
    await call.message.answer(text=f'{text}')
    await call.message.answer('Вы видите сообщение которое будет отправлено. Если все хорошо нажмите отправить.',
                              reply_markup=yes_sen_msg_kb)
    await Admin_Investor.msg_for_one_without_img.set()


# Yes send the msg without img
@dp.callback_query_handler(state=Admin_Investor.msg_for_one_without_img, text='yes_sen_msg')
async def add_person_start(call: types.CallbackQuery):
    text = sqLite.read_value_bu_name(name='data_2', table='users', telegram_id=int(workWF.read_admin()))[0]
    user_id = sqLite.read_value_bu_name(name='data', table='users', telegram_id=int(workWF.read_admin()))[0]
    try:
        await bot.send_message(chat_id=user_id, text=f'{text}')
        await call.message.answer('Сообщение отправлено', reply_markup=types.ReplyKeyboardRemove())
    except:
        await call.message.answer('Телеграм ID пользователя не действительный, либо пользователь не подписан на бота')
    finally:
        await call.message.answer(text="Здесь вы работаете с инвесторами", reply_markup=admin_investor)
        await Admin_Investor.admin_start_investor.set()


# Write a text of msg
@dp.message_handler(content_types=['photo'], state=Admin_Investor.msg_for_one_img)
async def photo_handler(message: types.Message):
    text = sqLite.read_value_bu_name(name='data_2', table='users', telegram_id=int(workWF.read_admin()))[0]
    await message.photo[-1].download(f'jpg/{str(message.from_user.id)}test.jpg')
    with open(f'jpg/{str(message.from_user.id)}test.jpg', 'rb') as photo:
        await bot.send_photo(chat_id=message.from_user.id, photo=photo, caption=f'{text}', )
    await message.answer('Вы видите сообщение которое будет отправлено. Если все хорошо нажмите отправить.',
                         reply_markup=yes_sen_msg_kb)
    photo.close()
    await Admin_Investor.msg_for_one_photo.set()


# Yes send the msg
@dp.callback_query_handler(state=Admin_Investor.msg_for_one_photo, text='yes_sen_msg')
async def add_person_start(call: types.CallbackQuery):
    user_id = sqLite.read_value_bu_name(name='data', table='users', telegram_id=int(workWF.read_admin()))[0]
    try:
        text = sqLite.read_value_bu_name(name='data_2', table='users', telegram_id=int(workWF.read_admin()))[0]
        with open(f'jpg/{str(call.from_user.id)}test.jpg', 'rb') as photo:
            await bot.send_photo(chat_id=int(user_id), photo=photo, caption=f'{text}')
        photo.close()
        await call.message.answer('Сообщение отправлено', reply_markup=types.ReplyKeyboardRemove())
    except:
        photo.close()
        await call.message.answer("Телеграм ID пользователя не действительный, либо пользователь не подписан на бота",
                                  reply_markup=types.ReplyKeyboardRemove())
    finally:
        await call.message.answer(text="Здесь вы работаете с инвесторами", reply_markup=admin_investor)
        await Admin_Investor.admin_start_investor.set()


# Check investors data
@dp.callback_query_handler(state=Admin_Investor.admin_work_investors, text='back')
@dp.callback_query_handler(state=Admin_Investor.admin_check_investors_name, text='back')
@dp.callback_query_handler(state=Admin_Investor.admin_start_investor, text='check_data')
async def add_person_start(call: types.CallbackQuery):
    await call.message.edit_text(text="Выберите как найти человека", reply_markup=search_investor)
    await Admin_Investor.admin_check_investors.set()


# Send msg for one investor search by name
@dp.callback_query_handler(state=Admin_Investor.admin_check_investors, text='search_poll_number')
async def add_person_start(call: types.CallbackQuery):
    date_keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    all_users = sqLite.read_all_value_bu_name(name='*', table=f'pools')
    for i in range(len(all_users)):
        show_data = f'Бассейн №{str(i + 1)}'
        i = KeyboardButton(show_data)
        date_keyboard.insert(i)
    await call.message.answer(text="Выберите бассейн рыба в котором принадлежит инвестору", reply_markup=date_keyboard)
    await Admin_Investor.admin_check_investors_pool.set()


# Start menu admin reply
@dp.message_handler(state=Admin_Investor.admin_check_investors_pool)
async def add_person_start(message: types.Message):
    if ' №' in str(message.text):
        date_keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        input_data = str(message.text).split('№')[1]
        users_tg_id = sqLite.read_values_in_db_by_phone(table='pools', name='number', data=str(input_data))[1]
        input_data = str(users_tg_id).split('TgID')
        for i in range(len(input_data) - 1):
            user_id = str(input_data[i])
            investor_name = sqLite.read_values_in_db_by_phone(name='telegram_id', table='users', data=int(user_id))[2]
            investor_surname = sqLite.read_value_bu_name(name='surname', table='users', telegram_id=int(user_id))[0]
            show_data = f'{investor_name} {investor_surname} TgID {input_data[i]}'
            i = KeyboardButton(show_data)
            date_keyboard.insert(i)
        await message.answer(text=f"Выберите инвестора который владеет рыбой в этом бассейне",
                             reply_markup=date_keyboard)
        await Admin_Investor.admin_check_investors_name.set()
    else:
        await message.answer(text="Нажмите кнопку ниже")


# Check investors by pool number
@dp.callback_query_handler(state=Admin_Investor.admin_sale_fish_id, text='back')
@dp.callback_query_handler(state=Admin_Investor.write_msg_text, text='back')
@dp.callback_query_handler(state=Admin_Investor.admin_check_investors, text='by_name')
async def add_person_start(call: types.CallbackQuery):
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
    await call.message.answer(text="Выберите инвестора", reply_markup=date_keyboard)
    await Admin_Investor.admin_check_investors_name.set()


# Input name and send data
@dp.message_handler(state=Admin_Investor.admin_check_investors_name)
async def photo_handler(message: types.Message):
    if 'TgID ' in message.text:
        tg_id = message.text.split('TgID ')[1]
        sqLite.insert_info(table_name='users', telegram_id=workWF.read_admin(), name='data', date=tg_id)
        pools = sqLite.read_all_value_bu_name(name='oners', table='pools')
        for i in range(0, len(pools)):
            if tg_id in str(pools[i]):
                pool_number = str(i + 1)
                position = str(pools[i][0]).split('TgID')
                for k in range(len(position) - 1):
                    if str(tg_id) == str(position[k]):
                        fish_mass = sqLite.read_values_in_db_by_phone(table='pools', name='number',
                                                                      data=int(pool_number))[3]
                        fish_mass = str(fish_mass).split('KG')[k]
                        fish_id = sqLite.read_values_in_db_by_phone(table='pools', name='number',
                                                                    data=int(pool_number))[2]
                        fish_id = str(fish_id).split('ID')[k]
                        all_fish = sqLite.read_values_in_db_by_phone(table='pools', name='number',
                                                                     data=int(pool_number))[4]
                        interest = int(int(fish_mass) * 100 / int(all_fish))
                        await message.answer(f'Бассейн - <b>№{pool_number}</b>\n'
                                             f'Количество рыбы - <b>{fish_mass} кг</b>\n'
                                             f'ID рыбы - <b>{fish_id} </b>\n'
                                             f'Процент от всей рыбы в бассейне <b>{interest} %</b>', parse_mode='html')
        data_investor = sqLite.read_all_values_in_db(int(tg_id))
        await message.answer(f'Имя инвестора - <b>{data_investor[2]}</b>\n'
                             f'Фамилия инвестора - <b>{data_investor[3]}</b>\n'
                             f'Телефон инвестора - <b>{data_investor[1]}</b>\n'
                             f'Баланс - <b>{data_investor[6]} RUR</b>\n'
                             f'', parse_mode='html', reply_markup=work_with_investors)
    else:
        await message.answer('Нажмите кнопку')
    await Admin_Investor.admin_work_investors.set()


# Check investors by pool number
@dp.callback_query_handler(state=Admin_Investor.write_msg_text, text='back')
@dp.callback_query_handler(state=Admin_Investor.admin_work_investors, text='sale_fish')
async def add_person_start(call: types.CallbackQuery):
    await call.message.answer('Введите ID рыбы которую вы хотите продать.\n'
                              'Только цифры')
    await Admin_Investor.admin_work_investors_fish.set()


# Input name and send data
@dp.message_handler(state=Admin_Investor.admin_work_investors_fish)
async def photo_handler(message: types.Message):
    if message.text.isdigit():
        sqLite.insert_info(table_name='users', telegram_id=workWF.read_admin(), name='data_2', date=message.text)
        await message.answer('Введите сумму за которую продали рыбу в RUR')
    else:
        await message.answer('Введите только цифры')
    await Admin_Investor.admin_work_investors_money.set()


# Input name and send data
@dp.message_handler(state=Admin_Investor.admin_work_investors_money)
async def photo_handler(message: types.Message):
    if message.text.isdigit():
        sqLite.insert_info(table_name='users', telegram_id=workWF.read_admin(), name='fish_number', date=message.text)
        user_id = sqLite.read_value_bu_name(name='data_2', table='users', telegram_id=workWF.read_admin())[0]
        await message.answer(f'Вы точно хотите продать рыбу с ID <b>№{user_id}</b>\n'
                             f'За <b>{message.text} RUR</b>?', parse_mode='html', reply_markup=confirm_kb)
    else:
        await message.answer('Введите только цифры')
    await Admin_Investor.admin_sale_fish_id.set()


# Check investors by pool number
@dp.callback_query_handler(state=Admin_Investor.admin_sale_fish_id, text='yes_all_good')
async def add_person_start(call: types.CallbackQuery):
    fish_id = sqLite.read_value_bu_name(name='data_2', table='users', telegram_id=workWF.read_admin())[0]
    pools = sqLite.read_all_value_bu_name(name='fish_id', table='pools')
    money = sqLite.read_value_bu_name(name='fish_number', table='users', telegram_id=workWF.read_admin())[0]
    user_id = sqLite.read_value_bu_name(name='data', table='users', telegram_id=workWF.read_admin())[0]
    user_money = sqLite.read_value_bu_name(name='balance', table='users', telegram_id=int(user_id))[0]
    user_money = float(float(user_money) + float(money))
    sqLite.insert_info(table_name='users', telegram_id=int(user_id), name='balance', date=user_money)
    for i in range(0, len(pools)):

        position = str(pools[i][0]).split('ID')

        if f'{str(fish_id)}ID' in str(pools[i]):
            oners = ''
            fish_id_base = ''
            start_fish_mass = ''
            for k in range(0, (len(position) - 1)):
                if int(position[k]) == int(fish_id):
                    data = sqLite.read_values_in_db_by_phone(table='pools', name='number', data=int(i + 1))
                    fish_little_mass = str(data[3]).split('KG')[k]
                    investor_id = str(data[1]).split('TgID')[k]
                    fish_mass = int(data[4]) - int(fish_little_mass)
                    sqLite.insert_info_pool(name='fish_mass', date=fish_mass, number=int(i + 1))
                    sqLite.insert_pool_db1(telegram_id=user_id,
                                           food_mass=money,
                                           fish_mass=fish_little_mass,
                                           fish_id=fish_id,
                                           number=int(i + 1),
                                           data=datetime.datetime.now(),
                                           type='admin_sell_fish')
                    try:
                        await bot.send_message(chat_id=investor_id, text=f'Администратор продал вашу рыбу с '
                                                                         f'ID {fish_id}, за {money} RUR')
                    except:
                        print(investor_id, f'продажа рыбы по ID {fish_id}')
                else:
                    data = sqLite.read_values_in_db_by_phone(table='pools', name='number', data=str(i + 1))
                    oners = oners + str(data[1]).split('TgID')[k] + 'TgID'
                    fish_id_base = fish_id_base + str(data[2]).split('ID')[k] + 'ID'
                    start_fish_mass = start_fish_mass + str(data[3]).split('KG')[k] + 'KG'
            sqLite.insert_info_pool(name='oners', date=oners, number=(i + 1))
            sqLite.insert_info_pool(name='fish_id', date=fish_id_base, number=(i + 1))
            sqLite.insert_info_pool(name='start_fish_mass', date=start_fish_mass, number=(i + 1))

        else:
            pass

    await call.message.answer('Рыба продана', reply_markup=types.ReplyKeyboardRemove())
    await call.message.answer(text="Здесь вы работаете с инвесторами", reply_markup=admin_investor)
    await Admin_Investor.admin_start_investor.set()


# Set new balance
@dp.callback_query_handler(state=Admin_Investor.admin_work_investors, text='balance_change')
async def add_person_start(call: types.CallbackQuery):
    await call.message.answer('Введите новый баланс в RUR')
    await Admin_Investor.admin_set_new_balance.set()


# Set new balance
@dp.message_handler(state=Admin_Investor.admin_set_new_balance)
async def photo_handler(message: types.Message):
    if message.text.isdigit():
        user_id = sqLite.read_value_bu_name(name='data', table='users', telegram_id=workWF.read_admin())[0]
        user_money = sqLite.read_value_bu_name(name='balance', table='users', telegram_id=int(user_id))[0]
        name = sqLite.read_value_bu_name(name='name', table='users', telegram_id=int(user_id))[0]
        surname = sqLite.read_value_bu_name(name='surname', table='users', telegram_id=int(user_id))[0]
        sqLite.insert_info(table_name='users', telegram_id=workWF.read_admin(), name='data_2', date=message.text)
        await message.answer(f'Старый баланс инвестора <b>{surname} {name}</b>\n'
                             f'Составляет <b>{user_money} RUR</b>\n'
                             f'Вы уверены что хотите установить новый баланс <b>{message.text}</b>?',
                             parse_mode='html', reply_markup=confirm_kb)
    else:
        await message.answer('Введите только цифры')
    await Admin_Investor.admin_set_new_balance.set()


# Set new balance
@dp.callback_query_handler(state=Admin_Investor.admin_set_new_balance, text='yes_all_good')
async def add_person_start(call: types.CallbackQuery):
    user_money = sqLite.read_value_bu_name(name='data_2', table='users', telegram_id=workWF.read_admin())[0]
    user_id = sqLite.read_value_bu_name(name='data', table='users', telegram_id=workWF.read_admin())[0]
    try:
        await bot.send_message(chat_id=user_id, text=f'Ваш баланс был пополнен и составляет на данный момент '
                                                     f'<b>{user_money} RUR</b>', parse_mode='html')
    except:
        await call.message.answer('Телеграмм ID не действительный, либо пользователь не подписан на бот.')
    sqLite.insert_info(table_name='users', telegram_id=int(user_id), name='balance', date=user_money)
    await call.message.answer('Данные сохранены', reply_markup=types.ReplyKeyboardRemove())
    await call.message.answer(text="Здесь вы работаете с инвесторами", reply_markup=admin_investor)
    await Admin_Investor.admin_start_investor.set()


# Изменить тариф
@dp.callback_query_handler(state=Admin_Investor.admin_confirm_change_price, text='back')
@dp.callback_query_handler(state=Admin_Investor.admin_change_price, text='back')
@dp.callback_query_handler(state=Admin_Investor.admin_food_services, text='back')
@dp.callback_query_handler(state=Admin_Investor.admin_start_investor, text='set_tax')
async def add_person_start(call: types.CallbackQuery):
    await call.message.edit_text(text="Выберите какой тариф", reply_markup=prices)
    await Admin_Investor.admin_set_services.set()


# Food price
@dp.callback_query_handler(state=Admin_Investor.admin_set_services, text='food_price')
async def add_person_start(call: types.CallbackQuery):
    price = sqLite.read_value_bu_name(name='food_price', table='users', telegram_id=workWF.read_admin())[0]
    sqLite.insert_info(table_name='users', telegram_id=workWF.read_admin(), name='data', date='food_price')
    await call.message.edit_text(text=f"Тариф на корм рыбы сейчас <b>{price} RUR</b> за 1кг",
                                 reply_markup=change_prices, parse_mode='html')
    await Admin_Investor.admin_food_services.set()


# Services price
@dp.callback_query_handler(state=Admin_Investor.admin_set_services, text='service_price')
async def add_person_start(call: types.CallbackQuery):
    price = sqLite.read_value_bu_name(name='price_of_service', table='users', telegram_id=workWF.read_admin())[0]
    sqLite.insert_info(table_name='users', telegram_id=workWF.read_admin(), name='data', date='price_of_service')
    await call.message.edit_text(text=f"Тариф на обслуживание сейчас <b>{price} RUR</b> за бассейн",
                                 reply_markup=change_prices, parse_mode='html')
    await Admin_Investor.admin_food_services.set()


# Fish price
@dp.callback_query_handler(state=Admin_Investor.admin_set_services, text='fish_price')
async def add_person_start(call: types.CallbackQuery):
    price = sqLite.read_value_bu_name(name='fish_price', table='users', telegram_id=workWF.read_admin())[0]
    sqLite.insert_info(table_name='users', telegram_id=workWF.read_admin(), name='data', date='fish_price')
    await call.message.edit_text(text=f"Стоимость рыбы сейчас <b>{price} RUR</b> за 1кг",
                                 reply_markup=change_prices, parse_mode='html')
    await Admin_Investor.admin_food_services.set()


# Change price
@dp.callback_query_handler(state=Admin_Investor.admin_food_services, text='change_price')
async def add_person_start(call: types.CallbackQuery):
    await call.message.edit_text(text=f"Введите сумму тарифа в RUR")
    await Admin_Investor.admin_change_price.set()


# Change price
@dp.message_handler(state=Admin_Investor.admin_change_price)
async def add_person_start(message: types.Message):
    if message.text.isdigit():
        type_price = sqLite.read_value_bu_name(name='data', table='users', telegram_id=workWF.read_admin())[0]
        text = 'blank'
        if type_price == 'food_price':
            text = 'корм рыбы'
        elif type_price == 'price_of_service':
            text = 'обслуживание'
        elif type_price == 'fish_price':
            text = 'стоимость рыбы'
        sqLite.insert_info(table_name='users', telegram_id=workWF.read_admin(), name='data_2',
                           date=message.text)
        await message.answer(text=f"Вы точно хотите установить тариф на {text} "
                                  f"равный <b>{message.text} RUR</b>", parse_mode='html', reply_markup=confirm_kb)
        await Admin_Investor.admin_confirm_change_price.set()
    else:
        await message.answer(text=f"Введите только цифры")


# Change price confirm
@dp.callback_query_handler(state=Admin_Investor.admin_confirm_change_price, text='yes_all_good')
async def add_person_start(call: types.CallbackQuery):
    type_price = sqLite.read_value_bu_name(name='data', table='users', telegram_id=workWF.read_admin())[0]
    price = sqLite.read_value_bu_name(name='data_2', table='users', telegram_id=workWF.read_admin())[0]
    sqLite.insert_info(table_name='users', telegram_id=workWF.read_admin(), name=type_price,
                       date=price)
    await call.message.answer('Данные сохранены', reply_markup=types.ReplyKeyboardRemove())
    await call.message.answer(text="Здесь вы работаете с инвесторами", reply_markup=admin_investor)
    await Admin_Investor.admin_start_investor.set()


# Dell investor
@dp.callback_query_handler(state=Admin_Investor.admin_work_investors, text='delete_investor')
async def add_person_start(call: types.CallbackQuery):
    user_id = sqLite.read_value_bu_name(name='data', table='users', telegram_id=workWF.read_admin())[0]
    data = sqLite.read_value_bu_name(name='*', table='users', telegram_id=int(user_id))
    await call.message.answer(f'Вы точно хотите удалить все данные об инвесторе <b>{data[2]} {data[3]}</b>,'
                              f' и удалить всю его рыбу из БД', reply_markup=confirm_kb, parse_mode='html')
    await Admin_Investor.admin_confirm_delete_inv.set()


# Dell investor
@dp.callback_query_handler(state=Admin_Investor.admin_confirm_delete_inv, text='yes_all_good')
async def add_person_start(call: types.CallbackQuery):
    user_id = sqLite.read_value_bu_name(name='data', table='users', telegram_id=workWF.read_admin())[0]
    pools = sqLite.read_all_value_bu_name(name='*', table=f'pools')

    for i in range(0, len(pools)):
        line = pools[i]
        oners = ''
        fish_id = ''
        start_fish_mass = ''
        fish_mass = ''
        if str(user_id) in str(line[1]):
            one_id = str(line[1]).split('TgID')
            one_fish_id = str(line[2]).split('ID')
            one_fish_mass = str(line[3]).split('KG')

            for k in range(0, len(one_id) - 1):
                if str(one_id[k]) == str(user_id):
                    inv_fish_mass_delete = int(one_fish_mass[k])
                    fish_mass = int(int(pools[i][4]) - inv_fish_mass_delete)
                else:
                    oners = oners + str(one_id[k]) + 'TgID'
                    fish_id = fish_id + str(one_fish_id[k]) + 'ID'
                    start_fish_mass = start_fish_mass + str(one_fish_mass[k]) + 'KG'
        else:
            pass
        sqLite.insert_info_pool(number=int(i + 1), name='oners', date=oners)
        sqLite.insert_info_pool(number=int(i + 1), name='fish_id', date=fish_id)
        sqLite.insert_info_pool(number=int(i + 1), name='start_fish_mass', date=start_fish_mass)
        sqLite.insert_info_pool(number=int(i + 1), name='fish_mass', date=fish_mass)
    sqLite.delete_str(table='users', name='telegram_id', data=int(user_id))
    await call.message.answer('Данные удалены', reply_markup=types.ReplyKeyboardRemove())
    await call.message.answer(text="Здесь вы работаете с инвесторами", reply_markup=admin_investor)
    await Admin_Investor.admin_start_investor.set()


# Change investors data
@dp.callback_query_handler(state=Admin_Investor.confirm_surname, text='back')
@dp.callback_query_handler(state=Admin_Investor.confirm_correct_name, text='back')
@dp.callback_query_handler(state=Admin_Investor.confirm_correct_phone, text='back')
@dp.callback_query_handler(state=Admin_Investor.admin_work_investors, text='correct')
async def add_person_start(call: types.CallbackQuery):
    await call.message.answer(text='Выберите что изменить', reply_markup=change_inv_contact_kb)
    await Admin_Investor.correct_inv.set()


# Phone input callback
@dp.message_handler(state=Admin_Investor.correct_inv)
async def start_menu(message: types.Message):
    if message.text == '📞 Телефон':
        await message.answer('Введите новый телефонный номер \n'
                             'пример: +7123456789')
        await Admin_Investor.correct_phone.set()
    elif message.text == 'Имя':
        sqLite.insert_info(table_name='users', name=f'data_2', date=f'telegram_id', telegram_id=workWF.read_admin())
        await message.answer('Введите новое Имя')
        await Admin_Investor.correct_name.set()
    elif message.text == 'Фамилия':
        sqLite.insert_info(table_name='users', name=f'data_2', date=f'activ', telegram_id=workWF.read_admin())
        await message.answer('Выберите новую фамилию')
        await Admin_Investor.correct_surname.set()
    else:
        await message.answer(text='Нажмите кнопку')


# Phone input
@dp.message_handler(state=Admin_Investor.correct_phone)
async def start_menu(message: types.Message):
    sqLite.insert_info(table_name='users', name=f'data_2', date=message.text, telegram_id=workWF.read_admin())
    user_id = sqLite.read_value_bu_name(name='data', table='users', telegram_id=workWF.read_admin())[0]
    old_phone = sqLite.read_value_bu_name(name='phone_number', table='users', telegram_id=int(user_id))[0]
    name = sqLite.read_value_bu_name(name='name', table='users', telegram_id=int(user_id))[0]
    surname = sqLite.read_value_bu_name(name='surname', table='users', telegram_id=int(user_id))[0]
    await message.answer(text=f'Вы уверены что хотите заменить телефонный номер <b>{old_phone}</b> у рабочего\n'
                              f'<b>{name} {surname}</b> на новый телефонный номер <b>{message.text}</b>',
                         reply_markup=confirm_kb, parse_mode='html')
    await Admin_Investor.confirm_correct_phone.set()


# Confirm new phone
@dp.callback_query_handler(state=Admin_Investor.confirm_correct_phone, text='yes_all_good')
async def add_person_start(call: types.CallbackQuery):
    user_id = sqLite.read_value_bu_name(name='data', table='users', telegram_id=workWF.read_admin())[0]
    phone_numb = sqLite.read_value_bu_name(name='data_2', table='users', telegram_id=workWF.read_admin())[0]
    sqLite.insert_info(table_name='users', name=f'phone_number', date=phone_numb, telegram_id=int(user_id))
    await call.message.answer(text='Данные сохранены', reply_markup=types.ReplyKeyboardRemove())
    await call.message.edit_text(text="Здесь вы работаете с инвесторами", reply_markup=admin_investor)
    await Admin_Investor.admin_start_investor.set()


# Tg ID input
@dp.message_handler(state=Admin_Investor.correct_name)
async def start_menu(message: types.Message):
    sqLite.insert_info(table_name='users', name=f'data_2', date=message.text, telegram_id=workWF.read_admin())
    user_id = sqLite.read_value_bu_name(name='data', table='users', telegram_id=workWF.read_admin())[0]
    name = sqLite.read_value_bu_name(name='name', table='users', telegram_id=int(user_id))[0]
    surname = sqLite.read_value_bu_name(name='surname', table='users', telegram_id=int(user_id))[0]
    await message.answer(text=f'Вы уверены что хотите заменить имя у рабочего '
                              f'<b>{name} {surname}</b> на новое имя <b>{message.text}</b>',
                         reply_markup=confirm_kb, parse_mode='html')
    await Admin_Investor.confirm_correct_name.set()


# Confirm new telegram id
@dp.callback_query_handler(state=Admin_Investor.confirm_correct_name, text='yes_all_good')
async def add_person_start(call: types.CallbackQuery):
    user_id = sqLite.read_value_bu_name(name='data', table='users', telegram_id=workWF.read_admin())[0]
    phone_numb = sqLite.read_value_bu_name(name='data_2', table='users', telegram_id=workWF.read_admin())[0]
    sqLite.insert_info(table_name='users', name=f'name', date=phone_numb, telegram_id=int(user_id))
    await call.message.answer(text='Данные сохранены', reply_markup=types.ReplyKeyboardRemove())
    await call.message.edit_text(text="Здесь вы работаете с инвесторами", reply_markup=admin_investor)
    await Admin_Investor.admin_start_investor.set()


# Status input
@dp.message_handler(state=Admin_Investor.correct_surname)
async def start_menu(message: types.Message):
    sqLite.insert_info(table_name='users', name=f'data_2', date=message.text, telegram_id=workWF.read_admin())
    user_id = sqLite.read_value_bu_name(name='data', table='users', telegram_id=workWF.read_admin())[0]
    name = sqLite.read_value_bu_name(name='name', table='users', telegram_id=int(user_id))[0]
    surname = sqLite.read_value_bu_name(name='surname', table='users', telegram_id=int(user_id))[0]
    await message.answer(text=f'Вы уверены что хотите заменить фамилию у рабочего '
                              f'<b>{name} {surname}</b> на новую фамилию <b>{message.text}</b>',
                         reply_markup=confirm_kb, parse_mode='html')
    await Admin_Investor.confirm_surname.set()


# Confirm new telegram id
@dp.callback_query_handler(state=Admin_Investor.confirm_surname, text='yes_all_good')
async def add_person_start(call: types.CallbackQuery):
    user_id = sqLite.read_value_bu_name(name='data', table='users', telegram_id=workWF.read_admin())[0]
    surname = sqLite.read_value_bu_name(name='data_2', table='users', telegram_id=workWF.read_admin())[0]
    sqLite.insert_info(table_name='users', name=f'surname', date=surname, telegram_id=int(user_id))
    await call.message.answer(text='Данные сохранены', reply_markup=types.ReplyKeyboardRemove())
    await call.message.edit_text(text="Здесь вы работаете с инвесторами", reply_markup=admin_investor)
    await Admin_Investor.admin_start_investor.set()
