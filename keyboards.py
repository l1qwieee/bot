from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

#1
btnReg = KeyboardButton(text='Узнать кто записался')
btnSch = KeyboardButton(text='Настроить расписание')

whoreg = ReplyKeyboardMarkup(resize_keyboard=True, keyboard=[[btnReg, btnSch]])

#2
btnVB = KeyboardButton(text='🏐 ВОЛЕЙБОЛ')
btnFB = KeyboardButton(text='⚽️ ФУТБОЛ')

def kbdata(days):
    keyboard = []
    for day in days:
        button = InlineKeyboardButton(text=f"{day}", callback_data=f"*{day}")
        keyboard.append([button])
    inkb1 = InlineKeyboardMarkup(inline_keyboard=keyboard)
    days.clear()
    return inkb1

def kbtime(times):
    keyboard = []
    for count in times:
        button = InlineKeyboardButton(text=f"{count}", callback_data=f"9{count}")
        keyboard.append([button])

    inkb2 = InlineKeyboardMarkup(inline_keyboard=keyboard)
    times.clear()
    return inkb2

mainGames = ReplyKeyboardMarkup(resize_keyboard=True, keyboard=[[btnVB, btnFB]])

#3
btnin = InlineKeyboardButton(text='Пн', callback_data="Пн")
btnin2 = InlineKeyboardButton(text='Вт', callback_data="Вт")
btnin3 = InlineKeyboardButton(text='Ср', callback_data="Ср")
btnin4 = InlineKeyboardButton(text='Чт', callback_data="Чт")
btnin5 = InlineKeyboardButton(text='Пт', callback_data="Пт")
btnin6 = InlineKeyboardButton(text='Cб', callback_data="Сб")
btnin7 = InlineKeyboardButton(text='Вс', callback_data="Вс")

inkb = InlineKeyboardMarkup(row_width=7, inline_keyboard=[[btnin, btnin2, btnin3, btnin4, btnin5, btnin6, btnin7]])

#4

btnt = InlineKeyboardButton(text="12:00", callback_data="12:00")
btnt2 = InlineKeyboardButton(text="17:00", callback_data="17:00")
btnt3 = InlineKeyboardButton(text="20:30", callback_data="20:30")

inkbtime = InlineKeyboardMarkup(row_width=3, inline_keyboard=[[btnt, btnt2, btnt3]])

btningames = InlineKeyboardButton(text="Волейбол", callback_data="volleyball")
btningames2 = InlineKeyboardButton(text="Футбол", callback_data="football")

InmainGames = InlineKeyboardMarkup(row_width=2, inline_keyboard=[[btningames, btningames2]])

btnyes = InlineKeyboardButton(text="Да", callback_data="yes")
btnno = InlineKeyboardButton(text="Нет", callback_data="no")

kbyes = InlineKeyboardMarkup(row_width=2, inline_keyboard=[[btnyes, btnno]])


btndel = InlineKeyboardButton(text="Удалить дату", callback_data="del")
btnchange = InlineKeyboardButton(text="Поменять дату", callback_data="change")

kbset = InlineKeyboardMarkup(row_width=2, inline_keyboard=[[btndel, btnchange]])
