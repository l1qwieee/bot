import logging
import datetime
from aiogram.utils.markdown import hlink
from aiogram import Bot, Dispatcher, Router, types
import asyncio
from dbad import DataBase
import keyboards as nav
import re

TOKEN = "5841486224:AAFf3GSIIZIVYxnsXD31Hvy3nPJWdvzZxwo"

bot = Bot(token=TOKEN)
dp = Dispatcher()
router = Router()
db = DataBase("..\\bot(for_all)\database.db")

countKeyboards = [nav.whoreg, nav.mainGames, nav.inkb, nav.inkbtime]

weekDays = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
weekDRus = ["Пн", "Вт", "Ср", "Чт", "Пт", "Сб", "Вс"]


# Порядок действий:
# 1. Првоерка точно ли это админ пользуется ботом
# 2. Выбор действия: 1)сделать расписание(дополнить) 2) посмотреть кто записался
# 1)
#   1. Выбор игры
#   2. Ввод даты
#   3. Ввод времени
#   4. Ввод кол-ва мест

#Начало
@router.message()
async def vector_mes(message: types.Message):
    if message.text == '/start':
        await start_comm(message)
    elif message.text == 'Узнать кто записался' or message.text == 'Настроить расписание':
        await choice_direction(message)
    elif message.text == '/whoreg':
        await startwhoreg(message)
    elif message.text == '/schedule':
        await schedule_comm(message)
    elif re.match(r"\d{1,2}-\d{1,2}-\d{4}", message.text):
        await dat(message)
    elif re.match(r"\d{2}:\d{2}", message.text):
        await added_times(message)
    elif re.match(r"\d{2}|\d{1}", message.text):
        await num_of_seats(message)
    else:
        await bot.send_message(message.from_user.id, text="ZzZzZzZzZzZ")

@router.callback_query()
async def vector_call(query: types.CallbackQuery):
    if query.data == "volleyball" or query.data == "football":
        await call_back_games2(query)
    elif query.data[0] == "*":
        ch = query.data[1:]
        await click_date(query, ch)
    elif query.data[0] == "9":
        ch = query.data[1:]
        await ckick_time(query, ch)
    elif query.data == "yes" or query.data == "no":
        await del_game(query)
    

async def start_comm(message: types.Message):
    if message.from_user.id == 738070596:
        await bot.send_message(message.from_user.id, text="Привет! Ты как раз тот, кто мне нуджен) Покажу тебе всю информацию которая у меня есть по твоему желанию", reply_markup=countKeyboards[0])
        await bot.send_message(message.from_user.id, text="Итак, вот несколько правил как мной пользоваться:\nЕсли вы решили что то посмотреть или дополнить расписание, то !ОБЯЗАТЕЛЬНО! начинайте все с самого начала, а если конкретнее, то с начальных кнопках клавиатуры. Или же используете спецальные команды, такие как:\n/schedule - любая правка расписания\n/whoreg - если хотите узнать кто куда зарегестрировался и для связи с игроками")
    else:
        await bot.send_message(message.from_user.id, text="Бро, ты кто? \n иди-ка ты отсюда")

#Выбор направления
async def choice_direction(message: types.Message):
    db.delete()
    db.delete_data()
    if message.text == 'Настроить расписание':
        db.ff_step("schedule_data", "start")
    else:
        db.ff_step("prog_who_reg", "start")
    await bot.send_message(message.from_user.id, text="Выберете игру:", reply_markup=nav.InmainGames)

#Выбор: узнаем кто куда записался
async def startwhoreg(message: types.Message):
    db.ff_step("prog_who_reg", "start")
    await bot.send_message(message.from_user.id, text="Выберете игру:", reply_markup=nav.InmainGames)

#Выбор: настройка расписания
#Вызов выбора игры
async def schedule_comm(message: types.Message):
    db.ff_step("schedule_data", "start")
    await bot.send_message(message.from_user.id, text="Выберете игру:", reply_markup=nav.InmainGames)

