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

brightness = 0.00
delta = 0.01

# cheap way to maintain a state machine
inOffState = False
inRampUp = False
inRampDown = False
monitorDistance = True  #start in this state
inDetectionRange = False

# setup for communicating with ultrasonic sensor
uart = busio.UART(board.TX, board.RX, baudrate=9600)
us100 = adafruit_us100.US100(uart)

offTimeSeconds = 0.1
detectionThresholdMm = 110




count = 0

while True:
    # this is time between increment/decrementing brightness in RampUp/RampDown
    # It probably could be moved to inside RampUp/RampDown blocks
    time.sleep(0.013)


    if (monitorDistance):
        distance = us100.distance
        #print("distance: %.1f" % distance)
        inDetectionRange = (distance < detectionThresholdMm)
        if (inDetectionRange):
            # print("DETECTED")
            # print("  start RampUp")
            inRampUp = True
            inRampDown = False
            monitorDistance = False
            inOffState = False
        continue

    if (inOffState):
        pixels.brightness = 0
        # OffState just waits here, no need to poll distance
        time.sleep(offTimeSeconds)
        inOffState = False
        monitorDistance = True
        inRampUp = False
        inRampDown = False

    # always ramp down, even if not in detection range
    if (inRampDown):
        deltaRampDown = -0.007
        pixels.brightness += deltaRampDown
        pixels.show()
        if (pixels.brightness <= 0.001):
            # print("  start OFF")
            inOffState = True
            startTime = time.time()
            inRampUp = False
            inRampDown = False
            monitorDistance = False
        continue

    if (inRampUp):
        #if (not inDetectionRange):
        #    continue
        deltaRampDown = 0.025
        pixels.brightness += deltaRampDown
        #pixels.show()
        if (pixels.brightness >= 0.25):
            # print("  start RampDown")
            inOffState = False
            inRampUp = False
            inRampDown = True
            monitorDistance = False
        continue


# test colors from colorwheel return result
    # for hue in range(0, 255, 3):
#         color = colorwheel(hue)
#         print(f'hue:{hue}   color: {color}')
#         pixels[:] = [pixel * color for pixel in heart_bitmap]
#         pixels.show()
#         time.sleep(.5)

