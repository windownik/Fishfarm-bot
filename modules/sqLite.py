import sqlite3


# Новый юзер создает таблицу в бд
def new_user_table(
        table_name: int
):
    db = sqlite3.connect('modules/database.db')
    cursor = db.cursor()
    cursor.execute(f'''CREATE TABLE IF NOT EXISTS pool{str(table_name)} (
     telegram_id INTEGER, 
     food_mass TEXT, 
     fish_mass TEXT, 
     fish_id TEXT, 
     type TEXT, 
     date DATETIME)''')
    db.commit()


# Пользователь проверяет все данные о себе по базе данных
def read_all_values_in_db(telegram_id: int):
    connect = sqlite3.connect('modules/database.db')
    curs = connect.cursor()
    for data in curs.execute(f'SELECT * FROM users WHERE telegram_id= "{telegram_id}"'):
        return data
    connect.close()


# Пользователь проверяет себя по базе данных
def read_value_bu_name(
        name: str,
        table: str,
        telegram_id: int):
    connect = sqlite3.connect('modules/database.db')
    curs = connect.cursor()
    for data in curs.execute(f'SELECT {name} FROM {table} WHERE telegram_id ="{telegram_id}"'):
        return data
    connect.close()


# Пользователь проверяет себя по базе данных
def read_all_value_bu_name(name: str = '*', table: str = 'users'):
    connect = sqlite3.connect('modules/database.db')
    curs = connect.cursor()
    curs.execute(f'SELECT {name} FROM {table}')
    data = curs.fetchall()
    connect.close()
    return data


# Создаем первую запись в бд о пользователе в таблице users
def insert_first_note(
        telegram_id: int, *, table: str = 'users'
):
    connect = sqlite3.connect('modules/database.db')
    curs = connect.cursor()
    curs.execute(f"INSERT INTO {table} (telegram_id) VALUES ('{telegram_id}')")
    connect.commit()
    connect.close()


# Обновляем любые данные в любую таблицу в файле modules/database.db
def insert_info(
        table_name: str,
        telegram_id: int,
        name: str,
        date):
    connect = sqlite3.connect('modules/database.db')
    curs = connect.cursor()
    curs.execute(f"UPDATE {table_name} SET {name}= ('{date}') WHERE telegram_id='{telegram_id}'")
    connect.commit()
    connect.close()


# Созданм новую запись о тратах или доходах в бд в личной таблице
def insert_pool_db1(telegram_id: str,
                    food_mass: str,
                    fish_mass: str,
                    fish_id: str,
                    number: int,
                    data,
                    type: str):
    connect = sqlite3.connect('modules/database.db')
    curs = connect.cursor()
    curs.execute(f"INSERT OR IGNORE INTO pool{number} VALUES (?,?,?,?,?,?,?)",
                 (f'{telegram_id}', f'{food_mass}', f'{fish_mass}', f'{fish_id}', f'{type}',
                  f'{data}', None))
    connect.commit()
    connect.close()


# Пользователь проверяет данные о себе по любым данным
def read_values_in_db_by_phone(table: str, name: str, data):
    connect = sqlite3.connect('modules/database.db')
    curs = connect.cursor()
    for d in curs.execute(f'SELECT * FROM {table} WHERE "{name}" = "{data}"'):
        return d
    connect.close()


# Пользователь проверяет данные о себе по любым данным
def read_admin(data, *, name: str = 'telegram_id'):
    connect = sqlite3.connect('modules/database.db')
    curs = connect.cursor()
    for d in curs.execute(f'SELECT * FROM admin_users WHERE "{name}" = "{data}"'):
        return d
    connect.close()


def insert_first_pool(
        number: int
):
    connect = sqlite3.connect('modules/database.db')
    curs = connect.cursor()
    curs.execute(f"INSERT INTO pools (number) VALUES ('{number}')")
    connect.commit()
    connect.close()


# Обновляем любые данные в таблице pools в файле modules/database.db
def insert_info_pool(
        number: int,
        name: str,
        date):
    connect = sqlite3.connect('modules/database.db')
    curs = connect.cursor()
    curs.execute(f"UPDATE pools SET {name}= ('{date}') WHERE number='{number}'")
    connect.commit()
    connect.close()


# Удаляем данные из таблицы
def delete_str(
        table: str,
        name: str,
        data):
    connect = sqlite3.connect('modules/database.db')
    curs = connect.cursor()
    curs.execute(f"DELETE FROM '{table}' WHERE {name}={data}")
    connect.commit()
    connect.close()


# insert data
def insert_pool_db(telegram_id: str,
                   name: str,
                   surname: str,
                   phone: str,
                   data,
                   type: str):
    connect = sqlite3.connect('modules/database.db')
    curs = connect.cursor()
    curs.execute(f"INSERT INTO admin_users VALUES (?,?,?,?,?,?)",
                 (f'{telegram_id}', f'{name}', f'{surname}', f'{phone}', f'{type}',
                  f'{data}'))
    connect.commit()
    connect.close()
