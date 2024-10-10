import adafruit_us100
import board
import busio

# TODO: make an interface so we can substitute in specific sensors

class UltrasonicSensor:
    """ sensor: AdaFruit US-100.  https://www.adafruit.com/product/4019 """

    def __init__(self, tx_pin=board.TX, rx_pin=board.RX, baudrate=9600):
        uart = busio.UART(tx_pin, rx_pin, baudrate=baudrate)
        self.sensor = adafruit_us100.US100(uart)

    def get_distance(self) -> float:
        """Return detection distance in cm.  If no detection, then it returns 1110.6
           
           detection range is 2.0 cm - 140.0 cm

           if less than 2.0 cm, then value returned can be erratic: sometimes will return a no-detect-value 
           and sometime will return an erroneous value"""
        return self.sensor.distance