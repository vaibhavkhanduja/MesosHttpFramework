
import sys
import httplib
import json

from MesosOffer import MesosOffer

class chunkReader:

    _eventChannel = None

    def __init__(self, eventChannel):
        self._eventChannel = eventChannel
        return

    def get_chunk_size(self):
        size_str = self._eventChannel.read(2)
        while size_str[-1:] != b"\n":
            size_str += self._eventChannel.read(1)
        return int(size_str)

    def get_chunk_data(self, chunk_size):
        data = self._eventChannel.read(chunk_size)
        return data

    def readChunkStream(self):
        chunk_data = None
        try:
            chunk_size = self.get_chunk_size()
            if (chunk_size == 0):
                return chunk_data
            else:
                chunk_data = self.get_chunk_data(chunk_size)
                print("Chunk Received: " + chunk_data.decode())
        except httplib.HTTPException as e:
            print e
        return chunk_data

class HTTPComm:

    _url = None

    def __init__(self, url):
        self._url = url
        return

    def post(self, data, api):
        response = None
        try:
            _data = json.dumps(data)
            headers = {"Content-type": "application/json",
                        "Accept": "application/json",
                        "Connection": "close"}
            comm = httplib.HTTPConnection(self._url)
            comm.request("POST", api, _data, headers)
            response = comm.getresponse()
        except httplib.HTTPException as e:
            print e
        return response


class Driver:

    _http = None
    _chunkReader = None
    _frameworkId = None
    _offer = []

    def __init__(self, master):
        self._http = HTTPComm(master)

    def run(self):
        self.subscribe()
        return

    def processResponse(self, chunk):
        payload = json.loads(chunk)
        if chunk is not None:
            callback = payload['type'].lower()
            getattr(self, callback)(payload)
        else:
            print "Could not decode message"
        return

    def subscribe(self):

        data = {
        "type" : "SUBSCRIBE",
        "subscribe" : {
            "framework_info" : {
                "user" : "root",
                "name" : "Test Framework"
            },
            "force" : True
            }
        }
        eventChannel = self._http.post(data, "/api/v1/scheduler")
        if eventChannel is not None:
            self._chunkReader = chunkReader(eventChannel)
            while True:
                chunk = self._chunkReader.readChunkStream()
                self.processResponse(chunk)
        else:
            print "Something went wrong! Could not connect with Master"
        return

    def subscribed(self, payload):
        self._frameworkId = payload['subscribed']['framework_id']['value']
        print self._frameworkId
        print "Subscribed"
        return

    def heartbeat(self, payload):
        print "HeartBeat"
        return

    def offers(self, payload):
        print json.dumps(payload['offers']['offers'][0], indent=4)
        for i in payload['offers']['offers']:
            print i['url']
            print i['framework_id']
            print i['agent_id']
            self._offer.append(MesosOffer(i))

        return

    def rescind(self, payload):
        print "Rescind"
        return

    def update(self, payload):
        print "Update"
        return

    def message(self, payload):
        print "Message"
        return

    def failure(self, payload):
        print "Failure"
        return

    def error(self, payload):
        print "Error"
        return

if __name__ == '__main__':
    print len(sys.argv)
    if len(sys.argv) < 3:
        print "No Master Provided"
    else:
        driver = Driver(sys.argv[1] + ":" + sys.argv[2])
        driver.run()