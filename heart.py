import time
import busio
import board
import digitalio
import neopixel
from rainbowio import colorwheel

# TODO: make interface so we can substitute in different heart displays

class Heart:
    """display: 5x5 NeoPixel Grid BFF Addon for QT Py and Xiao.  https://www.adafruit.com/product/5646"""

    # map of heart is used as mask for color data
    #
    # this heart is rotated clockwise 90 degrees 
    # Top of heart points to right in 'image' below.  like this: <3
    # 
    # This is because the board is mounted anti-clockwise 90 degrees on front of bot.
    # This is just a 1D array, but this is the LED layout of physical NeoPixel board
    HEART_SHAPE_MAP = [
            0, 0, 1, 1, 0,
            0, 1, 1, 1, 1,
            1, 1, 1, 1, 0,
            0, 1, 1, 1, 1,
            0, 0, 1, 1, 0,
            ]


    def __init__(self, pin=board.A0, brightness=0.0 ):
        # validate inputs
        # A0-A?
        # brightness 0.0 - 1.0

        self.pixels = neopixel.NeoPixel(pin=pin, 
                                        n=5*5,    # this neopixel display is a 5x5 grid.  so 25 LEDs
                                        brightness=brightness, 
                                        auto_write=True)
        # TODO: test if there is an issue with setting to zero.
        self.brightness_min = 0.001   # corresponds to OFF,
        self.brightness_max = 0.25  # although this could go up to 1.0, using 0.25 as max value is bright enough
        self.rampup_bightness_delta = 0.025  # brightness step difference when looping to rampup heartbeat
        self.rampdown_brightness_delta = -0.007  # rampdown delay is smaller so that heartbeat decays slower that heartbeat 'turnon'
        self.seconds_between_beats = 0.1
        # if you dont set the color the color is nothing, so pixels dont get lit
        self.set_heart_color(255)  # red

    def set_heart_color(self, color_value:int):
        """Sets display color.  Does not change brightness"""

        #TODO need to check: values likely [0,255]
        # validate input.  or: what happens if negative or > 255

        color = colorwheel(color_value)
        self.pixels[:] = [pixel * color for pixel in Heart.HEART_SHAPE_MAP]


    def set_heart_brightness(self, brightness:float):
        """Set display brightness.  0.25 appears to be a good max value"""
        
        # TODO what happens if you set values to negative or above 1.0?

        if brightness < 0:
            new_value = 0
        elif brightness > 1.0:
            new_value = 1.0
        else:
            new_value = brightness

        self.pixels.brightness = new_value

    def calculate_ramp_delay(self, distance_cm:float):
        """Calculates the delay between brightness adjustments when ramping up/down heartbeat.
        
           This allows the heartbeat to speed up when distance is closer."""

        # TODO: could make this a ctor  parameter and/or property
        # could pass in a tuple representing coefficients of a polynomial
        #
        # for now this is just a first pass using a spreadsheet (exercise: use python)
        return 0.015 - ((-1.3e-4 * distance_cm) + 0.0147)

    def trigger_1_beat(self, distance_cm):
        """Trigger 1 heartbeat.  
        
        This is rampup brightness to peak, rampdown to off, and a wait that refects duration to next beat.
        It looks better if rampup is shorter than the rampdown decay."""

        delay_between_brightness_changes_seconds = self.calculate_ramp_delay(distance_cm)

        self.rampup(delay_between_brightness_changes_seconds)
        self.rampdown(delay_between_brightness_changes_seconds)

        # TODO: adjust the sleep between beats based on distance
        time.sleep(self.seconds_between_beats)


    def rampup(self, delay_seconds:float):
        while self.pixels.brightness <= self.brightness_max:
            self.pixels.brightness += self.rampup_bightness_delta
            time.sleep(delay_seconds)
        
    def rampdown(self, delay_seconds:float):
        while(self.brightness_min <= self.pixels.brightness):     # TODO: need use a value just above zero?
            # print(f'    in rampdown:  {self.pixels.brightness}')
            self.pixels.brightness += self.rampdown_brightness_delta
            time.sleep(delay_seconds)