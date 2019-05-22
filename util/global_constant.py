import os
import csv
import threading

lock = threading.Lock()


def get_city_lines(force_refresh=False):
    global city_lines
    if force_refresh or city_lines is None:
        with lock:
            with open(os.path.join(os.getcwd(), 'city.csv'), 'r') as readFile:
                reader = csv.reader(readFile)
                city_lines = [{
                    'index': city[0],
                    'name': city[1],
                    'id': city[2]
                } for city in list(reader)]
        return city_lines
    return city_lines


city_lines = get_city_lines(True)
