import logging
import time
import re
import datetime
from aiogram import Bot, Dispatcher, Router, types
import markups as nav
from db import DataBase
import asyncio
from aiogram.fsm.context import FSMContext

countKeyboards = [nav.mainGames, nav.detalis, nav.choisePay, nav.kbINFO]
InlineKB = [nav.kb, nav.inkb, nav.kbDEL, nav.kbgames]
weekDays = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
weekDRus = ["Пн", "Вт", "Ср", "Чт", "Пт", "Сб", "Вс"]
steps = ["game", "day", "time", "people", "payment"]
TOKEN = "5898243671:AAEgODtzGWkIHW3Sf5kBdY0QrLdzLKsHq9o"
games = True
people = False
count  = -1

logging.basicConfig(level=logging.INFO)

bot = Bot(token=TOKEN)
dp = Dispatcher()
router = Router()

db = DataBase('database.db')

# Порядок действий:
# 1. Регистрация пользователя, если уже такой есть в базе даных, то тогда прдложение выбрать игру и продолжить регистрацию на игру
# 2. Регистрция на конкретную игру происходит в следующем порядке:
#   1. Выбор игры
#   2. Выбор даты
#   3. Выбор времени
#   4. Ввод кол-ва мест которые хочет пользователь занять
#   5. Выбор способа оплаты
# 3. Пользователь может посмоотреть какая инофрмация по нему есть у меня в базе данных
#   1. Выбор игры (на которые он регестрировался)
#   2. Выбор даты (на которые он регестрировался)
#   4. Выбор времени (на которые он регестрировался)
#   5. Показ информации по этой конкретной дате
#   6. Предложение удалить или оставить.
#       1. Удаление
#       2. Оставить все как есть


@router.message()
async def vector_mes(message: types.Message, state: FSMContext) -> None:
    if message.text == '/start':
        await startt(message)
    elif message.text =='/re_reg':
        await re_reg_com(message)
    if db.count(message.from_user.id) != None:
        if message.text == '🏐 ВОЛЕЙБОЛ' or message.text == '⚽️ ФУТБОЛ':
            await choice_game(message, True)
        elif message.text == '🗓 Расписание' or message.text == '📋 Правила' or message.text == '🤙 Рекомендации к тренировке' or message.text =='😎 Записаться':
            await studying(message, True)
        elif message.text.isdigit() and 0 < int(message.text):
            await quantity_people(message, True)
        elif message.text == '💷 Наличные' or message.text == '💳 Перевод':
            await pay(message, True)
        elif message.text == '/help':
            await help_com(message)
        elif message.text == '/delete':
            await delete_comm(message)
        elif message.text == 'Узнать информацию о себе':
            await inf(message)
        elif message.text == 'Да' or message.text == 'Нет':
            await delete_inf(message)
        elif message.text == '◀️ Назад':
            await goback(message)
        elif message.text == 'Завершить регистрацию':
            await complete_registration(message)
    else:
        await bot.send_message(message.from_user.id, text="ZzZzZzZz")

@router.callback_query()
async def vector_call(query: types.CallbackQuery):
    if query.data == "yes":
        ch = query.data
        await call_back_regs(query)
    if db.count(query.from_user.id) != None:
        if query.data[0] == "*":
            ch = query.data[1:]
            await show_schedule_time(query, ch, True)
        elif query.data[0] == "9":
            seats = query.data[7:]
            if int(seats) < 10:
                ch = query.data[1:][:-2]
            elif 100 < int(seats) < 1000:
                ch = query.data[1:][:-4]
            else:
                ch = query.data[1:][:-3]
            await call_back_time(ch, query, True)
        elif query.data == "game" or query.data == "all":
            ch = query.data
            await call_back_delete(ch, query)
        elif query.data == "volleyball" or query.data == "football":
            ch = query.data
            await call_back_games(ch, query)
        elif query.data[0] == "7":
            ch = query.data[1:]
            await call_back_inf(ch, query)
    else:
        await bot.send_message(query.from_user.id, text="ZzZzZzZz")


