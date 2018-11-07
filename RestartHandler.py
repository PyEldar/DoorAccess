from RestartClass import Restart
from DbHelperClass import DB


rest = Restart(1, 10)#Initialized with specified ID, PIN
rest.restartOnPush()#Restarts when button is pressed
