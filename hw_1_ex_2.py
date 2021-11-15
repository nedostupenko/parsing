import json
import requests

# Mapbox Geocoding API
params = {'access_token': '***'}
address_1 = 'Москва проспект Андропова 28'
address_2 = 'Москва Красная площадь'
url_1 = f'https://api.mapbox.com/geocoding/v5/mapbox.places/{address_1}.json'
url_2 = f'https://api.mapbox.com/geocoding/v5/mapbox.places/{address_2}.json'

# Making coordinates from addresses
result_1 = requests.get(url_1, params=params)
result_2 = requests.get(url_2, params=params)

# Getting coordinates from JSON
j_data_1 = result_1.json()
print(str(j_data_1.get('features')[0].get('center'))[1:-1])
j_data_2 = result_2.json()
print(j_data_2.get('features')[0].get('center'))

# Mapbox Directions API
# Calculating distance and trip-time between two coordinates from addresses above
url_3 = f'https://api.mapbox.com/directions/v5/mapbox/driving/{str(j_data_1.get("features")[0].get("center"))[1:-1]};' \
        f'{str(j_data_2.get("features")[0].get("center"))[1:-1]}?annotations=maxspeed,distance,duration&overview=full&geometries=geojson'

result_3 = requests.get(url_3, params=params)
j_data_3 = result_3.json()

# Saving info from API in JSON-file
try:
    with open("navig.json", 'w') as navig:
        json.dump([j_data_1,j_data_2,j_data_3], navig, indent=4, ensure_ascii=False)
except IOError:
    print("Произошла ошибка ввода-вывода!")

# Print the result
print(f'По маршруту от {address_1}\n\t\tдо {address_2}\n'
      f'кратчайший путь составляет: {round(j_data_3.get("routes")[0].get("distance")/1000, 2)} км\n'
      f'примерное время в пути: {j_data_3.get("routes")[0].get("duration")//360} часов '
      f'{int(j_data_3.get("routes")[0].get("duration")%360/60)} минут')

