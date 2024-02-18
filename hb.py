import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Cargo el dataset
df = pd.read_csv('CSVS STATS/todas_stats.csv')

# Filtrar el DataFrame para obtener solo los datos del Real Madrid y del resto
real_madrid = df[df['equipo'] == 'Real Madrid']
resto = df[df['equipo'] != 'Real Madrid']

# Seleccionar la columna 'Goles Marcados Local_esta_temp' de real_madrid y resto
goles_real_madrid = real_madrid['Goles Marcados Local_esta_temp'].values[0]
media_goles_resto = resto['Goles Marcados Local_esta_temp'].mean()

# Crear un DataFrame para la media del resto
df_media_resto = pd.DataFrame({'equipo': ['Resto de Equipos'], 'Goles Marcados Local_esta_temp': [media_goles_resto]})

# Concatenar el DataFrame de Real Madrid con el de la media del resto
df_plot = pd.concat([real_madrid, df_media_resto])

# Graficar los datos
plt.figure(figsize=(10, 6))
sns.barplot(x='equipo', y='Goles Marcados Local_esta_temp', data=df_plot, palette=['blue', 'red'])
plt.title('Comparación de Goles como Local')
plt.ylabel('Goles Marcados')
plt.show()