#Выбор игры/вызов ввода даты
async def call_back_games2(query: types.CallbackQuery):
    if examination_schedule("schedule_data", "start") == False and examination_who_reg("prog_who_reg") == False:
        await bot.send_message(query.from_user.id, text="Если бы не мой хозяин, то я бы сейчас залагал, т.к. вы нарушили мои правила.\nНа всякий случай вышлю вам их еще раз:")
        await bot.send_message(query.from_user.id, text="Итак, вот несколько правил как мной пользоваться:\nЕсли вы решили что то посмотреть или дополнить расписание, то !ОБЯЗАТЕЛЬНО! начинайте все с самого начала, а если конкретнее, то с начальных кнопках клавиатуры. Или же используете спецальные команды, такие как:\n/schedule - любая правка расписания\n/whoreg - если хотите узнать кто куда зарегестрировался и для связи с игроками")

    else:

        if examination_schedule("schedule_data", "start") == True:
            table = "schedule_data"
        elif examination_who_reg("prog_who_reg") == True:
            table = "prog_who_reg"
        game = query.data
        db.f_step(table, game, "game", "start")

        if table == "prog_who_reg":
            await kb_data(query)
        else:
            await bot.send_message(query.from_user.id, text="Напишите дату проведения игры. \nПример: 20-02-2023")



#Выбор даты/вызов ввода времени/ввод времени/вызов ввода кол-ва места/ввод кол-ва мест
async def dat(message: types.Message):

    if examination_schedule("schedule_data", "game") == False:
        await bot.send_message(message.from_user.id, text="Если бы не мой хозяин, то я бы сейчас залагал, т.к. вы нарушили мои правила.\nНа всякий случай вышлю вам их еще раз:")
        await bot.send_message(message.from_user.id, text="Итак, вот несколько правил как мной пользоваться:\nЕсли вы решили что то посмотреть или дополнить расписание, то !ОБЯЗАТЕЛЬНО! начинайте все с самого начала, а если конкретнее, то с начальных кнопках клавиатуры. Или же используете спецальные команды, такие как:\n/schedule - любая правка расписания\n/whoreg - если хотите узнать кто куда зарегестрировался и для связи с игроками")

    else:
        today = datetime.date.today()
        user_date_str = message.text
        user_date = datetime.datetime.strptime(user_date_str, "%d-%m-%Y").date()
        if today > user_date:
            await bot.send_message(message.from_user.id, text="Эта дата меньше, чем сегодняшняя. Зачем вы пытаетесь добавить в расписание дату из прошлого? 🧐")
        else:
    # Дата прошла проверку
    # Добавьте здесь ваш код для обработки даты

            if db.select("game", "game")[0] == "volleyball":
                sel_game = "volleyball"
            else:
                sel_game = "football"


            if db.chek_data(message.text, sel_game) != []:
                await bot.send_message(message.from_user.id, text="Такая дата уже есть. Вы можете ее удалить")
            else:
                db.add("data", message.text, "data", "game", sel_game)
                await bot.send_message(message.from_user.id, text="Дата успешно добавлена!")
                await bot.send_message(message.from_user.id, text="Введите время игры в следующем формате: 12:00 13:00 14:00 15:00")


# Выбор времени
async def added_times(message: types.Message):
    if examination_schedule("schedule_data", "data") == False:
        await bot.send_message(message.from_user.id, text="Если бы не мой хозяин, то я бы сейчас залагал, т.к. вы нарушили мои правила.\nНа всякий случай вышлю вам их еще раз:")
        await bot.send_message(message.from_user.id, text="Итак, вот несколько правил как мной пользоваться:\nЕсли вы решили что то посмотреть или дополнить расписание, то !ОБЯЗАТЕЛЬНО! начинайте все с самого начала, а если конкретнее, то с начальных кнопках клавиатуры. Или же используете спецальные команды, такие как:\n/schedule - любая правка расписания\n/whoreg - если хотите узнать кто куда зарегестрировался и для связи с игроками")

    else:
        ms = ''.join(message.text)
        times = ms.split()
        bool = False
        for i in ms:
            if i == ":":
                bool = True
                break
        if bool == True:
            cc = 0
            data_id = db.select_data_id("data")[0] # узнаю какая дата была выбрана
            while cc < len(times):
                if bool == True:
                    db.insert_time(data_id, times[cc], "time")
                cc += 1
            db.update_step(data_id, "time")
            await bot.send_message(message.from_user.id, text="Супер! Введите количество мест на одну игру. Если вы при вводе времени указали больше чем одно значение, то тогда сделайте тоже самое и тут. Пример: 11 12 13 (через пробел, двузначное число)")



