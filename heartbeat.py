"""
Heartbeat rate is based on ultrasonic distance measurement.
Heartbeat will be displayed on 5x5 NeoPixel Grid BFF  (has RGB LEDs)
"""

import time
# from AdaFruit CircuitPython Bundle
import adafruit_us100
import board
import digitalio
import busio
import neopixel
from rainbowio import colorwheel
# from adafruit_datetime import time


# confirm this after fixing power supply board
powerSupply = digitalio.DigitalInOut(board.A1)
powerSupply.direction = digitalio.Direction.OUTPUT
powerSupply.value = True

# map of heart is used as mask for color data
# this heart is rotated clockwise 90 degrees.  This is because the board is
# mounted anti-clockwise 90 degrees on front of bot.
heart_bitmap = [
    0, 0, 1, 1, 0,
    0, 1, 1, 1, 1,
    1, 1, 1, 1, 0,
    0, 1, 1, 1, 1,
    0, 0, 1, 1, 0,
]

# this is a 'vertical' heart map.  It is not used in following code
heart_bitmap_vert = [
    0, 1, 0, 1, 0,
    1, 1, 1, 1, 1,
    1, 1, 1, 1, 1,
    0, 1, 1, 1, 0,
    0, 0, 1, 0, 0,
]

# pixels are addressed through A0
# auto_write was originally set to False, so that we could .show() on all pixels,
# but doesn't seem to make a difference
pixels = neopixel.NeoPixel(pin=board.A0, n=5*5, brightness=.00, auto_write=True)

# NOTE: need to find documenation for colorwheel, but I believe range is [0,255]
#       experiment to see what values produce what color
#
#       can also assign to pixels like this:
#       RED = 0x100000
#       RED = (0x10, 0, 0)
#       RED = (255, 0, 0)
#       pixels[i] = RED
color = colorwheel(255)
pixels[:] = [pixel * color for pixel in heart_bitmap]


# setup for communicating with ultrasonic sensor
uart = busio.UART(board.TX, board.RX, baudrate=9600)
us100 = adafruit_us100.US100(uart)

offTimeSeconds = 0.1
monitorRampDelaySeconds = 0.013
detectionThresholdMm = 110  # millimeters


# heartbeat lights up faster, fade away is slower
deltaRampUp = 0.025
deltaRampDown = -0.007

"""Enums not available in CircuitPython"""
class State:
    MONITOR = 1
    RAMPUP = 2
    RAMPDOWN = 3
    OFF = 4

robotState = State.MONITOR

while True:
    if (robotState == State.MONITOR):
        # as long as we are not within range, just keep checking
        while (detectionThresholdMm < us100.distance):
            time.sleep(monitorRampDelaySeconds)
        robotState = State.RAMPUP
        continue

    # rampUp, rampDown, and offState dont check distance. This allows a heartbeat cycle to
    # complete once it has started

    if (robotState == State.OFF):
        pixels.brightness = 0
        # OffState just waits here, no need to poll distance
        time.sleep(offTimeSeconds)
        robotState = State.MONITOR
        continue

    if (robotState == State.RAMPUP):
        while (pixels.brightness <= 0.25):    # 25% brightness is good enough for max value
            pixels.brightness += deltaRampUp
            time.sleep(monitorRampDelaySeconds)
        robotState = State.RAMPDOWN
        continue

    # always ramp down, even if not in detection range
    if (robotState == State.RAMPDOWN):
        while(0.001 <= pixels.brightness):     # use a value just above zero
            pixels.brightness += deltaRampDown
            time.sleep(monitorRampDelaySeconds)
        robotState = State.OFF
        continue





# test colors from colorwheel return result
    # for hue in range(0, 255, 3):
#         color = colorwheel(hue)
#         print(f'hue:{hue}   color: {color}')
#         pixels[:] = [pixel * color for pixel in heart_bitmap]
#         pixels.show()
#         time.sleep(.5)

