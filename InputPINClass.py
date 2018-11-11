import RPi.GPIO as GPIO
import time


class InputPIN:

	"""Input on specified PIN"""

	def __init__(self, PIN):
		self.PIN = PIN
		self.STATUS = "INIT"
		GPIO.setmode(GPIO.BOARD)
		GPIO.setup(PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

	def __str__(self):
		return self.PIN

	def listen(self):
		"""Listen until signal comes then returns True"""
		while True:
			GPIO.setmode(GPIO.BOARD)
			input_state = GPIO.input(self.PIN)
			if input_state == False:
				return True
			time.sleep(0.2)

	def clean(self):
		"""Cleans the GPIO"""
		GPIO.cleanup()


