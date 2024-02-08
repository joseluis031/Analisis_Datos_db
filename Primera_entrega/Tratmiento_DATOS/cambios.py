

import pandas as pd
'''
# Cargar el dataset desde el CSV
df = pd.read_csv('CSVS/equipos.csv')

# Crear un mapeo de países a números
pais_a_numero = {pais: numero for numero, pais in enumerate(df['pais'].unique())}

# Aplicar el mapeo a la columna 'pais'
df['pais_numerico'] = df['pais'].map(pais_a_numero)

# Guardar el dataframe modificado en un nuevo CSV
df.to_csv('equipos_modificado.csv', index=False)
'''


# Cargar los datasets
df_enfrentamientos = pd.read_csv('CSVS/partidos.csv')  # Asegúrate de tener el archivo correcto con los números de los equipos
df_puntajes = pd.read_csv('CSVS/equipos.csv')  # Asegúrate de tener el archivo correcto con los números de los equipos y sus puntajes

# Combinar la información de los puntajes usando el número de equipo
df_enfrentamientos = pd.merge(df_enfrentamientos, df_puntajes, left_on='equipo_local', right_on='id', how='left')
df_enfrentamientos = pd.merge(df_enfrentamientos, df_puntajes, left_on='equipo_visistante', right_on='id', how='left', suffixes=('_local', '_visitante'))

# Calcular la diferencia de puntaje
df_enfrentamientos['diferencia_puntaje'] = df_enfrentamientos['puntaje_local'] - df_enfrentamientos['puntaje_visitante']



# Guardar el dataframe modificado en un nuevo CSV

columnas_a_eliminar = ['id_y','nombre_local','escudo_local','pais_local','puntaje_local','activado_local','id','nombre_visitante','escudo_visitante','pais_visitante','puntaje_visitante','activado_visitante']

# Verificar si las columnas existen antes de intentar eliminarlas
columnas_existen = all(col in df_enfrentamientos.columns for col in columnas_a_eliminar)

if columnas_existen:
    # Eliminar las columnas
    df_enfrentamientos.drop(columnas_a_eliminar, axis=1, inplace=True)
    print(f"Las columnas {columnas_a_eliminar} han sido eliminadas.")
    df_enfrentamientos.to_csv('predicciones.csv', index=False)

else:
    # Al menos una de las columnas no existe
    columnas_no_existen = [col for col in columnas_a_eliminar if col not in df_enfrentamientos.columns]
    print(f"Las columnas {columnas_no_existen} no existen en el DataFrame.")
    

