import time
from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd

url_pagina = 'https://www.flashscore.es/futbol/europa/champions-league-2021-2022/resultados/'

# Usar Selenium para abrir la página
driver = webdriver.Chrome()  # Necesitas tener instalado ChromeDriver
driver.get(url_pagina)

# Esperar a que la página se cargue dinámicamente (ajusta el tiempo de espera si es necesario)
time.sleep(10)  # Aumenté el tiempo de espera a 10 segundos, ajusta según sea necesario

# Obtener el código fuente de la página después de la ejecución de JavaScript
page_source = driver.page_source

# Cerrar el navegador controlado por Selenium después de obtener el código fuente
driver.quit()

# Crear objeto BeautifulSoup
soup = BeautifulSoup(page_source, 'html.parser')

# Obtener el número de resultados
resultados = soup.find_all('div', class_='event__match event__match--static event__match--last event__match--twoLine')
print(f'Se encontraron {len(resultados)} resultados.')

df = pd.DataFrame()

for resultado in resultados:
    local_element = resultado.find('div', class_='event__participant event__participant--home')
    visitante_element = resultado.find('div', class_='event__participant event__participant--away')
    goles_local_element = resultado.find('div', class_='event__score event__score--home')
    goles_visitante_element = resultado.find('div', class_='event__score event__score--away')

    # Verificar si se encontraron los elementos antes de acceder a sus atributos
    if local_element and visitante_element and goles_local_element and goles_visitante_element:
        datos = {
            'local': local_element.text,
            'visitante': visitante_element.text,
            'goles_local': goles_local_element.text,
            'goles_visitante': goles_visitante_element.text
        }
        df = pd.concat([df, pd.DataFrame([datos])], ignore_index=True)

# Guardar el DataFrame en un archivo CSV
df.to_csv('4resultadosss.csv', index=False)
