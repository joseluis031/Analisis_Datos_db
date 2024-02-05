import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Cargar el CSV en un DataFrame
df = pd.read_csv('CSVS/equipos_modificado.csv')

# Análisis descriptivo básico
print("Resumen estadístico:")
print(df.describe())

# Calcular la media de los puntajes
media_puntajes = df['puntaje'].mean()
print(f"\nMedia de puntajes: {media_puntajes:.2f}")

# Visualizar la distribución de puntajes
plt.figure(figsize=(10, 6))
sns.histplot(df['puntaje'], bins=30, kde=True, color='skyblue')
plt.title('Distribución de Puntajes')
plt.xlabel('Puntaje')
plt.ylabel('Frecuencia')
plt.show()

# Graficar un gráfico de barras con el promedio de puntajes por pais
plt.figure(figsize=(12, 6))
sns.barplot(x='pais', y='puntaje', data=df, ci=None, palette='viridis')
plt.title('Puntaje Promedio por Pais')
plt.xlabel('nombre')
plt.ylabel('Puntaje Promedio')
plt.xticks(rotation=45, ha='right')
plt.show()

# Graficar una regresión lineal del puntaje vs. pais
plt.figure(figsize=(10, 6))
sns.regplot(x='puntaje', y='pais_numerico', data=df)
plt.title('Regresión Lineal del Puntaje respecto al Pais')
plt.xlabel('Puntaje')
plt.ylabel('Pais')
plt.show()
