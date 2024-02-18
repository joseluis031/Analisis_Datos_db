import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

#Cargo el dataset
df = pd.read_csv('CSVS STATS/todas_stats.csv')

#

# Filtrar el DataFrame para obtener solo los datos del Real Madrid y del resto
real_madrid = df[df['equipo'] == 'Real Madrid']
resto = df[df['equipo'] != 'Real Madrid']

# selecciona la columna victorias_esta_temp de real_madrid y resto

victorias_real_madrid = real_madrid['victorias_esta_temp']
victorias_resto = resto['victorias_esta_temp']


# Graficar los datos
sns.histplot(victorias_real_madrid, kde=True, color='blue', label='Real Madrid', stat='density')
sns.histplot(victorias_resto, kde=True, color='red', label='Resto', stat='density')
plt.title('Distribución de victorias')
plt.xlabel('Victorias')
plt.ylabel('Densidad')
plt.legend()
plt.show()