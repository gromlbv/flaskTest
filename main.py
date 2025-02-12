from flask import Flask, url_for, render_template, session, request, redirect, flash
import json


x =  '{ "name":"John", "age":30, "city":"New York"}'

y = json.loads(x)

print(y["age"])

app = Flask(__name__)
app.secret_key = 'rulev-secret-key'

@app.route('/')
def redirect_feed():
    return redirect(url_for('feed'))

@app.route('/feed')
def feed():
    return render_template('feed.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'email' in session:
        return redirect(url_for('me'))
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        session['email'] = email
        flash('Вы успешно вошли в аккаунт', 'successful')

        return redirect(url_for('me'))

    
    return render_template('login.html')

@app.route('/me')
def me():
    if 'email' in session:
        return render_template('me.html')

    else:
        return redirect(url_for('login'))

@app.route('/set_border_radius', methods=["POST"])
def set_border_radius():
    session['border-radius'] = request.form.get('border-radius')
    return redirect(url_for('me'))

@app.route('/logout')
def logout():
    if 'email' in session:
        session.pop('email', None)
        session.pop('border-radius', None)
        session.pop('_flashes', None)
    flash('Вы вышли из аккаунта')
    return redirect(url_for('login'))

@app.errorhandler(404)
@app.route('/404')
def error404():
    return render_template('404.html')


@app.route('/register')
def register():
    if 'email' in session:
        flash('Сначала стоит выйти перед тем как регистрироваться')
        return redirect(url_for('me'))
    return render_template('register.html')

if __name__ == "__main__":
    app.run(debug=True)
