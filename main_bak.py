##############################################################################################################################
##                                                                                                                          ##
##                      Counter firmware                                                                                    ##
##                       Version 1.0                                                                                        ##
##                                                                                                                          ##
##############################################################################################################################

### Imports ###
import machine
from machine import Pin
import pycom 
from time import sleep_ms, ticks_ms, ticks_diff
tick_count=ticks_ms
import _thread
from network import WLAN

## Variables ##
how_Long_pressed = 0 
timeSinceLastInput=ticks_ms()
timeSinceLastFunctionInput = ticks_ms()
counter=5
previous_1 = 0
previous_2 = 0
previous_3 = 0
previous_4 = 0
timespan = 0


wlan = WLAN()
wlan.deinit()
############################################################################
##                             write to oled                              ##
##                                                                        ##
############################################################################
def WriteToScreen(delay, id):
    global counter 
    global previous_1


    while True:
        sleep_ms(delay) 

        print(" --- Print to screen  -----")    
        print("counter", counter)
        print("previous", previous_1)

############################################################################
###  Deepsleep initiate                                              #######
###                                                                  #######
###                                                                  #######
############################################################################
def DeepSleepInit(delay, id, lastevent):                
    global timeSinceLastInput
    global timespan
    global counter

    while True:
        sleep_ms(delay) 
    
        
        timespan=(ticks_ms()-timeSinceLastInput)
        if timespan >50000:
            timeSinceLastInput=ticks_ms()
            timespan==0
            pycom.nvs_set('counter', counter)
            print("counter reads", pycom.nvs_get('counter'))
            print("+-=+-+-+-=+-+Go to sleep_=+-+-+-+-+-+-+-+-+")
            machine.deepsleep()

############################################################################
### debounce routen                                                  #######
###                                                                  #######
###                                                                  #######
############################################################################
def debounce(arg):
   
    sleep_ms(150)


############################################################################
### hall sensor change of state detected                             #######
###                                                                  #######
###                                                                  #######
############################################################################
def sensor_1_detect(arg):
    global timeSinceLastInput
    global counter 
    

    if arg() == 0:
        debounce(arg)
        if arg() ==0:
            print("got an interrupt in pin %s" % (arg.id()))
            counter+=1
            print("counter ", counter)
    else:
        if arg()==1:
            timeSinceLastInput=ticks_ms()

############################################################################
### hall sensor 2 change of state detected                             #######
###                                                                  #######
###                                                                  #######
############################################################################
def sensor_2_detect(arg):
    global timeSinceLastInput
    global counter
    if arg() == 0:
        debounce(arg)
        if arg() == 0:
            print("got an interrupt in pin %s" % (arg.id()))
            # counter +=1
    else:
        if arg() == 1:
            timeSinceLastInput = ticks_ms()

###########################################################################
###        This call back handles the reset button                      ###  
###       pressed for 5 seconds to reset the counter                    ###                                                                                    #######
###                                                                     ###
###########################################################################


def resetButton(delay, id, buttonstate):
    global how_Long_pressed
    global timeSinceLastFunctionInput
    global counter
    global previous_1

    while True:
        sleep_ms(delay) 
        if buttonstate() == 0:
            if timeSinceLastFunctionInput == 0:
                timeSinceLastFunctionInput=ticks_ms() 
            elif ((ticks_ms()-timeSinceLastFunctionInput)>5000):
                print ("+-+-+-+-+-+-+_+_+_-=_==_initiate a reset_=_+-+-+-+-+-+-=_++_++_+")
            
                pycom.nvs_set('previous_1', counter)
                pycom.nvs_set('counter', 0)
                previous_1 = pycom.nvs_get('previous_1')
                counter = pycom.nvs_get('counter')
                sleep_ms(1000)

            
        else:
            if buttonstate() ==1: 
                timeSinceLastFunctionInput=0

       
  

###############################################################################           
##                                                                           ##
##                     Call backs                                            ##
##                                                                           ##
###############################################################################

p_1 = Pin(('P2'), mode=Pin.IN, pull=Pin.PULL_UP)             #hall sensor 1
p_1.callback(Pin.IRQ_FALLING | Pin.IRQ_RISING, sensor_1_detect)

p_3 = Pin(('P3'), mode=Pin.IN, pull=Pin.PULL_UP)             #hall sensor 1
p_3.callback(Pin.IRQ_FALLING | Pin.IRQ_RISING, sensor_2_detect)

p_2 = Pin('P4', mode=Pin.IN, pull=Pin.PULL_UP)  # reset/function button
# p_2.callback(Pin.IRQ_FALLING | Pin.IRQ_RISING, function_1_detect)



_thread.start_new_thread(resetButton, (1000, 1, p_2))
_thread.start_new_thread(WriteToScreen, (3000, 2))
_thread.start_new_thread(DeepSleepInit, (5000, 3, 1))

wake_reason = (machine.wake_reason())
machine.pin_deepsleep_wakeup(pins = ('P2',), mode = machine.WAKEUP_ALL_LOW, enable_pull = True)
print("wake  ",wake_reason)
try:
    counter = pycom.nvs_get('counter')
    pycom.nvs_set('counter', counter)
except ValueError:
    pycom.nvs_set('counter', counter)

try:
    previous_1 = pycom.nvs_get('previous_1')
    pycom.nvs_set('previous_1', previous_1)
except ValueError:
    pycom.nvs_set('previous_1', previous_1)

try:
    previous_2 = pycom.nvs_get('previous_2')
    pycom.nvs_set('previous_2', previous_2)
except ValueError:
    pycom.nvs_set('previous_2', previous_2)

try:
    previous_3 = pycom.nvs_get('previous_3')
    pycom.nvs_set('previous_3', previous_3)
except ValueError:
    pycom.nvs_set('previous_3', previous_3)

try:
    previous_4 = pycom.nvs_get('previous_4')
    pycom.nvs_set('previous_4', previous_4)
except ValueError:
    pycom.nvs_set('previous_4', previous_4)

print("wake reason", wake_reason[0])
if wake_reason[0] == 1:
        counter = pycom.nvs_get('counter')+1
        pycom.nvs_set('counter', counter)