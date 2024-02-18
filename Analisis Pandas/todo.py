import pandas as pd

# Leer los archivos CSV
csv1 = pd.read_csv('CSVS STATS/resultados_esta_temp.csv')
csv2 = pd.read_csv('CSVS STATS/resultados_ultimas10_temp.csv')
csv3 = pd.read_csv('CSVS STATS/tabla_goles_temp_actual.csv')
csv4 = pd.read_csv('CSVS STATS/tabla_goles_ult10_temp.csv')
csv5 = pd.read_csv('CSVS STATS/tabla_golesxpartido.csv')



# Unir los archivos CSV basándote en la columna 'equipo_local'
result = pd.merge(csv1, csv2, on='equipo', how='inner')
result = pd.merge(result, csv3, on='equipo', how='inner')
result = pd.merge(result, csv4, on='equipo', how='inner')
result = pd.merge(result, csv5, on='equipo', how='inner')


# Mostrar el resultado
print(result)
# Guardar el resultado en un archivo CSV
result.to_csv('CSVS STATS/todas_stats.csv', index=False)
