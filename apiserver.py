import BaseHTTPServer
import threading
import monitor
import urlparse
import SocketServer
import json
import eventBus

class LightingAPIHandler(BaseHTTPServer.BaseHTTPRequestHandler):

    def __init__(self, *args, **kwargs):
        BaseHTTPServer.BaseHTTPRequestHandler.__init__(self, *args, **kwargs)
   
        return

    def log_message(self, *args, **kwargs):
        pass

    def do_GetOutputStatus(self, outputID):
        """ Get the status of an output """
        outputID = self.path[15:19].upper()
        if outputID not in monitor.OutputStatuses:
            self.send_response(404)
            self.end_headers()
            return
        else:
            state = monitor.OutputStatuses[outputID]
            self.send_response(200)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write( {'00' : 'off', '64' : 'on'}[state] )
            return

    def do_GetOutputOff(self, outputIDs):
        cmds = []
        ids = outputIDs.split(',')
        for outputId in ids:
            eventBus.putEventOnBus( eventBus.E_OUTPUT_SET, (outputId, "00") )

        self.send_response(200)
        self.send_header('Content-type', 'text/json')
        self.end_headers()
        return

    def do_GetOutputOn(self, outputIDs):
        cmds = []
        ids = outputIDs.split(',')
        for outputId in ids:
            eventBus.putEventOnBus( eventBus.E_OUTPUT_SET, (outputId, "64") )

        self.send_response(200)
        self.send_header('Content-type', 'text/json')
        self.end_headers()
        return

    def do_GET(self):
        if self.path.startswith('/output/status/'):
            return self.do_GetOutputStatus(self.path[15:19].upper())
        elif self.path.startswith('/output/on/'):
            return self.do_GetOutputOn(self.path[11:].upper())
        elif self.path.startswith('/output/off/'):
            return self.do_GetOutputOff(self.path[12:].upper())

        # catchall 404
        self.send_response(404)
        self.end_headers()
        return

class ThreadedHTTPServer(SocketServer.ThreadingMixIn, BaseHTTPServer.HTTPServer):
    """ one request per thread """

def startServing(address='', port=8000):
    server_address = (address, port)
    httpd = ThreadedHTTPServer( server_address, LightingAPIHandler )
    apiServingThread = threading.Thread( target = httpd.serve_forever )
    apiServingThread.start()
                           
