#!/usr/bin/env python3

import time
import threading
import sys

from LockClass import Lock
from PermissionClass import Permission
from LogClass import Log
from UserClass import User
from DbHelperClass import DB
from InputPINClass import InputPIN
from ButtonClass import Button
from RestartClass import Restart

class Core:
	"""Handles Locks, Communicates with DB"""

	def __init__(self, dbname):
		"""Connects to database and loads Users, Locks, Permissions, Buttons"""
		self.dbname = dbname
		self.DB = DB(dbname)
		try:
			self.DB.connect()
		except Exception as err:
			print(err)
			print("Could not connect to Database " + self.dbname)
			self.status = "Error"
			sys.exit()
		self.Locks = []
		self.Users = []
		self.Permissions = []
		self.Buttons = []
		#self.RestartButtons = []
		self.update()
		self.threads = []
		self.errors = 0
		self.status = "Initialized"



	def update(self):
		"""Updates Objects from Database"""
		try:
			self.Users = self.LoadUsers()
			self.Locks = self.LoadLocks()
			self.Permissions = self.LoadPermissions()
			self.Buttons = self.LoadButtons()
			#self.RestartButtons = self.LoadRestartButtons()
		except:
			print("Could not connect to Database " + self.dbname)

	def LoadRestartButtons(self):
		"""Returns list of 'Restart' objects from DB"""
		RESTARTBUTTONS = self.DB.retrieveTable("RESTARTBUTTONS")
		RestartButtons = []
		for restartButton in RESTARTBUTTONS:
			RestartButtons.append(Restart(restartButton[0], restartButton[1]))
		return RestartButtons

	
	def LoadButtons(self):
		"""Returns list of 'Button' objects from DB"""
		BUTTONS = self.DB.retrieveTable("BUTTONS")
		Buttons = []
		for button in BUTTONS:
			Buttons.append(Button(button[0],button[1],button[2]))
		return Buttons


	def LoadUsers(self):
		"""Returns list of 'User' objects from DB"""
		USERS = self.DB.retrieveTable("USERS")
		Users = []
		for user in USERS:
			Users.append(User(user[0], user[1], user[2], user[3], user[4], user[5]))
		return Users


	def LoadLocks(self):
		"""Returns list of 'Lock' objects from DB"""
		LOCKS = self.DB.retrieveTable("LOCKS")
		Locks = []
		for lock in LOCKS:
			Locks.append(Lock(lock[0], lock[1], lock[2], lock[3]))
		return Locks


	def LoadPermissions(self):
		"""Returns list of 'Permission' objects from DB"""
		PERMS = self.DB.retrieveTable("PERMISSIONS")
		Perms = []
		for perm in PERMS:
			Perms.append(Permission(perm[0], perm[1]))
		return Perms


	def CreateLog(self, UserID, Access, LockID):
		"""Creates record in DB"""
		self.DB.createLog(UserID, time.ctime(), Access, LockID)


	def UserHasPermission(self, UserID, LockID):
		"""Checks if specified User has permissions to Specified Lock"""
		"""Returns True\False"""
		for Perm in self.Permissions:
			if UserID == Perm.UserID:
				if LockID == Perm.LockID:
					return True
		return False
	
	
	def getUserByCard(self,CardID):
		"""Return User object based on CardID"""
		for user in self.Users:
			if CardID == user.CardID:
				return user
		return None


	def startHandle(self):
		"""Starts handeling Locks and Buttons from lists one by one"""
		if len(self.Locks) > 0: #If there are any Locks starts otherwise EXITS

			for lock in self.Locks:
				if lock.status == "OK": #If Lock is 'OK' starts handeling otherwise continues to other Locks
					print("Starting " + lock.Name)
					#Starts 'Handle' in Thread
					thread = threading.Thread(target=self.Handle, args=(lock, ))
					thread.start()
					print("Lock " + lock.Name + " started")
				else:
					print("Lock could not be initialized")
			
		else:
			print("No Locks")
			sys.exit()

		if len(self.Buttons) > 0:
			for button in self.Buttons:
				print("Button " + str(button.ButtonID))
				#Starts 'HandleButton' in Thread
				thread = threading.Thread(target=self.HandleButton, args=(button, ))
				thread.start()
				print("Button " + str(button.ButtonID) + " started")
		"""
		if len(self.RestartButtons) > 0:
			for restbutt in self.RestartButtons:
				print("Restart Button " + str(restbutt.ID))
				#Starts 'HandleRestart' in Thread
				thread = threading.Thread(target=self.HandleRestart, args=(restbutt,))
				thread.start()
				print("Restart Button " + str(restbutt.ID) + " started")
		"""

		
	def HandleRestart(self, RestartButton):
		"""Restarts when button is pressed"""
		RestartButton.restartOnPush()
			

	def startHandleSingleLock(self, Lock1):
		"""Start handeling single Lock passed as an argument // used for debug only"""
		if Lock1.status == "OK":
			print("Starting " + Lock1.Name)
			self.Handle(Lock1)
			print("Lock " + Lock1.Name + " started")
			input(" gg ")
		else:
			
			input("Lock could not be initialized")




	def Handle(self, Lock1):
		while True:
			result = Lock1.listen() #Returns (CardID, LockID)

			if Lock1.isConnected():  #if Lock is connected continues otherwise tries to reconnect
				ActiveUser = self.getUserByCard(result[0]) #Finds user by CardID
				if ActiveUser is not None:	#If user is in DB continues
					if self.UserHasPermission(ActiveUser.UserID, result[1]):
						Lock1.openTime(6)
						self.CreateLog(ActiveUser.UserID, 1, Lock1.LockID)
						print("Access allowed, User: " + ActiveUser.LastName)
					else:
						self.CreateLog(ActiveUser.UserID, 0, Lock1.LockID)
						print("Access denied, User: " + ActiveUser.LastName)
				else:
					print("Access denied, Unknown User, CardID: " + result[0])
			else:
				Lock1.reconnect()


	def HandleButton(self, button):
		"""Starts Listening"""
		while True:
			button.listen()



