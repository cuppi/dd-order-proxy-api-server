import os
import csv

city_lines = None

with open(os.path.join(os.getcwd(), 'city.csv'), 'r') as readFile:
    reader = csv.reader(readFile)
    city_lines = [{
        'index': city[0],
        'name': city[1],
        'id': city[2]
    } for city in list(reader)]
    print(city_lines)
