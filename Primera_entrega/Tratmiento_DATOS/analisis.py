import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os

class AnalisisDatos:
    def __init__(self, carpeta_graficas='Graficas'):
        self.carpeta_graficas = carpeta_graficas

        if not os.path.exists(self.carpeta_graficas):
            os.makedirs(self.carpeta_graficas)

    def guardar_grafico(self, nombre_grafico):
        """Guardar el gráfico en un archivo PNG en la carpeta 'Graficas'."""
        ruta_grafico = os.path.join(self.carpeta_graficas, nombre_grafico + '.png')
        plt.savefig(ruta_grafico, bbox_inches='tight')
        print(f'Gráfico guardado en: {ruta_grafico}')

    def cargar_datos(self, ruta_csv):
        return pd.read_csv(ruta_csv)

    def resumen_estadistico(self, datos):
        print("Resumen estadístico:")
        print(datos.describe())

    def calcular_media_puntajes(self, datos, columna_puntajes):
        media_puntajes = datos[columna_puntajes].mean()
        print(f"\nMedia de puntajes: {media_puntajes:.2f}")

    def visualizar_distribucion_puntajes(self, datos, columna_puntajes):
        plt.figure(figsize=(10, 6))
        sns.histplot(datos[columna_puntajes], bins=30, kde=True, color='skyblue')
        plt.title('Distribución de Puntajes')
        plt.xlabel('Puntaje')
        plt.ylabel('Frecuencia')
        
        self.guardar_grafico('distribucion_puntajes')

        plt.show()

    def grafico_barras_promedio(self, datos, columna_categorica, columna_puntajes):
        plt.figure(figsize=(12, 6))
        sns.barplot(x=columna_categorica, y=columna_puntajes, data=datos, ci=None, palette='viridis')
        plt.title(f'Puntaje Promedio por {columna_categorica.capitalize()}')
        plt.xlabel(columna_categorica.capitalize())
        plt.ylabel('Puntaje Promedio')
        plt.xticks(rotation=45, ha='right')
        
        self.guardar_grafico(f'barra_promedio_{columna_categorica.lower()}')

        plt.show()

    def regresion_lineal(self, datos, columna_puntajes, columna_categorica_numerica):
        plt.figure(figsize=(10, 6))
        sns.regplot(x=columna_puntajes, y=columna_categorica_numerica, data=datos)
        plt.title(f'Regresión Lineal del Puntaje respecto a {columna_categorica_numerica.capitalize()}')
        plt.xlabel('Puntaje')
        plt.ylabel(columna_categorica_numerica.capitalize())
        
        self.guardar_grafico(f'regresion_lineal_{columna_categorica_numerica.lower()}')

        plt.show()

    def diagrama_sectores_paises(self, datos, columna_categorica, umbral_paises=8):
        plt.figure(figsize=(10, 6))
        frecuencia_paises = datos[columna_categorica].value_counts()
        paises_resto = frecuencia_paises.nsmallest(umbral_paises)
        paises_resto_total = pd.Series({'Resto de Europa': paises_resto.sum()})
        paises_principales = frecuencia_paises.drop(paises_resto.index)
        frecuencia_final = paises_principales.append(paises_resto_total)
        frecuencia_final.plot.pie(autopct='%1.1f%%', startangle=90, cmap='viridis')
        plt.title(f'Cantidad de Equipos por {columna_categorica.capitalize()} en la competición')
        plt.ylabel('')
        
        self.guardar_grafico(f'diagrama_sectores_{columna_categorica.lower()}')

        plt.show()

analisis = AnalisisDatos()
ruta_csv = 'CSVS/equipos_modificado.csv'
datos = analisis.cargar_datos(ruta_csv)

analisis.resumen_estadistico(datos)
analisis.calcular_media_puntajes(datos, 'puntaje')
analisis.visualizar_distribucion_puntajes(datos, 'puntaje')
analisis.grafico_barras_promedio(datos, 'pais', 'puntaje')
analisis.regresion_lineal(datos, 'puntaje', 'pais_numerico')
analisis.diagrama_sectores_paises(datos, 'pais')
