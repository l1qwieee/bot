from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardRemove
defualtkb = []

#1
btnReg = KeyboardButton(text='Узнать кто записался')
btnSch = KeyboardButton(text='Настроить расписание')
btnNewus = KeyboardButton(text='Записать нового пользователя')
defualtkb.append([btnReg])
defualtkb.append([btnSch])
defualtkb.append([btnNewus])
whoreg = ReplyKeyboardMarkup(resize_keyboard=True, keyboard=defualtkb)
defualtkb.clear()

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

def kbtime(times, seats):
    keyboard = []
    for count, item in zip(times, seats):
        button = InlineKeyboardButton(text=f"{count}({item} мест)", callback_data=f"9{count}")
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


btnNext = KeyboardButton(text="Следующий шаг")
btnBack = KeyboardButton(text="Назад")

kbstep = ReplyKeyboardMarkup(resize_keyboard=True, keyboard=[[btnNext, btnBack]])


btn1 = KeyboardButton(text="1👍")
btn2 = KeyboardButton(text="2👎")
admuser = ReplyKeyboardMarkup(resize_keyboard=True, keyboard=[[btn1, btn2]])

btnCash = KeyboardButton(text='💷 Наличные')
btnCard = KeyboardButton(text='💳 Перевод')
defualtkb.append([btnCash])
defualtkb.append([btnCard])

payment = ReplyKeyboardMarkup(resize_keyboard=True, keyboard=defualtkb)
defualtkb.clear()

btn_1 = KeyboardButton(text='1')
btn_2= KeyboardButton(text='2')
btn_3 = KeyboardButton(text='3')
btn_4 = KeyboardButton(text='4')
btn_5 = KeyboardButton(text='5')
btn_6 = KeyboardButton(text='6')
btn_itsok = KeyboardButton(text='Завершить регистрацию')
defualtkb.append([btn_1, btn_2, btn_3])
defualtkb.append([btn_4, btn_5, btn_6])
defualtkb.append([btn_itsok])


chang_the_data = ReplyKeyboardMarkup(resize_keyboard=True, keyboard=defualtkb)
defualtkb.clear()


kbremove = ReplyKeyboardRemove()