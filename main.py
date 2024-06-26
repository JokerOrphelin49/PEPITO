import RPi.GPIO as GPIO
import time
import discord
from discord import Webhook
import aiohttp
import asyncio
from time import sleep
import random
from datetime import datetime, timedelta

WEBHOOK_URL='https://discordapp.com/api/webhooks/1246380452315398144/SAPJAb2EHz-37K58-zcW_8gCJCgvORAEU8n7lmS50NeeiX1upHjR-sM3AMOEFLLsma92'

# time step
STEP = 0.1

# Sleep time
SLEEP = 23 # heure, attention si on le déplace après minuit le code ne marchera plus
WAKE = 6

# Jours de sommeils
SLEEP_DAYS=[5, 6] # 5 = Samedi, 6 = Dimanche

# Pin numbers
#RED = 14
#YELLOW = 15
SENSOR = 18

# Set the modes of each pin
# RED and YELLOW are LEDs for testing
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
#GPIO.setup(RED, GPIO.OUT)
#GPIO.setup(YELLOW, GPIO.OUT)
GPIO.setup(SENSOR, GPIO.IN, pull_up_down = GPIO.PUD_UP)

# Variables to wait some time before acting (ex: if the door rapidly opens and closes in repetition)
TIME_BEFORE_ACTION = 1 # delay in seconds
time_from_change = 0

# Messages
START_MESSAGE = "Pepito.png"
class MessagePair:
	def __init__(self, opened, closed):
		self.opened = opened
		self.closed = closed
MESSAGES = []
state_messages_file = open("/home/pepito/PEPITO/state_messages.txt", "r")
for line in state_messages_file.readlines():
	opened, closed = line.split("|")
	message = MessagePair(opened, closed)
	MESSAGES.append(message)

message = None
def getOpenedMessage():
	global message, MESSAGES
	message = random.choice(MESSAGES)
	return message.opened
def getClosedMessage():
	global message, MESSAGES
	if message == None:
		message = random.choice(MESSAGES)
	return message.closed

# action à réaliser lors du démarrage
def onStart():
	send_image(START_MESSAGE)
	print("Started!")

# action à réaliser lors de l'ouverture
def onOpen():
	send_image(getOpenedMessage())
	print("Opened!")
	#GPIO.output(RED, False)
	#GPIO.output(YELLOW, True)

# action à réaliser lors de la fermeture
def onClose():
	send_image(getClosedMessage())
	print("Closed!")
	#GPIO.output(YELLOW, False)
	#GPIO.output(RED, True)

# Envoyer un message sur discord
# Plus utilisé pour l'instant
def send_message(msg: str):
	async def inner():
		async with aiohttp.ClientSession() as session:
			webhook = Webhook.from_url(WEBHOOK_URL, session=session)
			await webhook.send(msg, username='Pepito')
	try:
		asyncio.run(inner())
	except Exception as e:
		print("an error occured: ")
		print(e)

# Envoyer une image sur discord
# msg: le nom du fichier image à envoyer depuis le dossier Images
def send_image(msg: str):
	async def inner():
		async with aiohttp.ClientSession() as session:
			webhook = Webhook.from_url(WEBHOOK_URL, session=session)

			file = discord.File("/home/pepito/PEPITO/Images/"+msg.strip())
			#embed = discord.Embed()
			#embed.set_image(url="attachment://ferme_clement.png")

			await webhook.send(file=file, username='Pepito')
	try:
		asyncio.run(inner())
	except Exception as e:
		print("an error occured: ")
		print(e)
	

# Variables to check if the state changes
isOpen = None # Current door state
oldIsOpen = GPIO.input(SENSOR) # Last registered door state (for which an action was taken)

onStart()
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
	
	# sleep during the night
	now = datetime.now()
	today_sleep_time = datetime(year = now.year, month = now.month, day = now.day) + timedelta(hours = SLEEP)
	tommorow_wake_time = datetime(year = now.year, month = now.month, day = now.day) + timedelta(days = 1, hours = WAKE)
	while now >= today_sleep_time and now < tommorow_wake_time:
		now = datetime.now()
		sleep(10*60) # 10 minutes
	while now.weekday() in SLEEP_DAYS:
		now = datetime.now()
		sleep(60*60) # 1 heure
		
