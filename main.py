import RPi.GPIO as GPIO
import time

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

# Pin numbers
RED = 14
YELLOW = 15
SENSOR = 18

# Set the modes of each pin
# RED and YELLOW are LEDs for testing
GPIO.setup(RED, GPIO.OUT)
GPIO.setup(YELLOW, GPIO.OUT)
GPIO.setup(SENSOR, GPIO.IN, pull_up_down = GPIO.PUD_UP)

x = 0

# Variables to check if the state changes
isOpen = None
oldIsOpen = None

# Variables to wait some time before acting (ex: if the door rapidly opens and closes in repetition)
# May not be a good idea if used as a security device
TIME_BEFORE_ACTION = 5 # seconds
time_from_change = 0

while True:
	# Get the state of the sensor
	isOpen = GPIO.input(SENSOR)

	# the door opened
	if (isOpen and (isOpen != oldIsOpen)):
		# Wait some time
		# Need to be fixed, the timer should reset when the state of the sensor changes
		if time_from_change >= TIME_BEFORE_ACTION:
			print("Opened!")
			GPIO.output(RED, False)
			GPIO.output(YELLOW, True)
			time_from_change = 0
			oldIsOpen = isOpen
		else:
			# should be improved
			time_from_change += 0.1
	elif (isOpen != oldIsOpen): # the door closed
		if time_from_change >= TIME_BEFORE_ACTION:
			print("Closed!")
			GPIO.output(YELLOW, False)
			GPIO.output(RED, True)
			time_from_change = 0
			oldIsOpen = isOpen
		else:
			time_from_change += 0.1

	time.sleep(0.1)
