#!/usr/bin/python

import RPi.GPIO as GPIO
import time

# Signal: 'INT','PA','SET','ABORT'
switches = [22, 11, 13, 15]
states = [0, 0, 0, 0]
oldMsg = ''

def _setup():
  GPIO.setwarnings(False) 
  GPIO.setmode(GPIO.BOARD)
  for switch in switches:
    GPIO.setup(switch, GPIO.IN, GPIO.PUD_UP)

if __name__ == "__main__":
  _setup()
  while 1:
    for i in range(0, len(switches)):
      states[i] = GPIO.input(switches[i])
    if states[0] == 0:
      newMsg = 'ALARM!'
    elif states[1] == 0:
      newMsg = 'PANIC!'
    elif states[2] == 0:
      newMsg = 'Alarm set'
    elif states[3] == 0:
      newMsg = 'Awaiting restore'
    else:
      newMsg = 'Alarm unset'
    if newMsg <> oldMsg:
      # Do something here eg email/sms/growl...!
      print newMsg
    oldMsg = newMsg
    time.sleep(0.1)
