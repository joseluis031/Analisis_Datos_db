import requests
from bs4 import BeautifulSoup


url_pagina = 'https://www.flashscore.es/futbol/europa/champions-league-2021-2022/resultados/'

# Hacemos la petición a la página
pagina = requests.get(url_pagina)

# Creamos el objeto BeautifulSoup
soup = BeautifulSoup(pagina.content, 'html.parser')

# Buscamos el elemento que contiene los resultados
resultados = soup.find_all('div', class_='event__match event__match--static')

# quiero acabar pasando los resultados a un archivo CSV
# pero antes, vamos a ver cómo se ven los resultados
for resultado in resultados:
    print(resultado.text)
    print('---')

# Ahora vamos a guardar los resultados en un archivo CSV
# Para ello, necesitamos la librería pandas
import pandas as pd

# Creamos un DataFrame vacío
df = pd.DataFrame()

# Iteramos sobre los resultados
for resultado in resultados:
    # Creamos un diccionario con los datos del resultado
    datos = {
        'local': resultado.find('div', class_='event__participant--home').text,
        'visitante': resultado.find('div', class_='event__participant--away').text,
        'goles_local': resultado.find('div', class_='event__score--home').text,
        'goles_visitante': resultado.find('div', class_='event__score--away').text
    }
    # Añadimos una fila al DataFrame con los datos del resultado
    df = df.append(datos, ignore_index=True)
    
# Guardamos el DataFrame en un archivo CSV
df.to_csv('resultados.csv', index=False)
