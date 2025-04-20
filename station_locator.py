#!/usr/bin/python3

import re

class Direction:
    NORTHBOUND = 0
    SOUTHBOUND = 1

TRAIN_LOCATIONS = {
    '0': 'WAL',
    '1': 'WAL-BHR',
    '2': 'BHR',
    '3': 'BHR-TTH',
    '4': 'TTH',
    '5': 'TTH-SVS',
    '6': 'SVS',
    '7': 'SVS-FPK',
    '8': 'FPK',
    '9': 'FPK-HBY',
    '10': 'HBY',
    '11': 'HBY-KXX',
    '12': 'KXX',
    '13': 'KXX-EUS',
    '14': 'EUS',
    '15': 'EUS-WST',
    '16': 'WST',
    '17': 'WST-OXC',
    '18': 'OXC',
    '19': 'OXC-GPK',
    '20': 'GPK',
    '21': 'GPK-VIC',
    '22': 'VIC',
    '23': 'VIC-PIM',
    '24': 'PIM',
    '25': 'PIM-VUX',
    '26': 'VUX',
    '27': 'VUX-STK',
    '28': 'STK',
    '29': 'STK-BRX',
    '30': 'BRX',
}

STATION_CODE_LOOKUP = {
    'WAL': 'Walthamstow Central',
    'BHR': 'Blackhorse Road',
    'TTH': 'Tottenham Hale',
    'SVS': 'Seven Sisters',
    'FPK': 'Finsbury Park',
    'HBY': 'Highbury & Islington',
    'KXX': 'Kings Cross St. Pancras',
    'EUS': 'Euston',
    'WST': 'Warren Street',
    'OXC': 'Oxford Circus',
    'GPK': 'Green Park',
    'VIC': 'Victoria',
    'PIM': 'Pimlico',
    'VUX': 'Vauxhall',
    'STK': 'Stockwell',
    'BRX': 'Brixton',
}

STATIONS = [ 
    'Walthamstow Central',
    'Blackhorse Road',
    'Tottenham Hale',
    'Seven Sisters',
    'Finsbury Park',
    'Highbury & Islington',
    'Kings Cross St. Pancras',
    'Euston',
    'Warren Street',
    'Oxford Circus',
    'Green Park',
    'Victoria',
    'Pimlico',
    'Vauxhall',
    'Stockwell',
    'Brixton',
]


def truncate_station_name(station_name):
    # The station names are sometimes truncated
    return station_name[:10]

def get_location_number(code):
    for k, v in TRAIN_LOCATIONS.items():
        if v == code:
            return k

def get_between_location_number(code1, code2):
    between_location_code = '{}-{}'.format(code1, code2)
    location_number = get_location_number(between_location_code)
    if location_number is not None:
        return location_number
        
    between_location_code = '{}-{}'.format(code2, code1)
    location_number = get_location_number(between_location_code)
    if location_number is not None:
        return location_number


def get_location(location_number):
    for k, v in TRAIN_LOCATIONS.items():
        if k == location_number:
            return v


def get_station_code(station_name):
    for k, v in STATION_CODE_LOOKUP.items():
        if truncate_station_name(v) in station_name:
            return k

def get_previous_station(station):
    stations = [station for station in STATIONS]
    for i in range(1, len(stations)):
        if truncate_station_name(station) in stations[i]:
            return stations[i - 1]
        

def get_next_station(station):
    stations = [station for station in STATIONS]
    for i in range(0, len(stations)-1):
        if truncate_station_name(station) in stations[i]:
            return stations[i + 1]


def approaching_matcher(direction, current_location):
    pattern = re.compile(r'Approaching (.*)')
    match = pattern.search(current_location)
    if match:
        destination_station = match.group(1)
        source_station = get_previous_station(destination_station) if direction == Direction.SOUTHBOUND else get_next_station(destination_station)
        code1 = get_station_code(destination_station)
        code2 = get_station_code(source_station)
        return get_between_location_number(code1, code2)
    

def departing_matcher(direction, current_location):
    pattern = re.compile(r'Depart(?:ed|ing) (.*)')
    match = pattern.search(current_location)
    if match:
        source_station = match.group(1)
        destination_station = get_next_station(source_station) if direction == Direction.SOUTHBOUND else get_previous_station(source_station)
        code1 = get_station_code(destination_station)
        code2 = get_station_code(source_station)
        return get_between_location_number(code1, code2)


def between_matcher(current_location):
    pattern = re.compile(r'Between (.*) and (.*)')
    match = pattern.search(current_location)
    if match:
        code1 = get_station_code(match.group(1))
        code2 = get_station_code(match.group(2))
        return get_between_location_number(code1, code2)
    

def at_matcher(direction, current_location):
    pattern = re.compile(r'At (.*)')
    match = pattern.search(current_location)
    if match:
        station = match.group(1)
        if station.lower() == 'platform':
            code = 'WAL' if direction is Direction.NORTHBOUND else 'BRX'
        else:
            code = get_station_code(station)

        if code is not None:
            return get_location_number(code)
    

def locate(direction, current_location):
    print(f'current_location={current_location}')

    location_number = between_matcher(current_location)
    if location_number is not None:
        return location_number
    
    location_number = at_matcher(direction, current_location)
    if location_number is not None:
        return location_number
    
    location_number = approaching_matcher(direction, current_location)
    if location_number is not None:
        return location_number
    
    location_number = departing_matcher(direction, current_location)
    if location_number is not None:
        return location_number


if __name__ == '__main__':
    # location_number = locate(Direction.NORTHBOUND, 'Between Blackhorse Road and Walthamstow Central')
    # print(f'{location_number}')

    # location_number = locate(Direction.NORTHBOUND, 'At Kings Cross St. Pancras')
    # print(f'{location_number}')

    # location_number = locate(Direction.NORTHBOUND, 'At Platform')
    # print(f'{location_number}')

    # location_number = locate(Direction.SOUTHBOUND, 'At Platform')
    # print(f'{location_number}')

    # location_number = locate(Direction.SOUTHBOUND, 'Approaching Seven Sisters')
    # print(f'{location_number}')

    # location_number = locate(Direction.SOUTHBOUND, 'Between Kings Cross St. Pancras and Highbury & Isl')
    # print(f'{location_number}')


    location_number = locate(Direction.NORTHBOUND, 'Departing Stockwell')
    print(f'{location_number}')

    location_number = locate(Direction.SOUTHBOUND, 'Departing Stockwell')
    print(f'{location_number}')
