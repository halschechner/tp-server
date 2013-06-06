import devices
import httplib


def reportStatusChange(output, status):
    # just ignore any output we don't know about
    if output not in devices.DeviceIDToName:
        return
    statusText = {'00' : 'OFF', '64' : 'ON'}[status]
    outputName = devices.DeviceIDToName[output].replace(' ', '_')
    con = httplib.HTTPConnection('127.0.0.1', 8888) 
    url = "http://127.0.0.1:8888/rest/items/Light_%s/state" %outputName
    print 'Sending "%s" to "%s"' %(statusText, url)
    con.request("PUT", 
                url,
                statusText,
                {'Content-Type' : 'text/plain'})
    con.close()
