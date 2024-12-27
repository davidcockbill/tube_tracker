#!/usr/bin/python3

import requests
import json
from tabulate import tabulate
import RPi.GPIO as GPIO
import time

VICTORIA_PIN = 13
PIMLICO_PIN = 11
VAUXHALL_PIN = 7
STOCKWELL_PIN = 5
BRIXTON_PIN = 3

STATIONS = [
'Walthamstow Central Underground Station',
'Blackhorse Road Underground Station',  
'Tottenham Hale Underground Station',      
'Seven Sisters Underground Station',   
'Finsbury Park Underground Station',    
'Highbury & Islington Underground Station',   
'Kings Cross St. Pancras Underground Station',
'Euston Underground Station',      
'Warren Street Underground Station',  
'Oxford Circus Underground Station',
'Green Park Underground Station',
'Victoria Underground Station',
'Pimlico Underground Station',
'Vauxhall Underground Station', 
'Stockwell Underground Station',
'Brixton Underground Station',    
]
NORTHBOUND_STATIONS = STATIONS
SOUTHBOUND_STATIONS = STATIONS[::-1]

NORTHBOUND_ALL = {
'Walthamstow Central Underground Station': ['At Walthamstow Central'],
'Black - Walt': ['Departed Blackhorse Road', 'Departing Blackhorse Road', 'Between Blackhorse Road and Walthamstow Central', 'Approaching Walthamstow Central'],
'Blackhorse Road Underground Station': ['At Blackhorse Road'],
'Tott - Black': ['Departed Tottenham Hale', 'Departing Tottenham Hale', 'Between Tottenham Hale and Blackhorse Road', 'Approaching Blackhorse Road'],
'Tottenham Hale Underground Station': ['At Tottenham Hale'],
'Seven - Tott': ['Departed Seven Sisters', 'Departing Seven Sisters', 'Between Seven Sisters and Tottenham Hale', 'Approaching Tottenham Hale'],      
'Seven Sisters Underground Station': ['At Seven Sisters Platform 5', 'At Seven Sisters'], 
'Fin - Seven': ['Departed Finsbury Park', 'Departing Finsbury Park', 'Between Finsbury Park and Seven Sisters', 'Approaching Seven Sisters'],
'Finsbury Park Underground Station': ['At Finsbury Park'],
'High - Fin':['Departed Highbury & Islington', 'Departing Highbury & Islington', 'Between Highbury & Islington and Finsbury Park', 'Approaching Finsbury Park'],
'Highbury & Islington Underground Station': ['At Highbury & Islington'],  
'King - High': ['Departed Kings Cross St. Pancras', 'Departing Kings Cross St. Pancras', 'Between Kings Cross St. Pancras and Highbury & Islington', 'Approaching Highbury & Islington'],
'Kings Cross St. Pancras Underground Station': ['At Kings Cross St. Pancras'],
'Eus - King':['Departed Euston', 'Departing Euston', 'Between Euston and Kings Cross St. Pancras', 'Approaching Kings Cross St. Pancras'],
'Euston Underground Station': ['At Euston'],      
'War - Eus': ['Departed Warren Street', 'Departing Warren Street', 'Between Warren Street and Euston', 'Approaching Euston'],
'Warren Street Underground Station': ['At Warren Street'],  
'Ox - War': ['Departed Oxford Circus', 'Departing Oxford Circus', 'Between Oxford Circus and Warren Street', 'Approaching Warren Street'],
'Oxford Circus Underground Station': ['At Oxford Circus'],
'Green - Ox': ['Departed Green Park', 'Departing Green Park', 'Between Green Park and Oxford Circus', 'Approaching Oxford Circus'],
'Green Park Underground Station': ['At Green Park'],
'Vic - Green': ['Departed Victoria', 'Departing Victoria', 'Between Victoria and Green Park', 'Approaching Green Park'],
'Victoria Underground Station': ['At Victoria'],
'Pim - Vic': ['Departed Pimlico', 'Departing Pimlico', 'Between Pimlico and Victoria', 'Approaching Victoria'],
'Pimlico Underground Station': ['At Pimlico'],
'Vaux - Pim': ['Departed Vauxhall', 'Departing Vauxhall', 'Between Vauxhall and Pimlico', 'Approaching Pimlico'],
'Vauxhall Underground Station': ['At Vauxhall'], 
'Stock - Vaux': ['Departed Stockwell', 'Departing Stockwell', 'Between Stockwell and Vauxhall', 'Approaching Vauxhall'],
'Stockwell Underground Station': ['At Stockwell'],
'Brix - Stock': ['Departed Brixton', 'Departing Brixton', 'Between Brixton and Stockwell', 'Approaching Stockwell'],
'Brixton Underground Station': ['At Brixton','Brixton Area'],
}

