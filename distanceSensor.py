import adafruit_us100
import board
import busio

class UltrasonicSensor:
    def __init__(self, tx_pin=board.TX, rx_pin=board.RX, baudrate=9600):
        uart = busio.UART(tx_pin, rx_pin, baudrate=baudrate)
        self.sensor = adafruit_us100.US100(uart)

    def get_distance(self):
        return self.sensor.distance