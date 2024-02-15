import pandas as pd
import os

# Cargar los datos de los archivos CSV
resultados_actual = pd.read_csv('Eliminatoria actual/eliminatoria.csv')

# Especifica el nombre del archivo CSV que deseas cargar
csv_file = 'CSVS/temp2023_24.csv'  # Reemplaza 'nombre_del_archivo.csv' con el nombre real del archivo

# Ruta completa al archivo CSV
file_path = csv_file

# Leer el archivo CSV en un DataFrame
resultados_anterior = pd.read_csv(file_path)

# Equipos en octavos de final de la temporada actual
equipos_octavos_local = resultados_actual[resultados_actual['fase'] == 'Octavos']['equipo_local'].tolist()
equipos_octavos_visitante = resultados_actual[resultados_actual['fase'] == 'Octavos']['equipo_visitante'].tolist()
equipos_octavos = list(set(equipos_octavos_local + equipos_octavos_visitante))

# Limpiar nombres de equipos en el conjunto de datos anterior
resultados_anterior['equipo_local'] = resultados_anterior['equipo_local'].str.strip()
resultados_anterior['equipo_visitante'] = resultados_anterior['equipo_visitante'].str.strip()

# Filtrar los datos de la temporada anterior para incluir solo equipos en octavos
resultados_anterior_octavos = resultados_anterior[
    (resultados_anterior['equipo_local'].isin(equipos_octavos)) |
    (resultados_anterior['equipo_visitante'].isin(equipos_octavos))
]

# Calcular goles marcados y recibidos para cada equipo en la temporada anterior
goles_marcados_local = {}
goles_marcados_visitante = {}
goles_recibidos_local = {}
goles_recibidos_visitante = {}

for equipo in equipos_octavos:
    # Goles marcados como local
    goles_marcados_local[equipo] = resultados_anterior_octavos.loc[
        (resultados_anterior_octavos['equipo_local'] == equipo),
        'goles_equipo_local'
    ].sum()

    # Goles marcados como visitante
    goles_marcados_visitante[equipo] = resultados_anterior_octavos.loc[
        (resultados_anterior_octavos['equipo_visitante'] == equipo),
        'goles_equipo_visitante'
    ].sum()
    
    # Goles recibidos como local
    goles_recibidos_local[equipo] = resultados_anterior_octavos.loc[
        (resultados_anterior_octavos['equipo_local'] == equipo),
        'goles_equipo_visitante'
    ].sum()

    # Goles recibidos como visitante
    goles_recibidos_visitante[equipo] = resultados_anterior_octavos.loc[
        (resultados_anterior_octavos['equipo_visitante'] == equipo),
        'goles_equipo_local'
    ].sum()

# Crear un DataFrame con los resultados
tabla_goles = pd.DataFrame({
    'Equipo': equipos_octavos,
    'Goles Marcados Local': [goles_marcados_local.get(equipo, 0) for equipo in equipos_octavos],
    'Goles Marcados Visitante': [goles_marcados_visitante.get(equipo, 0) for equipo in equipos_octavos],
    'Goles Recibidos Local': [goles_recibidos_local.get(equipo, 0) for equipo in equipos_octavos],
    'Goles Recibidos Visitante': [goles_recibidos_visitante.get(equipo, 0) for equipo in equipos_octavos],
})

print(tabla_goles)
tabla_goles.to_csv('CSVS STATS/tabla_goles_temp_actual.csv', index=False)