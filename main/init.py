import sqlite3
conn = sqlite3.connect('ahoy.db')
cur = conn.cursor()
cur.execute('CREATE TABLE user (id INTEGER NOT NULL, username VARCHAR, password VARCHAR, PRIMARY KEY (id))')
conn.commit()
conn.close()