import telebot
import config
import time
import data_save
import formating
import sqlite3

# bot connect
token = config.token
bot = telebot.TeleBot(token)

#Время на боте ЧЧ:ММ
mytime = time.strftime("%H:%M", time.localtime())


# command START
@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, config.hello_mess)
    custom_name = data_save.custom_name(message)
    data_save.log_save(message, mytime)
    if custom_name != "Незнакомец":
        time.sleep(2)
        bot.send_message(message.chat.id, config.iknowu_mess + custom_name)
        user_status = 1
        data_save.status_update(message, user_status)
    else:
        time.sleep(2)
        bot.send_message(message.chat.id, (config.name_mess + message.from_user.first_name + "?"))
        user_status = 0
        data_save.login_save(message, time, user_status)
        data_save.status_update(message, user_status)

# команда для просмотра имени обращения
@bot.message_handler(commands=['name'])
def whatmyname(message):
    bot.send_message(message.chat.id, "Тебя зовут " + data_save.custom_name(message))
    data_save.log_save(message, mytime)

# команда Reset, стирает данные из базы DATA
@bot.message_handler(commands=['reset'])
def reset(message):
    bot.send_message(message.chat.id,"До свидания, " + data_save.custom_name(message) + "\n" + config.reset_mess)
    data_save.reset(message)
    data_save.log_save(message, mytime)
# Если юзверь просит время
@bot.message_handler(commands=['time'])
def send_time(message):
    bot.send_message(message.chat.id, "Сейчас " + time.strftime("%H:%M:%S", time.localtime()))
    data_save.log_save(message, mytime)

# Инфо бота
@bot.message_handler(commands=['help', 'info'])
def about_bot(message):
    bot.send_message(message.chat.id, config.info_mess)
    data_save.log_save(message, mytime)



# Подключение к БД и запись статуса  - 0 - знакомство, 1 - готовность к приему напоминания, 2- запоминание обращения   
@bot.message_handler(func = lambda message: data_save.status_check(message) == 0)
def save_username(message):
    print(message.from_user.first_name + " " + message.text)
    if message.text.lower() == "да":
        bot.send_message(message.chat.id, "Хорошо, " + message.from_user.first_name)
        user_status = 1
        data_save.status_update(message, user_status)
        data_save.log_save(message, mytime)
    else:
        bot.send_message(message.chat.id, "А как тебя звать?")
        user_status = 2
        data_save.status_update(message, user_status)
        data_save.log_save(message, mytime)

# восстановление статуса 1, регистрация завершена
@bot.message_handler(func = lambda message: data_save.status_check(message) == 2)
def save_custom_username(message):
    bot.send_message(message.chat.id, "Хорошо, " + message.text + ", будем знакомы.")
    data_save.custom_name_update(message)
    user_status = 1
    data_save.status_update(message, user_status)
    bot.send_message(message.chat.id, config.info_mess)
    data_save.log_save(message, mytime)

# отслеживание запроса 
@bot.message_handler(func = lambda message: formating.check_mess(message))
def save_notification(message):
    data_save.task_save(message)
    bot.send_message(message.chat.id, "Хорошо, я напомню")
    data_save.log_save(message, mytime)
    

# если сообщение не обработано, то оно попадает сюда
@bot.message_handler(content_types=["text"])
def logg(message):
    bot.send_message(message.chat.id, "Вы, вероятно, ошиблись:(")
    data_save.non_read(message, time)
    data_save.log_save(message, mytime)

# проверка заданий

# опрос сервера телеграм
bot.polling()
 