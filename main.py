import monitor
import time
import apiserver
import openHABInterface
import eventBus

# start the eventBus
eventBus.startEventBus()

# make sure that openHAB gets events
eventBus.addEventListener(eventBus.E_OUTPUT_STATE, openHABInterface.reportStatusChange)

# Start monitoring the TimeKeeper
monitor.startMonitoring('192.168.1.200', 4000)

# Start the API service
apiserver.startServing(port=8000)


# Goop to display the "on" outputs every few seconds
while 1:
    for key in monitor.OutputStatuses.keys():
        if monitor.OutputStatuses[key] == '64':
            print '%s: on' %key
    print '--------------------------'
    time.sleep(5)
