import sqlite3

# Conectar a la base de datos
conn = sqlite3.connect('bookmaker_limpio.db')
cursor = conn.cursor()

# Encontrar filas duplicadas y conservar la primera
cursor.execute('''
    DELETE FROM apuestas
    WHERE ROWID NOT IN (
        SELECT MIN(ROWID)
        FROM apuestas
        GROUP BY id
    )
''')

# Confirmar y cerrar
conn.commit()
