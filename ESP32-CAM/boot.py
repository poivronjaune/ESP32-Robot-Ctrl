# This file is executed on every boot (including wake-boot from deepsleep)
#import esp
#esp.osdebug(None)
#import webrepl
#webrepl.start()

# TOD: Implement a delay for CTRL-C to prevent automatic start when developping
#execfile('go.py')