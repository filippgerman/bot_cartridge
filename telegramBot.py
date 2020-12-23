import logging
from dataBase import *

from aiogram import Bot, Dispatcher, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram import types
from aiogram.types import ContentType

logging.basicConfig(level=logging.INFO)  # начало логирования.

bot = Bot(token="1446559916:AAEL6dgMqPVJzTj_1_wO7Lt-tcaZ_9aSbRo")  # токен нашего бота
dp = Dispatcher(bot, storage=MemoryStorage())  # Диспетчер


@dp.message_handler(commands=['start'])
async def start_work_bot(message: types.Message):
    await bot.send_message(message.from_user.id,
                           f"Здравствуйте, я Ваш новый помощник!\n"
                           f"Позвольте я расскажу, что я умею\n"
                           f"Вы вводите название и номер принтера "
                           f"(чем детальнее Вы введете, тем лучше будет результат)\n"
                           f"а я дам Вам список картриджей для него. \n")


@dp.message_handler(content_types=ContentType.TEXT)
async def find_cartridge(message: types.Message):
    result = session.query(Cart).filter(Cart.printer.like(f'%{message.text}%')).count()
    if result:

        data = session.query(Cart).filter(Cart.printer.like(f'%{message.text}%'))
        message_to_user = "По Вашему запросу я нашел следующее:\n"
        count_row = 0
        for i in data:
            if count_row < 20:
                message_to_user += f"Принтер : {i.printer}  картридж : {i.cartridge}\n"
                count_row += 1
            else:
                break
    else:
        message_to_user = f"Записей нет"

    await bot.send_message(message.from_user.id, message_to_user)


@dp.message_handler(commands=['help'])
async def help_bot(message: types.Message):
    await bot.send_message(message.from_user.id,
                           f"Сейчас расскажу, как мной пользоваться\n"
                           f"Вы вводите название и номер принтера "
                           f"(чем детальнее Вы введете, тем лучше будет результат)\n"
                           f"а я дам Вам список картриджей для него.\n")


@dp.message_handler(content_types=ContentType.ANY)
async def garbage_collector(message: types.Message):
    await bot.send_message(message.from_user.id,
                           f"К сожалению я Вас не понимаю\n"
                           f"Если вдруг Вы запутались в моем управлении то Вам может помочь команда /help")


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)  # поллинг, для получения обновлений от бота