#Начало/Регистрация нового пользолвателя
async def startt(message: types.Message):
    if db.chek_reg(message.from_user.id) == 1:
        await bot.send_message(message.from_user.id, text="Бро, ты уже зарегестрирован) Для того, чтоб тебе повторно зарегаться на нашу игру нажми /re_reg")
    else:
        db.add_new_user(message.from_user.id, "users")
        await bot.send_message(message.from_user.id, "Привет! Я бот который будет вас регистрировать на игры по волейболу или футболу! Но для начала прошу вас зарегестрироваться)", reply_markup=nav.kb)

async def call_back_regs(query: types.CallbackQuery):
    if db.sel_user(query.from_user.id)[0] != 0:
        db.del_prog_to_game(query.from_user.id)
    db.f_step(query.from_user.id, "lvl1")
    db.new_us(query.from_user.id, query.from_user.first_name, query.from_user.last_name, query.from_user.username, query.from_user.language_code)
    await query.message.reply("Регистрация прошла успешно!", reply_markup=nav.mainGames)

async def re_reg_com(message: types.Message):
    if db.sel_user(message.from_user.id)[0] != 0:
        db.del_prog_to_game(message.from_user.id)
    db.f_step(message.from_user.id, "lvl1")
    await bot.send_message(message.from_user.id, text="Ура! Вы к нам вернулись! Ну ладно, свои родостные эмоции я оставлю при себе, а вас заново зарегестрирую на игру, которую вы хотите",
                           reply_markup=nav.mainGames)

#def schedule_function():
 #   now = datetime.now()
 #   next_midnight = (now + time.delta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0)
 #   delay = (next_midnight - now).total_seconds()
 #   schedule.every(delay).seconds.do(relevance)

#schedule_function()

#Выбор игры
async def choice_game(message: types.Message, vector):
    if vector == True:
        bool = await check_lvl(message, "lvl1", vector)
    else:
        bool = await check_lvl(message, "lvl3", vector)
    if bool == False:
        await bot.send_message(message.from_user.id, text="Большая просьба: регестрируйтесь пошагово и отвечайте на вопрос только если бот его вам задает прямо сейчас")
    else:
        if message.text == '🏐 ВОЛЕЙБОЛ':
            db.update_prog_reg("game", "volleyball", "lvl2", message.from_user.id)
        elif message.text == '⚽️ ФУТБОЛ':
            db.update_prog_reg("game", "football", "lvl2", message.from_user.id)
        await bot.send_message(message.from_user.id, "Как на счет изучить, что мы можем предложить?", reply_markup=nav.detalis)

#Предложение изучить что есть у нас и продолжить регистрацию
async def studying(message: types.Message, vector):
    if vector == True:
        bool = await check_lvl(message, "lvl2", vector)
    else:
        bool = await check_lvl(message, "lvl4", vector)
    if bool == False:
        await bot.send_message(message.from_user.id, text="Большая просьба: регестрируйтесь пошагово и отвечайте на вопрос только если бот его вам задает прямо сейчас")
    else:
        game = db.select("game", message.from_user.id)[0]
        if message.text == '🗓 Расписание':
            if game == "volleyball":
                await bot.send_photo(message.from_user.id, photo="https://binaries.templates.cdn.office.net/support/templates/ru-ru/lt03413074_quantized.png")
            else:
                await bot.send_photo(message.from_user.id, photo="https://my-organizer.ru/wa-data/public/shop/products/14/24/2414/images/19897/19897.600.JPG")
        elif message.text == '📋 Правила':
            if game == "volleyball":
                await bot.send_message(message.from_user.id, "https://volleyplay.ru/ofitsialnyie-voleybolnyie-pravila-voleybola/")
            else:
                await bot.send_message(message.from_user.id, "https://www.ballgames.ru/%D1%84%D1%83%D1%82%D0%B1%D0%BE%D0%BB/%D0%BF%D1%80%D0%B0%D0%B2%D0%B8%D0%BB%D0%B0_%D1%84%D1%83%D1%82%D0%B1%D0%BE%D0%BB%D0%B0/")
        elif message.text == '🤙 Рекомендации к тренировке':
            await bot.send_message(message.from_user.id, "Желательна спортивная форма, ботинки и хорошее настроение (Вода за счет заведения, но можно взять и свою тоже)")
        elif message.text == '😎 Записаться':
            await show_schedule_data(message, vector)
            await bot.send_message(message.from_user.id, text="Если вы захотите вернуться назад, то просто нажмите:\n' ◀️Назад' ", reply_markup=nav.kbback)

