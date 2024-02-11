import requests
from bs4 import BeautifulSoup
import pandas as pd

url_pagina = 'https://www.flashscore.es/futbol/europa/champions-league-2021-2022/resultados/'

# Hacemos la petición a la página
pagina = requests.get(url_pagina)

# Creamos el objeto BeautifulSoup
soup = BeautifulSoup(pagina.content, 'html.parser')

# Buscamos el contenedor que contiene los resultados
contenedor_resultados = soup.find('body')  #aqui he probao ya muchas cosas y me sigue sin salir

# Verificamos si el contenedor de resultados existe
if contenedor_resultados:
    # Buscamos los elementos individuales de los resultados
    resultados = contenedor_resultados.find_all('div', class_='event__match event__match--static event__match--twoLine')

    # Creamos un DataFrame vacío
    df = pd.DataFrame()

    # Iteramos sobre los resultados
    for resultado in resultados:
        # Creamos un diccionario con los datos del resultado
        local = resultado.find('div', class_='event__participant event__participant--home')
        visitante = resultado.find('div', class_='event__participant event__participant--away')
        goles_local = resultado.find('div', class_='event__score event__score--home')
        goles_visitante = resultado.find('div', class_='event__score event__score--away')

        # Comprobamos si los elementos existen antes de intentar acceder a sus propiedades
        if local and visitante and goles_local and goles_visitante:
            datos = {
                'local': local.text.strip(),
                'visitante': visitante.text.strip(),
                'goles_local': goles_local.text.strip(),
                'goles_visitante': goles_visitante.text.strip()
            }
            # Añadimos una fila al DataFrame con los datos del resultado
            df = df.append(datos, ignore_index=True)

    # Verificamos si se encontraron datos
    if not df.empty:
        # Guardamos el DataFrame en un archivo CSV
        df.to_csv('resultados2.csv', index=False)
        print("Datos guardados correctamente en resultados.csv")
    else:
        print("No se encontraron datos válidos en los resultados.")
else:
    print("No se encontró el contenedor de resultados en la página.")
