
class User:
	"""User Class"""

	def __init__(self, UserID, FirstName, LastName, Email, CardID, RoleID):
		self.UserID = UserID
		self.FirstName = FirstName
		self.LastName = LastName
		self.Email = Email
		self.CardID = CardID
		self.RoleID = RoleID

	def __str__(self):
		return self.FirstName
