# See LICENSE file for details.
# Copyright 2015-2015

__author__ = 'Vaibhav Khanduja - VK'

from Object import Object
import httplib
import json

class HTTPComm(Object):
    """
    The Main class for HTTP Communication.
    """
    _url = None

    def __init__(self, url):
        """
        :param url: The URL to connect for HTTP communication.
        :return:
        """
        self._url = url
        return

    def post(self, data, api):
        """
        :param data: The data parameter of HTTP Post.
        :param api: The URL of the API exposed by Mesos Master.
        :return:
        """
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