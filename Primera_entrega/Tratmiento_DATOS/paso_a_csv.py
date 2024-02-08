import sqlite3
import pandas as pd

# Conectar a la base de datos
conn = sqlite3.connect('bookmaker.db')

# Obtener la lista de tablas en la base de datos
cursor = conn.cursor()
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()

# Exportar cada tabla a un archivo CSV
for table in tables:
    table_name = table[0]
    query = f"SELECT * FROM {table_name};"
    
    # Leer la tabla en un DataFrame de pandas
    df = pd.read_sql_query(query, conn)
    
    # Exportar el DataFrame a un archivo CSV
    csv_filename = f"{table_name}.csv"
    df.to_csv(csv_filename, index=False)
