from flask import Flask, render_template
import sqlite3

app = Flask(__name__)

def get_user_activity():
    conn = sqlite3.connect('user_activity.db')
    cursor = conn.cursor()
    cursor.execute('SELECT username, latitude, longitude, activity, timestamp FROM activity ORDER BY timestamp DESC LIMIT 10')
    rows = cursor.fetchall()
    conn.close()
    return rows

@app.route('/')
def index():
    activities = get_user_activity()
    return render_template('index.html', activities=activities)

if __name__ == '__main__':
    app.run(debug=True)
