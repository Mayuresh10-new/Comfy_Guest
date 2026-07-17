from module_5_output_controller import OutputController
import time

outputs = OutputController(
    relay_port=5,
    room_led_port=6,
    status_led_port=7
    new_led_port=4
)

while True:
    outputs.relay_on()
    outputs.room_light_on()
    outputs.status_led_on()
    print("ON")
    time.sleep(2)

    outputs.relay_off()
    outputs.room_light_off()
    outputs.status_led_off()
    print("OFF")
    time.sleep(2)