#Ввод места
async def num_of_seats(message: types.Message):
    if examination_schedule("schedule_data", "time") == False:
        await bot.send_message(message.from_user.id, text="Если бы не мой хозяин, то я бы сейчас залагал, т.к. вы нарушили мои правила.\nНа всякий случай вышлю вам их еще раз:")
        await bot.send_message(message.from_user.id, text="Итак, вот несколько правил как мной пользоваться:\nЕсли вы решили что то посмотреть или дополнить расписание, то !ОБЯЗАТЕЛЬНО! начинайте все с самого начала, а если конкретнее, то с начальных кнопках клавиатуры. Или же используете спецальные команды, такие как:\n/schedule - любая правка расписания\n/whoreg - если хотите узнать кто куда зарегестрировался и для связи с игроками")
    else:
        ms = ''.join(message.text)
        place = ms.split()
        print(place)
        bool = False
        for i in ms:
            if i == ":":
                bool = True
                break
        if bool == True:
            await added_times(message)
        else:
            data_id = db.select_data_id("time")[0]
            res = db.select_id(data_id)
            hmid = [item[0] for item in res]
            cc = 0
            while cc < len(place):
                db.add_place(place[cc], hmid[cc], data_id)
                cc += 1
            await bot.send_message(message.from_user.id, text="Расписание завершено")
            await bot.send_message(message.from_user.id, text="Вот две моих главные команды:\n/schedule - настроить расписание\n/whoreg - посмотреть кто куда записался и заодно связаться с ними")




#Выбор: узнаем кто куда записался

#Выбор даты
async def kb_data(message: types.Message):
    if examination_who_reg("prog_who_reg") == False:
        await bot.send_message(message.from_user.id, text="Если бы не мой хозяин, то я бы сейчас залагал, т.к. вы нарушили мои правила.\nНа всякий случай вышлю вам их еще раз:")
        await bot.send_message(message.from_user.id, text="Итак, вот несколько правил как мной пользоваться:\nЕсли вы решили что то посмотреть или дополнить расписание, то !ОБЯЗАТЕЛЬНО! начинайте все с самого начала, а если конкретнее, то с начальных кнопках клавиатуры. Или же используете спецальные команды, такие как:\n/schedule - любая правка расписания\n/whoreg - если хотите узнать кто куда зарегестрировался и для связи с игроками")
    else:
        days = []
        
        row = [date[0] for date in db.sel_all_data()]
        for item in row:
            days.append(item)

        await bot.send_message(message.from_user.id, text="Выберете дату:", reply_markup=nav.kbdata(days))


#Узнаю какая дата выбрана
async def click_date(query: types.CallbackQuery, text):
    if examination_who_reg("prog_who_reg") == False:
        await bot.send_message(query.from_user.id, text="Если бы не мой хозяин, то я бы сейчас залагал, т.к. вы нарушили мои правила.\nНа всякий случай вышлю вам их еще раз:")
        await bot.send_message(query.from_user.id, text="Итак, вот несколько правил как мной пользоваться:\nЕсли вы решили что то посмотреть или дополнить расписание, то !ОБЯЗАТЕЛЬНО! начинайте все с самого начала, а если конкретнее, то с начальных кнопках клавиатуры. Или же используете спецальные команды, такие как:\n/schedule - любая правка расписания\n/whoreg - если хотите узнать кто куда зарегестрировался и для связи с игроками")
    else:
        choice = text
        db.update("data", choice, "data", "game")
        times = []
        data_id = db.sel_data_id(choice)[0]

        row = [date[0] for date in db.sel_time(data_id)]
        for item in row:
            times.append(item)

        await bot.send_message(query.from_user.id, text="Выберете время:", reply_markup=nav.kbtime(times))


