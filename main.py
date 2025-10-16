from flask import Flask, render_template, request, jsonify, session, flash, redirect, url_for
import random
import string
import os

app = Flask(__name__)
app.secret_key = 'your-secret-key-123'

# Храним пользователей в переменной (вместо фиксированного списка)
USERS_FILE = 'users.txt'

def generate_password(length, difficulty):
    """Генерация пароля в зависимости от сложности"""
    if difficulty == 'easy':
        characters = string.ascii_letters
    else:
        characters = string.ascii_letters + string.digits + "!@#$%^&*()_+-=[]{}|;:,.<>?"
    password = ''.join(random.choice(characters) for _ in range(length))
    return password



def load_users():
    """Загрузка пользователей из файла"""
    users = []
    if os.path.exists(USERS_FILE):
        try:
            with open(USERS_FILE, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if line and ':' in line:
                        username, password, role = line.split(':', 2)
                        users.append({
                            'username': username,
                            'password': password,
                            'role': role
                        })
        except Exception as e:
            print(f"Ошибка при загрузке пользователей: {e}")


    if not users:
        default_users = [
            {'username': 'admin', 'password': 'admin', 'role': 'admin'},
            {'username': 'user', 'password': 'user', 'role': 'user'}
        ]
        save_users(default_users)
        return default_users

    return users

def save_users(users):
    """Сохранение пользователей в файл"""
    try:
        with open(USERS_FILE, 'w', encoding='utf-8') as f:
            for user in users:
                f.write(f"{user['username']}:{user['password']}:{user['role']}\n")
        return True
    except Exception as e:
        print(f"Ошибка при сохранении пользователей: {e}")
        return False

def login_required(f):
    def decorated_function(*args, **kwargs):
        if 'username' not in session:
            flash('Пожалуйста, войдите в систему', 'error')
            return redirect(url_for('login.html'))
        return f(*args, **kwargs)
    decorated_function.__name__ = f.__name__
    return decorated_function


@app.route('/generate', methods=['POST'])
def generate_password_ajax():
    try:
        data = request.get_json()
        length = int(data.get('length', 12))
        difficulty = data.get('difficulty', 'easy')

        if length < 4:
            length = 4
        elif length > 50:
            length = 50

        password = generate_password(length, difficulty)

        return jsonify({
            'success': True,
            'password': password,
            'length': length,
            'difficulty': difficulty
        })

    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        })

# Сначала регистрация
@app.route('/')
def home():
    return redirect(url_for('register'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if 'username' in session:
        return redirect(url_for('index'))

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']


        users = load_users()

        for user in users:
            if user['username'] == username:
                flash('Имя пользователя уже существует', 'error')
                return redirect(url_for('register'))


        users.append({'username': username, 'password': password, 'role': 'user'})
        save_users(users)

        flash('Регистрация успешна! Теперь войдите в систему', 'success')
        return redirect(url_for('login'))

    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'username' in session:
        return redirect(url_for('index'))

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']


        users = load_users()

        for user in users:
            if user['username'] == username and user['password'] == password:
                session['username'] = user['username']
                session['role'] = user.get('role', 'user')
                flash(f'Добро пожаловать, {username}!', 'success')
                return redirect(url_for('index'))

        flash('Неверное имя пользователя или пароль', 'error')

    return render_template('login.html')


@app.route('/index')
@login_required
def index():
    return render_template('index.html', username=session.get('username'))


@app.route('/logout')
def logout():
    # Очищаем сессию
    session.clear()
    flash('Вы вышли из системы', 'info')
    return redirect(url_for('register'))


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=1200)