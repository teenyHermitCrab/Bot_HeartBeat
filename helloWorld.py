import time
# from Adafruit CircuitPython Library Bundle
import board
import neopixel

pixels = neopixel.NeoPixel(pin=board.NEOPIXEL, n=1, brightness=0.05)


# TODO: make this helloWorld an investigation of colorwheel, or add a new file for that

while True:
    pixels.fill((255, 0, 0))
    time.sleep(0.55)
    pixels.fill((0, 0, 0))
    time.sleep(0.25)
    pixels.fill((255, 255, 255))
    time.sleep(0.55)
    pixels.fill((0, 0, 0))
    time.sleep(0.25)
