import RPi.GPIO as GPIO

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

RED = 14
YELLOW = 15
SENSOR = 18

GPIO.setup(RED, GPIO.OUT)
GPIO.setup(YELLOW, GPIO.OUT)
GPIO.setup(SENSOR, GPIO.IN, pull_up_down = GPIO.PUD_UP)

x = 0

while True:
	oldIsOpen = isOpen
	isOpen = GPIO.input(DOOR_SENSOR_PIN)

    if (isOpen and (isOpen != oldIsOpen)):
        print "Space is unoccupied!"
        GPIO.output(RED, False)
        GPIO.output(YELLOW, True)
    elif (isOpen != oldIsOpen):
        print "Space is occupied!"
        GPIO.output(YELLOW, False)
        GPIO.output(RED, True)

    time.sleep(0.1)
