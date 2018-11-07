import RPi.GPIO as GPIO
import threading
import time

class PIN:
	""" Class handeling PIN output """

	def __init__(self, PIN):
		self.PIN = PIN
		self.STATUS = "OFF"
		GPIO.setmode(GPIO.BOARD)			
	

	def __str__(self):
		return self.PIN
	

	def ON(self):
		"""ON until 'OFF()' or 'cleanup()' is caled"""
		GPIO.setmode(GPIO.BOARD)
		GPIO.setup(self.PIN, GPIO.OUT)
		GPIO.output(self.PIN,True)
		self.STATUS = "ON"


	def OFF(self):
		GPIO.setmode(GPIO.BOARD)		
		GPIO.setup(self.PIN, GPIO.OUT)
		GPIO.output(self.PIN,False)
		self.STATUS = "OFF"


	def ONTime(self, SleepTime=1):
		"""ON for specified 'SleepTime'"""
		thread = threading.Thread(target=self.ThreadONTime, args=(SleepTime,))
		thread.start()
	

	def ThreadONTime(self, SleepTime):
		"""Method called in thread by 'ONTime()'"""
		self.ON()
		time.sleep(SleepTime)
		self.OFF()


	def clean(self):
		"""Cleans the GPIO"""
		GPIO.cleanup()

