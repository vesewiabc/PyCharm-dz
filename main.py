from flask import Flask, render_template, request, redirect, session
import sqlite3
import os

app = Flask(__name__)


connection = sqlite3.connect('password.db')
cursor = connection.cursor()
#пользователи
cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
id INTEGER PRIMARY KEY,
username TEXT NOT NULL,
password TEXT NOT NULL
)
''')

#хранение пароля
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
    if 'user_id' in session:
        return redirect('/passwords')
    return redirect('/login')

@app.route('/register', methods=['GET', 'POST'])
def register():
        if request.method == 'POST':
                username = request.form['username']
                password = request.form['password']

                try:
                    connection = sqlite3.connect('password.db')
                    cursor=connection.cursor()
                    cursor.execute('INSERT INTO Users (username, password) VALUES (?, ?)', (username,password))
                    connection.commit()
                    connection.close()
                    return redirect('/login')
                except:
                    return render_template('register.html', error = "Error")
        return render_template('register.html')    

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        

        connection = sqlite3.connect('password.db')
        connection = connection.cursor()
        cursor.execute("SELECT username FROM users WHERE username = ? AND password = ?", (username, password))
        user = connection.fetchone()
        connection.close()

        if user:
            session['user_id'] = user[0]
            session['username'] = username
            return redirect('/index')
        else:
             return render_template('login.html', error='error')
        
    return render_template('login.html')

@app.route('/index')
def passwords():
    if 'user_id' not in session:
        return redirect('/login')
    
    user_id = session['user_id']
    
    connection = sqlite3.connect('password.db')
    connection = connection.cursor()
    cursor.execute("SELECT * FROM password WHERE user_id = ?", (user_id,))
    passwords = cursor.fetchall()
    connection.close()
    
    return render_template('index.html', 
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
    cursor.execute("INSERT INTO password (website, login, password) VALUES (?, ?, ?, ?)", (website, login, password))
    connection.commit()
    connection.close()
    
    return redirect('/index')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)