# Bot Lord Humongous
Heartbeat activates if bot senses nearby object.  Heartrate speeds up as object moves closer

## Description
This adds heartbeat to a bot sculpture. Heartbeat rate is based on ultrasonic distance measurement.
Heartbeat will be displayed on 5x5 LED grid. 

## Dependencies
- [Adafruit CircuitPython](https://github.com/adafruit/circuitpython)
- add required dependecies here
- 

## Hardware 
  * [dev board: AdaFruit QT Py SAMD21 Dev Board w/STEMMA QT](https://www.adafruit.com/product/4600)  Could use a variety of microprocessors, no need for high capability
  * [ultrasonic sensor: AdaFruit US-100](https://www.adafruit.com/product/4019)
  * [LED display: AdaFruit 5x5 NeoPixel Grid BFF Addon for QT Py and Xiao](https://www.adafruit.com/product/5646)
  * [lithium battery charger](https://www.amazon.com/gp/product/B0836J8LR4/)
  * [want to switch to this charger](https://www.adafruit.com/product/5397)



## Demo
![](https://github.com/teenyHermitCrab/Bot_LordHumongous/blob/main/hearbeat_demo.gif)



## TODO
- Replace bad battery pack.
- sometimes bot does not start when plugging in USB cable and need to press reset button. Add some logging and track this down
- Check `lib` folder on bot filesystem and verify there are no leftover dependencies not being used.
- Add required dependencies to this repo.
- Add a settings file so can adjust
  - max, min distance sensing (be sure to add sensor limitations as comments in file)
  - brightness
  - distance-to-heartrate function
- Are there other heartbeat modes to add? a rainbow color transition, scrolling heartbeat, is 5x5 enough to grow/shrink heartbeat image?

## Notes
- https://learn.adafruit.com/adafruit-qt-py/what-is-circuitpython
