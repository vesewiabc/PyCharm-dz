from flask import Flask, render_template, request, redirect, session,url_for
import sqlite3
import os

app = Flask(__name__)
app.secret_key = '123'

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
                    cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username,password))
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
        cursor = connection.cursor()
        cursor.execute("SELECT username FROM users WHERE username = ? AND password = ?", (username, password))
        users = cursor.fetchall()
        
        connection.close()
        
        for user in users:
            print(user)
        
        if user:
            session['user_id'] = user[0]
            session['username'] = username
            return redirect('/passwords')
        else:
            flash('Неверное имя пользователя или пароль!')
    
        
       
    return render_template('login.html')
       
@app.route('/passwords')
def passwords():
    if 'id' not in session:
        return redirect('/login')
    
    user = session['id']
    
    connection = sqlite3.connect('password.db')
    connection = connection.cursor()
    cursor.execute("SELECT id FROM password WHERE id = ?", (id))
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
    cursor.execute("INSERT INTO password (website, login, password) VALUES (?, ?, ?)", (website, login, password))
    connection.commit()
    connection.close()
    
    return redirect('/passwrods')

@app.route('/logout', methods=['POST'])
def logout():
    session.clear()
    return redirect('/login')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5555)
