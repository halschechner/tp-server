import Queue
import threading

# Event details
EventQueue = Queue.Queue()

# idempotent announcement of an output's state.  Alerts to changes as well as periodically sent for
# listeners to "catch up" 
E_OUTPUT_STATE = 1 # args: (output, status[00|64] )

# a request to change the state of an output.  
E_OUTPUT_SET = 2 # args: (output, newstate[00|64] )

# send a generic timekeeper command
E_SEND_TIMEKEEPER_COMMAND = 3 # args: (string)

# Listeners
LISTENERS = {
    E_OUTPUT_STATE : [],
    E_OUTPUT_SET : [],
    E_SEND_TIMEKEEPER_COMMAND : []
}

ListenerThread = None

def putEventOnBus(eventType, eventData):
    global EventQueue
    EventQueue.put( (eventType, eventData) )

def addEventListener(EventType, func):
    global LISTENERS
    LISTENERS[EventType].append(func)

def runListeners():
    """
    Monitor the EventQueue and run listeners of various events as they come
    """

    global LISTENERS
    global EventQueue

    while 1:
        event = EventQueue.get()
        for func in LISTENERS[event[0]]:
            func(*event[1])

def startEventBus():
    global ListenerThread

    # thread to hand events to listeners
    ListenerThread = threading.Thread(
        target = runListeners,
        args = ()
        )

    ListenerThread.start()
