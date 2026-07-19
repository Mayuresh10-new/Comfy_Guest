

import time
import plugwise

USB_PORT = "/dev/serial/by-id/usb-FTDI_FT232R_USB_UART_A6010MU7-if00-port0"

stick = plugwise.stick(
    USB_PORT,
    print_progress=True
)

stick.connect()
stick.initialize_stick()

print("\nScanning...\n")

stick.scan()

time.sleep(5)

print("\nAvailable methods:\n")

print(dir(stick))

stick.disconnect()