#Генерация даты
async def show_schedule_data(message: types.Message, vector):
    if vector == True:
        bool = await check_lvl(message, "lvl2", vector)
    else:
        bool = await check_lvl(message, "lvl4", vector)
    if bool == False:
        await bot.send_message(message.from_user.id, text="Большая просьба: регестрируйтесь пошагово и отвечайте на вопрос только если бот его вам задает прямо сейчас")
    else:
        i = 1
        data_list = []
        days_list = []
        prev_data_str = None
        if db.select("game", message.from_user.id)[0] == "volleyball":
            sel_game = "volleyball"
        else:
            sel_game = "football"
        sid = db.select_id_data()[0]
        while i <= sid:
            if db.select_data(i, sel_game) == None:
                data = db.select_data(i, sel_game)
            else:
                data = db.select_data(i, sel_game)[0]

            
            if data != None and data != prev_data_str:
                data_str = data
                dt = datetime.datetime.strptime(data_str, "%d-%m-%Y").date()
                data_list.append(dt.strftime("%d-%m-%Y"))
                weekday = dt.strftime("%A")
                cnt = 0
                while weekday != weekDays[cnt]:
                    cnt += 1
                days_list.append(weekDRus[cnt])
            i += 1
            prev_data_str = data
        #logging.warning(nav.inkb())
        db.update_prog_reg("day", "progress", "lvl3", message.from_user.id)
        await bot.send_message(message.from_user.id, text="А теперь выберите в какой день недели вы хотите поиграть", reply_markup=nav.inkb(data_list, days_list))

#Генирация времени
async def show_schedule_time(message: types.CallbackQuery, day, vector):
    if vector == True:
        bool = await check_lvl(message, "lvl3", vector)
    else:
        bool = await check_lvl(message, "lvl5", vector)
    if bool == False:
        await bot.send_message(message.from_user.id, text="Большая просьба: регестрируйтесь пошагово и отвечайте на вопрос только если бот его вам задает прямо сейчас")
    else:
        times = []
        places = []
        game = db.select_game(message.from_user.id)[0]
        data_id = db.select_id_wh_data(day, game)[0]
        print(data_id)
        row = db.return_info(data_id)
        print(row)
        for item in row:
            times.append(item[0])
            places.append(item[1])
        db.update_prog_reg("day", day, "lvl4", message.from_user.id)
        await bot.send_message(message.from_user.id, text="Выберете время проведения игры", reply_markup=nav.timekb(times, places))

#Выбор времени
async def call_back_time(ch, query: types.CallbackQuery, vector):
    if vector == True:
        bool = await check_lvl(query, "lvl4", vector)
    else:
        bool = await check_lvl(query, "lvl6", vector)
    if bool == False:
        await bot.send_message(query.from_user.id, text="Большая просьба: регестрируйтесь пошагово и отвечайте на вопрос только если бот его вам задает прямо сейчас")
    else:
        await bot.send_message(query.from_user.id, f"Хорошо, регестрирую вас на {ch}\n А теперь напишите сколько человек мне с вами регистрировать (или вас одного все же?):")
        db.update_prog_reg("time", ch, "lvl5", query.from_user.id)