SOUTHBOUND_ALL = {
'Walthamstow Central Underground Station': ['At Walthamstow Central'],
'Black - Walt': ['Departed Walthamstow Central', 'Departing Walthamstow Central', 'Between Walthamstow Central and Blackhorse Road', 'Between Blackhorse Road and Walthamstow Central','Approaching Blackhorse Road'],
'Blackhorse Road Underground Station': ['At Blackhorse Road'],
'Tott - Black': ['Departed Blackhorse Road', 'Departing Blackhorse Road', 'Between Blackhorse Road and Tottenham Hale', 'Approaching Tottenham Hale'],
'Tottenham Hale Underground Station': ['At Tottenham Hale'],
'Seven - Tott': ['Departed Tottenham Hale', 'Departing Tottenham Hale', 'Between Tottenham Hale and Seven Sisters', 'Approaching Seven Sisters'],      
'Seven Sisters Underground Station': ['At Seven Sisters Platform 5', 'At Seven Sisters'], 
'Fin - Seven': ['Departed Seven Sisters', 'Departing Seven Sisters', 'Between Seven Sisters and Finsbury Park', 'Approaching Finsbury Park'],
'Finsbury Park Underground Station': ['At Finsbury Park'],
'High - Fin':['Departed Finsbury Park', 'Departing Finsbury Park', 'Between Finsbury Park and Highbury & Islington', 'Approaching Highbury & Islington'],
'Highbury & Islington Underground Station': ['At Highbury & Islington'],  
'King - High': ['Departed Highbury & Islington', 'Departing Highbury & Islington', 'Between Highbury & Islington and Kings Cross St. Pancras', 'Approaching Kings Cross St. Pancras'],
'Kings Cross St. Pancras Underground Station': ['At Kings Cross St. Pancras'],
'Eus - King':['Departed Kings Cross St. Pancras', 'Departing Kings Cross St. Pancras', 'Between Kings Cross St. Pancras and Euston', 'Approaching Euston'],
'Euston Underground Station': ['At Euston'],      
'War - Eus': ['Departed Euston', 'Departing Euston', 'Between Euston and Warren Street', 'Approaching Warren Street'],
'Warren Street Underground Station': ['At Warren Street'],  
'Ox - War': ['Departed Warren Street', 'Departing Warren Street', 'Between Warren Street and Oxford Circus', 'Approaching Oxford Circus'],
'Oxford Circus Underground Station': ['At Oxford Circus'],
'Green - Ox': ['Departed Oxford Circus', 'Departing Oxford Circus', 'Between Oxford Circus and Green Park', 'Approaching Green Park'],
'Green Park Underground Station': ['At Green Park'],
'Vic - Green': ['Departed Green Park', 'Departing Green Park', 'Between Green Park and Victoria', 'Approaching Victoria'],
'Victoria Underground Station': ['At Victoria'],
'Pim - Vic': ['Departed Victoria', 'Departing Victoria', 'Between Victoria and Pimlico', 'Approaching Pimlico'],
'Pimlico Underground Station': ['At Pimlico'],
'Vaux - Pim': ['Departed Pimlico', 'Departing Pimlico', 'Between Pimlico and Vauxhall', 'Approaching Vauxhall'],
'Vauxhall Underground Station': ['At Vauxhall'], 
'Stock - Vaux': ['Departed Vauxhall', 'Departing Vauxhall', 'Between Vauxhall and Stockwell', 'Approaching Stockwell'],
'Stockwell Underground Station': ['At Stockwell'],
'Brix - Stock': ['Departed Stockwell', 'Departing Stockwell', 'Between Stockwell and Brixton', 'Approaching Brixton'],
'Brixton Underground Station': ['At Brixton','Brixton Area'],
}

