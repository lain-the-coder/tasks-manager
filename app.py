from flask import Flask, jsonify, request
import sqlite3

app = Flask(__name__)

# Get route
@app.route('/tasks', methods=['GET'])
def get_tasks():
    conn = sqlite3.connect('tasks.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM tasks')
    rows = cursor.fetchall()
    conn.close()

    tasks = []
    for row in rows:
        task = {
            'id': row[0],
            'title': row[1],
            'description': row[2],
            'completed': bool(row[3])
        }
        tasks.append(task)

    return jsonify(tasks)

# Post route
@app.route('/tasks', methods=['POST'])
def create_task():
    data = request.get_json()
    title = data.get('title')
    description = data.get('description', '')
    completed = data.get('completed', False)

    # Title validation
    if not title:
        return jsonify({'error': 'Title is required'}), 400

    conn = sqlite3.connect('tasks.db')
    cursor = conn.cursor()
    cursor.execute(
      'INSERT INTO tasks (title, description, completed) VALUES (?, ?, ?)',
        (title, description, int(completed))
    )
    conn.commit()
    task_id = cursor.lastrowid
    conn.close()

    new_task = {
        'id': task_id,
        'title': title,
        'description': description,
        'completed': completed
    }

    return jsonify(new_task), 201

@app.route('/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    data = request.get_json()
    title = data.get('title')
    description = data.get('description', '')
    completed = data.get('completed', False)

    # Validate title field
    if not title:
        return jsonify({'error': 'Title is required'}), 400
    
    conn = sqlite3.connect('tasks.db')
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM tasks WHERE id = ?', (task_id,))
    task = cursor.fetchone()

    if task is None:
        conn.close()
        return jsonify({'error': 'Task not found'}), 404
    
    cursor.execute('''
    UPDATE tasks
    SET title = ?, description = ?, completed = ?
    WHERE id = ?
    ''', (title, description, int(completed), task_id))

    conn.commit()
    conn.close()

    updated_task = {
        'id': task_id,
        'title': title,
        'description': description,
        'completed': completed
    }

    return jsonify(updated_task)

@app.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    conn = sqlite3.connect('tasks.db')
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM tasks where id = ?', (task_id,))
    task = cursor.fetchone()

    if task is None:
        conn.close()
        return jsonify({'error': 'Task not found'}), 404
    
    cursor.execute('DELETE FROM tasks where id = ?', (task_id,))
    conn.commit()
    conn.close()

    return jsonify({'message': f'Task {task_id} deleted successfully'}), 200

# Start the app if run directly
if __name__ == '__main__':
    app.run(debug=True)