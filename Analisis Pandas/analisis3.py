import pandas as pd

# Ruta al archivo CSV
archivo_csv = "temp2022_23.csv"

# Leer el archivo CSV en un DataFrame de pandas
dataframe = pd.read_csv(archivo_csv)
'''
# Actualizar los valores en la columna "false"
dataframe["fase"] = dataframe["fase"].replace("fase_de_grupos", "Grupos")

# Mostrar el DataFrame con los valores actualizados
print(dataframe)

# Guardar el DataFrame actualizado en un nuevo archivo CSV
dataframe.to_csv("temp2022_23.csv", index=False)'''


# Crear nuevas columnas para los goles del equipo local y del equipo visitante
dataframe["goles_equipo_local"] = dataframe["resultado_final"].str.split("-", expand=True)[0].fillna(0).astype(int)
dataframe["goles_equipo_visitante"] = dataframe["resultado_final"].str.split("-", expand=True)[1].fillna(0).astype(int)

# Mostrar el DataFrame con las nuevas columnas
print(dataframe)

# Guardar el DataFrame actualizado en un nuevo archivo CSV
dataframe.to_csv("evo2_archivo.csv", index=False)