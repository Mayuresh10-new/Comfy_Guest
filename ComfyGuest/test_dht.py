#!/usr/bin/env python3

import time
from module_1_dht11 import DHT11Sensor

dht = DHT11Sensor(port=2)

while True:

    t, h = dht.read()

    print(t, h)

    time.sleep(2)