#Узнаю какое время было выбрано
async def ckick_time(query: types.CallbackQuery, text):
    if examination_who_reg("prog_who_reg") == False:
        await bot.send_message(query.from_user.id, text="Если бы не мой хозяин, то я бы сейчас залагал, т.к. вы нарушили мои правила.\nНа всякий случай вышлю вам их еще раз:")
        await bot.send_message(query.from_user.id, text="Итак, вот несколько правил как мной пользоваться:\nЕсли вы решили что то посмотреть или дополнить расписание, то !ОБЯЗАТЕЛЬНО! начинайте все с самого начала, а если конкретнее, то с начальных кнопках клавиатуры. Или же используете спецальные команды, такие как:\n/schedule - любая правка расписания\n/whoreg - если хотите узнать кто куда зарегестрировался и для связи с игроками")
    else:
        choice = text
        data = db.select_data("data")[0]
        data_id = db.select_data_id_chek(data)[0]
        game_id = db.select_game_id(data_id, choice)[0]
        reg_list = db.chek_guys(game_id)
        db.update("time", choice, "time", "data")
        if reg_list == []:
            await bot.send_message(query.from_user.id, text="Тут никого нет(((")
            await bot.send_message(query.from_user.id, text="Желаете удалить эту игру?", reply_markup=nav.kbyes)
        else:

            nicknames = await link_generetion(game_id)



            inf_list = ["Имя", "Сколько человек вместе с ним(ней)", "Способ оплаты"]
            message_text = "Вот кто зарегистрировался на эту игру: \n"
            i = 0
            j = 0
            while i < len(reg_list):
                while j < 3:
                    text = reg_list[i][j]
                    if j == 0:
                        text = hlink(reg_list[i][j], nicknames[i])
                    message_text += f"<b>-{inf_list[j]}:</b>   <u>{text}</u>\n"
                    j += 1
                i += 1
                j = 0

            await bot.send_message(query.from_user.id, text=message_text, parse_mode="HTML")
            db.delete()



async def link_generetion(game_id):

    all_nicknames = [date[0] for date in db.sel_all_nickname(game_id)]
    message_text = []
    for item in all_nicknames:
        message_text.append(f"t.me/{item}")



    return message_text


def examination_who_reg(table):
    if db.w_is_inside(table) == False:
        ex = False
    else:
        ex = True
    return ex

def examination_schedule(table, step):
    if db.ex_step(table, step) == False:
        ex = False
    else:
        ex = True
    return ex

#Удаление игры
async def del_game(query: types.CallbackQuery):
    if query.data == 'yes':
        all_inf_game = db.inf_game()
        data_id = db.sel_data_id(all_inf_game[0][2])[0]
        count_games = db.hm_games(data_id)[0]
        game_id = db.select_game_id(data_id, all_inf_game[0][3])[0]
        if count_games == 1:
            db.del_game(game_id)
            db.del_data(all_inf_game[0][2], "schedule_data")
        else:
            db.del_game(game_id)
        await bot.send_message(query.from_user.id, text="Данная игра удалена")
        db.delete()
    else:
        await bot.send_message(query.from_user.id, text="Хорошо, тогда возвращаю вас в начало")
        await bot.send_message(query.from_user.id, text="Вот две моих главные команды:\n/schedule - настроить расписание\n/whoreg - посмотреть кто куда записался и заодно связаться с ними")
        
       


#async def what_date(message: types.Message):   
#    global weekDays
#    current_day = datetime.datetime.now().strftime("%A")  
#    logging.warning(current_day)
#    day = "Sunday"
#    i = 0
#    while weekDays[i] != current_day:
#        i += 1
#    j = i
#    while weekDays[j] != day:
#        j += 1
#    count = j - i
#    days = count
#    logging.warning(days)
#    future_date = datetime.datetime.now() + datetime.timedelta(days=days)
#    future_date_str = future_date.strftime("%Y-%m-%d")
#    await bot.send_message(message.from_user.id, text=future_date_str)




#    await bot.send_message(user.id, text="Напишите в какое время будет проходить игра через двоеточие и запятые. Например: 12:00,09:00,22:00 \n!БЕЗ ПРОБЕЛОВ!\nМаксимальное количество игр привязанное к одному дню - 4")


async def main():
    print("zzz")
    dp = Dispatcher()
    dp.include_router(router)
    await dp.start_polling(bot, skip_updates=True)


if __name__ == "__main__":
    print("wtf")
    asyncio.run(main())