import sqlite3

# Conectar a la base de datos
conn = sqlite3.connect('bookmaker_limpio.db')
cursor = conn.cursor()

cursor.execute("DELETE FROM partidos WHERE id >= 98")

conn.commit()
