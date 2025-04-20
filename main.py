#!/usr/bin/python3

import urequests
import network
import time
import ujson
from station_locator import locate, get_location, Direction, TRAIN_LOCATIONS
from wifi_config import WIFI_SSID, WIFI_PASSWORD


NAPTANS = {
    'walthamstow': '940GZZLUWWL',
    'victoria': '940GZZLUVIC',
    'brixton': '940GZZLUBXN',
    }


def wifi():
    last_timestamp = time.ticks_ms()

    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)

    wlan.connect(WIFI_SSID, WIFI_PASSWORD)

    connection_check_duration = 500
    retry = 0
    while True:
        timestamp = time.ticks_ms()
        if timestamp - last_timestamp > connection_check_duration:
            last_timestamp = timestamp
            if wlan.isconnected:
                break
            print(f'[{retry}] Waiting for wifi connection...')

        time.sleep(0.1)
        retry += 1

    network_info = wlan.ifconfig()
    print(f"Connected: {network_info}")


def request_data(url):
    try:
        response = urequests.get(url)
        print(f'status_code={response.status_code}')
        return ujson.loads(response.text)
    except Exception as e:
        print(f'Error fetching data: {e}')
    
    
def sort_trains(trains):
    filtered_trains = {}
    for train in trains:
        vehicle_id = train['vehicleId']
        if vehicle_id not in filtered_trains:
            filtered_trains[vehicle_id] = train
               
    sorted_trains = sorted(filtered_trains.values(), key=lambda x: x['timeToStation'])
    return sorted_trains


def get_victoria_line_trains(destination_station):
    template = 'https://api.tfl.gov.uk/Line/victoria/Arrivals/{station}'
    url = template.format(station=NAPTANS[destination_station])
    trains = request_data(url)
    return sort_trains(trains)
    

def print_trains(trains):
    for train in trains:
        vehicle_id = train['vehicleId']
        current_location = train['currentLocation']
        platform_name = train['platformName']
        print(f'[{vehicle_id}] {current_location}, platform={platform_name}')


def locate_trains(trains, direction):
    current_trains = {k: [] for k in TRAIN_LOCATIONS.keys()}
    for train in trains:
        vehicle_id = train['vehicleId']
        current_location = train['currentLocation']
        location = locate(direction, current_location)
        if location is not None:
            current_trains[location].append(vehicle_id)
        else:
            print(f'Could not locate {vehicle_id}: {current_location}')
    return current_trains


def print_located_trains(located_trains):
    for idx in range(0, len(located_trains)):
        location_number = str(idx)
        vehicle_list = located_trains[location_number]
        location = get_location(location_number)
        location = location if location and '-' not in location else ''
        vehicles = ', '.join(vehicle_list)
        print(f'{location:3}: {vehicles}')


if __name__ == '__main__':
    print(f'Starting..')
    northbound_trains = get_victoria_line_trains('walthamstow')
    #southbound_trains = get_victoria_line_trains('brixton')
    
    # print('NORTHBOUND:')
    # print_trains(northbound_trains)
    # print('SOUTHBOUND:')
    # print_trains(southbound_trains)

    located_trains = locate_trains(northbound_trains, Direction.NORTHBOUND)
    print_located_trains(located_trains)


