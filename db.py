import sqlite3

# This connects to the database file (or creates it if it doesn't exist)
conn = sqlite3.connect('tasks.db')
cursor = conn.cursor()

# Create the "tasks" table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        description TEXT,
        completed BOOLEAN NOT NULL CHECK (completed IN (0, 1))
    )
''')

# Save changes and close
conn.commit()
conn.close()