from flask import Flask, request, jsonify
import sqlite3
import time

app = Flask(__name__)

conn = sqlite3.connect("traxex.db", check_same_thread=False)
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS users(
user_id TEXT PRIMARY KEY,
balance INTEGER,
power INTEGER,
left_ref INTEGER,
right_ref INTEGER
)
""")
conn.commit()

POOL = {"ton": 1000}

# 👤 گرفتن کاربر
@app.route("/user/<uid>")
def user(uid):
    cur.execute("SELECT * FROM users WHERE user_id=?", (uid,))
    u = cur.fetchone()

    if not u:
        cur.execute("INSERT INTO users VALUES (?,?,?,?,?)",
                    (uid, 0, 1, 0, 0))
        conn.commit()
        return jsonify({"balance":0,"power":1,"left":0,"right":0})

    return jsonify({
        "balance":u[1],
        "power":u[2],
        "left":u[3],
        "right":u[4]
    })

# ⛏ ماین
@app.route("/mine", methods=["POST"])
def mine():
    uid = request.json["user_id"]

    cur.execute("SELECT * FROM users WHERE user_id=?", (uid,))
    u = cur.fetchone()

    if not u:
        return jsonify({"reward":1})

    reward = u[2] * 2

    cur.execute("UPDATE users SET balance = balance + ? WHERE user_id=?", (reward, uid))
    conn.commit()

    return jsonify({"reward":reward})

# 🌳 باینری رفرال
@app.route("/ref", methods=["POST"])
def ref():
    uid = request.json["user_id"]
    side = request.json["side"]  # left / right

    if side == "left":
        cur.execute("UPDATE users SET left_ref = left_ref + 1 WHERE user_id=?", (uid,))
    else:
        cur.execute("UPDATE users SET right_ref = right_ref + 1 WHERE user_id=?", (uid,))

    conn.commit()
    return jsonify({"status":"ok"})

# 💰 درآمد باینری
@app.route("/binary_income/<uid>")
def income(uid):
    cur.execute("SELECT left_ref,right_ref FROM users WHERE user_id=?", (uid,))
    u = cur.fetchone()

    if not u:
        return jsonify({"income":0})

    income = min(u[0], u[1]) * 5

    cur.execute("UPDATE users SET balance = balance + ? WHERE user_id=?", (income, uid))
    conn.commit()

    return jsonify({"income":income})

# 🛒 خرید از Pool
@app.route("/buy", methods=["POST"])
def buy():
    uid = request.json["user_id"]
    item = request.json["item"]

    if POOL["ton"] <= 0:
        return jsonify({"status":"no_pool"})

    POOL["ton"] -= 1

    if item == "power":
        cur.execute("UPDATE users SET power = power + 1 WHERE user_id=?", (uid,))

    conn.commit()
    return jsonify({"status":"ok","pool":POOL["ton"]})

# 💸 برداشت (fake approve)
@app.route("/withdraw", methods=["POST"])
def withdraw():
    uid = request.json["user_id"]

    cur.execute("SELECT balance FROM users WHERE user_id=?", (uid,))
    bal = cur.fetchone()[0]

    if bal < 100:
        return jsonify({"status":"min_not_met"})

    cur.execute("UPDATE users SET balance = 0 WHERE user_id=?", (uid,))
    conn.commit()

    return jsonify({"status":"sent","amount":bal})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)

