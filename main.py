import RPi.GPIO as GPIO

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(40, GPIO.IN)
GPIO.setup(12, GPIO.OUT)

x = 0

while True:
	if GPIO.input(40) == GPIO.HIGH:
		print(f"abababa{x}")
		x += 1
