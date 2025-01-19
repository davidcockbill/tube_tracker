#!/usr/bin/python3

from machine import Pin, Timer

import time

# https://cdn-shop.adafruit.com/datasheets/sn74hc595.pdf


class LedMatrix:

    def __init__(self):
        # x axis pins
        self.x0 = Pin(0, Pin.OUT)
        self.x1 = Pin(1, Pin.OUT)
        self.x2 = Pin(2, Pin.OUT)
        self.x3 = Pin(3, Pin.OUT)
        self.x4 = Pin(4, Pin.OUT)
        self.x5 = Pin(5, Pin.OUT)
        self.x6 = Pin(6, Pin.OUT)
        self.x7 = Pin(7, Pin.OUT)
        
        # y axis pins
        self.y0 = Pin(12, Pin.OUT)
        self.y1 = Pin(13, Pin.OUT)
        self.y2 = Pin(14, Pin.OUT)
        self.y3 = Pin(15, Pin.OUT)
        
        # Pin to matrix mapping
        self.x_axis = [self.x0, self.x1, self.x2, self.x3, self.x4, self.x5, self.x6, self.x7]
        self.y_axis = [self.y0, self.y1, self.y2, self.y3]
        
        self.max_x = len(self.x_axis)
        self.max_y = len(self.y_axis)
        
        # Initialise matrix off
        [self.x_axis[x].off() for x in range(self.max_x)]
        [self.y_axis[y].off() for y in range(self.max_y)]
        
        self.y_refresh = 0
        
        # Define and set matrix to off
        self.matrix = [[False for x in range(self.max_x)] for y in range(self.max_y)]
        
        
        #self.timer = Timer(period=1000, mode=Timer.PERIODIC, callback=self.refresh)

        
    def set(self, led_id, on):
        x = int(led_id % self.max_x)
        y = int(led_id / self.max_x)
        self.matrix[y][x] = on
        
        
    def refresh(self):
        # Turn off current row
        self.y_axis[self.y_refresh].off()
        
        # Next row
        self._increment_y_refresh()
        y = self.y_refresh
        
        # Set all column values for new row
        for x in range(self.max_x):
            self.x_axis[x].value(self.matrix[y][x])
        
        # Turn on new row
        self.y_axis[y].on()
        print(f'[{y}]: on')

        
    def _increment_y_refresh(self):
        self.y_refresh += 1
        self.y_refresh %= len(self.y_axis)
        
        

if __name__ == '__main__':    
    matrix = LedMatrix()
    matrix.set(0, True)
    matrix.set(1, True)
    matrix.set(2, True)
    matrix.set(3, True)
    matrix.set(4, True)
    matrix.set(5, True)
    matrix.set(6, True)
    matrix.set(7, True)
    
    while True:
        matrix.matrix()
        time.sleep(1)
    