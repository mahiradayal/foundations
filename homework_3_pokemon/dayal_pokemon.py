# Mahira Dayal
# Nov 3 2020

# Documentation: https://pokeapi.co/docs/v2
# Golduck: https://pokeapi.co/api/v2/pokemon/55

# library, module, package
# no module named 'requests'

import requests
import json

# Part One Pokemon API

url = "https://pokeapi.co/api/v2/pokemon/55"

response = requests.get(url, allow_redirects=True)
data = response.json()

print (data['height'])

# Height is 17 decimetres

url_version = "https://pokeapi.co/api/v2/version?limit=100"
version = requests.get(url_version, allow_redirects=True)
version_data = version.json()

# The API says count: 34, so I assume there are 34 counts, so 34 versions. 

print ("The number of versions listed is:",len(version_data['results']))

url_type = "https://pokeapi.co/api/v2/type/electric"
type = requests.get(url_type, allow_redirects=True)
version_type = type.json()

for x in version_type['pokemon']:
    print (x['pokemon']['name'])

# Info. for Korean: https://pokeapi.co/api/v2/language/3/

for y in version_type['names']:
    if y['language']['name'] == "ko":
        print (y['name'])

url_pikachu = "https://pokeapi.co/api/v2/pokemon/pikachu"
pikachu = requests.get(url_pikachu, allow_redirects=True)
version_pikachu = pikachu.json()

# print(json.dumps(version_pikachu, indent=2))

for z in version_pikachu['stats']:
    if z['stat']['name'] == 'speed':
        pikachu_speed = (z['base_stat'])
        print (pikachu_speed)

url_eevee = "https://pokeapi.co/api/v2/pokemon/eevee"
eevee = requests.get(url_eevee, allow_redirects=True)
version_eevee = eevee.json()

for w in version_eevee['stats']:
    if w['stat']['name'] == 'speed':
        eevee_speed = (w['base_stat'])
        print (eevee_speed)

if pikachu_speed>eevee_speed:
    print ("Pikachu has a higher speed stat")
elif eevee_speed>pikachu_speed:
    print ("Eevee has a higher speed stat")