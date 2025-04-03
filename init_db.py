import sqlite3

conn = sqlite3.connect('user_activity.db')
cursor = conn.cursor()
cursor.execute('''
CREATE TABLE IF NOT EXISTS activity (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT,
    latitude REAL,
    longitude REAL,
    activity TEXT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
)
''')
conn.commit()
conn.close()
print("Database initialized successfully!")
