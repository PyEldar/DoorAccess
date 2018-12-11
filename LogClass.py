import time


class Log:
    """Open Request record"""

    def __init__(self, UserID, Access):
        self.UserID = UserID
        self.Created = time.ctime()
        self.Access = Access

    def __str__(self):
        return self.UserID, self.Access
