from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from modules import workWF

import logging


telegram_token = workWF.xsl_read()


storage = MemoryStorage()
logging.basicConfig(level=logging.INFO)
bot = Bot(telegram_token)
dp = Dispatcher(bot, storage=storage)


# Welcome form
class start_Form(StatesGroup):
    first_menu = State()
    second_menu = State()

    set_admin = State()


# Admin menu
class Admin_Form(StatesGroup):
    admin_first_menu = State()
    manual_input = State()
    phone_input = State()
    surname_input = State()
    name_input = State()
    telegram_id_input = State()
    type_input = State()
    set_balance_investor = State()
    set_pool_number = State()
    set_ID_number = State()
    set_fish_number = State()
    finish = State()

    phone_input_search = State()


# Admin worker menu
class Admin_Worker(StatesGroup):
    admin_all_worker = State()
    worker_data = State()
    correct_worker_data = State()
    pick_data = State()
    correct_phone = State()
    confirm_correct_phone = State()
    correct_tg_id = State()
    confirm_correct_tg_id = State()
    correct_status = State()
    confirm_status = State()

    delete_worker = State()

    journal = State()


# Admin investor menu
class Admin_Investor(StatesGroup):
    admin_start_investor = State()
    send_msg = State()
    send_msg_for_all = State()
    send_msg_for_all_without_img = State()
    write_msg_text = State()
    send_photo_msg_text = State()
    end_msg = State()

    msg_for_one = State()
    msg_for_one_by_name = State()
    msg_for_one_by_pool = State()
    msg_for_one_text = State()
    msg_for_one_img = State()
    msg_for_one_without_img = State()
    msg_for_one_photo = State()

    admin_check_investors = State()
    admin_check_investors_name = State()
    admin_check_investors_pool = State()
    admin_work_investors = State()
    admin_work_investors_fish = State()
    admin_work_investors_money = State()
    admin_sale_fish_id = State()

    admin_set_new_balance = State()
    admin_set_new_balance_confirm = State()
    admin_set_services = State()
    admin_food_services = State()
    admin_change_price = State()
    admin_confirm_change_price = State()

    admin_confirm_delete_inv = State()

    correct_phone = State()
    correct_inv = State()
    correct_name = State()
    correct_surname = State()
    confirm_correct_phone = State()
    confirm_correct_name = State()
    confirm_surname = State()


class Worker(StatesGroup):
    worker_start = State()

    feed_fish = State()
    feed_fish_food = State()
    feed_fish_confirm = State()

    size_fish = State()
    size_fish_food = State()
    size_fish_confirm = State()

    send_photo = State()
    pick_photo = State()
    confirm_send_photo = State()


class Investor(StatesGroup):
    investor_start = State()
    send_msg = State()
    msg_realy_send = State()

    my_fish = State()

    journal = State()
    journal_pick_month = State()


class NoName(StatesGroup):
    noname_start = State()
    noname_send_msg = State()
    noname_surname = State()
    noname_contact = State()


class Admin_Pool(StatesGroup):
    pool_start = State()
    create_pool = State()
    confirm_new_pool = State()

    check_poll_data = State()
    sale_fish_in_pool = State()
    delete_fish_in_pool = State()
    money_from_fish = State()
    sale_fish_in_pool_confirm = State()

    add_fish = State()
    pick_investor = State()
    pick_fish_mass = State()
    pick_fish_id = State()
    confirm_fish = State()
    save_fish = State()


class Admin_db(StatesGroup):
    db_start = State()
    db_pick_pool = State()
    show_data = State()
