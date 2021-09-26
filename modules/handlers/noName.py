from aiogram import types
from main import dp
from modules import sqLite
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext
from modules.dispatcher import bot, NoName
from modules.keyboards import send_contact_kb


# Start menu noName Callback
@dp.callback_query_handler(state=NoName.noname_start, text='call_admin')
async def add_person_start(call: types.CallbackQuery):
    await call.message.edit_text(text="Введите вашу фамилию.")
    await NoName.noname_send_msg.set()


# Start menu noName Message
@dp.message_handler(Text(equals='⬅️ Назад', ignore_case=True), state=NoName.noname_surname)
async def add_person_start(message: types.Message):
    await message.answer(text="Введите вашу фамилию.", reply_markup=types.ReplyKeyboardRemove())
    await NoName.noname_send_msg.set()


# Start menu noName surName
@dp.message_handler(Text(equals='⬅️ Назад', ignore_case=True), state=NoName.noname_contact)
@dp.message_handler(state=NoName.noname_send_msg)
async def add_person_start(message: types.Message):
    telegram_id = message.from_user.id
    data = sqLite.read_all_values_in_db(telegram_id)
    if data is None:
        sqLite.insert_first_note(telegram_id)
    else:
        pass
    sqLite.insert_info(table_name='users', name=f'surname', date=f'{str(message.text)}', telegram_id=telegram_id)
    await message.answer(text="Введите ваше имя.")
    await NoName.noname_surname.set()


# Start menu noName name
@dp.message_handler(state=NoName.noname_surname)
async def add_person_start(message: types.Message):
    sqLite.insert_info(table_name='users', name=f'name', date=f'{str(message.text)}',
                       telegram_id=message.from_user.id)
    await message.answer(text="Если хотите зарегистрироваться отправьте свои данные администратору.",
                         reply_markup=send_contact_kb)
    await NoName.noname_contact.set()


# Keep contact
@dp.message_handler(state=NoName.noname_contact, content_types=['contact'])
async def contact(message: types.Message, state: FSMContext):
    if message.contact is not None:
        phone_number = str(message.contact.phone_number)
        user_id = message.contact.user_id
        sqLite.insert_info(table_name='users', name=f'phone_number', date=f'{phone_number}',
                           telegram_id=user_id)
        data = sqLite.read_all_values_in_db(user_id)
        await bot.send_message(message.chat.id, 'Ваша заявка сформирована ждите сообщение от администратора.\n'
                                                'Для перехода на стартовую страницу нажмите /start')
        admins = sqLite.read_all_value_bu_name()
        for i in admins:
            if 'admin' in str(i[4]):
                try:
                    await bot.send_message(chat_id=int(i[0]), text=f'У вас новая заявка от <b>{data[2]} {data[3]}</b>\n'
                                                                   f'Вот его телефон и телеграм ID', parse_mode='html')
                    await bot.send_message(chat_id=int(i[0]), text=f'<b>{data[1]}</b>', parse_mode='html')
                    await bot.send_message(chat_id=int(i[0]), text=f'<b>{data[0]}</b>', parse_mode='html')
                except:
                    print(int(i[0]), 'Ошибка новой заявки')
            else:
                pass
        await state.finish()
    else:
        pass
