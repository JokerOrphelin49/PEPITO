import RPi.GPIO as GPIO
import time
from discord import Webhook
import aiohttp
import asyncio
from time import sleep

# time step
STEP = 0.1

# Pin numbers
RED = 14
YELLOW = 15
SENSOR = 18

# Set the modes of each pin
# RED and YELLOW are LEDs for testing
GPIO.setup(RED, GPIO.OUT)
GPIO.setup(YELLOW, GPIO.OUT)
GPIO.setup(SENSOR, GPIO.IN, pull_up_down = GPIO.PUD_UP)

# Variables to check if the state changes
isOpen = None # Current door state
oldIsOpen = None # Last registered door state (for which an action was taken)

# Variables to wait some time before acting (ex: if the door rapidly opens and closes in repetition)
TIME_BEFORE_ACTION = 5 # delay in seconds
time_from_change = 0

# Messages
OPENED_MESSAGE = "Porte Ouverte"
CLOSED_MESSAGE = "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcR01SR_zVtraxBzNdicrhSqSBOxZShSeMlHr2W5WcEbaA&s"

def getOpenedMessage():
	return OPENED_MESSAGE

def getClosedMessage():
	return CLOSED_MESSAGE

# action à réaliser lors de l'ouverture
def onOpen():
	send_message(getOpenedMessage())
	print("Opened!")
	GPIO.output(RED, False)
	GPIO.output(YELLOW, True)

# action à réaliser lors de la fermeture
def onClose():
	send_message(getClosedMessage())
	print("Closed!")
	GPIO.output(YELLOW, False)
	GPIO.output(RED, True)

# Envoyer un message sur discord
def send_message(msg: str):
	async def inner():
	    async with aiohttp.ClientSession() as session:
	        webhook = Webhook.from_url('https://discordapp.com/api/webhooks/1239175726641451008/U8uIUUcKhWd2FnEVxfJoPlQ-Q2YTz825B0GSDgtvjUirOmG-eXW8XH8CUJaAm8WG9UFk', session=session)
	        await webhook.send(msg, username='Pepito Ier')
	asyncio.run(inner())

# boucle principale
while True:
	# Get the state of the sensor
	isOpen = GPIO.input(SENSOR)

    # la porte vient de changer d'été
	if (isOpen != oldIsOpen):
        # on vérifie si le délai est dépassé
		if time_from_change >= TIME_BEFORE_ACTION:
			time_from_change = 0
			if (isOpen):
				onOpen()
			else:
				onClose()
			oldIsOpen = isOpen
		else:
			time_from_change += STEP
	else:
		time_from_change = 0

	time.sleep(STEP)
