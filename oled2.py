# Complete project details at https://RandomNerdTutorials.com

from machine import Pin, I2C
import ssd1306
from time import sleep

# ESP32 Pin assignment 
i2c = I2C(0, I2C.MASTER, baudrate=10000, pins=("P9","P10"))


# ESP8266 Pin assignment
#i2c = I2C(-1, scl=Pin(5), sda=Pin(4))

oled_width = 128
oled_height = 64
num=0

oled = ssd1306.SSD1306_I2C(oled_width, oled_height, i2c)
while True:
    num=num+1
  
    oled.text(str(num), 50, 40)
    oled.show()
    oled.fill(0)
    