#Ввод желаемого кол-ва мест
async def quantity_people(message: types.Message, vector):
    if vector == True:
        bool = await check_lvl(message, "lvl5", vector)
    else:
        bool = await check_lvl(message, "maxlvl", vector)
    if bool == False:
        await bot.send_message(message.from_user.id, text="Большая просьба: регестрируйтесь пошагово и отвечайте на вопрос только если бот его вам задает прямо сейчас")
    else:
        if int(message.text) <= 11:
            res_data = db.select_game_us(message.from_user.id)[1]
            res_time = db.select_game_us(message.from_user.id)[2]
            game = db.select_game(message.from_user.id)[0]
            data_id = db.select_id_wh_data(res_data, game)[0]
            game_id = db.select_game_id(data_id, res_time)[0]
            row = db.select_place(game_id)[0]
            if int(message.text) <= row:
                db.update_prog_reg("people", int(message.text), "lvl6", message.from_user.id)
                db.update_places((row - int(message.text)), data_id, game_id)
                await bot.send_message(message.from_user.id, text="Хорошо, данные внесены. Теперь пожалуйста выберете cпособ оплаты", reply_markup=nav.choisePay)
            else:
                await bot.send_message(message.from_user.id, text="Столько мест на эту игру нет. Введите другое количество людей или выбирете другую дату")
        else:
            await bot.send_message(message.from_user.id, text="Я могу записать вас на игру, но при условии что вас будет 11 или меньше человек")

#Оплата
async def pay(message: types.Message, vector):
    bool = await check_lvl(message, "lvl6", vector)
    if bool == False:
        await bot.send_message(message.from_user.id, text="Большая просьба: регестрируйтесь пошагово и отвечайте на вопрос только если бот его вам задает прямо сейчас")
    else:
        if message.text == '💷 Наличные':
            mes = 'Наличные'
            await bot.send_message(message.from_user.id, "Хорошо, всю информацию я отправлю информацию организатору, а вы пожалуйста не забывайте❤️)\n По всем интересующим вас вопросам, большая просьба обращаться к админу группы)",
                                reply_markup=nav.kbcom)
        elif message.text == '💳 Перевод':
            mes = 'Перевод'
            await bot.send_message(message.from_user.id, "Ну что ж тогда вот реквизиты:\n 012350237481923\n Мухамед Абдул\n 300TL за человека\n По всем интересующим вас вопросам, большая просьба обращаться к админу группы)",
                                reply_markup=nav.kbcom)
        db.update_prog_reg("payment", mes, "maxlvl", message.from_user.id)
        await bot.send_message(message.from_user.id, text="Для завершения регистрации на игру нажмите:\nЗавершить регистрацию\nДля того чтобы исправить какие то данные при регистрации вернитесь назад:\n◀️ Назад")


#Завершение регистрации
async def complete_registration(message: types.Message):
    data = db.chek_condition(message.from_user.id)[0]
    time_click = db.chek_condition(message.from_user.id)[1]
    game = db.select_game(message.from_user.id)[0]
    data_id = db.select_id_wh_data(data, game)[0]
    game_id = db.select_game_id(data_id, time_click)[0]
    people = db.select_pep(message.from_user.id)[0]
    payment = db.sel_pay(message.from_user.id)[0]

    db.com_reg_to_games(message.from_user.id, game_id, people, payment)
    db.complete_registration(message.from_user.id)
    await bot.send_message(message.from_user.id, text="УРА! Вы зарегестировались у нас на игру! Чтоб посмотреть на какие будущие вы игры уже регестрировались нажмите:\nУзнать информацию о себе\nИли просто вернитесь в начало:\n◀️ Назад", reply_markup=nav.kbINFO)
    await bot.send_message(message.from_user.id, text="Вот несколько команд которые я знаю\n /help - информация обо мне тут\n /re_reg - если бы уже регестрировались во мне, то повторно все делать не нужно) надо просто выбрать игру в которую вы хотите сыграть)\nНу или напишите мне в чат - Узнать информацию о себе")










