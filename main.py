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
from machine import Pin, I2C
import ssd1306
from time import sleep

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
oled_width = 128
oled_height = 64





############################################################################
##                             write to oled                              ##
##                                                                        ##
############################################################################
def WriteToScreen():
    global counter 
    global previous_1
    global oled
    global i2c

    try:
        oled.text("Count ", 35, 30)
        oled.text("( " + str(counter)+ " )", 35, 40)
        oled.text("Last Count", 20, 0)
        oled.text("( " + str(previous_1)+" )", 30, 10)
        oled.show()
        oled.fill(0)
    except OSError:
        i2c = I2C(0, I2C.MASTER, baudrate=1000000, pins=("P9","P10"))
        oled = ssd1306.SSD1306_I2C(oled_width, oled_height, i2c)

    writeToMem()
############################################################################
###  Deepsleep initiate                                              #######
###                                                                  #######
###                                                                  #######
############################################################################
def deepSleepInit(delay, id, lastevent):                
    global timeSinceLastInput
    global timespan
    global counter

    while True:
        sleep_ms(delay)                                          #part of thread repeat delay
        timespan=(ticks_ms()-timeSinceLastInput)
        print (timespan)
        if timespan >300000:
            timeSinceLastInput=ticks_ms()
            timespan==0
            pycom.nvs_set('counter', counter)
            #print("counter reads", pycom.nvs_get('counter'))
            #print("+-=+-+-+-=+-+Go to sleep_=+-+-+-+-+-+-+-+-+")
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
        #debounce(arg)
        if arg() ==0:
            #print("got an interrupt in pin %s" % (arg.id()))
            counter+=1
            #print("counter ", counter)
            WriteToScreen()
    else:
        if arg()==1:
            timeSinceLastInput=ticks_ms()


############################################################################
### Periodic memory write                                            #######
###                                                                  #######
###                                                                  #######
############################################################################    
  
def writeToMem():
    global counter
    global previous_1
    pycom.nvs_set('counter', counter)


############################################################################
### hall sensor 2 change of state detected                           #######
###                                                                  #######
###                                                                  #######
############################################################################
def sensor_2_detect(arg):
    global timeSinceLastInput
    global counter
    if arg() == 0:
        #debounce(arg)
        if arg() == 0:
            #print("got an interrupt in pin %s" % (arg.id()))
            # counter +=1
            pass
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
    Latch = True

    while True:
        sleep_ms(delay) 
        if buttonstate() == 0:
            if timeSinceLastFunctionInput == 0 & Latch:
                timeSinceLastFunctionInput=ticks_ms() 
            elif ((ticks_ms()-timeSinceLastFunctionInput)>5000) & Latch:
                #print ("+-+-+-+-+-+-+_+_+_-=_==_initiate a reset_=_+-+-+-+-+-+-=_++_++_+")
            
                pycom.nvs_set('previous_1', counter)
                pycom.nvs_set('counter', 0)
                previous_1 = pycom.nvs_get('previous_1')
                counter = pycom.nvs_get('counter')
                Latch = False
                WriteToScreen()

            
        else:
            if buttonstate() ==1: 
                timeSinceLastFunctionInput=0
                Latch = True


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



_thread.start_new_thread(resetButton, (3000, 1, p_2))
#_thread.start_new_thread(writeToMem, (3000, 2))
_thread.start_new_thread(deepSleepInit, (10000, 3, 1))

wake_reason = (machine.wake_reason())
machine.pin_deepsleep_wakeup(pins = ('P2',), mode = machine.WAKEUP_ALL_LOW, enable_pull = True)
#print("wake  ", wake_reason)
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


#print("wake reason", wake_reason[0])
if wake_reason[0] == 1:
        counter = pycom.nvs_get('counter')+1
        pycom.nvs_set('counter', counter)

#############################################################################
#                                                                          ##
#    INIT                                                                  ##
#############################################################################
     
i2c = I2C(0, I2C.MASTER, baudrate=1000000, pins=("P9","P10"))
oled = ssd1306.SSD1306_I2C(oled_width, oled_height, i2c)  
WriteToScreen()

#############################################################################
# end #######################################################################
#############################################################################