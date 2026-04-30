from flask import Flask, render_template, request, redirect, url_for
import os
import psycopg2
import psycopg2.extras

app = Flask(__name__)

# Environment variables for DB
DB_HOST = os.environ.get('DB_HOST', 'localhost')
DB_NAME = os.environ.get('DB_NAME', 'mydatabase')
DB_USER = os.environ.get('DB_USER', 'myuser')
DB_PASSWORD = os.environ.get('DB_PASSWORD', 'mypassword')

def get_db_connection():
    return psycopg2.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )

@app.route('/', methods=['GET', 'POST'])
def index():
    try:
        conn = get_db_connection()
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

        if request.method == 'POST':
            message_content = request.form.get('content')
            if message_content:
                cur.execute('INSERT INTO messages (content) VALUES (%s)', (message_content,))
                conn.commit()
                return redirect(url_for('index'))

        cur.execute('SELECT id, content FROM messages ORDER BY id DESC')
        messages = cur.fetchall()
        cur.close()
        conn.close()
        return render_template('index.html', messages=messages)

    except Exception as e:
        # DB connection or query failed
        return f"<h2>Database connection failed</h2><pre>{e}</pre>", 500

@app.route('/health')
def health():
    return "OK", 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, threaded=True)
