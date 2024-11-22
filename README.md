Simple project using following hardware:
  * dev board:         AdaFruit QT Py SAMD21 Dev Board w/STEMMA QT. https://www.adafruit.com/product/4600
  * ultrasonic sensor: AdaFruit US-100.  https://www.adafruit.com/product/4019
  * display:           AdaFruit 5x5 NeoPixel Grid BFF Addon for QT Py and Xiao.  https://www.adafruit.com/product/5646
  * LiPo charger:      lithium battery charger https://www.amazon.com/gp/product/B0836J8LR4/
  * want to switch to this charger: https://www.adafruit.com/product/5397

This adds heartbeat to a bot sculpture. Heartbeat rate is based on ultrasonic distance measurement.
Heartbeat will be displayed on 5x5 LED grid. 

Microprocessor expects to find code.py in root location

Follow steps listed here to install CircuitPython onto dev board.
 https://learn.adafruit.com/adafruit-qt-py/what-is-circuitpython

Using Mu editor since it was a simple example described in above link.
Issues to address when using PyCharm with CircuitPython are described here:
  https://learn.adafruit.com/welcome-to-circuitpython/pycharm-and-circuitpython 
 
