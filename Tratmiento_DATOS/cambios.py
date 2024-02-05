import pandas as pd

# Cargar el dataset desde el CSV
df = pd.read_csv('CSVS/equipos.csv')

# Crear un mapeo de países a números
pais_a_numero = {pais: numero for numero, pais in enumerate(df['pais'].unique())}

# Aplicar el mapeo a la columna 'pais'
df['pais_numerico'] = df['pais'].map(pais_a_numero)

# Guardar el dataframe modificado en un nuevo CSV
df.to_csv('equipos_modificado.csv', index=False)
