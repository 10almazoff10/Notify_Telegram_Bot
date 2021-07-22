import sqlite3

# сохранение данных в базу DATA
def login_save(message, time, user_status):
  conn = sqlite3.connect('data.db')
  cursor = conn.cursor()
  
  date_rus = time.strftime("%d.%m.%Y %H:%M:%S", time.localtime(message.date))
  id_user = message.from_user.id
  name = message.from_user.first_name
  last_name = message.from_user.last_name
  usertag = message.from_user.username
  custom_name = name
  
  saving_data = [(id_user, date_rus, name, last_name, usertag, user_status, custom_name)]
  print(saving_data)
  cursor.executemany("""INSERT INTO users_data VAlUES
	              			(?, ?, ?, ?, ?, ?, ?) 
				            """, saving_data)
  conn.commit()

def status_update(message, user_status):
  conn = sqlite3.connect('data.db')
  cursor = conn.cursor()
  
  id_user = message.from_user.id
  update_data = [(user_status), (id_user)]
  sql = "UPDATE users_data SET status = (?) WHERE id = (?)"
  
  cursor.execute(sql, update_data)
  conn.commit()


def status_check(message):
  if message.from_user.id < 1 or message.from_user.id == "":
    status = 0
    return status

  else:
    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()
    sql = "SELECT * FROM users_data WHERE id=?"
    cursor.execute(sql, [(message.from_user.id)])
    status_all = cursor.fetchone()
    status = status_all[5]
    return status

  
def custom_name_update(message):
  conn = sqlite3.connect('data.db')
  cursor = conn.cursor()
  name_user = message.text
  id_user = message.from_user.id
  update_data = [(name_user), (id_user)]
  sql = "UPDATE users_data SET Обращение = (?) WHERE id = (?)"
  
  cursor.execute(sql, update_data)
  conn.commit()

def custom_name(message):
  conn = sqlite3.connect('data.db')
  cursor = conn.cursor()
  sql = "SELECT * FROM users_data WHERE id=?"
  cursor.execute(sql, [(message.from_user.id)])
  status_all = cursor.fetchone()
  if status_all != None:
    cust_name = status_all[6]
  else:
    cust_name = "Незнакомец"
   
  return cust_name


def reset(reset_data):
  conn = sqlite3.connect('data.db')
  cursor = conn.cursor()
  id_user = reset_data.from_user.id
  data_delete =[(id_user)]
  sql = "DELETE FROM users_data WHERE id = (?)"
  cursor.execute(sql, data_delete)
  conn.commit()

def non_read(message, time):
  conn = sqlite3.connect('data.db')
  cursor = conn.cursor()
  
  date_rus = time.strftime("%d.%m.%Y %H:%M:%S", time.localtime(message.date))
  id_user = message.from_user.id
  text_message = message.text
  saving_data = [(id_user, date_rus, text_message)]
  cursor.executemany("""INSERT INTO non_read VAlUES
	              			(?, ?, ?) 
				            """, saving_data)
  conn.commit()

def task_save(message):
  conn = sqlite3.connect('data.db')
  cursor = conn.cursor()

  time_for_noty = message.text.split(" ")[2]
  id_user = message.from_user.id
  text_message = message.text[15:]

  saving_data = [(id_user, time_for_noty, text_message)]
  cursor.executemany("""INSERT INTO tasks VAlUES
	              			(?, ?, ?) 
				            """, saving_data)
  conn.commit()
  print("Запись от пользователя ", message.from_user.first_name, " сохранена.")


#print into log
def log_save(mes, tim):
  user_name = mes.from_user.first_name
  text_from_user = mes.text
  time_log = tim
  print(time_log + " " + user_name + " " + text_from_user)
  f = open('log.txt', 'a')
  f.write(time_log + " " + user_name + " " + text_from_user + '\n')
  f.close()