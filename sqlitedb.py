import sqlite3
import myjwt
import os

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

def createAccount(email, password):
    with get_db() as conn:
        print('aaaaa')
        c = conn.cursor()
        c.execute("INSERT INTO users (email, username, password, creation_date) VALUES (?, ?, ?, ?)",
                  (email, None, password, '111'))
        conn.commit()

def loginAccount(email, password):
    with get_db() as conn:
        c = conn.cursor()
        c.execute("SELECT password, username FROM users WHERE email = ?", (email,))
        result = c.fetchone()

        if result and result[0] == password:
            token = myjwt.generate_jwt(email, result[1])
            print('УСПЕШНО ВОШЕЛ')
            print('JWT Token:', token)
            return token
        else:
            print('не вышло')
            return None

def verifyToken(token):
    decoded_token = myjwt.verify_jwt(token)
    if decoded_token:
        return decoded_token
    return None


# Пример использования
# myemail = 'usernamegmail2'
# mypassword = '1231232'

# createAccount(myemail, mypassword)
# token = loginAccount(myemail, mypassword)
