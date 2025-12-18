# Создаём файл app.py с кодом Flask-приложения для работы с SQLite

app_py_content = """
from flask import Flask, jsonify, request
import sqlite3
import json

app = Flask(__name__)

# Функция для подключения к базе данных
def get_db_connection():
    conn = sqlite3.connect('nmo.db')
    conn.row_factory = sqlite3.Row
    return conn

# Инициализация базы данных
@app.before_first_request
def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS questions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            question TEXT NOT NULL,
            answers TEXT NOT NULL,
            topics TEXT NOT NULL,
            correctAnswers TEXT NOT NULL
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS topics (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            completed INTEGER,
            inputIndex INTEGER,
            dirty INTEGER
        )
    ''')
    conn.commit()
    conn.close()

# Добавление нового вопроса
@app.route('/api/questions', methods=['POST'])
def add_question():
    new_question = request.json
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO questions (question, answers, topics, correctAnswers)
        VALUES (?, ?, ?, ?)
    ''', (
        new_question['question'],
        json.dumps(new_question['answers']),
        json.dumps(new_question['topics']),
        json.dumps(new_question['correctAnswers'])
    ))
    conn.commit()
    conn.close()
    return jsonify({"message": "Вопрос успешно добавлен!"})

# Получение всех вопросов
@app.route('/api/questions', methods=['GET'])
def get_questions():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM questions')
    questions = cursor.fetchall()
    conn.close()
    return jsonify([dict(question) for question in questions])

# Получение вопросов по теме
@app.route('/api/questions/<int:topic_id>', methods=['GET'])
def get_questions_by_topic(topic_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM questions WHERE json_extract(topics, '$[0]') = ?', (str(topic_id),))
    questions = cursor.fetchall()
    conn.close()
    return jsonify([dict(question) for question in questions])

# Добавление новой темы
@app.route('/api/topics', methods=['POST'])
def add_topic():
    new_topic = request.json
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO topics (name, completed, inputIndex, dirty)
        VALUES (?, ?, ?, ?)
    ''', (
        new_topic['name'],
        new_topic.get('completed', 0),
        new_topic.get('inputIndex', 0),
        new_topic.get('dirty', 0)
    ))
    conn.commit()
    conn.close()
    return jsonify({"message": "Тема успешно добавлена!"})

# Получение всех тем
@app.route('/api/topics', methods=['GET'])
def get_topics():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM topics')
    topics = cursor.fetchall()
    conn.close()
    return jsonify([dict(topic) for topic in topics])

if __name__ == '__main__':
    app.run(debug=True)
"""

with open('app.py', 'w', encoding='utf-8') as file:
    file.write(app_py_content)

'Файл app.py создан.'