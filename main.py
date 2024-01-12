import RPi.GPIO as GPIO
import time
from discord import Webhook
import aiohttp
import asyncio
from time import sleep
#Buzzer
BUZZER = 4

def send_message(msg: str):
	async def inner():
	    async with aiohttp.ClientSession() as session:
	        webhook = Webhook.from_url('https://discord.com/api/webhooks/1195361569270407259/VdWl_9swoRMxeUnEJYuwHeyKHXWXs0nYIc4ReFvBFg6itygQxzmUty2idMwXkDlpmLlq', session=session)
	        await webhook.send(msg, username='Pepito Ier')
	asyncio.run(inner())

 


GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(BUZZER, GPIO.OUT)
pin7 = GPIO.PWM(BUZZER, 100)
pin7.start(50)

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
			GPIO.output(BUZZER, GPIO.HIGH)
			pin7.ChangeFrequency(16.35) # C0
			sleep(1)
			pin7.ChangeFrequency(261.63) # C4
			sleep(1)
			pin7.ChangeFrequency(293.66) # D4
			sleep(1)
			pin7.ChangeFrequency(329.63) # E4
			sleep(1)
			pin7.ChangeFrequency(349.23) # F4
			sleep(1)
			pin7.ChangeFrequency(392.00) # G4
			sleep(1)
			pin7.ChangeFrequency(440.00) # A4
			sleep(1)
			pin7.ChangeFrequency(493.88) # B4
			sleep(1)
			pin7.ChangeFrequency(523.25) # A5
			sleep(1.5)
			pin7.ChangeFrequency(16.35) # C0
			sleep(1)
			GPIO.output(BUZZER, GPIO.LOW)
			print(GPIO.LOW)
		else:
			time_from_change += 0.1

	time.sleep(0.1)
