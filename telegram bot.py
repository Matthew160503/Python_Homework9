import telebot
from telebot import types
import random
import emoji

user_sweets = 0
sweets = 221
count_bot_sweets = 0
count_user_sweets = 0
flag = ''
name1 =''
name2 ='bot'
bot = telebot.TeleBot('5691635955:AAHHgMzSQue0pey8Ew4qacm-5sntMJ5h__o')

@bot.message_handler(commands = ['start'])
def start(message):
    bot.send_message(message.chat.id, f'Привет,{message.from_user.first_name}!. Сейчас'+
                    ' мы поиграем в игру "221 конфет на столе. Задача игры состоит в том,'+
                    'чтобы взять больше конфет со стола чем бот, но за один ход'+
                    ' можно взять максимум 25 конфет. Если готов, вбивай команду /go')
    bot.register_next_step_handler(message, start_game)

@bot.message_handler(commands= ['go'])
def start_game(message):
    global name1, name2, flag
    name1 = message.from_user.first_name
    first_turn = random.choice([name1, name2])
    if first_turn == name1:
        flag = name1
        bot.send_message(message.chat.id,f'Первым ходит {name1}')
        user(message)
    else:
        flag = name2
        bot.send_message(message.chat.id,f'Первым ходит {name2}')
        Bot(message)

def Bot(message):
    global count_bot_sweets, user_sweets
    user_sweets = random.randint(1, 25)
    count_bot_sweets += user_sweets
    bot.send_message(message.chat.id,f'Бот взял {user_sweets} конфет')
    get_count(message)

def user(message):
    bot.send_message(message.chat.id, f'введите количество конфет не больше 25')
    bot.register_next_step_handler(message, user_input)

def user_input(message):
    global user_sweets, count_user_sweets
    user_sweets = int(message.text)
    count_user_sweets += user_sweets
    get_count(message)

def get_count(message):
    global sweets, user_sweets
    sweets = sweets - user_sweets
    bot.send_message(message.chat.id, f'Осталось {sweets} конфет на столе')
    if sweets <= 0:
        if count_user_sweets > count_bot_sweets:
            bot.send_message(message.chat.id,
            emoji.emojize(f'Победил игрок {message.from_user.first_name}, набравший {count_user_sweets} конфет :red_heart:'))
        else:
            bot.send_message(message.chat.id,
            emoji.emojize(f'Победил игрок {name2}, набравший {count_bot_sweets} конфет :thumbs_up:'))
    else: 
        peredachya_hoda(message)
    
def peredachya_hoda(message):
    global flag, name1, name2
    if flag == name1:
        bot.send_message(message.chat.id, f'Теперь ходит {name2}')
        flag = name2
        Bot(message)
    else:
        flag = name1
        bot.send_message(message.chat.id, f'Теперь ходит {name1}')
        user(message)

@bot.message_handler(commands=['button'])
def button(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button1 = types.KeyboardButton('start')
    markup.add(button1)
    bot.send_message(message.chat.id,"Выбери ниже", reply_markup=markup)

bot.infinity_polling()