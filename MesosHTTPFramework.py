# See LICENSE file for details.
# Copyright 2015-2015

__author__ = 'Vaibhav Khanduja - VK'

import sys
import json

from common.Object import Object
from common.HTTPComm import HTTPComm
from common.HTTPChunkReader import HTTPChunkReader

from DataObjects.MesosOffer import MesosOffer

class Driver(Object):
    """
    The main driver class.
    """
    _http = None
    _chunkReader = None
    _frameworkId = None
    _offer = []

    def __init__(self, master):
        """
        :param master: The Mesos master address.
        :return: None.
        """
        self._http = HTTPComm(master)

    def run(self):
        """
        :return: The main run method of the driver.
        The first step is to subscribe.
        """
        self.subscribe(self)
        return

    @staticmethod
    def processResponse(self, chunk):
        """
        The method reads through the response received from Mesos master.
        :param chunk: The chunk received.
        :return:None.
        """
        payload = json.loads(chunk)
        if chunk is not None:
            callback = payload['type'].lower()
            getattr(self, callback)(payload)
        else:
            print "Could not decode message"

    @staticmethod
    def subscribe(self):
        """
        The first function call to Mesos Master, is subscribe for events.
        :return:
        """

        data = {
            "type": "SUBSCRIBE",
            "subscribe": {
                "framework_info": {
                    "user": "root",
                    "name": "Test Framework"
                },
                "force": True
            }
        }
        eventChannel = self._http.post(data, "/api/v1/scheduler")
        if eventChannel is not None:
            self._chunkReader = HTTPChunkReader(eventChannel)
            while True:
                chunk = self._chunkReader.readChunkStream()
                self.processResponse(self, chunk)
        else:
            print "Something went wrong! Could not connect with Master"
        return

    def subscribed(self, payload):
        """
        The return call from Mesos master, as acknowledment for subscribe.
        :param payload:The return json string, from Mesos master.
        :return:
        """
        self._frameworkId = payload['subscribed']['framework_id']['value']
        print self._frameworkId
        print "Subscribed"
        return

    def heartbeat(self, payload):
        """
        The heatbeat method is sent regularly by Mesos master.
        :param payload:The payload or json string sent along with hearbeat method.
        :return:
        """
        print "HeartBeat"
        return

    def offers(self, payload):
        """
        The offers are sent, originating from Mesos slave.
        :param payload:The JSON string.
        :return:
        """
        for i in payload['offers']['offers']:
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