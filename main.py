from flask import Flask, url_for, render_template, session, request, redirect, flash
import sqlitedb as db

app = Flask(__name__)
app.secret_key = 'rulev-secret-key'

@app.route('/')
def redirect_feed():
    return redirect(url_for('feed'))

@app.route('/feed')
def feed():
    all_threads = db.parse_threads()
    return render_template('feed.html', all_threads=all_threads)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'token' in session:
        decoded_token = db.verifyToken(session['token'])
        if decoded_token:
            return redirect(url_for('me'))
    if request.method == 'POST':
        print('начал')
        email = request.form.get('email')
        password = request.form.get('password')

        token = db.loginAccount(email, password)
        if token == None:
            return redirect(url_for('login'))
        else:
            session['border-radius'] = 0
            session['token'] = token


        flash('Вы успешно вошли в аккаунт', 'successful')
        return redirect(url_for('me'))
    
    return render_template('login.html')

@app.route('/me')
def me():
    if 'token' in session:
        decoded_token = db.verifyToken(session['token'])
        if decoded_token:
            email = decoded_token.get('email')
            username = decoded_token.get('username')
            return render_template('me.html', me_email=email, me_username=username)
        else:
            flash('Неверный или истекший токен', 'error')
            return redirect(url_for('login'))
    else:
        return redirect(url_for('login'))

@app.route('/neural')
def neural():
    return render_template('neural.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if 'token' in session:
        decoded_token = db.verifyToken(session['token'])
        if decoded_token:
            flash('Сначала стоит выйти перед тем как регистрироваться')
            return redirect(url_for('me'))
        flash('wtf')
        return redirect(url_for('register'))
        
    if request.method == 'POST':
        print('Создание - Запрос')
        email = request.form.get('email')
        password = request.form.get('password')

        token = db.create_account(email, password)

        if token == (False, None):
            flash('Вы точно правильно написали почту?')
            return redirect(url_for('register'))
        elif token == (True, False):
            flash('Проверьте написание пароля')
            return redirect(url_for('register'))
        else:
            session['token'] = token


        flash('Аккаунт успешно создан!')
        return redirect(url_for('login'))
    
    return render_template('register.html')


@app.route('/change_password', methods=['POST'])
def change_password():

    flash('Пароль не обновлен')
    return redirect(url_for('me'))


@app.route('/logout')
def logout():
    if 'token' in session:
        session.pop('border-radius', None)
        session.pop('token', None)
    flash('Вы вышли из аккаунта')
    return redirect(url_for('login'))


# Бред!

@app.route('/set_border_radius', methods=["POST"])
def set_border_radius():
    new_radius = request.form.get('border-radius')
    if session['border-radius'] == new_radius:
        flash('Вы ничего не поменяли...')
    else:
        session['border-radius'] = new_radius
        flash('Теперь закругление еще круче!')
    return redirect(url_for('me'))

@app.errorhandler(404)
@app.route('/404')
def error404(e):
    return render_template('404.html')

@app.route('/new', methods=['POST', 'GET'])
def new_thread():
    if 'token' in session:
        decoded_token = db.verifyToken(session['token'])
        if decoded_token:
            if request.method == 'POST':
                userid = db.get_userid(decoded_token.get('email'))
                print('Создание - Успешно', userid)
                db.create_thread(request.form.get('name'), userid)
                return redirect(url_for('feed'))
            return render_template('newthread.html')
        
    flash('Сначала войдите в аккаунт')
    return redirect(url_for('feed'))
    


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=8000)