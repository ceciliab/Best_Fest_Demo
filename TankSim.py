#!/usr/bin/python

import RPi.GPIO as GPIO
import time
import requests
import json
# import curses

from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

GPIO.setwarnings(False)

url = 'https://jmr5sxvm.pp.vuforia.io:8443/Thingworx'
headers = { 'Content-Type': 'application/json', 'appKey': '562cdff5-d060-4f14-8480-27ba3b008e20' }
thing = 'TankThing'

def bin2dec(string_num):
    return str(int(string_num, 2))

# Initialize curses module for key presses

# stdscr = curses.initscr() # Get the curses screen window
# curses.noecho()           # Turn off automatic echoing of keys
# curses.cbreak()           # respond to keys immediately, does not require the Enter key to be pressed
# stdscr.keypad(True)       # Give special keys special values

# Initialize variables

Temp1 = 70
Temp2 = 69
Temp3 = 68
AC1 = 0
AC2 = 0
AC3 = 1
time_min = 300.00  # Enter the time the demo should last (in minutes) 
time_left = time_min
interval = 2    # Enter time between data changes (seconds)
duration = time_min*60.00

FillLevel1 = 57
FillLevel2 = 84
FillLevel3 = 10
pump1 = 1
pump2 = 1
pump3 = 1

var = 0.00
while (var < duration):
	
	# Check for button press to exit while loop
	# key = stdscr.getkey()


	# if key == 'q':
	# 	print 'Exiting Script'
	#	break                     	


# Temp1	
	if (Temp1 < 72 ):
		if (AC1 == 0):
			Temp1 += 0.1  # raise the temp to 72 if AC is off   
	else:
		AC1 = 1              # Turn AC on if at 72

	if (Temp1 > 65):
		if (AC1 == 1):
			Temp1 = Temp1 -0.1   # lower the temp to 65 if AC is on
	else:
		Temp1 += 0.1       
		AC1 = 0             # Below 65, raise the temperature and turn AC off

# Temp2
	if (Temp2 < 72 ):
		if (AC2 == 0):
			Temp2 += 0.1  # raise the temp to 72 if AC is off   
	else:
		AC2 = 1              # Turn AC on if at 72

	if (Temp2 > 65):
		if (AC2 == 1):
			Temp2 = Temp2 -0.1   # lower the temp to 65 if AC is on
	else:
		Temp2 += 0.1       
		AC2 = 0             # Below 65, raise the temperature and turn AC off

# Temp3
	if (Temp3 < 72 ):
		if (AC3 == 0):
			Temp3 += 0.5  # raise the temp to 72 if AC is off   
	else:
		AC3 = 1              # Turn AC on if at 72

	if (Temp3 > 65):
		if (AC3 == 1):
			Temp3 = Temp3 -0.5   # lower the temp to 65 if AC is on
	else:
		Temp3 += 0.5       
		AC3 = 0             # Below 65, raise the temperature and turn AC off

# Level1
	if (FillLevel1 < 100 ):
		if (pump1 == 1):
			FillLevel1 += 1   # raise the level to 100 if pump is on   
	else:
		pump1 = 0              # Turn pump on off at 100

	if (FillLevel1 > 0):
		if (pump1 == 0):
			FillLevel1 -= 1  # lower the level to 0 if pump is off   
	else:
		FillLevel1 += 1
		pump1 = 1

# Level2
	if (FillLevel2 < 100 ):
		if (pump2 == 1):
			FillLevel2 += 1  # raise the level to 100 if pump is on   
	else:
		pump2 = 0              # Turn pump on off at 100
		
	if (FillLevel2 > 0):
		if (pump2 == 0):
			FillLevel2 -= 1  # lower the level to 0 if pump is off   
	else:
		FillLevel2 += 1
		pump2 = 1

# Level3
	if (FillLevel3 < 100 ):
		if (pump3 == 1):
			FillLevel3 += 1  # raise the level to 100 if pump is on   
	else:
		pump3 = 0              # Turn pump on off at 100

	if (FillLevel3 > 0):
		if (pump3 == 0):
			FillLevel3 -= 1  # lower the level to 0 if pump is off   
	else:
		FillLevel3 += 1
		pump3 = 1

	
	# Send info to ThingWorx
	payload = { 'Temp1' : Temp1, 'Temp2' : Temp2, 'Temp3' : Temp3, 'FillLevel1' : FillLevel1, 'FillLevel2' : FillLevel2, 'FillLevel3' : FillLevel3}
	response = requests.put(url + '/Things/' + thing + '/Properties/*', headers=headers, json=payload, verify=False)
	
	var = var + interval
	
	time_left = time_min - (var/60.00)

	print 'Temp: ', Temp2
	print 'Fill: ', FillLevel1
	print 'Time Remaining: ', time_left

	time.sleep(interval) 

# Terminate curses application

# curses.nocbreak()
# stdscr.keypad(False)
# curses.echo()
# curses.endwin()


print 'End'


