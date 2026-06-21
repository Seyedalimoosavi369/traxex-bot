from flask import Flask, request, jsonify
import sqlite3
import os

app = Flask(__name__)
DB_NAME = os.path.expanduser("~/traxex/traxex.db")

def get_db():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/api/user/init', methods=['POST'])
def init_user():
    data = request.json
    telegram_id = data.get('telegram_id')
    username = data.get('username', 'User')
    ref = data.get('ref')

    if not telegram_id:
        return jsonify({"error": "Missing telegram_id"}), 400

    conn = get_db()
    user = conn.execute('SELECT * FROM users WHERE telegram_id = ?', (telegram_id,)).fetchone()

    if not user:
        conn.execute('''
            INSERT INTO users (telegram_id, username, parent_id)
            VALUES (?, ?, ?)
        ''', (telegram_id, username, ref))
        conn.commit()
        user = conn.execute('SELECT * FROM users WHERE telegram_id = ?', (telegram_id,)).fetchone()

    result = dict(user)
    conn.close()
    return jsonify(result)

@app.route('/api/user/save', methods=['POST'])
def save_user():
    data = request.json
    telegram_id = data.get('telegram_id')
    balance = data.get('balance', 0)
    hashrate = data.get('hashrate', 1)
    level = data.get('level', 1)
    item_levels = data.get('item_levels', '{}')

    if not telegram_id:
        return jsonify({"error": "Missing telegram_id"}), 400

    conn = get_db()
    conn.execute('''
        UPDATE users SET balance=?, hashrate=?, level=?, items_owned=?
        WHERE telegram_id=?
    ''', (balance, hashrate, level, str(item_levels), telegram_id))
    conn.commit()
    conn.close()
    return jsonify({"status": "ok"})

@app.route('/api/user/get', methods=['GET'])
def get_user():
    telegram_id = request.args.get('telegram_id')
    if not telegram_id:
        return jsonify({"error": "Missing telegram_id"}), 400

    conn = get_db()
    user = conn.execute('SELECT * FROM users WHERE telegram_id = ?', (telegram_id,)).fetchone()
    conn.close()

    if not user:
        return jsonify({"error": "User not found"}), 404

    return jsonify(dict(user))

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
