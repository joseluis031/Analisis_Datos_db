import requests
from bs4 import BeautifulSoup


url_pagina = 'https://www.flashscore.es/futbol/europa/champions-league-2021-2022/resultados/'

# Hacemos la petición a la página
pagina = requests.get(url_pagina)

# Creamos el objeto BeautifulSoup
html = pagina.content
soup = BeautifulSoup(pagina.content, 'html.parser')

# Buscamos el elemento que contiene los resultados
resultados = soup.find('div')
#convertir a string
resultados_str = resultados.prettify() 


#creame un archivo html con el contenido de la pagina
with open('web2.html', 'w', encoding='utf-8') as file:
    file.write(resultados_str)