#async def examination(message: types.Message, data):
#    data_list = data
#    if len(data_list) > 2 and:




async def relevance():
    today = datetime.date.today()
    days = db.all_days()
    days_list  = [item[0] for item in days]
    i = 0
    while i < len(days_list):
        date = datetime.datetime.strptime(days_list[i], '%d-%m-%Y').date()
        formatted_date = date.strftime('%d-%m-%Y')
        if today > date:
            db.del_data(formatted_date)
        i += 1
    






async def help_com(message: types.Message):
    await bot.send_message(message.from_user.id, "Привет! Я тг бот, который будет вас, а возможно не только вас, регестрировать на волейбол или футбол в стумбуле\nВот мой полный смписок команд:\n/help - это та же команда, что и сейчас вы нажали\n/re_reg - зарегистрирую вас заново на любую игру\n/delete - помогу выбрать и удалить любую информацию которую вы мне когда либо сообщали)")



async def delete_comm(message: types.Message):
    await bot.send_message(message.from_user.id, text="Окей, выбери какую информацию ты хочешь удалить:", reply_markup=nav.kbDEL)

async def call_back_delete(ch, query: types.CallbackQuery):
    if ch == "game":
        await bot.send_message(query.from_user.id, text="Окей, запись на какую игру вы хотите удалить?", reply_markup=nav.kbgames)
    elif ch == "all":
        db.del_all_inf(query.from_user.id)
        reply_markup = types.ReplyKeyboardRemove()
        await bot.send_message(query.from_user.id, text="Вся информация о вас удалена\nЕсли вы решите к нам вернуться, то просто нажимите /start", reply_markup=reply_markup)
        
async def call_back_games(ch, query: types.CallbackQuery):
    if ch == "football":
        await choice_data(query, "football")
    elif ch ==  "volleyball":
        await choice_data(query, "volleyball")

async def   choice_data(message: types.Message, game):
    choice_data_us = []
    choice_time = []
    db.start_inf(message.from_user.id)
    game_id = db.sel_us_game_id(message.from_user.id)
    result = [item[0] for item in game_id]
    for item in result:
        game_inf = db.sel_data(item, game)
        print(game_inf)
        data_id = game_inf[0]
        if db.chek_game(data_id)[0] == game:
            print(data_id)
            choice_time.append(game_inf[1])
            print(data_id, game)
            data_user = db.select_data(data_id)[0]
            choice_data_us.append(data_user)

    if choice_data_us != []:
        await bot.send_message(message.from_user.id, text="Выберете дату и время проведения игры на которые вы зарегистрировались", reply_markup=nav.choicekb(choice_time, choice_data_us))
    else:
        await bot.send_message(message.from_user.id, text="У вас нет активных игр по это игре")


async def call_back_inf(ch, query: types.CallbackQuery):
    await bot.send_message(query.from_user.id, text="Желаете удалить запись на эту игру?", reply_markup=nav.kbwat)
    data_id = db.select_data_id(ch[:-5])[0]
    game_id = db.select_game_id(data_id, ch[-5:])[0]
    db.isert_game_id(query.from_user.id, game_id)




