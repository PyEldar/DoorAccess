import time
import serial
import PINClass
import os.path


class Lock:

	"""Lock and Card reader"""

	def __init__(self, LockID, Name, LockAddr, ReaderAddr):
		try:
			self.ser = serial.Serial(ReaderAddr)
			self.ReaderAddr = ReaderAddr
			self.alldata = b""
			self.PIN = PINClass.PIN(LockAddr)
			self.LockAddr = LockAddr
			self.Name = Name
			self.LockID = LockID
			self.status = "OK"
		except Exception as err:
			try:
				del self.ser
			except:
				print("ERR 1")
			self.status = "Error"
			print(err)

	def listen(self):

		"""
		Listens on CardReader and returns CardID, LockID when card is enclosed,
		returns 'ERROR' when there is an Error
		"""

		while True:
			try:
				if self.isConnected():
					data = b""
					dataGroup = b""
					data = self.ser.read(12)
					self.alldata += data
					self.ser.reset_input_buffer()

					if data != b"":
						return data.decode(), self.LockID
				else:
					print("NOT CONN")
					try:
						self.ser.close()
					except:
						print("ERR 2")
					return "ERROR"
				time.sleep(0.05)
			except:
				try:
					self.ser.close()
				except:
					print("ERR 3")
				return "ERROR"

	def openTime(self, time):
		"""Opens PIN(LockAddr) for specified Time"""
		print("Open")
		self.PIN.ONTime(time)

	def open(self):
		"""Opens PIN(LockAddr) until close() or cleanup() is called"""
		print("Open")
		self.PIN.ON()

	def close(self):
		print("Close")
		self.PIN.OFF()

	def status(self):
		"""return 'OK' or 'ERROR'"""
		return self.PIN.STATUS


	def __str__(self):
		return self.Name

	def reconnect(self):
		"""Tries to Reconnect to Reader on same addres when disconnect"""
		self.ser.close()
		print("RECONNECT")
		while not self.isConnected():
			time.sleep(1)
			print("NOT CONNECTED")
		print("CONNECTED AGAIN")
		self.ser = serial.Serial(self.ReaderAddr)
		self.alldata = b""
		self.status = "OK"

	def isConnected(self):
		"""Returns True if reader is connected on 'ReaderAddr'"""
		return os.path.exists(self.ReaderAddr)

	def __del__(self):
		del self.ser
