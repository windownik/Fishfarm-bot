from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


back_reply_btn = KeyboardButton('⬅️ Назад')
send_contact_btn = KeyboardButton(text='Поделится своим контактом', request_contact=True)
back_reply = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(back_reply_btn)

send_contact_kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(send_contact_btn)
send_contact_kb.add(back_reply_btn)


# Стартовое меню
client = InlineKeyboardButton(text='Инвесторы', callback_data='client')
staff = InlineKeyboardButton(text='Рабочие', callback_data='staff')
add_person = InlineKeyboardButton(text='Добавить инвестора/рабочего', callback_data='add_person')
pool = InlineKeyboardButton(text='Бассейны', callback_data='pool')
db = InlineKeyboardButton(text='База данных', callback_data='db')


start_admin_kb = InlineKeyboardMarkup()
start_admin_kb.add(client, staff)
start_admin_kb.add(db, pool)
start_admin_kb.add(add_person)

# Стартовое меню администратора
person_msg = InlineKeyboardButton(text='Пользователь присылал запрос', callback_data='input')
hand_data = InlineKeyboardButton(text='Ввести все самому в ручную', callback_data='manual_input')
back_callBack = InlineKeyboardButton(text='Назад', callback_data='back')


admin_kb_start = InlineKeyboardMarkup()
admin_kb_start.add(person_msg)
admin_kb_start.add(hand_data)
admin_kb_start.add(back_callBack)

worker_add_reply = KeyboardButton('🛠 Рабочий')
investor_add_reply = KeyboardButton('💵 Инвестор')

add_person_reply = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(investor_add_reply)
add_person_reply.add(worker_add_reply)
add_person_reply.add(back_reply_btn)


# Клавиатура назад
back_kb = InlineKeyboardMarkup()
back_kb.add(back_callBack)


all_staff = InlineKeyboardButton(text='Просмотреть всех рабочих', callback_data='all_staff')
admin_worker = InlineKeyboardMarkup()
admin_worker.add(all_staff)
admin_worker.add(back_callBack)


# Клавиатура по рабочим
worker_kb_correct = InlineKeyboardButton(text='Изменить', callback_data='change')
worker_kb_magazine = InlineKeyboardButton(text='Журнал активности', callback_data='jornal')
worker_kb_delete = InlineKeyboardButton(text='Удалить', callback_data='delete')
worker_kb = InlineKeyboardMarkup()
worker_kb.add(worker_kb_magazine)
worker_kb.add(worker_kb_correct)
worker_kb.add(worker_kb_delete)
worker_kb.add(back_callBack)


# Работа с инвесторами
all_send_msg = InlineKeyboardButton(text='Отправить сообщение', callback_data='send_message')
check_all_investors = InlineKeyboardButton(text='Просмотреть данные инвесторов', callback_data='check_data')
set_tax = InlineKeyboardButton(text='Задать тариф', callback_data='set_tax')
admin_investor = InlineKeyboardMarkup()
admin_investor.add(all_send_msg)
admin_investor.add(check_all_investors)
admin_investor.add(set_tax)
admin_investor.add(back_callBack)


# Отправить сообщение
for_all = InlineKeyboardButton(text='Всем инвесторам', callback_data='for_all')
for_one = InlineKeyboardButton(text='Выбрать одного', callback_data='for_one')
admin_msg_investor = InlineKeyboardMarkup()
admin_msg_investor.add(for_all)
admin_msg_investor.add(for_one)
admin_msg_investor.add(back_callBack)


without_img = InlineKeyboardButton(text='Без изображения', callback_data='without_img')
send_msg_img = InlineKeyboardMarkup()
send_msg_img.add(without_img)
send_msg_img.add(back_callBack)

# Да отправить сообщение с фото
yes_sen_msg = InlineKeyboardButton(text='Да, отправить сообщение', callback_data='yes_sen_msg')
yes_sen_msg_kb = InlineKeyboardMarkup()
yes_sen_msg_kb.add(yes_sen_msg)
yes_sen_msg_kb.add(back_callBack)

# Выбор инвестора по бассейну и имени
btn_search_pool = InlineKeyboardButton(text='По номеру бассейна', callback_data='search_poll_number')
by_name_investor = InlineKeyboardButton(text='По имени', callback_data='by_name')
search_investor = InlineKeyboardMarkup()
search_investor.add(btn_search_pool)
search_investor.add(by_name_investor)
search_investor.add(back_callBack)


# Первоя клавиатура для рабочих
i_feed_fish = InlineKeyboardButton(text='Я покормил рыбу', callback_data='i_feed_fish')
send_photo_msg = InlineKeyboardButton(text='Отправить фотоотчет владельцу', callback_data='send_photo_msg')
send_text_msg = InlineKeyboardButton(text='Отправить отчет замеров', callback_data='send_text_msg')
worker_first_kb = InlineKeyboardMarkup()
worker_first_kb.add(i_feed_fish)
worker_first_kb.add(send_photo_msg)
worker_first_kb.add(send_text_msg)


