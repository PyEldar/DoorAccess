from InputPINClass import InputPIN
from PINClass import PIN
import time

class Button:
	"""Handles the button Press on specified InputPIN"""
	def __init__(self, ButtonID, ButtonPIN, LockPIN, time=5):
		self.ButtonID = ButtonID
		self.LockPIN = LockPIN		#PIN enabled by button press
		self.status = "INIT"
		self.inputPIN = InputPIN(ButtonPIN) #Instance of InputPIN class
		self.PIN = PIN(LockPIN)		#Instance of PIN class
		self.time = time		#time during that is PIN enabled by openTime()


	def listen(self):
		"""Listens for button press, when is button pressed 'openTime()' is called"""
		while True:
			if self.inputPIN.listen():
				self.openTime()
			time.sleep(0.1)


	def openTime(self):
		"""Enables PIN for specified time(self.time)"""
		self.PIN.ONTime(self.time)		


	def __str__(self):
		return self.ButtonID


		
