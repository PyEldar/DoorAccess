#!/usr/bin/env python3

import time
import sys
from Core import Core

if __name__ == "__main__":
        try:
                Handler = Core(sys.argv[1])  # Creates Handler object 'dbname' is passed as command-line argument
                if Handler.status == "Initialized":
                        Handler.startHandle()  # Starts handeling of all locks and buttons
                        print("Started " + time.ctime())
                        while True:    # Updates every Xseconds - passed as command-line argument
                                time.sleep(float(sys.argv[2]))
                                Handler.update()   # after the time calls 'update' method
                                print("Updated " + time.ctime())
                elif Handler.status == "Error":
                        sys.exit()
        except IndexError:  # Occurs when there are not passed all command-line arguments
                print("ERROR\nNo database or update time specified\nusage: sudo python3 Main.py <dbname> <seconds>")
                sys.exit()

        except Exception as err:  # Uknown error
                print(err)
                print("EXCEPTION")
                Handler.DB.close()
                time.sleep(2)
                sys.exit()
