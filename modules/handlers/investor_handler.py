from aiogram import types
from main import dp
from modules import sqLite, workWF
from modules.dispatcher import bot, Investor
from modules.keyboards import back_kb, yes_send_msg_kb, investor_first_kb
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


# Start menu investor Callback
@dp.callback_query_handler(state=Investor.investor_start, text='send_msg_for_admin')
async def add_person_start(call: types.CallbackQuery):
    await call.message.edit_text(text="Введите текст сообщения.", reply_markup=back_kb)
    await Investor.send_msg.set()


# Menu investor send msg
@dp.message_handler(state=Investor.send_msg)
async def add_person_start(message: types.Message):
    await message.answer(text="Ваше сообщение")
    await message.answer(text=message.text, reply_markup=yes_send_msg_kb)
    sqLite.insert_info(table_name='users', name=f'data', date=f'{message.text}', telegram_id=message.from_user.id)
    await Investor.msg_realy_send.set()


# Menu investor send msg
@dp.callback_query_handler(state=Investor.msg_realy_send)
async def add_person_start(call: types.CallbackQuery):
    admin_id = workWF.read_admin()
    invr = sqLite.read_value_bu_name(name='*', table='users', telegram_id=call.from_user.id)
    text = sqLite.read_value_bu_name(name='data', table='users', telegram_id=call.from_user.id)[0]
    await bot.send_message(chat_id=admin_id, text=f'Вам сообщение от <b>{invr[2]} {invr[3]}</b> \n\n{text}',
                           parse_mode='html')
    await call.message.answer('Ваше сообщение отправлено')
    await call.message.answer(text=f'Добрый день. <b>{invr[2]} {invr[3]}</b> ваш баланс сейчас составляет: '
                                   f'<b>{invr[6]}RUR</b>', parse_mode='html', reply_markup=investor_first_kb)
    await Investor.investor_start.set()


# Start menu find all fish
@dp.callback_query_handler(state=Investor.investor_start, text='see_my_fish')
async def add_person_start(call: types.CallbackQuery):
    tg_id = call.from_user.id
    pools = sqLite.read_all_value_bu_name(name='oners', table='pools')
    number = 0
    for i in range(0, len(pools)):
        if str(tg_id) in str(pools[i]):
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
                    size_fish = sqLite.read_values_in_db_by_phone(table='pools', name='number',
                                                                  data=int(pool_number))[5]
                    interest = int(int(fish_mass) * 100 / int(all_fish))
                    await call.message.answer(f'Бассейн - <b>№{pool_number}</b>\n'
                                              f'Начальное количество рыбы - <b>{fish_mass} кг</b>\n'
                                              f'ID рыбы - <b>{fish_id} </b>\n'
                                              f'Процент от всей рыбы в бассейне <b>{interest} %</b>\n'
                                              f'Контрольный размер одной рыбы <b>{size_fish} кг</b>', parse_mode='html')
                    number += 1
                else:
                    pass
    if number == 0:
        await call.message.answer('У вас пока нету рыбы в бассейне')
    investor = sqLite.read_value_bu_name(name='*', table='users', telegram_id=tg_id)
    await call.message.answer(text=f'Добрый день. <b>{investor[2]} {investor[3]}</b> ваш баланс сейчас составляет: '
                                   f'<b>{investor[6]}RUR</b>', parse_mode='html', reply_markup=investor_first_kb)
    await Investor.investor_start.set()


# Check my fish in journal
@dp.callback_query_handler(state=Investor.investor_start, text='live_journal')
async def add_person_start(call: types.CallbackQuery):
    tg_id = call.from_user.id
    pools = sqLite.read_all_value_bu_name(name='oners', table='pools')
    date_keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    for i in range(0, len(pools)):
        if str(tg_id) in str(pools[i]):
            pool_number = str(i + 1)
            position = str(pools[i][0]).split('TgID')
            for k in range(len(position) - 1):
                if str(tg_id) == str(position[k]):
                    fish_id = sqLite.read_values_in_db_by_phone(table='pools', name='number',
                                                                data=int(pool_number))[2]
                    fish_id = str(fish_id).split('ID')[k]
                    k = KeyboardButton(f'Рыба с ID №{str(fish_id)}, бассейн №{pool_number}')
                    date_keyboard.add(k)
    await call.message.answer(text="Перед вами ID всех ваших действующих сделок по рыбе.\n"
                                   "Выберите ID рыбы журнал событий которого вы хотите посмотреть",
                              reply_markup=date_keyboard)
    await Investor.journal.set()


# Menu investor check fish in journal by ID
@dp.message_handler(state=Investor.journal)
async def add_person_start(message: types.Message):
    fish_id = str(message.text.split('№')[1])[:-10]
    pool_id = str(message.text.split('№')[2])[-10:]
    tg_id = message.from_user.id
    sqLite.insert_info(table_name='users', telegram_id=tg_id, name='data', date=fish_id)
    sqLite.insert_info(table_name='users', telegram_id=tg_id, name='data_2', date=pool_id)
    data = sqLite.read_all_value_bu_name(name='*', table=f'pool{str(pool_id)}')
    date_keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    month = ''
    for i in range(0, len(data)):
        fish_id_in_bd = data[i][3]
        if str(fish_id) in str(fish_id_in_bd):
            line_month = str(data[i][5]).split(' ')[0][:-3]
            if str(line_month) in str(month):
                pass
            else:
                month = month + line_month + ' '
                i = KeyboardButton(line_month)
                date_keyboard.add(i)
    await message.answer(text='Выберите месяц за который хотите просмотреть все записи', reply_markup=date_keyboard)
    await Investor.journal_pick_month.set()


# Show investor journal by fish ID in one month
@dp.message_handler(state=Investor.journal_pick_month)
async def add_person_start(message: types.Message):
    tg_id = message.from_user.id
    fish_id = sqLite.read_value_bu_name(name='data', table='users', telegram_id=tg_id)[0]
    pool_id = sqLite.read_value_bu_name(name='data_2', table='users', telegram_id=tg_id)[0]
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
                    await message.answer(text=f'Вашу рыбку с ID - <b>{str(data[i][3])}</b> покормили. На эту ушло'
                                              f'<b>{str(data[i][1])} кг</b> корма. '
                                              f'Дата записи - <b>{str(data[i][5]).split(".")[0]}</b>',
                                         parse_mode='html', reply_markup=types.ReplyKeyboardRemove())
                elif line_type == 'size_fish':
                    await message.answer(text=f'Вашу рыбку с ID - <b>{str(data[i][3])}</b> измеряли. Ее вес составил'
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
                        text=f"Запись не определена -{line_type}- Дата и время записи - {str(data[i][5]).split('.')[0]}"
                        , reply_markup=types.ReplyKeyboardRemove())
    investor = sqLite.read_value_bu_name(name='*', table='users', telegram_id=tg_id)
    await message.answer(text=f'Добрый день. <b>{investor[2]} {investor[3]}</b> ваш баланс сейчас составляет: '
                              f'<b>{investor[6]}RUR</b>', parse_mode='html', reply_markup=investor_first_kb)
    await Investor.investor_start.set()
