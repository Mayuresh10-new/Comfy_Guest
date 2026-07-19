#!/usr/bin/env python3
# module_7_hotel_automation_logic.py

class HotelAutomation:
    def __init__(self, relay_on_temp=30, relay_off_temp=27):
        self.relay_on_temp = relay_on_temp
        self.relay_off_temp = relay_off_temp

        # Stores the previous relay state (used for hysteresis)
        self.relay_state = False

    def update(self, temperature, occupied, dark, guest_near, manual_mode, manual_relay):
        outputs = {}

        # STATUS LED
        outputs["status_led"] = guest_near

        # ROOM LIGHT
        outputs["room_led"] = occupied and dark

        # RELAY
        if manual_mode:
            # Manual mode overrides automatic control
            self.relay_state = manual_relay

        else:
            if temperature is not None:
                if temperature >= self.relay_on_temp:
                    self.relay_state = True
                elif temperature <= self.relay_off_temp:
                    self.relay_state = False
        outputs["relay"] = self.relay_state
        return outputs