import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

def cargar_datos(ruta_csv):
    """Cargar el CSV en un DataFrame."""
    return pd.read_csv(ruta_csv)

def resumen_estadistico(datos):
    """Realizar un análisis descriptivo básico."""
    print("Resumen estadístico:")
    print(datos.describe())

def calcular_media_puntajes(datos, columna_puntajes):
    """Calcular la media de los puntajes."""
    media_puntajes = datos[columna_puntajes].mean()
    print(f"\nMedia de puntajes: {media_puntajes:.2f}")

def visualizar_distribucion_puntajes(datos, columna_puntajes):
    """Visualizar la distribución de puntajes."""
    plt.figure(figsize=(10, 6))
    sns.histplot(datos[columna_puntajes], bins=30, kde=True, color='skyblue')
    plt.title('Distribución de Puntajes')
    plt.xlabel('Puntaje')
    plt.ylabel('Frecuencia')
    plt.show()

def grafico_barras_promedio(datos, columna_categorica, columna_puntajes):
    """Graficar un gráfico de barras con el promedio de puntajes por categoría."""
    plt.figure(figsize=(12, 6))
    sns.barplot(x=columna_categorica, y=columna_puntajes, data=datos, ci=None, palette='viridis')
    plt.title(f'Puntaje Promedio por {columna_categorica.capitalize()}')
    plt.xlabel(columna_categorica.capitalize())
    plt.ylabel('Puntaje Promedio')
    plt.xticks(rotation=45, ha='right')
    plt.show()

def regresion_lineal(datos, columna_puntajes, columna_categorica_numerica):
    """Graficar una regresión lineal del puntaje vs. categoría."""
    plt.figure(figsize=(10, 6))
    sns.regplot(x=columna_puntajes, y=columna_categorica_numerica, data=datos)
    plt.title(f'Regresión Lineal del Puntaje respecto a {columna_categorica_numerica.capitalize()}')
    plt.xlabel('Puntaje')
    plt.ylabel(columna_categorica_numerica.capitalize())
    plt.show()

ruta_csv = 'CSVS/equipos_modificado.csv'
datos = cargar_datos(ruta_csv)
resumen_estadistico(datos)
calcular_media_puntajes(datos, 'puntaje')
visualizar_distribucion_puntajes(datos, 'puntaje')
grafico_barras_promedio(datos, 'pais', 'puntaje')
regresion_lineal(datos, 'puntaje', 'pais_numerico')
