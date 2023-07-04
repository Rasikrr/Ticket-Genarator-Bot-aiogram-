import sqlite3 as sq

db = sq.connect(r".\databases\DATABASE.db")
cur = db.cursor()


async def connect_database():
    cur.execute("""
        CREATE TABLE IF NOT EXISTS
        accounts(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        telegram_id INTEGER,
        is_questioned BOOLEAN,
        answer TEXT
        )
        """)
    db.commit()


async def register_users(name, user_id):
    is_exist = cur.execute("""
    SELECT username,telegram_id FROM accounts
    WHERE username = ? AND telegram_id = ?
    """, (name, user_id)).fetchone()

    if not is_exist:
        cur.execute(f"""
        INSERT INTO accounts(username, telegram_id, is_questioned)
        VALUES (?,?,?)
        """, (name, user_id, 0))
        db.commit()


async def is_questioned(name, user_id):
    answer = cur.execute("""
    SELECT answer FROM accounts
    WHERE username = ? AND telegram_id = ?
    """, (name, user_id)).fetchone()
    if answer[-1] is None:
        return True
    else:
        return False


async def insert_feedback_data(name, user_id, answer):
    cur.execute("""
    UPDATE accounts
    SET is_questioned = 1,
    answer = ?
    WHERE telegram_id = ? AND 
    username = ?
    """, (answer, user_id, name))
    db.commit()
