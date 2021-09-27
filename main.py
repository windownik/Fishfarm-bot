import threading
import time
from aiogram import executor
from modules.dispatcher import dp
import schedule
from modules.servic_payments import day_tax
from modules import workWF


#
def sleeper():
    while True:
        telegram_token = workWF.xsl_read()
        time.sleep(1200)


def day_tax_run():
    schedule.every().day.at("04:10").do(day_tax)

    while True:
        schedule.run_pending()
        time.sleep(10)


if __name__ == '__main__':
    t = threading.Thread(target=sleeper, name="Thread")
    t.start()

    k = threading.Thread(target=day_tax_run, name="Thread2")
    k.start()

    executor.start_polling(dp)
