from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
import logging

#1
btnreg = InlineKeyboardButton(text='Регистрация', callback_data="yes")
kb = InlineKeyboardMarkup(row_width=2,inline_keyboard=[[btnreg]])

#kb.add(btnreg)

#2

btnVB = KeyboardButton(text='🏐 ВОЛЕЙБОЛ')
btnFB = KeyboardButton(text='⚽️ ФУТБОЛ')

mainGames = ReplyKeyboardMarkup(resize_keyboard=True,keyboard=[[btnVB, btnFB]])
#mainGames = ReplyKeyboardMarkup(resize_keyboard=True,keyboard=[[KeyboardButton(text='🏐 ВОЛЕЙБОЛ'), KeyboardButton(text='⚽️ ФУТБОЛ')]])
#mainGames.add(btnVB, btnFB)




btnBack = KeyboardButton(text='◀️ Назад')
kbback = ReplyKeyboardMarkup(resize_keyboard=True, keyboard=[[btnBack]])

#3

btnRul = KeyboardButton(text='📋 Правила')
btnRecom = KeyboardButton(text='🤙 Рекомендации к тренировке')
btnMakeing = KeyboardButton(text='😎 Записаться')
btnSchedule = KeyboardButton(text='🗓 Расписание')

detalis = ReplyKeyboardMarkup(resize_keyboard=True, keyboard=[[btnRul, btnRecom, btnMakeing, btnSchedule, btnBack]])
#detalis.add(btnRul, btnRecom, btnMakeing, btnSchedule, btnBack)

#5
def inkb(data, days):

    keyboard = []
    day = 0
    for day, date in zip(days, data):
        button = InlineKeyboardButton(text=f"{day} ({date})", callback_data=f"*{date}")
        keyboard.append([button])
        
        
    inkb1 = InlineKeyboardMarkup(inline_keyboard=keyboard)
    days.clear()
    data.clear()

    return inkb1
    

#6
def timekb(time: list, place: list):

    keyboard = []
    i = 0
    while i < len(time):
        button = InlineKeyboardButton(text=f"{time[i]} (мест на эту игру: {place[i]})", callback_data=f"9{time[i]} {place[i]}")
        keyboard.append([button])
        i += 1


    intimekb = InlineKeyboardMarkup(inline_keyboard=keyboard)
    time.clear()
    return intimekb


#5

btnCash = KeyboardButton(text='💷 Наличные')
btnCard = KeyboardButton(text='💳 Перевод')

choisePay = ReplyKeyboardMarkup(resize_keyboard=True, keyboard=[[btnCash, btnCard, btnBack]])
#choisePay.add(btnCash, btnCard, btnBack)

#6

btnInf = KeyboardButton(text='Узнать информацию о себе')

kbINFO = ReplyKeyboardMarkup(resize_keyboard=True, keyboard=[[btnInf, btnBack]])
#kbINFO.add(btnInf, btnBack)

btnyes = KeyboardButton(text='Да')
btnno = KeyboardButton(text='Нет')
kbwat = ReplyKeyboardMarkup(resize_keyboard=True, keyboard=[[btnyes, btnno]])
#kbwat.add(btnyes, btnno)

#7

def choicekb(choice_time, choice_data_us):
    keyboard = []
    i = 0
    while i < len(choice_time):
        button = InlineKeyboardButton(text=f"{choice_data_us[i]} (Время проведения игры: {choice_time[i]})", callback_data=f"7{choice_data_us[i]}{choice_time[i]}")
        keyboard.append([button])
        i += 1
    
    data_timekb = InlineKeyboardMarkup(inline_keyboard=keyboard)
    choice_time.clear()
    choice_data_us.clear()
    return data_timekb





btnDel = InlineKeyboardButton(text="Информация по записям", callback_data="game")
btnDel2 = InlineKeyboardButton(text="Вся информация обо мне", callback_data="all")

kbDEL = InlineKeyboardMarkup(row_width=2, inline_keyboard=[[btnDel, btnDel2]])

#kbDEL.add(btnDel, btnDel2)


btnfoot = InlineKeyboardButton(text="Футбол", callback_data="football")
btnvoll = InlineKeyboardButton(text="Волейбол", callback_data="volleyball")

kbgames = InlineKeyboardMarkup(row_width=2, inline_keyboard=[[btnfoot, btnvoll]])

#kbgames.add(btnfoot, btnvoll)

btnBack2 = KeyboardButton(text='◀️ Назад')
back = ReplyKeyboardMarkup(resize_keyboard=True, keyboard=[[btnBack2]])
#back.add(btnBack2)

btncom = KeyboardButton(text='Завершить регистрацию')
kbcom = ReplyKeyboardMarkup(resize_keyboard=True, keyboard=[[btncom, btnBack]])



peremennaya = 1