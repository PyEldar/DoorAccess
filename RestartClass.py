import time
import os

from InputPINClass import InputPIN

class Restart:
	"""Handles restart button"""
	def __init__(self, ID, inputPIN):
		self.inputPIN = InputPIN(inputPIN)
		self.ID = ID

	def restartOnPush(self):
		"""When button is pressed calls 'reboot()'"""
		while True:
			if self.inputPIN.listen():
				self.reboot()
			time.sleep(0.2)

	def reboot(self):
		"""Restarts RPi"""
		os.system("sudo reboot")
