import pandas as pd

# Especifica la ruta de tu archivo CSV
ruta_csv = 'Eliminatoria actual/eliminatoria.csv'

# Lee el archivo CSV con pandas
df = pd.read_csv(ruta_csv)


# Filtra las filas donde la primera columna sea "Octavos"
filas_octavos = df[df.iloc[:, 0] == 'Octavos']

# Accede a la segunda columna y conviértela en una lista
equipos_octavos = filas_octavos.iloc[:, 1].tolist()

# Imprime o utiliza la lista según tus necesidades
print(equipos_octavos)

ruta_nuevo_csv = 'CSVS/temp2023_24.csv'
nuevo_csv = pd.read_csv(ruta_nuevo_csv)

# Filtrar las filas que contienen equipos en octavos
equipos_octavos_resultados = nuevo_csv[
    (nuevo_csv['equipo_local'].isin(equipos_octavos)) | 
    (nuevo_csv['equipo_visitante'].isin(equipos_octavos))
]

# Función para determinar el resultado del partido
def determinar_resultado(row):
    if row['goles_equipo_local'] > row['goles_equipo_visitante']:
        return 'Ganado'
    elif row['goles_equipo_local'] < row['goles_equipo_visitante']:
        return 'Perdido'
    else:
        return 'Empatado'

# Crear una nueva columna 'Resultado' basada en la función
equipos_octavos_resultados['Resultado'] = equipos_octavos_resultados.apply(determinar_resultado, axis=1)

# Calcular las estadísticas por equipo
estadisticas_por_equipo = equipos_octavos_resultados.groupby('equipo_local')['Resultado'].value_counts(normalize=True).unstack(fill_value=0)

# Imprimir o utilizar según necesidades
print(estadisticas_por_equipo)