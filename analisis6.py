#por fin este coge bien los datos de los equipos en octavos

import pandas as pd 

# Cargar los datos de ambos archivos CSV
ruta_archivo_temporada = "CSVS/temp2023_24.csv"
ruta_archivo_clasificados = "Eliminatoria actual/eliminatoria.csv"

temporada_df = pd.read_csv(ruta_archivo_temporada)
clasificados_df = pd.read_csv(ruta_archivo_clasificados)

# Aquí selecciona solo la columna de "equipo local" para los equipos que en la columna fase tenga "Octavos"
equipos_clasificados = clasificados_df.loc[clasificados_df['fase'] == 'Octavos', 'equipo_local'].tolist()

# Filtrar los datos de la temporada solo para los equipos clasificados y partidos de octavos
temporada_clasificados_octavos_df = temporada_df[
    (temporada_df['equipo_local'].isin(equipos_clasificados) | temporada_df['equipo_visitante'].isin(equipos_clasificados)) 
]

# Contar las victorias, empates y derrotas para cada equipo clasificado en octavos
resultados = {'equipo': [], 'victorias': [], 'empates': [], 'derrotas': []}

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

    resultados['equipo'].append(equipo)
    resultados['victorias'].append(victorias)
    resultados['empates'].append(empates)
    resultados['derrotas'].append(derrotas)

# Crear un DataFrame con los resultados
resultados_df = pd.DataFrame(resultados)

# Mostrar el DataFrame con los resultados
print(resultados_df)
