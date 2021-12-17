import sqlite3

connection = sqlite3.connect('posts.db')

connection.commit()
connection.close()