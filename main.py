import pandas as pd
import datetime
from tok import token
import telebot
from telebot import types
import time
import schedule
from threading import Thread

bot = telebot.TeleBot(token)

answers = []
question_numbers = ['Стресс', 'Общее самочувствие', 'ЧД', 'Время сна', 'Качество диеты','ВСЕ']
question_number = 0

def send_message():
    keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    btn1 = types.KeyboardButton(text='1')
    btn2 = types.KeyboardButton(text='2')
    btn3 = types.KeyboardButton(text='3')
    btn4 = types.KeyboardButton(text='4')
    btn5 = types.KeyboardButton(text='5')
    btn6 = types.KeyboardButton(text='6')
    btn7 = types.KeyboardButton(text='7')
    btn8 = types.KeyboardButton(text='8')
    btn9 = types.KeyboardButton(text='9')
    btn10 = types.KeyboardButton(text='10')
    keyboard.add(btn1,btn2,btn3,btn4,btn5,btn6,btn7,btn8,btn9,btn10)

    bot.send_message(447999564, 'Что по стрессу', reply_markup=keyboard)


@bot.message_handler()
def next_question(message):
    # bot.register_next_step_handler(message, record_answer)
    global question_number
    question_number+=1
    print (question_number)
    answer = message.text


    if question_number <6:
        answers.append(answer)
        bot.send_message(447999564, question_numbers[question_number])
        if question_numbers[question_number] == 'ВСЕ':

            try:
                df = pd.read_excel('дневник 2254.xlsx', usecols='B:G')
                answers.insert(0, datetime.datetime.now())
                df.loc[len(df.index)] = answers
                df.to_excel('дневник 2254.xlsx')
                answers.clear()
                question_number = 0
            except:
                answers.insert(0, datetime.datetime.now())
                df.loc[len(df.index)] = answers
                df.to_excel('дневник 2254.xlsx')
                answers.clear()
                question_number = 0

    print(answers)


def record_answer(message):
    answer = message.text
    answers.append(answer)
    print(answers)
    next_question(message)

def main1():
    print('Бот запущен')
    schedule.every().day.at("21:28:30").do(send_message)
    while True:
        schedule.run_pending()
        time.sleep(1)


Thread(target=main1).start()
bot.polling(none_stop=True, interval=0)