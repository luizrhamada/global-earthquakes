"""
Vamos criar um mapa mostrando a localização dos terremotos ocorridos num período de 30 dias anteriores, bem como a
localização dos epicentros e a magnitude de cada um deles.

Fonte: https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_month.geojson. Acessado em 7 de janeiro de 2025.
"""

from pathlib import Path
import json
import plotly.express as px

"""
Criamos uma pasta com nome desejado ("nome_da_pasta"), de maneira que faremos acesso a essa pasta o arquivo específico 
que iremos trabalhar. Ressalta-se que a pasta deve ser criada onde esta sendo armazenado os programas do seu projeto.
"""

arq = Path('global_data_earthquake/earthquake_data_07JAN2025.geojson') # últimos 30 dias de registro
file = open(arq, encoding="utf8")
contents = file.read()
all_earthquake_data = json.loads(contents)

"""
{
    "type": "FeatureCollection",
    "metadata": {
        "generated": 1736277525000,
        "url": "https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_month.geojson",
        "title": "USGS All Earthquakes, Past Month",
        "status": 200,
        "api": "1.14.1",
        "count": 9539
    },
...

Metadata nos informa quando o arquivo foi gerado, onde podemos encontrar os dados online, número de terremotos gerados 
em um período de 24 horas, título legível por humanos.

A chave 'properties' contém várias informações sobre o terremoto. Desejamos plotar em um mapa mundi os pontos onde 
ocorreram abalos sísmicos, suas coordenadas e a magnitude. As informações que é de interesse é a magnitude ('mag') e o 
título ('title'), na chave 'properties'. A chave 'geometry' fornece informações acerca do local em que ocorreu o 
terremoto, logo, precisaremos das informações de latitude e longitude para mapear o evento.

IMPORTANTE: O formato GeoJSON segue a convenção (longitude, latitude).
"""

# Primeiramente, vamos criar uma lista que examina todos os terremotos
all_earthquake = all_earthquake_data['features']
# print(len(all_eq_dicts)) # contém 160 registros de terremotos

"""
Podemos percorrer uma lista contendo os dados sobre cada terremoto com um loop e extrair qualquer informação que 
quisermos
"""

"""
Dentro do loop, cada terremoto será representado por eq_dict. Aqui, a magnitude e o título estão esta armazenados em 
'properties' desse dicionário, com a chave 'mag' e 'title'. A localização esta armazenada em 'geometry' com a chave 
'coordinates'.
"""

# Magnitude, Localização

mags, lons, lats, eq_titles = [], [], [], []
for earthquake_dict in all_earthquake:
    mag = earthquake_dict['properties']['mag']
    lon = earthquake_dict['geometry']['coordinates'][0] # Lembrando que GeoJSON segue a convenção (longitude, latitude)
    lat = earthquake_dict['geometry']['coordinates'][1]
    eq_title = earthquake_dict['properties']['title']
    mags.append(mag)
    lons.append(lon)
    lats.append(lat)
    eq_titles.append(eq_title)

print(mags[:5]) # [1.6, 1.6, 2.2, 3.7, 2.92000008]
print(lons[:5]) # [-150.7585, -153.4716, -148.7531, -159.6267, -155.248336791992]
print(lats[:5]) # [61.7591, 59.3152, 63.1633, 54.5612, 18.7551670074463]

"""Escala de cores: 

['aggrnyl', 'agsunset', 'blackbody', 'bluered', 'blues', 'blugrn', 'bluyl', 'brwnyl', 'bugn', 'bupu', 'burg', 'burgyl', 
'cividis', 'darkmint', 'electric', 'emrld', 'gnbu', 'greens', 'greys', 'hot', 'inferno', 'jet', 'magenta', 'magma', 
'mint', 'orrd', 'oranges', 'oryel', 'peach', 'pinkyl', 'plasma', 'plotly3', 'pubu', 'pubugn', 'purd', 'purp', 'purples', 
'purpor', 'rainbow', 'rdbu', 'rdpu', 'redor', 'reds', 'sunset', 'sunsetdark', 'teal', 'tealgrn', 'turbo', 'viridis', 
'ylgn', 'ylgnbu', 'ylorbr', 'ylorrd', 'algae', 'amp', 'deep', 'dense', 'gray', 'haline', 'ice', 'matter', 'solar', 
'speed', 'tempo', 'thermal', 'turbid', 'armyrose', 'brbg', 'earth', 'fall', 'geyser', 'prgn', 'piyg', 'picnic', 
'portland', 'puor', 'rdgy', 'rdylbu', 'rdylgn', 'spectral', 'tealrose', 'temps', 'tropic', 'balance', 'curl', 'delta', 
'oxy', 'edge', 'hsv', 'icefire', 'phase', 'twilight', 'mrybm', 'mygbm']

"""
title = "Registros de atividades sísmicas ao redor do mundo (09/12/2024 - 07/01/2025)"
fig = px.scatter_geo(lat=lats, lon=lons, title=title,
                     color=mags,
                     color_continuous_scale='rainbow',
                     labels={'color': 'Magnitude na Escala Richter'},
                     projection='natural earth',
                     hover_name=eq_titles,
                     )
fig.show()
