import jwt
import datetime

SECRET_KEY = 'your_secret_key'

def generate_jwt(email, username):
    current_time = datetime.datetime.now(datetime.timezone.utc)
    
    payload = {
        'email': email,
        'username': username,
        'exp': current_time + datetime.timedelta(hours=2)
    }
    
    token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
    
    return token

def verify_jwt(token):
    try:
        decoded_token = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        print('Пользователь аутентифицирован:', decoded_token['email'])
        return decoded_token
    except jwt.ExpiredSignatureError:
        print('Срок действия токена истек')
        return None
    except jwt.InvalidTokenError:
        print('Неверный токен')
        return None
