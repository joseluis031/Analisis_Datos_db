import pandas as pd
import os

# Cargar los datos de los archivos CSV
resultados_actual = pd.read_csv('Eliminatoria actual/eliminatoria.csv')

csv_folder = 'CSVS'
csv_files = [file for file in os.listdir(csv_folder) if file.endswith('.csv')]

# Inicializar DataFrames vacíos para almacenar los resultados anteriores
resultados_anterior = pd.DataFrame()

# Cargar y concatenar todos los archivos CSV en uno solo
for csv_file in csv_files:
    file_path = os.path.join(csv_folder, csv_file)
    df = pd.read_csv(file_path)
    resultados_anterior = pd.concat([resultados_anterior, df])

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

# Calcular goles marcados y recibidos por partido para cada equipo en la temporada anterior
goles_marcados_local = {}
goles_marcados_visitante = {}
goles_recibidos_local = {}
goles_recibidos_visitante = {}

for equipo in equipos_octavos:
    # Goles marcados como local
    goles_marcados_local[equipo] = round(resultados_anterior_octavos.loc[
        (resultados_anterior_octavos['equipo_local'] == equipo),
        'goles_equipo_local'
    ].mean(), 1)

    # Goles marcados como visitante
    goles_marcados_visitante[equipo] = round(resultados_anterior_octavos.loc[
        (resultados_anterior_octavos['equipo_visitante'] == equipo),
        'goles_equipo_visitante'
    ].mean(), 1)
    
    # Goles recibidos como local
    goles_recibidos_local[equipo] = round(resultados_anterior_octavos.loc[
        (resultados_anterior_octavos['equipo_local'] == equipo),
        'goles_equipo_visitante'
    ].mean(), 1)

    # Goles recibidos como visitante
    goles_recibidos_visitante[equipo] = round(resultados_anterior_octavos.loc[
        (resultados_anterior_octavos['equipo_visitante'] == equipo),
        'goles_equipo_local'
    ].mean(), 1)

# Crear un DataFrame con los resultados
tabla_goles = pd.DataFrame({
    'Equipo': equipos_octavos,
    'Golesxpartido Local': [goles_marcados_local.get(equipo, 0) for equipo in equipos_octavos],
    'Golesxpartido Visitante': [goles_marcados_visitante.get(equipo, 0) for equipo in equipos_octavos],
    'Golesxpartido Recibidos Local': [goles_recibidos_local.get(equipo, 0) for equipo in equipos_octavos],
    'Golesxpartido Recibidos Visitante': [goles_recibidos_visitante.get(equipo, 0) for equipo in equipos_octavos],
})

print(tabla_goles)

tabla_goles.to_csv('CSVS STATS/tabla_golesxpartido.csv', index=False)
