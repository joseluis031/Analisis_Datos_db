import pandas as pd

# Tu DataFrame con los resultados de la temporada actual
resultados_actual = pd.read_csv('temp2023_24.csv')

# Eliminar la primera columna completa
resultados_actual = resultados_actual.iloc[:, 1:]

# Imprimir el DataFrame después de la eliminación
print(resultados_actual)