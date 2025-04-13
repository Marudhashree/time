from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('tasks.db')
    conn.row_factory = sqlite3.Row
    return conn

def get_all_tasks():
    conn = get_db_connection()
    tasks = conn.execute('SELECT * FROM tasks').fetchall()
    conn.close()
    return tasks

@app.route('/')
def index():
    tasks = get_all_tasks()
    return render_template('index.html', tasks=tasks)

@app.route('/add', methods=['POST'])
def add_task():
    task = request.form['task']
    deadline = request.form['deadline']
    category = request.form.get('category', 'General')  # Default category if not provided
    conn = get_db_connection()
    conn.execute(
        'INSERT INTO tasks (name, deadline, category, done) VALUES (?, ?, ?, ?)',
        (task, deadline, category, 0)  # 0 = False in SQLite
    )
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

@app.route('/done/<int:task_id>')
def mark_done(task_id):
    conn = get_db_connection()
    conn.execute('UPDATE tasks SET done = ? WHERE id = ?', (1, task_id))  # 1 = True in SQLite
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

@app.route('/delete/<int:task_id>')
def delete_task(task_id):
    conn = get_db_connection()
    conn.execute('DELETE FROM tasks WHERE id = ?', (task_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
