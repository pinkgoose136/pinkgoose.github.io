import sqlite3

def create_tables():
    conn = sqlite3.connect('db.db')
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS bad (
            id TEXT
        )
    ''')

    conn.commit()
    conn.close()

def add_data(id):
    conn = sqlite3.connect('db.db')
    cursor = conn.cursor()

    cursor.execute('INSERT INTO bad (id) VALUES (?)', (str(id),))

    conn.commit()
    conn.close()

def get_bad_records():
    conn = sqlite3.connect('db.db')
    cursor = conn.cursor()

    cursor.execute('SELECT COUNT(*) FROM bad')
    total_records = cursor.fetchone()[0]

    cursor.execute('SELECT * FROM bad LIMIT 30')
    thirty_records = cursor.fetchall()

    conn.close()
    return [total_records, thirty_records]


def get_data(id):
    conn = sqlite3.connect('db.db')
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM bad WHERE key = ?', (id,))
    items = cursor.fetchall()

    return items

def delete_item(id):
    conn = sqlite3.connect('db.db')
    cursor = conn.cursor()

    cursor.execute('DELETE FROM bad WHERE key = ?', (id,))
    conn.commit()

create_tables()