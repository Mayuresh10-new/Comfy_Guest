#!/usr/bin/env python3
# module_7_hotel_automation_logic.py

class HotelAutomation:
    def __init__(self,
                 relay_on_temp=30,
                 relay_off_temp=27):
        """
        Hotel Automation Logic

        relay_on_temp  : Temperature (°C) to turn relay ON
        relay_off_temp : Temperature (°C) to turn relay OFF
        """

        self.relay_on_temp = relay_on_temp
        self.relay_off_temp = relay_off_temp

        # Stores the previous relay state (used for hysteresis)
        self.relay_state = False

    def update(
        self,
        temperature,
        occupied,
        dark,
        guest_near,
        manual_mode,
        manual_relay,
    ):
        """
        Updates the hotel automation logic.

        Parameters:
            temperature  : Current temperature (°C)
            occupied     : True if room is occupied
            dark         : True if room is dark
            guest_near   : True if someone is near the room
            manual_mode  : True if manual mode is enabled
            manual_relay : Relay state requested in manual mode

        Returns:
            Dictionary containing output states.
        """

        outputs = {}

        ##################################################
        # STATUS LED
        ##################################################

        outputs["status_led"] = guest_near

        ##################################################
        # ROOM LIGHT
        ##################################################

        outputs["room_led"] = occupied and dark

        ##################################################
        # RELAY
        ##################################################

        if manual_mode:

            # Manual mode overrides automatic control
            self.relay_state = manual_relay

        else:

            # Automatic temperature control
            if temperature is not None:

                # Relay ON above upper threshold
                if temperature >= self.relay_on_temp:
                    self.relay_state = True

                # Relay OFF below lower threshold
                elif temperature <= self.relay_off_temp:
                    self.relay_state = False

                # Otherwise, keep previous relay state
                # (Hysteresis)

        outputs["relay"] = self.relay_state

        return outputs