# Первоя клавиатура для инвестора
see_my_fish = InlineKeyboardButton(text='Посмотреть рыбу', callback_data='see_my_fish')
send_msg_for_admin = InlineKeyboardButton(text='Отправить сообщение админу', callback_data='send_msg_for_admin')
live_jornal = InlineKeyboardButton(text='Журнал событий', callback_data='live_journal')
investor_first_kb = InlineKeyboardMarkup()
investor_first_kb.add(see_my_fish)
investor_first_kb.add(send_msg_for_admin)
investor_first_kb.add(live_jornal)


# Клавиатура для инвестора отправка сообщения
yes_send_msg = InlineKeyboardButton(text='Да. Отправить.', callback_data='yes_send_msg')
yes_send_msg_kb = InlineKeyboardMarkup()
yes_send_msg_kb.add(yes_send_msg)
yes_send_msg_kb.add(back_callBack)


# Первоя клавиатура для нового посетителя
call_admin = InlineKeyboardButton(text='Связаться с администратором', callback_data='call_admin')
no_name_kb = InlineKeyboardMarkup()
no_name_kb.add(call_admin)


# Первоя клавиатура для бассейна
add_fish_btn = InlineKeyboardButton(text='Добавить рыбу', callback_data='add_fish_btn')
check_all_pools_btn = InlineKeyboardButton(text='Просмотреть', callback_data='check_all_pools')
create_pools_btn = InlineKeyboardButton(text='Создать', callback_data='create_pools_btn')
pool_kb = InlineKeyboardMarkup()
pool_kb.add(add_fish_btn)
pool_kb.add(check_all_pools_btn)
pool_kb.add(create_pools_btn)
pool_kb.add(back_callBack)


# Создание бассейна
yes_all_good = InlineKeyboardButton(text='Да все правильно', callback_data='yes_all_good')
confirm_kb = InlineKeyboardMarkup()
confirm_kb.add(yes_all_good)
confirm_kb.add(back_callBack)


# Создание бассейна
sail_fish = InlineKeyboardButton(text='Продать всю рыбу', callback_data='sail_all')
delete_pool = InlineKeyboardButton(text='Удалить бассейн', callback_data='delete_pool')
work_with_fish = InlineKeyboardMarkup()
work_with_fish.add(sail_fish)
work_with_fish.add(delete_pool)
work_with_fish.add(back_callBack)

# Создание бассейна
sale_fish = InlineKeyboardButton(text='Продать рыбу', callback_data='sale_fish')
balance_change = InlineKeyboardButton(text='Изменить баланс', callback_data='balance_change')
delete_inv = InlineKeyboardButton(text='Удалить инвестора', callback_data='delete_investor')
correct_data = InlineKeyboardButton(text='Редактировать', callback_data='correct')
work_with_investors = InlineKeyboardMarkup()
work_with_investors.add(sale_fish)
work_with_investors.add(balance_change)
work_with_investors.add(correct_data)
work_with_investors.add(delete_inv)
work_with_investors.add(back_callBack)


# Установка тарифа
food_price = InlineKeyboardButton(text='Тариф на корм рыбы', callback_data='food_price')
service_price = InlineKeyboardButton(text='Тариф на обслуживание', callback_data='service_price')
fish_price = InlineKeyboardButton(text='Стоимость рыбы', callback_data='fish_price')
prices = InlineKeyboardMarkup()
prices.add(food_price)
prices.add(service_price)
prices.add(fish_price)
prices.add(back_callBack)


# Изменить тариф
change_price = InlineKeyboardButton(text='Изменить тариф', callback_data='change_price')
change_prices = InlineKeyboardMarkup()
change_prices.add(change_price)
change_prices.add(back_callBack)

change_phone = KeyboardButton('📞 Телефон')
change_ID = KeyboardButton('🧭 Телеграм ID')
status = KeyboardButton('⚙️ Статус')
change_contact_kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
change_contact_kb.add(change_phone)
change_contact_kb.add(change_ID)
change_contact_kb.add(status)

# Изменить статус аккаунта
turn_off = KeyboardButton('⚙️ Отключить аккаунт')
tyrn_on = KeyboardButton('⚙️ Включить аккаунт')
activity_kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
activity_kb.add(tyrn_on)
activity_kb.add(turn_off)


change_name = KeyboardButton('Имя')
change_surname = KeyboardButton('Фамилия')
change_inv_contact_kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
change_inv_contact_kb.add(change_phone)
change_inv_contact_kb.add(change_name)
change_inv_contact_kb.add(change_surname)
