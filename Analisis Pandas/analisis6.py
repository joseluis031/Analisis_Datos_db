import pandas as pd
import os

# Carpeta donde se encuentran los archivos CSV
carpeta_csv = "CSVS"

# Lista para almacenar los DataFrames de cada archivo
list_dataframes = []

# Recorrer todos los archivos en la carpeta
for archivo_csv in os.listdir(carpeta_csv):
    if archivo_csv.endswith(".csv"):
        ruta_archivo = os.path.join(carpeta_csv, archivo_csv)
        # Cargar el DataFrame desde el archivo CSV
        df = pd.read_csv(ruta_archivo)
        # Agregar el DataFrame a la lista
        list_dataframes.append(df)

# Concatenar todos los DataFrames en uno solo
temporada_df = pd.concat(list_dataframes, ignore_index=True)
ruta_archivo_clasificados = "Eliminatoria actual/eliminatoria.csv"

clasificados_df = pd.read_csv(ruta_archivo_clasificados)

# Aquí selecciona solo la columna de "equipo local" para los equipos que en la columna fase tenga "Octavos"
equipos_clasificados = clasificados_df.loc[clasificados_df['fase'] == 'Octavos', 'equipo_local'].tolist()

# Filtrar los datos de la temporada solo para los equipos clasificados y partidos de octavos
temporada_clasificados_octavos_df = temporada_df[
    (temporada_df['equipo_local'].isin(equipos_clasificados) | temporada_df['equipo_visitante'].isin(equipos_clasificados)) 
]

# Contar las victorias, empates y derrotas para cada equipo clasificado en octavos
resultados = {'equipo': [], 'victorias': [], 'empates': [], 'derrotas': [], 'victoriasxtemporada': [], 'empatesxtemp': [], 'derrotasxtemp': [],
              'porcentaje_victorias': [], 'porcentaje_empates': [], 'porcentaje_derrotas': []}

# Crear un DataFrame con los resultados
resultados_df = pd.DataFrame(resultados)

for equipo in equipos_clasificados:
    partidos_equipo = temporada_clasificados_octavos_df[
        (temporada_clasificados_octavos_df['equipo_local'] == equipo) | (temporada_clasificados_octavos_df['equipo_visitante'] == equipo)
    ]

    victorias_local = partidos_equipo.eval('equipo_local == @equipo and goles_equipo_local > goles_equipo_visitante').sum()
    victorias_visitante = partidos_equipo.eval('equipo_visitante == @equipo and goles_equipo_visitante > goles_equipo_local').sum()
    empates_local = partidos_equipo.eval('equipo_local == @equipo and goles_equipo_local == goles_equipo_visitante').sum()
    empates_visitante = partidos_equipo.eval('equipo_visitante == @equipo and goles_equipo_visitante == goles_equipo_local').sum()

    victorias = victorias_local + victorias_visitante
    empates = empates_local + empates_visitante
    derrotas_local = partidos_equipo.eval('equipo_local == @equipo and goles_equipo_local < goles_equipo_visitante').sum()
    derrotas_visitante = partidos_equipo.eval('equipo_visitante == @equipo and goles_equipo_visitante < goles_equipo_local').sum()
    derrotas = derrotas_local + derrotas_visitante

    victorias_temporada = resultados_df[resultados_df['equipo'] == equipo]['victorias'].sum()
    empates_temporada = resultados_df[resultados_df['equipo'] == equipo]['empates'].sum()
    derrotas_temporada = resultados_df[resultados_df['equipo'] == equipo]['derrotas'].sum()

    equipo_resultados = pd.DataFrame({
        'equipo': [equipo],
        'victorias': [victorias],
        'empates': [empates],
        'derrotas': [derrotas],
        'victoriasxtemporada': [victorias_temporada + victorias],
        'empatesxtemp': [empates_temporada + empates],
        'derrotasxtemp': [derrotas_temporada + derrotas],
        'porcentaje_victorias': [round((victorias / (victorias + empates + derrotas)) * 100, 1)],
        'porcentaje_empates': [round((empates / (victorias + empates + derrotas)) * 100, 1)],
        'porcentaje_derrotas': [round((derrotas / (victorias + empates + derrotas)) * 100, 1)]
    })

    resultados_df = pd.concat([resultados_df, equipo_resultados], ignore_index=True)

# Mostrar solo las primeras 3 y últimas 3 columnas del DataFrame con los resultados
print(resultados_df[['equipo', 'victorias', 'empates', 'derrotas', 'porcentaje_victorias', 'porcentaje_empates', 'porcentaje_derrotas']])

# Guardar el DataFrame con los resultados en un archivo CSV
resultados_df.to_csv('CSVS STATS/resultados2_ultimas10_temp.csv', index=False)
