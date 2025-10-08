from flask import Flask, render_template, request, jsonify
import random
import string

app = Flask(__name__)


def generate_password(length, difficulty):
    """Генерация пароля в зависимости от сложности"""
    if difficulty == 'easy':
        # Легкий: только буквы (строчные и заглавные)
        characters = string.ascii_letters
    else:
        # Сложный: буквы, цифры и специальные символы
        characters = string.ascii_letters + string.digits + "!@#$%^&*()_+-=[]{}|;:,.<>?"

    # Генерируем пароль
    password = ''.join(random.choice(characters) for _ in range(length))
    return password


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/generate', methods=['POST'])
def generate_password_ajax():
    try:
        data = request.get_json()
        length = int(data.get('length', 12))
        difficulty = data.get('difficulty', 'easy')

        # Проверка валидности длины
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


if __name__ == '__main__':
    app.run(debug=True)