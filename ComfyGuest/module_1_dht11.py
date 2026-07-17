#!/usr/bin/env python3
# module_1_dht11.py

import grovepi
import time


class DHT11Sensor:
    def __init__(self, port=2):
        self.port = port
        self.sensor_type = 0

        self.temperature = None
        self.humidity = None

        self.last_read = 0

    def read(self):

        now = time.time()

        # only read every 2 seconds
        if now - self.last_read < 2:
            return self.temperature, self.humidity

        self.last_read = now

        try:
            temp, hum = grovepi.dht(self.port, self.sensor_type)
        
            if temp <= 0 or hum <= 0:
                time.sleep(0.05)
                temp, hum = grovepi.dht(self.port, self.sensor_type)
        
            if temp > 0 and hum > 0:
                self.temperature = temp
                self.humidity = hum
        
        except IOError:
            pass

        return self.temperature, self.humidity