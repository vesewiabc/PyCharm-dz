from flask import Flask, render_template, request, redirect, session
import sqlite3

app = Flask(__name__)
app.secret_key = '123'

# Создаем таблицы
def create_tables():
    connection = sqlite3.connect('password.db')
    cursor = connection.cursor()
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY,
    username TEXT NOT NULL,
    password TEXT NOT NULL
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS pass (
    id INTEGER PRIMARY KEY,
    login TEXT NOT NULL,
    password TEXT NOT NULL,
    website TEXT NOT NULL              
    )
    ''')

    connection.commit()
    connection.close()

@app.route('/')
def index():
    return redirect('/login')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        try:
            connection = sqlite3.connect('password.db')
            cursor = connection.cursor()
            cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, password))
            connection.commit()
            connection.close()
            return redirect('/login')
        except:
            return render_template('register.html', error="Ошибка")
    
    return render_template('register.html')    

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        connection = sqlite3.connect('password.db')
        cursor = connection.cursor()
        cursor.execute("SELECT id FROM users WHERE username = ? AND password = ?", (username, password))
        user = cursor.fetchone()
        connection.close()
        
        if user:
            session['user_id'] = user[0]
            session['username'] = username
            return redirect('/passwords')
        else:
            return render_template('login.html', error="ошибка")
    
    return render_template('login.html')

@app.route('/passwords')
def passwords():
    if 'user_id' not in session:
        return redirect('/login')
    
    connection = sqlite3.connect('password.db')
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM pass")
    passwords = cursor.fetchall()
    connection.close()
    
    return render_template('passwords.html', 
                         passwords=passwords, 
                         username=session['username'])

@app.route('/add', methods=['POST'])
def add_password():
    if 'user_id' not in session:
        return redirect('/login')
    
    website = request.form['website']
    login = request.form['login']
    password = request.form['password']
    
    connection = sqlite3.connect('password.db')
    cursor = connection.cursor()
    cursor.execute("INSERT INTO pass (website, login, password) VALUES (?, ?, ?)", (website, login, password))
    connection.commit()
    connection.close()
    
    return redirect('/passwords')

@app.route('/delete/<int:password_id>')
def delete_password(password_id):
    if 'user_id' not in session:
        return redirect('/login')
    
    connection = sqlite3.connect('password.db')
    cursor = connection.cursor()
    cursor.execute("DELETE FROM pass WHERE id = ?", (password_id,))
    connection.commit()
    connection.close()
    
    return redirect('/passwords')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/login')

if __name__ == '__main__':
    create_tables()
    app.run(debug=True, host='0.0.0.0', port=5555)
