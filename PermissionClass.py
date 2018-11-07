
class Permission:
	"""Specifies permissions for Users"""

	def __init__(self, UserID, LockID):
		self.UserID = UserID
		self.LockID = LockID

	def __str__(self):
		return self.UserID, self.LockID
