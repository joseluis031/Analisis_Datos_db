import pandas as pd

# Rutas de los archivos CSV
ruta_nuevo_csv = 'CSVS/temp2023_24.csv'  # Reemplaza con la ruta real

# Lista de equipos en octavos
equipos_octavos = ['Copenhague', 'Leipzig', 'PSG', 'Lazio', 'PSV', 'Inter', 'Porto', 'Napoles', 'Bayern', 'Real Sociedad', 'Manchester City', 'Barcelona', 'Arsenal', 'Atletico Madrid', 'Dortmund', 'Real Madrid']

# Leer el nuevo archivo CSV
nuevo_csv = pd.read_csv(ruta_nuevo_csv)

# Filtrar las filas que contienen equipos en octavos como local o visitante
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
estadisticas_por_equipo_local = equipos_octavos_resultados.groupby('equipo_local')['Resultado'].value_counts(normalize=True).unstack(fill_value=0)
estadisticas_por_equipo_visitante = equipos_octavos_resultados.groupby('equipo_visitante')['Resultado'].value_counts(normalize=True).unstack(fill_value=0)

# Combinar las estadísticas de local y visitante
estadisticas_por_equipo = estadisticas_por_equipo_local.add(estadisticas_por_equipo_visitante, fill_value=0)

# Imprimir o utilizar según necesidades
print(estadisticas_por_equipo)  
