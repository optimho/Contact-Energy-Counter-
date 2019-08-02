from machine import UART
#from network import WLAN
import machine
import os
from network import WLAN

uart = UART(0, baudrate=115200)
os.dupterm(uart)
wlan = WLAN()
wlan.deinit()
machine.main('main.py')# boot.py -- run on boot-up
