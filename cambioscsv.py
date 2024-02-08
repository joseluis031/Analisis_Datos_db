import pandas as pd

# Cargar el archivo CSV original
df = pd.read_csv('temp2023_24.csv')

# Añadir la columna 'Grupo' y rellenar con 'Grupos'
df.insert(0, 'Grupo', 'Grupos')

# Guardar el nuevo DataFrame en un nuevo archivo CSV
df.to_csv('temp2023_24.csv', index=False)