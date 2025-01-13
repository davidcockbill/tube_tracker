# Tube Tracker

Use the TFL API to track trains specifically on the Victoria Line.

The idea is to run this on a Raspberry PI Pico 2 W (wifi is obviously needed)

## API

API used is defined [here](https://api-portal.tfl.gov.uk/api-details#api=Line&operation=Line_ArrivalsWithStopPointByPathIdsPathStopPointIdQueryDirectionQueryDestina)

NOTE: The `direction` URL query parameter does not work consistently. I am assuming that this is due to the inconsistent presence of the 'direction' key in the returned JSON results.

## MicroPython

The Pico 2 can run Python and C++. I have chosen to use Python, however this is not the full Python release, but a cut down micro processor version called MicroPython.

This has some limitations:
1) Certain packages are replaced with a cut down version:
  - `requests` is replaced with `urequests`
  - `json` is replaced with `ujson`
2) Dictionaries do not preserve ordering. Therefore I have had to put in strange code to iterate stations in order.

## Code

Code to test this on my local PC is in `tube.py`
Code to run on the RPI Pico 2 W is in `main.py`

Both import `station_locator.py` to match the `currentLocation` key in the JSON results to a station.

### LEDs using 74HC595

There are limited GPIO pins for use on the Pico 2 W.

A solution is to use multiple shift registers (74HC595)

https://cdn-shop.adafruit.com/datasheets/sn74hc595.pdf
https://docs.arduino.cc/tutorials/communication/guide-to-shift-out/

Sample code is in led_driver.py

There are 30 train positions in both north and south directions; so 60 in total LEDs are required.

There are 28 GPIO pins in total on the Pico 2 W.

For a minimal hardware solution you would need:
- 3 GPIO pins to attach serially to the 74HC595
- This leaves 25 GPIO remaining for LEDs
- 60 total LEDs - 25 GPIO LEDs = 35 74HC595 driven LEDs
- This means 5 74HC595 chips are needed with capacity to spare.

Based on this I think the best solution is:
- 40 serial LEDs (5*74HC595)
- 20 GPIO LEDs
- 3 GPIO pins for serial control

This leaves 5 free GPIO pins for general purpose use! (maybe OE/MR control if needed)


## WiFi

I don't want to check in my wifi credentials therefore create a file called `wifi_config.py` with the following contents:

```
WIFI_SSID = '<ssid>'
WIFI_PASSWORD = '<password>'
```