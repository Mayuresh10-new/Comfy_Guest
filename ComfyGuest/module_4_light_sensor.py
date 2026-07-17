#!/usr/bin/env python3
# module_4_light_sensor.py

import grovepi


class LightSensor:
    def __init__(self, port=0, threshold=400):
        """
        Initialize Grove Light Sensor

        port      : Analog port number
        threshold : Darkness threshold
        """

        self.port = port
        self.threshold = threshold

        self.value = None

    def read(self):
        """
        Reads the light sensor.

        Returns:
            Analog value (0-1023)
        """

        try:
            value = grovepi.analogRead(self.port)

            if 0 <= value <= 1023:
                self.value = value

        except IOError:
            pass

        return self.value

    def is_dark(self):
        """
        Returns True if the room is dark.
        """

        value = self.read()

        if value is None:
            return False

        return value < self.threshold

    def brightness_percentage(self):
        """
        Returns brightness as a percentage.
        """

        value = self.read()

        if value is None:
            return 0.0

        return round((value / 1023) * 100, 1)