async def delete_inf(message: types.Message):
    if message.text == 'Да':
        game_id = db.s_game_id(message.from_user.id)[0]
        db.del_inf_game(message.from_user.id, game_id)
        await bot.send_message(message.from_user.id, text="Ваша запись на эту игру удалена", reply_markup=nav.mainGames)
    else:
        pass
    await bot.send_message(message.from_user.id, text="Вот несколько команд которые я знаю\n /help - информация обо мне тут\n /re_reg - если бы уже регестрировались во мне, то повторно все делать не нужно) надо просто выбрать игру в которую вы хотите сыграть)\nНу или напишите мне в чат - Узнать информацию о себе")
 #   choice = []
 #   ch_list = db.select_entry("day", message.from_user.id, game)
 #   for ch in ch_list:
 #       choice.append(ch)
 #   await bot.send_message(message.from_user.id, text="Выберете время проведения игры", reply_markup=nav.choicekb(choice))
 #   db.change_step(message.from_user.id, "del")
 #   @router.inline_query(lambda query:query.data[0] == "7")
 #   async def del_entry(query: types.CallbackQuery):
 #       click = query.data[1:]
 #       if db.select("step", message.from_user.id)[0] == "del":
 #           db.del_entry(query.from_user.id, game, click)
 #          await bot.send_message(message.from_user.id, text=f"Информация по {click} ({game}) удалена")
 #      else:
 #          db_list = ["Имя", "Игра", "Зарегестрированно человек с вами", "День", "Время", "Оплата"]
 #           res_inf = db.select_info(message.from_user.id, game, click)
 #           all_inf_list  = list(res_inf[0])
 #           message_text = "Ваши данные: \n"
 #          i = 0
 #          while i < len(db_list):
 #              message_text += f"-{db_list[i]}:   {all_inf_list[i]}\n"
 #               i += 1
 #           await bot.send_message(message.from_user.id, text=message_text)
 #       await bot.send_message(message.from_user.id, text="Желаете удалить эту запись?", reply_markup=nav.kbwat)
 #       @router.message(lambda message:message.text in ['Да', 'Нет'])
 #       async def yes_no(message: types.Message):
 #           if message.text == 'Да':
 #               db.del_entry(message.from_user.id, game, click)
 #              await bot.send_message(message.from_user.id, text=f"Информация по {click} ({game}) удалена")
 #               await bot.send_message(message.from_user.id, text="Вот несколько команд которые я знаю\n /help - информация обо мне тут\n /re_reg - если бы уже регестрировались во мне, то повторно все делать не нужно) надо просто выбрать игру в которую вы хотите сыграть)\n /delete - нажав на эту команду вы сможете выбрать какую информацию о вас вы хотите удалить или же отменить запись на игру")
 #           else:
 #               await bot.send_message(message.from_user.id, text="Супер! Тогда оставляем все как есть)\nВот несколько команд которые я знаю\n /help - информация обо мне тут\n /re_reg - если бы уже регестрировались во мне, то повторно все делать не нужно) надо просто выбрать игру в которую вы хотите сыграть)\n /delete - нажав на эту команду вы сможете выбрать какую информацию о вас вы хотите удалить или же отменить запись на игру")

#@dp.callback_query_handler()
#async def asdafg(query: types.CallbackQuery):
 #   logging.warning(query.data)


#@dp.callback_query_handler(lambda query: query.data in [f"Пн, {nav.data[nav.day]}", f"Вт, {nav.data[nav.day]}", f"Ср, {nav.data[nav.day]}", f"Чт, {nav.data[nav.day]}", f"Пт, {nav.data[nav.day]}", f"Сб, {nav.data[nav.day]}", f"Вс, {nav.data[nav.day]}"])

    #await callback_query.message.reply("Супер! А теперь выберете время", reply_markup=nav.inkbtime)


async def what_date(choice):
    global weekDays, weekDRus, user
    current_day = datetime.datetime.now().strftime("%A")  
    day = choice
    i = 0
    k = 0
    while weekDays[i] != current_day:
        i += 1
    j = i
    while weekDRus[j] != day:
        j += 1
        if j >= len(weekDRus):
            k = j
            j = j % len(weekDRus)
    count = k + j - i
    days = count
    future_date = datetime.datetime.now() + datetime.timedelta(days=days)
    choice = future_date.strftime("%Y-%m-%d")
    return choice



       #db.update_something(user.id, "reg_volleyball", "stage", "registration_completed")





#        if db.select("game", message.from_user.id)[0] == "volleyball":
#            await bot.send_message(message.from_user.id, "Это круто, что ты хочешь поиграть в волейбол! А теперь напиши мне сколько вас будет человек. Или же ты один будешь?")
#        else:
#            await bot.send_message(message.from_user.id, "Это круто, что ты хочешь поиграть в футбол! А теперь напиши мне сколько вас будет человек. Или же ты один будешь?")






