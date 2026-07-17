#!/usr/bin/env python3
# module_6_switch_controller.py

import time
import grovepi


class SwitchController:
    def __init__(self, port=3):
        """
        Initialize Switch Controller

        port : Digital port number
        """

        self.port = port

        grovepi.pinMode(self.port, "INPUT")

        self.last_state = 0

        self.manual_mode = False

        # Manual state for every actuator. The physical button only
        # ever drives "relay" directly (see update() below). The other
        # actuators are set via dashboard-issued manual commands, but
        # live here too so main.py has one place to read from.
        self.manual_states = {
            "relay": False,
            "room_led": False,
            "status_led": False,
            "new_led": False,
            "circle": False,
            "circle_plus": False,
        }

    def update(self):
        """
        Reads the physical button and updates the manual control state.

        Returns:
            True  -> Button was pressed
            False -> No new button press
        """

        pressed = False

        try:
            current = grovepi.digitalRead(self.port)

            # Rising edge detection
            if current == 1 and self.last_state == 0:

                pressed = True

                # First press enters Manual Mode
                if not self.manual_mode:
                    self.manual_mode = True
                    self.manual_states["relay"] = True

                # Subsequent presses toggle the relay only.
                # (The physical button was only ever wired to the relay;
                # the other actuators are controlled from the dashboard.)
                else:
                    self.manual_states["relay"] = not self.manual_states["relay"]

                # Debounce
                time.sleep(0.2)

            self.last_state = current

        except IOError:
            pass

        return pressed

    def apply_manual_command(self, command: dict):
        """
        Merges an externally-issued manual command (e.g. from the
        dashboard) into the current state. Only keys present in the
        command are updated — anything omitted is left untouched.
        """

        if "manual_mode" in command:
            self.manual_mode = bool(command["manual_mode"])

        for key in self.manual_states.keys():
            if key in command:
                self.manual_states[key] = bool(command[key])

    @property
    def manual_relay(self):
        """Kept for backwards compatibility with older code."""
        return self.manual_states["relay"]

    def auto_mode(self):
        """
        Switch back to Automatic Mode.
        """

        self.manual_mode = False

        for key in self.manual_states.keys():
            self.manual_states[key] = False

    def get_mode(self):
        """
        Returns the current operating mode.

        Returns:
            "MANUAL" or "AUTO"
        """

        if self.manual_mode:
            return "MANUAL"

        return "AUTO"