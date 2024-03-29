import sqlite3

# Conectar a la base de datos original
conn_orig = sqlite3.connect('bookmaker.db')
cursor_orig = conn_orig.cursor()

# Conectar a la nueva base de datos (con un nombre diferente)
conn_nueva = sqlite3.connect('bookmaker_limpio.db')
cursor_nueva = conn_nueva.cursor()
'''
# Obtener el esquema de la base de datos original
cursor_orig.execute("SELECT sql FROM sqlite_master WHERE type='table';")
tablas = cursor_orig.fetchall()

# Crear las tablas en la nueva base de datos
for tabla in tablas:
    cursor_nueva.execute(tabla[0])

# Transferir datos de la base de datos original a la nueva base de datos
for tabla in tablas:
    nombre_tabla = tabla[0].split()[2]  # Obtener el nombre de la tabla
    cursor_orig.execute(f"SELECT * FROM {nombre_tabla};")
    datos = cursor_orig.fetchall()

    # Obtener nombres de columnas
    cursor_nueva.execute(f"PRAGMA table_info({nombre_tabla});")
    columnas = [columna[1] for columna in cursor_nueva.fetchall()]

    # Insertar datos en la nueva base de datos
    for fila in datos:
        # Crear una cadena de marcadores de posición (?, ?, ...) según la cantidad de columnas
        marcadores = ', '.join('?' for _ in range(len(columnas)))
        cursor_nueva.execute(f"INSERT INTO {nombre_tabla} VALUES ({marcadores});", fila)

# Guardar los cambios y cerrar conexiones
conn_nueva.commit()

'''

# Eliminar filas en la tabla 'apuestas' donde 'equipo_ganador_id' es NULL
#cursor_nueva.execute('''
#    DELETE FROM apuestas
#    WHERE equipo_ganador_id IS NULL
#''')


# Obtener las filas duplicadas en la tabla 'apuestas'
cursor_nueva.execute('''
    SELECT fecha, equipo_ganador_id, MIN(ROWID)
    FROM apuestas
    GROUP BY fecha, equipo_ganador_id
    HAVING COUNT(*) > 1
''')

filas_duplicadas = cursor_nueva.fetchall()

# Eliminar una de las filas duplicadas
for fila in filas_duplicadas:
    fecha, equipo_ganador_id, rowid_min = fila
    print(f"Eliminando duplicados: fecha={fecha}, equipo_ganador_id={equipo_ganador_id}, rowid_min={rowid_min}")
    cursor_nueva.execute('''
        DELETE FROM apuestas
        WHERE fecha = ? AND equipo_ganador_id = ? AND ROWID != ?
    ''', (fecha, equipo_ganador_id, rowid_min))

# Guardar los cambios y cerrar la conexión
try:
    conn_nueva.commit()
except Exception as e:
    print(f"Error al guardar los cambios: {e}")
finally:
    pass
