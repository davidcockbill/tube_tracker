#!/usr/bin/python3

from machine import Pin
import time

# https://cdn-shop.adafruit.com/datasheets/sn74hc595.pdf


class LedDriver:
    TOTAL_LEDS = 16

    def __init__(self):
        self.data_pin = Pin(15, Pin.OUT)  # DS (Data input)
        self.clock_pin = Pin(14, Pin.OUT) # SH_CP (Shift clock)
        self.latch_pin = Pin(13, Pin.OUT) # ST_CP (Latch clock)
        self.oe_pin = Pin(12, Pin.OUT)
        self.mr_pin = Pin(11, Pin.OUT)
        
        self.oe_pin.low()  # 74HC595 output enable on low signal
        self.mr_pin.high() # 74HC595 output enable on low signal
        
    def write(self, data):
        self._shift_out(data)
        self._latch()

    # Shifts data serially to the 74HC595
    def _shift_out(self, data):
        for i in range(self.TOTAL_LEDS):  # Loop through each bit of the data
            if data & (1 << (self.TOTAL_LEDS - 1 - i)):
                self.data_pin.value(1)
            else:
                self.data_pin.value(0)
            
            self.clock_pin.value(1)  # Send clock pulse to shift data in
            self._wait()
            self.clock_pin.value(0)  # Reset clock

    # Latches data into the parallel output register
    def _latch(self):
        self.latch_pin.value(1)  # Enable latch to output the data
        self._wait()
        self.latch_pin.value(0)  # Disable latch to prevent further output changes
        
    @staticmethod
    def _wait():
        time.sleep_us(1)


if __name__ == '__main__':    
    leds = LedDriver()
    count = 0
    while True:
        leds.write(count)
        time.sleep(0.01)
        count += 1