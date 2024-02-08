import sqlite3

# Conectar a la base de datos
conn = sqlite3.connect('bookmaker_limpio.db')
cursor = conn.cursor()

# Nombre de la tabla y columna que deseas eliminar
nombre_tabla = 'partidos'
nombre_columna_a_eliminar = 'ganador'

# Obtener la lista de columnas excluyendo la que deseas eliminar
cursor.execute(f"PRAGMA table_info({nombre_tabla});")
columnas = [columna[1] for columna in cursor.fetchall() if columna[1] != nombre_columna_a_eliminar]

# Crear una nueva tabla sin la columna que deseas eliminar
cursor.execute(f'''
    CREATE TABLE nueva_{nombre_tabla} AS
    SELECT {', '.join(columnas)} FROM {nombre_tabla}
''')

# Transferir datos de la tabla original a la nueva tabla
cursor.execute(f'''
    INSERT INTO nueva_{nombre_tabla} ({', '.join(columnas)})
    SELECT {', '.join(columnas)} FROM {nombre_tabla}
''')

# Eliminar la tabla original
cursor.execute(f'DROP TABLE {nombre_tabla}')

# Renombrar la nueva tabla con el nombre original
cursor.execute(f'ALTER TABLE nueva_{nombre_tabla} RENAME TO {nombre_tabla}')

# Guardar los cambios y cerrar la conexión
conn.commit()
