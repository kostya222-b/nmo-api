# Создаём файл init_db.py для инициализации базы данных с тестовыми данными

init_db_py_content = """
import sqlite3
import json

def init_db():
    conn = sqlite3.connect('nmo.db')
    cursor = conn.cursor()
    
    # Создаём таблицы
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
    
    # Добавляем тестовые данные
    test_questions = [
        {
            "question": "Какой тип наследования имеет себорейный кератоз?",
            "answers": json.dumps({
                "type": "Выберите ОДИН правильный ответ",
                "answers": [
                    "аутосомно-доминантное наследование с неполной пенетрантностью",
                    "аутосомно-рецессивное наследование с неполной пенетрантностью",
                    "аутосомное промежуточное наследование",
                    "доминантное Х-сцепленное наследование"
                ]
            }),
            "topics": json.dumps([1]),
            "correctAnswers": json.dumps({
                "type": ["аутосомно-доминантное наследование с неполной пенетрантностью"]
            })
        }
    ]
    
    test_topics = [
        {
            "name": "Себорейный кератоз (по утвержденным клиническим рекомендациям) - 2025 Дерматовенерология",
            "completed": 2,
            "inputIndex": 1,
            "dirty": 1
        }
    ]
    
    cursor.executemany('''
        INSERT INTO questions (question, answers, topics, correctAnswers)
        VALUES (?, ?, ?, ?)
    ''', [(q['question'], q['answers'], q['topics'], q['correctAnswers']) for q in test_questions])
    
    cursor.executemany('''
        INSERT INTO topics (name, completed, inputIndex, dirty)
        VALUES (?, ?, ?, ?)
    ''', [(t['name'], t['completed'], t['inputIndex'], t['dirty']) for t in test_topics])
    
    conn.commit()
    conn.close()

if __name__ == '__main__':
    init_db()
"""

with open('init_db.py', 'w', encoding='utf-8') as file:
    file.write(init_db_py_content)

'Файл init_db.py создан.'