STATIONS_ENUM = {
'0':'Walthamstow Central Underground Station',
'1':'Black - Walt',
'2':'Blackhorse Road Underground Station',
'3':'Tott - Black',
'4':'Tottenham Hale Underground Station',
'5':'Seven - Tott',
'6':'Seven Sisters Underground Station',
'7':'Fin - Seven',
'8':'Finsbury Park Underground Station',
'9':'High - Fin',
'10':'Highbury & Islington Underground Station',
'11':'King - High',
'12':'Kings Cross St. Pancras Underground Station',
'13':'Eus - King',
'14':'Euston Underground Station',
'15':'War - Eus',
'16':'Warren Street Underground Station',
'17':'Ox - War',
'18':'Oxford Circus Underground Station',
'19':'Green - Ox',
'20':'Green Park Underground Station',
'21':'Vic - Green',
'22':'Victoria Underground Station',
'23':'Pim - Vic',
'24':'Pimlico Underground Station',
'25':'Vaux - Pim',
'26':'Vauxhall Underground Station',
'27':'Stock - Vaux',
'28':'Stockwell Underground Station',
'29':'Brix - Stock',
'30':'Brixton Underground Station',
}

SOUTHBOUND_DESTINATIONS = ['Brixton Underground Station']
NORTHBOUND_DESTINATIONS = ['Walthamstow Central Underground Station','Seven Sisters Underground Station','Blackhorse Road Underground Station']






def predictions():
    data = request_data('https://api.tfl.gov.uk/Line/victoria/Arrivals')

    vehicles = {}
    for idx, vehicle in enumerate(data):
        vehicle_id = vehicle['vehicleId']
        station_name = vehicle['stationName']
        if vehicle_id not in vehicles:
            vehicles[vehicle_id] = []
        vehicles[vehicle_id].append(vehicle)

    vehicle = list(vehicles.values())[0]
    # vehicle = vehicles['222']
    vehicle_id = vehicle[0]['vehicleId']
    print(f'vehicle id = {vehicle_id}')

    sorted_info = sorted(vehicle, key=lambda x: x['timeToStation'])
    table_rows = []
    for entry in sorted_info:
        vehicle_id = entry['vehicleId']
        destinationName = entry['destinationName']
        timeToStation = entry['timeToStation']
        stationName = entry['stationName']
        currentLocation = entry['currentLocation']

        time = int(timeToStation/60)
        # print(f'[{vehicle_id}] stationName={stationName}, timeToStation={time}, currentLocation={currentLocation}')
        table_rows.append([stationName, time, currentLocation])

    headers = ['station', 'time (mins)', 'current location']
    table = tabulate(table_rows, headers, tablefmt='rounded_outline')
    print(table)

    # for vehicle_id, stations in vehicles.items():
    #     stations_list = ', '.join(stations)
    #     print(f'Vehicle: {vehicle_id} = {stations_list}')

    # for idx, entry in enumerate(data):
        # vehicle_id = entry['vehicleId']
        # station_name = entry['stationName']
        # print(f'[{idx}]: {vehicle_id} {station_name}')

    # write_file('/Users/davidcockbill/Desktop/tfl/prediction.json', data)


def get_victoria_line_trains():
    data = request_data('https://api.tfl.gov.uk/Line/victoria/Arrivals')

    trains = {}
    for idx, train in enumerate(data):
        vehicle_id = train['vehicleId']
        if vehicle_id not in trains:
            trains[vehicle_id] = []
        trains[vehicle_id].append(train)
    return trains


