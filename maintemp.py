import machine
from network import WLAN
import machine
import pycom
import _thread
import time

pycom.heartbeat(False)

def th_func_gotoSleep(delay, ticks):
    while True:
        time.sleep(delay)
        ticks=ticks+1
        print ('ticks => %d ', ticks)
        if ticks==1000:
            print('Now go to sleep')
            machine.deepsleep(20000)
        
_thread.start_new_thread(th_func_gotoSleep, (1, 0))
wlan = WLAN()
wlan.deinit() #make sure the wifi is off
pin_int = Pin

print("wake")

wake_reason = (machine.wake_reason())
machine.pin_deepsleep_wakeup(pins = ('P2',), mode = machine.WAKEUP_ALL_LOW, enable_pull = True)
sleeps = pycom.nvs_get('sleeps') + 1
interuptions = pycom.nvs_get('interuptions') + 1
pycom.nvs_set('sleeps', sleeps)
if wake_reason[0] == 1:
     pycom.nvs_set('interuptions', interuptions)

print("sleep: %d" % (sleeps))
print("interuptions: %d" % (interuptions))
print("This is the wake integer %d" % wake_reason[0])
