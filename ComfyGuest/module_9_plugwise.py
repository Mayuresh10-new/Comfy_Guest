#!/usr/bin/env python3
# module_9_plugwise.py

import time
import plugwise


class PlugwiseController:

    def __init__(
        self,
        usb,
        circle_plus_mac,
        circle_mac
    ):
        """
        Plugwise Controller

        usb              : USB serial device path
        circle_plus_mac  : Circle+ MAC address
        circle_mac       : Circle MAC address
        """

        self.usb = usb
        self.circle_plus_mac = circle_plus_mac
        self.circle_mac = circle_mac

        self.stick = None

        self.circle_plus = None
        self.circle = None

        self.circle_plus_state = False
        self.circle_state = False

        self.connect()

    ########################################################

    def connect(self):

        print("--------------------------------------")
        print("Connecting to Plugwise...")
        print("--------------------------------------")

        self.stick = plugwise.stick(
            self.usb,
            print_progress=False
        )

        self.stick.connect()
        self.stick.initialize_stick()
        self.stick.scan()

        print("Waiting for Plugwise devices...")

        while self.circle_plus is None or self.circle is None:

            if self.circle_plus is None:
                self.circle_plus = self.stick.node(
                    self.circle_plus_mac
                )

            if self.circle is None:
                self.circle = self.stick.node(
                    self.circle_mac
                )

            time.sleep(1)

        self.circle_plus_state = self.circle_plus.get_relay_state()
        self.circle_state = self.circle.get_relay_state()

        print("Plugwise Ready")

    ########################################################
    # Circle
    ########################################################

    def circle_on(self):

        try:

            self.circle.set_relay_state(True)
            self.circle_state = True

        except Exception as e:

            print("Circle ON Error:", e)

    def circle_off(self):

        try:

            self.circle.set_relay_state(False)
            self.circle_state = False

        except Exception as e:

            print("Circle OFF Error:", e)

    def circle_toggle(self):

        if self.circle_state:

            self.circle_off()

        else:

            self.circle_on()

    ########################################################
    # Circle+
    ########################################################

    def circle_plus_on(self):

        try:

            self.circle_plus.set_relay_state(True)
            self.circle_plus_state = True

        except Exception as e:

            print("Circle+ ON Error:", e)

    def circle_plus_off(self):

        try:

            self.circle_plus.set_relay_state(False)
            self.circle_plus_state = False

        except Exception as e:

            print("Circle+ OFF Error:", e)

    def circle_plus_toggle(self):

        if self.circle_plus_state:

            self.circle_plus_off()

        else:

            self.circle_plus_on()

    ########################################################

    def get_states(self):

        return {

            "circle": self.circle_state,
            "circle_plus": self.circle_plus_state

        }

    ########################################################

    def print_status(self):

        print("--------------------------------------")
        print("PLUGWISE STATUS")
        print("--------------------------------------")

        print("Circle      :", self.circle_state)
        print("Circle+     :", self.circle_plus_state)

        print("--------------------------------------")

    ########################################################

    def cleanup(self):

        try:

            if self.stick is not None:

                self.stick.disconnect()

                print("Plugwise Disconnected")

        except Exception as e:

            print("Plugwise Disconnect Error:", e)