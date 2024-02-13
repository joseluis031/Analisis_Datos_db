import pandas as pd
import os

# Obtener la lista de archivos CSV en la carpeta
carpeta = 'CSVS'
archivos_csv = [archivo for archivo in os.listdir(carpeta) if archivo.endswith('.csv')]

# Inicializar un DataFrame vacío para almacenar los resultados
resultados_totales = pd.DataFrame()

# Iterar sobre cada archivo CSV
for archivo in archivos_csv:
    # Cargar el archivo CSV
    resultados_temporada = pd.read_csv(os.path.join(carpeta, archivo))
    
    # Extraer el año de la temporada del nombre del archivo (ajusta esto según tus necesidades)
    temporada = archivo.split('_')[1].split('.')[0]
    
    # Agregar la columna 'temporada' con el año
    resultados_temporada['temporada'] = temporada
    
    # Concatenar los resultados de la temporada actual al DataFrame total
    resultados_totales = pd.concat([resultados_totales, resultados_temporada], ignore_index=True)

# Obtener los equipos en octavos de la temporada actual
equipos_octavos_local = resultados_totales[resultados_totales['fase'] == 'Octavos']['equipo_local'].tolist()
equipos_octavos_visitante = resultados_totales[resultados_totales['fase'] == 'Octavos']['equipo_visitante'].tolist()
equipos_octavos = set(equipos_octavos_local + equipos_octavos_visitante)

# Filtrar los datos para incluir solo los equipos en octavos de la temporada actual
resultados_octavos = resultados_totales[
    (resultados_totales['equipo_local'].isin(equipos_octavos)) |
    (resultados_totales['equipo_visitante'].isin(equipos_octavos))
]

# Calcular la media de victorias, derrotas y empates por temporada
resultados_octavos['Tipo_Resultado'] = resultados_octavos.apply(lambda row: 'Ganado' if row['goles_equipo_local'] > row['goles_equipo_visitante'] else ('Empatado' if row['goles_equipo_local'] == row['goles_equipo_visitante'] else 'Perdido'), axis=1)
media_por_temporada = resultados_octavos.groupby('temporada')['Tipo_Resultado'].value_counts(normalize=True).unstack(fill_value=0)

# Imprimir los resultados
print(media_por_temporada)