async def inf(message: types.Message):
    await bot.send_message(message.from_user.id, text="Выберете игру:", reply_markup=nav.kbgames)
    #message_text = "Ваши данные: \n"
    #i = 0
    #while i < len(database_list):
    #    message_text += f"-{database_list[i]}:   {name_list[i]}\n"
    #    i += 1
   # await bot.send_message(message.from_user.id, text=message_text)



#Функция возврата на шаг назад
async def goback(message: types.Message):
    lvls = ['lvl1', 'lvl2', 'lvl3', 'lvl4', 'lvl5', 'lvl6', 'maxlvl' ]
    print(db.countprog(message.from_user.id))
    if db.countprog(message.from_user.id) != None:

        lvl = db.sel_lvl(message.from_user.id)[0]
        i = 0
        if lvl != lvls[0]:
            while lvl != lvls[i]:
                i += 1
            #if lvl == 'maxlvl':
            #   backstep = lvls[i]
            #else:
        backstep = lvls[i-1]
        if backstep == 'lvl1':
            await re_reg_com(message)
        elif backstep == 'lvl2':
            ch = db.click_game(message.from_user.id)[0]
            if ch == "volleyball":
                ch = "🏐 ВОЛЕЙБОЛ"
            else:
                ch = "⚽️ ФУТБОЛ"
            game_mes = return_mes(message, ch)
            await choice_game(game_mes, False)
        elif backstep == 'lvl3':
            await show_schedule_data(message, False)


        elif backstep == 'lvl4':
            ch = db.click_data(message.from_user.id)[0]
            await show_schedule_time(message, ch, False)
        elif backstep == 'lvl5':
            return_seats(message)
            ch = db.click_time(message.from_user.id)[0]
            await call_back_time(ch, message, False)
        elif backstep == 'lvl6':
            return_seats(message)
            ch = db.click_people(message.from_user.id)[0]
            mes = return_mes(message, ch)
            await quantity_people(mes, False)
        else:
            await bot.send_message(message.from_user.id, text="Мы и так в начале куда уж дальше то")
    else:
        await re_reg_com(message)
    

def return_seats(message: types.Message):
    p = db.click_people(message.from_user.id)[0]
    if p != None:
        res_data = db.select_game_us(message.from_user.id)[1]
        res_time = db.select_game_us(message.from_user.id)[2]
        data_id = db.select_id_wh_data(res_data)[0]
        game_id = db.select_game_id(data_id, res_time)[0]
        row = db.select_place(game_id)[0]
        db.update_places((row + p), data_id, game_id)

def return_mes(message: types.Message, text):
    orig_mes = message
    up_mes = types.Message(
        message_id=orig_mes.message_id,
        date=orig_mes.date,
        chat=orig_mes.chat,
        from_user=orig_mes.from_user,
        text=text,
        entities=orig_mes.entities,
        reply_markup=orig_mes.reply_markup
    )
    return up_mes



async def check_lvl(message: types.Message, lvl, vector):
    lvls = ['lvl1', 'lvl2', 'lvl3', 'lvl4', 'lvl5', 'lvl6', 'maxlvl']
    print("check_lvl:")
    print(lvl, "lvl", vector, "vector")
    i = 0
    now_lvl = db.check_lvl(message.from_user.id)[0]
    while i < len(lvls):
        if now_lvl == lvls[i]:
            count_nowlvl = i
        if lvl == lvls[i]:
            count_lvl = i
        i += 1
    if vector == True:
        if count_lvl < count_nowlvl:
            res = False
        else:
            res = True
    else:
        if count_lvl > count_nowlvl:
            res = False
        else:
            res = True
        
    return res

async def main():
    dp = Dispatcher()
    dp.include_router(router)
    await dp.start_polling(bot, skip_updates=True)


if __name__ == "__main__":
    asyncio.run(main())