import busio
import neopixel
from rainbowio import colorwheel
from distanceSensor import UltrasonicSensor
from heart import Heart
from robot import Robot


# Setup power supply
power_supply = digitalio.DigitalInOut(board.A1)
power_supply.direction = digitalio.Direction.OUTPUT
power_supply.value = True

# Instantiate objects
heart_display = HeartDisplay(pin=board.A0, brightness=0.1)
ultrasonic_sensor = UltrasonicSensor(tx_pin=board.TX, rx_pin=board.RX)
robot = Robot(heart_display=heart_display, ultrasonic_sensor=ultrasonic_sensor)

# Start the robot
robot.run()
