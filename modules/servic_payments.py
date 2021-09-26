from modules import sqLite, workWF
import requests, datetime

telegram_token = workWF.xsl_read()
API_link = f'https://api.telegram.org/bot{telegram_token}/'


def send_massage(user_id: str, text: str):
    try:
        requests.get(API_link + f'sendMessage?chat_id={user_id}&text={text}').json()
    except:
        pass


def day_tax():
    admin_id = workWF.read_admin()
    pools = sqLite.read_all_value_bu_name(name='*', table='pools')
    for i in range(0, len(pools)):
        user_tg_ids = str(pools[i][1]).split('TgID')
        fish_ids = str(pools[i][2]).split('ID')
        start_fish_mass = str(pools[i][3]).split('KG')

        for k in range(0, len(user_tg_ids) - 1):
            user_tg_id = user_tg_ids[k]
            fish_id = fish_ids[k]
            fish_mass_one = float(start_fish_mass[k])

            old_balance = float(sqLite.read_value_bu_name(name='balance', table='users',
                                                          telegram_id=int(user_tg_id))[0])
            service_price = float(sqLite.read_value_bu_name(name='price_of_service', table='users',
                                                            telegram_id=workWF.read_admin())[0])
            new_balance = round(old_balance - fish_mass_one * service_price, 2)
            sqLite.insert_info(table_name='users', telegram_id=int(user_tg_id), name='balance',
                               date=str(new_balance))

            sqLite.insert_pool_db1(telegram_id=admin_id,
                                   food_mass=str(round(fish_mass_one * service_price, 2)),
                                   fish_mass='None',
                                   fish_id=fish_id,
                                   number=int(i + 1),
                                   data=datetime.datetime.now(),
                                   type='service_pay')
            price = fish_mass_one * service_price
            try:
                send_massage(user_id=user_tg_id,
                             text=f'Плата за обслуживание рыбы с ID {fish_id} составила {price} RUR')
            except:
                send_massage(user_id=workWF.read_admin(), text=f'Списание денег за обслуживание ID рыбы {fish_id},'
                                                               f'телеграм ID {user_tg_id} не действительный ')
