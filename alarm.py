#!/usr/bin/python

import RPi.GPIO as GPIO
import time
from sitewinder.utils import sms, prowl

# Signal: 'INT','PA','SET','ABORT'
# GPIO: 3, 5, 7, 11

switches = [3, 5, 7, 11]
states = [True, True, True, True]

def _setup():
  GPIO.setwarnings(False) 
  GPIO.setmode(GPIO.BOARD)
  for switch in switches:
    GPIO.setup(switch, GPIO.IN, GPIO.PUD_UP)

if __name__ == "__main__":
  _setup()
  while 1:
    for i in range(0, len(switches)):
      valSwitch = GPIO.input(switches[i])
      valState = states[i]
      if (valSwitch != valState):
        nowTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) 
        if i==0 and valSwitch==False:
          msg='ALARM!'
        elif i==1 and valSwitch==False:
          msg='PANIC!'
        elif i==2 and valSwitch==True:
          msg='Alarm unset'
        elif i==2 and valSwitch==False:
          msg='Alarm set'
        elif i==3 and valSwitch==True:
          msg='System restored'
        elif i==3 and valSwitch==False:
          msg='Awaiting restore'
        else:
          msg=''
        if msg:
          # Always log the new state
          with open('/home/pi/inetpub/alarm.txt', 'a') as myfile:
            myfile.write(nowTime  + ': ' + msg + '\n')
          # Always prowl the new state
          prowl(msg, msg)
          # SMS if Alarm or Duress
          if msg in ("ALARM!", "PANIC!"):
            sms(msg)
          # Remember the new states
          states[i] = valSwitch
    time.sleep(0.1)
