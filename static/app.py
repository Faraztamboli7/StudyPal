from flask import Flask, render_template, request, redirect
import sqlite3
import os

app = Flask(__name__)

# Database setup
def init_db():
    if not os.path.exists('studypal.db'):
        conn = sqlite3.connect('studypal.db')
        c = conn.cursor()
        c.execute('''
            CREATE TABLE tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                subject TEXT NOT NULL,
                topic TEXT NOT NULL,
                due_date TEXT NOT NULL,
                estimated_time INTEGER,
                completed INTEGER DEFAULT 0
            )
        ''')
        conn.commit()
        conn.close()

init_db()

# Routes
@app.route('/')
def index():
    conn = sqlite3.connect('studypal.db')
    c = conn.cursor()
    c.execute('SELECT * FROM tasks ORDER BY due_date ASC')
    tasks = c.fetchall()
    conn.close()
    return render_template('index.html', tasks=tasks)

@app.route('/add', methods=['POST'])
def add():
    subject = request.form['subject']
    topic = request.form['topic']
    due_date = request.form['due_date']
    estimated_time = request.form['estimated_time']
    
    conn = sqlite3.connect('studypal.db')
    c = conn.cursor()
    c.execute('INSERT INTO tasks (subject, topic, due_date, estimated_time) VALUES (?, ?, ?, ?)',
              (subject, topic, due_date, estimated_time))
    conn.commit()
    conn.close()
    return redirect('/')

@app.route('/delete/<int:task_id>')
def delete(task_id):
    conn = sqlite3.connect('studypal.db')
    c = conn.cursor()
    c.execute('DELETE FROM tasks WHERE id = ?', (task_id,))
    conn.commit()
    conn.close()
    return redirect('/')

@app.route('/complete/<int:task_id>')
def complete(task_id):
    conn = sqlite3.connect('studypal.db')
    c = conn.cursor()
    c.execute('UPDATE tasks SET completed = 1 WHERE id = ?', (task_id,))
    conn.commit()
    conn.close()
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
