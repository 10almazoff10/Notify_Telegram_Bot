import telebot
import time
import sqlite3
import config

# bot connect
token = config.token
bot = telebot.TeleBot(token)

def get_tasks():
    print("Get Task v 0.0.5")
    while True:
        conn = sqlite3.connect('data.db')
        cursor = conn.cursor()
        sql = "SELECT * FROM tasks WHERE time=?"
        cursor.execute(sql, [(time.strftime("%H:%M", time.localtime()))])
        user_task = cursor.fetchone()
        print("Поиск...")
        if user_task != None:
            id_user = user_task[0]
            text_user_task = user_task[2]
            sql = "DELETE FROM tasks WHERE time = (?)"
            cursor.execute(sql, [(time.strftime("%H:%M", time.localtime()))])
            conn.commit()
            print("Обнаружена запись от пользователя " + str(id_user) + "\nЗапись отправлена и удалена из базы.")
            bot.send_message(id_user, "Братишкас, помнишь ты просил напомнить '" + text_user_task + "' \nНу лови, хуле))")
        else:
            print("Заданий нет.")
            time.sleep(5)

get_tasks()