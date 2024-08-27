from pathlib import Path

import aiogram
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
import datetime
import excel
import userInterface
import subprocess
import pandas as pd
import logging
import send_email
import asyncio


# то есть когда IP падает, прога должна обратиться к этой функции

def main():
    global dp, bot
    is_updated = False
    while is_updated == False:
        try:

            with open('ApiBot.txt', 'r') as file:
                bot = Bot(token=file.readline())  # токен бота
                dp = Dispatcher(bot)
                print()
                array_of_pinged_ip_tg = []
                array_of_pinged_ip_mail = []
                logging.basicConfig(filename='app.log', filemode='w+', format='%(name)s - %(levelname)s - %(message)s')
                is_updated = True

            def search_variable(value: str) -> str:
                for i in range(len(userInterface.global_data)):
                    if userInterface.global_data[i][excel.HEADERS[i][1]].isin([value]).any():
                        return excel.HEADERS[i][0]

            @dp.message_handler(commands=['activate'])  # добавляет реакцию на сообщение "/activate"
            async def send_to_group_command(message: types.Message):
                global dp, bot
                sms_tg = ""

                sms_mail = ""
                file_path = "chatID.txt"  # путь к файлу в котором будет храниться группа в которую нужно отправлять уведомления
                with open(file_path, "w") as file:
                    file.write(str(message.chat.id))  # перезаписывает файл

                await bot.send_message(chat_id=message.chat.id,
                                       text="Уведомления активированы ✅✅✅")  # отправляет сообщение об удачном сохранении ID
                logging.warning('Уведомления активированы')

                await send_note()
                asyncio.run(send_note())

            async def send_note():
                while True:
                    file_path = "chatID.txt"  # Укажите путь к файлу в котором хранится ID группы
                    with open(file_path, "r") as file:
                        value = file.read()  # считывает ID группы из файла выше
                    # чтение csv файла
                    try:
                        to_note_list = pd.read_csv('notification_data.csv').values.tolist()
                    except:
                        to_note_list = []
                    sms_tg = ""
                    sms_mail = ''
                    for i, item in enumerate(to_note_list):
                        output = subprocess.run(["ping", "-n", "1", item[1]], capture_output=True, text=True,
                                                creationflags=subprocess.CREATE_NO_WINDOW)
                        if output.returncode == 0:
                            try:
                                array_of_pinged_ip_tg.pop(array_of_pinged_ip_tg.index(item[1]))
                                array_of_pinged_ip_mail.pop(array_of_pinged_ip_mail.index(item[1]))
                                logging.warning(f'{item[1]} в сети')
                            except:
                                pass
                        else:
                            logging.warning(
                                f'{item[1]} отключился от сети в {str(datetime.datetime.now().replace(microsecond=0))}')
                            # проверка уведомлял ли уже
                            if str(item[1]) not in array_of_pinged_ip_tg:

                                if item[2] == '☑':  # уведомлять ли в тг
                                    sms_tg += f"🚨🚨 {search_variable(item[1])} '{str(item[0])} с IP   {str(item[1])}  отключился от сети в  {str(datetime.datetime.now().replace(microsecond=0))}  🚨🚨 \n"

                                array_of_pinged_ip_tg.append(
                                    str(to_note_list[i][1]))  # добавление в список уже уведомленных
                            if str(item[1]) not in array_of_pinged_ip_mail:
                                if item[3] == '☑':  # уведомлять ли в мыле
                                    # # #
                                    sms_mail += f"🚨🚨 {search_variable(item[1])} '{str(item[0])} с IP   {str(item[1])}  отключился от сети в  {str(datetime.datetime.now().replace(microsecond=0))}  🚨🚨 \n"
                                array_of_pinged_ip_mail.append(str(to_note_list[i][1]))
                        if is_updated == False:
                            break
                        print(str(i) + " по счету ip проверен", len(userInterface.global_data))

                    if sms_tg != '':
                        if len(sms_tg) > 4096:
                            for x in range(0, len(sms_tg), 4096):
                                await bot.send_message(value, sms_tg[x:x + 4096])
                        else:
                            await bot.send_message(value, sms_tg)
                    if sms_mail != '':
                        send_email.sendEmail("mail.betaren.ru", 25, 'monit@betagran.ru', 'Yc8sB2#vdSW1mN@5%ffR',
                                             'monit@betagran.ru', 'Уведомление!', sms_mail)
                    #
                    if sms_tg != "":
                        sms_tg = ""
                    if sms_mail != "":
                        sms_mail = ""
                await asyncio.sleep(1)

            executor.start_polling(dp, skip_updates=False)  # Запуск бота из мейна
        except:
            pass

