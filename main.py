import RPi.GPIO as GPIO
import time
from discord import Webhook
import aiohttp

async def send_message(msg: str):
    async with aiohttp.ClientSession() as session:
        webhook = Webhook.from_url('https://discord.com/api/webhooks/1195361569270407259/VdWl_9swoRMxeUnEJYuwHeyKHXWXs0nYIc4ReFvBFg6itygQxzmUty2idMwXkDlpmLlq', session=session)
        await webhook.send(msg, username='Pepito Ier')

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
isOpen = None # sensor 
oldIsOpen = None 

# Variables to wait some time before acting (ex: if the door rapidly opens and closes in repetition)
# May not be a good idea if used as a security device
TIME_BEFORE_ACTION = 5 # seconds
time_from_change = 0

def onOpen():
	send_message("Porte Ouverte")
	print("Opened!")
	GPIO.output(RED, False)
	GPIO.output(YELLOW, True)

def onClose():
	send_message("https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcR01SR_zVtraxBzNdicrhSqSBOxZShSeMlHr2W5WcEbaA&s")
	print("Closed!")
	GPIO.output(YELLOW, False)
	GPIO.output(RED, True)

while True:
	# Get the state of the sensor
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
