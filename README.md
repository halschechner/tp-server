To run, "python main.py"


Configuration:

There's no configuration file yet.  
  * main.py: Line 14 contains the IP and port where we can find the timekeeper
  * main.py: Line 17 tells us which port to run the REST api server on
  * openHABInterface.py: line 12 tells us where to find openHab's rest API
  * main.py: comment out lines 4 and 11 to avoid OpenHAB stuff from loading

Device ID (timekeeper side) to Device Name (OpenHAB side) can be found in 
devices.py.  

Basic REST api:

Turn a device on:
http://localhost:8000/output/on/05A

Turn a device off:
http://localhost:8000/output/off/05A

Get the status of a device:
http://localhost:8000/output/status/05A

Notes:

* To keep the two systems in sync, there is a timer set up to send a PUSH STATUS
to the timekeeper periodically, and update the internal status table and push
the status into OpenHAB.  OpenHAB should not see these as events.

* I have not upgraded from OpenHAB v1, so I'm a few minor releases behind. 
It should be relatively easy to upgrade, and I'll report back with any 
problems once I have.

* Every 5 seconds, a list of "on" devices will be displayed to stdout

* I have no dimmers, so there is currently no dimmer support.  00 is off, 
064 is on.

* my openhab configs are in openhab_config
