from aiogram import types
from main import dp
from aiogram.dispatcher.filters import Text
import logging
from aiogram.dispatcher import FSMContext
from modules import workWF, sqLite
from modules.keyboards import start_admin_kb, worker_first_kb, no_name_kb, investor_first_kb
from modules.dispatcher import start_Form, bot, Admin_Form, Admin_Worker, \
    Admin_Investor, Worker, Investor, NoName, Admin_Pool


# Start menu
@dp.message_handler(commands=['start'], state='*')
async def start_menu(message: types.Message):
    telegram_id = message.from_user.id
    try:
        admin_data = sqLite.read_value_bu_name(name='user_type', table='users', telegram_id=telegram_id)[0]
    except:
        admin_data = ' '
    if telegram_id == workWF.read_admin():
        admin_data = 'admin'
    if str(admin_data) == 'worker':
        await message.answer(text='Добрый день. Чем могу помочь?', reply_markup=worker_first_kb)

        await Worker.worker_start.set()
    elif str(admin_data) == 'investor':
        invr = sqLite.read_value_bu_name(name='*', table='users', telegram_id=telegram_id)
        await message.answer(text=f'Добрый день. <b>{invr[2]} {invr[3]}</b> ваш баланс сейчас составляет: '
                                  f'<b>{invr[6]}RUR</b>', parse_mode='html', reply_markup=investor_first_kb)
        await Investor.investor_start.set()
    elif 'admin' in str(admin_data):
        await message.answer(text=f'Добрый день. Администратор чем тебе помочь', reply_markup=start_admin_kb)
        await Admin_Form.admin_first_menu.set()
    else:
        await message.answer(text=' Привет. Это закрытый бот. Тебя нет в базе данных. Свяжись с администратором.',
                             reply_markup=no_name_kb)
        await NoName.noname_start.set()


# Start menu
@dp.callback_query_handler(state=Worker.confirm_send_photo, text='back')
@dp.callback_query_handler(state=Worker.size_fish_confirm, text='back')
@dp.callback_query_handler(state=Worker.feed_fish_confirm, text='back')
@dp.callback_query_handler(state=Admin_Pool.pool_start, text='back')
@dp.callback_query_handler(state=Investor.send_msg, text='back')
@dp.callback_query_handler(state=NoName.noname_send_msg, text='back')
@dp.callback_query_handler(state=Admin_Investor.admin_start_investor, text='back')
@dp.callback_query_handler(state=Admin_Form.name_input, text='back')
@dp.callback_query_handler(state=Admin_Worker.admin_all_worker, text='back')
async def start_menu(call: types.CallbackQuery):
    telegram_id = call.from_user.id
    admin_data = sqLite.read_value_bu_name(name='user_type', table='users', telegram_id=telegram_id)[0]
    if telegram_id == workWF.read_admin():
        admin_data = 'admin'
    if str(admin_data) == 'worker':
        await call.message.edit_text(text='Добрый день. Чем могу помочь?', reply_markup=worker_first_kb)
        await Worker.worker_start.set()
    elif str(admin_data) == 'investor':
        investor = sqLite.read_value_bu_name(name='*', table='users', telegram_id=telegram_id)
        await call.message.edit_text(text=f'Добрый день. <b>{investor[2]} {investor[3]}</b>'
                                          f' ваш баланс сейчас составляет: '
                                          f'<b>{investor[6]}RUR</b>', parse_mode='html', reply_markup=investor_first_kb)
        await Investor.investor_start.set()
    elif 'admin' in str(admin_data):
        await call.message.edit_text(text=f'Добрый день. Администратор чем тебе помочь', reply_markup=start_admin_kb)
        await Admin_Form.admin_first_menu.set()
    else:
        await call.message.edit_text(
            text=' Привет. Это закрытый бот. Тебя нет в базе данных. Свяжись с администратором.',
            reply_markup=no_name_kb)
        await NoName.noname_start.set()


# Help menu
@dp.message_handler(commands=['help'], state='*')
async def start_menu(message: types.Message):
    await message.answer(text='Привет! Ты попал в Телеграм бот рыбного хозяйства. Мы занемаемся выращиванием фарели. '
                              'Ты можешь попросить нас купить мальков фарели, а мы будем о ней заботится, кормить и '
                              'присылать тебе отчет.\n Вот основные функци бота:\n\n'
                              'Для перехода на стартовую страницу нажмите /start\n'
                              'Для отмены всех действий в любой момент нажмите /cancel')


# Cancel all process
@dp.message_handler(state='*', commands=['cancel'])
@dp.message_handler(Text(equals='cancel', ignore_case=True), state='*')
async def cancel_handler(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    await message.reply('Процес отменен. Все данные стерты. Что бы начать все с начала нажми /start',
                        reply_markup=types.ReplyKeyboardRemove())
    if current_state is None:
        return
    logging.info('Cancelling state %r', current_state)
    # Cancel state and inform user about it
    await state.finish()


# Start menu
@dp.message_handler(commands=['take_db'], state='*')
async def start_menu(message: types.Message):
    chat_id = message.from_user.id
    with open('modules/database.db', 'rb') as file:
        await bot.send_document(chat_id=chat_id, document=file, caption='Отправил')

    await start_Form.first_menu.set()


# Set admin
@dp.message_handler(commands=['setadmin'], state='*')
async def start_menu(message: types.Message):
    await message.answer('Для начала зарегистрируйте нового админа как рабочего. '
                         'Если новый админ уже в базе введите TG ID тового админа.\n'
                         'Для выхода /cancel')
    await start_Form.set_admin.set()


# Set admin
@dp.message_handler(state=start_Form.set_admin)
async def start_menu(message: types.Message):
    data = sqLite.read_value_bu_name(name='*', table='users', telegram_id=message.text)
    if data is not None:
        try:
            sqLite.insert_info(table_name='users', name='user_type', date='admin-worker', telegram_id=message.text)
            await message.answer("Данные сохранены. Нажми /start")
        except:
            await message.answer("Ошибка записи /start")
    else:
        await message.answer("Ошибка чтения из бд /start")
