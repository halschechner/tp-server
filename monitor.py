import threading
import devices
import telnetlib
import time
import eventBus

# how many seconds between complete status checks
FULL_STATUS_PERIOD = 60

TIMEKEEPER_HOST = "0.0.0.0"
TIMEKEEPER_PORT = 4000

# output statuses
OutputStatuses = {}


def separateCommands(s):
    """ 
    separate s into a list of represented commands as well as any partial 
    commands at the trailing end
    """
    commands = []
    extra = []
    while '<' in s and '>' in s:
        commands.append( s[s.index('<'):s.index('>')+1] )
        s = s[s.index('>')+1:]
    return commands, s

def monitorSystem(host, port):
    """
    Monitor a timekeeper system, separate commands and parse them
    """
    con = telnetlib.Telnet(host, port)
    lastCompleteStatus = time.time()

    data = ""
    while 1:
        data = data + con.read_some()
        commands, data = separateCommands(data)
        handleCommands(commands)

def requestFullSystemStatus(host, port):
    eventBus.putEventOnBus(eventBus.E_SEND_TIMEKEEPER_COMMAND, ( "<PUSH STATUS ON />\n", ) )

def handleCommands(cmds):
    global OutputStatuses
    global EventQueue

    for cmd in cmds:
        output = None
        status = None
        if cmd.startswith('<OS'):
            output = cmd[3:6]
            status = cmd[6:8]
        if cmd.startswith('<GET OUTPUT LEVEL'):
            output = cmd[18:21]
            status = cmd[22:24]

        if output and status:
            eventBus.putEventOnBus( eventBus.E_OUTPUT_STATE, (output, status) )
            OutputStatuses[ output ] = status

def setOutputState(output, state):
    sendCommand( "<SET OUTPUT %s %s 0000 />" %(output, state) )

def sendCommand(cmd):
    sendCommands( [cmd] )

def sendCommands(cmds):
    global TIMEKEEPER_HOST
    global TIMEKEEPER_PORT
    con = telnetlib.Telnet(TIMEKEEPER_HOST, TIMEKEEPER_PORT)
    for cmd in cmds: 
        print 'Sending %s' %cmd
        con.write(cmd + "\n")
    con.close()

def runFullSystemUpdates(host, port):    
    while 1:
        time.sleep(5)
        requestFullSystemStatus(host, port)
        print 'PUSHING COMPLETE'
        time.sleep(FULL_STATUS_PERIOD)

def startMonitoring(timekeeperIP, timekeeperPort):        
    global TIMEKEEPER_HOST
    global TIMEKEEPER_PORT
    TIMEKEEPER_HOST = timekeeperIP
    TIMEKEEPER_PORT = timekeeperPort

    # add a listener for output setting events
    eventBus.addEventListener(eventBus.E_OUTPUT_SET, setOutputState)

    # add a listener for sending commands to the timekeeper
    eventBus.addEventListener(eventBus.E_SEND_TIMEKEEPER_COMMAND, sendCommand)

    # Thread to watch the Timekeeper Event stream
    monitorThread = threading.Thread(
        target = monitorSystem, 
        args = (timekeeperIP, timekeeperPort)
        )


    # thread to periodically ask for a full system status
    statusThread = threading.Thread(
        target = runFullSystemUpdates,
        args = (timekeeperIP, timekeeperPort)
        )

    monitorThread.start()
    statusThread.start()
