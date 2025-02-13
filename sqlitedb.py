import sqlite3
import myjwt
import os
import re

currentdirectory = os.path.dirname(os.path.abspath(__file__))

def get_db():
    # Создаем соединение с базой данных
    conn = sqlite3.connect('lbvforum.db')
    conn.row_factory = sqlite3.Row
    return conn

def firstLaunch():
    with get_db() as conn:
        c = conn.cursor()
        c.execute("""CREATE TABLE IF NOT EXISTS users(
            email text, 
            username text,
            password text,
            creation_date integer         
        )""")
        conn.commit()

def DB_create_account(email, password):
    with get_db() as conn:
        c = conn.cursor()
        c.execute("INSERT INTO users (email, username, password, creation_date) VALUES (?, ?, ?, ?)",
                  (email, None, password, '111'))
        conn.commit()
        print('Создан аккаунт')

def loginAccount(email, password):
    with get_db() as conn:
        c = conn.cursor()
        c.execute("SELECT password, username FROM users WHERE email = ?", (email,))
        result = c.fetchone()

        if result and result[0] == password:
            token = myjwt.generate_jwt(email, result[1])
            print('Логин - Успешно вошел')
            print('JWT Token:', token)
            return token
        else:
            print('Логин - Вход отклонен')
            return None

def verifyToken(token):
    decoded_token = myjwt.verify_jwt(token)
    if decoded_token:
        return decoded_token
    return None

def create_account(email, password):
    password_pattern = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).{8,}$'
    email_pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'

    if re.match(email_pattern, email) is None:
        return(False, None)
    
    if re.match(password_pattern, password) is None:
        return(True, False)
    
    DB_create_account(email=email, password=password)
    return(True)



# Пример использования
# myemail = 'usernamegmail2'
# mypassword = '1231232'

# create_account(myemail, mypassword)
# token = loginAccount(myemail, mypassword)