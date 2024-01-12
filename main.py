import RPi.GPIO as GPIO
import time

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

RED = 14
YELLOW = 15
SENSOR = 18

GPIO.setup(RED, GPIO.OUT)
GPIO.setup(YELLOW, GPIO.OUT)
GPIO.setup(SENSOR, GPIO.IN, pull_up_down = GPIO.PUD_UP)

x = 0

isOpen = None # sensor 
oldIsOpen = None 

TIME_BEFORE_ACTION = 5 # seconds
time_from_change = 0

def onOpen():
	print("Opened!")
	GPIO.output(RED, False)
	GPIO.output(YELLOW, True)

def onClose():
	print("Closed!")
	GPIO.output(YELLOW, False)
	GPIO.output(RED, True)

while True:
	isOpen = GPIO.input(SENSOR)

	if (isOpen != oldIsOpen):
		if time_from_change >= TIME_BEFORE_ACTION:
			time_from_change = 0
			oldIsOpen = isOpen
			if (isOpen):
				onOpen()
			else:
				onClose()
		else:
			time_from_change += 0.1
	


	""" if (isOpen and (isOpen != oldIsOpen)):
		if time_from_change >= TIME_BEFORE_ACTION:
			onOpen()
			time_from_change = 0
			oldIsOpen = isOpen
		else: # à améliorer
			time_from_change += 0.1
	elif (isOpen != oldIsOpen):
		if time_from_change >= TIME_BEFORE_ACTION:
			onClose()
			time_from_change = 0
			oldIsOpen = isOpen
		else:
			time_from_change += 0.1 """

	time.sleep(0.1)