def request_data(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f'Error fetching data: {e}')


def write_file(filename, data):
    with open(filename, 'w') as file:
        file.write(json.dumps(data))  

def show_victoria_line():
    headers = ['station']
    table_data = [[station] for station in STATIONS]
    table = tabulate(table_data, headers, tablefmt='rounded_outline')
    print(table)

def get_key_from_value(dictionary, value):
    for station, labelArray in dictionary.items():
        for label in labelArray:
            if label == value:
                return station
    print(value)
    return 'Unknown'
       

def get_station_dictionaries():
    data = request_data('https://api.tfl.gov.uk/Line/victoria/Arrivals')

    northbound_data = {}
    southbound_data = {}
    doneTrains = []

    for train in data:
        # If the train has already been inputted into table, skip
        if train['vehicleId'] in doneTrains :
            continue
        else :
            #If it's going North..
            if train['destinationName'] in NORTHBOUND_DESTINATIONS:
                # If it's at a platform, use current station name
                if(train['currentLocation'] == 'At Platform'):
                    northbound_data[train['stationName']] = train['vehicleId']
                    doneTrains.append(train['vehicleId'])
                # Otherwise look at the current location and refer to dictionary to find station stop. Add to output data.
                else:
                    northbound_data[get_key_from_value(NORTHBOUND_ALL,train['currentLocation'])] = train['vehicleId']
                    doneTrains.append(train['vehicleId'])
            # If i's going South...
            elif train['destinationName'] in SOUTHBOUND_DESTINATIONS:
                if(train['currentLocation'] == 'At Platform'):
                    southbound_data[train['stationName']] = train['vehicleId']
                    doneTrains.append(train['vehicleId'])
                else:
                    southbound_data[get_key_from_value(SOUTHBOUND_ALL,train['currentLocation'])] = train['vehicleId']
                    doneTrains.append(train['vehicleId'])
            else:
                print(train)

    return northbound_data, southbound_data

def sort_dictionary(d):
    output = {}
    for i, label in STATIONS_ENUM.items():
        try :
            output[i] = d[label]
        except :
            output[i] = ''
    return output

def create_table(n,s):
    table_rows = []
    for key, value in STATIONS_ENUM.items():
        north = n[key]
        south = s[key]
        stationName = value
        table_rows.append([stationName, north, south])

    headers = ['station', 'north', 'south']
    table = tabulate(table_rows, headers, tablefmt='rounded_grid')
    return table

def setup_leds():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(VICTORIA_PIN, GPIO.OUT)
    GPIO.setup(PIMLICO_PIN, GPIO.OUT)
    GPIO.setup(VAUXHALL_PIN, GPIO.OUT)
    GPIO.setup(STOCKWELL_PIN, GPIO.OUT)
    GPIO.setup(BRIXTON_PIN, GPIO.OUT)


def led(pin, on):
    GPIO.output(pin, GPIO.HIGH if on else GPIO.LOW)

def set_station_led(pin, status):
    in_station = status != ''
    led(pin, in_station)

def main():
    trains = get_victoria_line_trains()

def harriet_show_lines():
    n, s = get_station_dictionaries()
    n = sort_dictionary(n)
    s = sort_dictionary(s)
    print(create_table(n,s))

if __name__ == '__main__':
    setup_leds()
    # harriet_show_lines()

    while True:
        n, s = get_station_dictionaries()
        n = sort_dictionary(n)
        s = sort_dictionary(s)
        print(create_table(n,s))

        # brixton_train = n['28'] != '' or s['28'] != ''
        # brixton_train = n['28'] != ''
        # print(f'{brixton_train}')
        # led(BRIXTON_PIN, brixton_train)

        set_station_led(VICTORIA_PIN, n['22'])
        set_station_led(PIMLICO_PIN, n['24'])
        set_station_led(VAUXHALL_PIN, n['26'])
        set_station_led(STOCKWELL_PIN, n['28'])
        set_station_led(BRIXTON_PIN, n['30'])
        time.sleep(10)



