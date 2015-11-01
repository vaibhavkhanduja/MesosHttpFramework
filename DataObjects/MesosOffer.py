# See LICENSE file for details.
# Copyright 2015-2015

__author__ = 'Vaibhav Khanduja - VK'

from MesosHttpFramework.common.Object import Object

class SlaveAddress(Object):
    """
    The address of Mesos slave returned as part of
    Offer.
    """
    _ip = None
    _hostname = None
    _port = None

    def __init__(self, address):
        """
        :param address: The address present in the json stream.
        :return:None
        """
        self._ip = address['ip']
        self._hostname = address['hostname']
        self._port = address['port']

class SlaveURL(Object):
    """
    The URL details sent by json stream.
    """
    _path = None
    _scheme = None
    _address = None

    def __init__(self, url):
        """
        :param url:URL json object.
        :return:
        """
        self._path = url['path']
        self._scheme = url['scheme']
        self._address = SlaveAddress(url['address'])


class SlaveResourceRange(Object):
    """
    The resource of type, has a begin and end values.
    """
    _begin = None
    _end = None

    def __init__(self, range):
        """
        :param range: The JSON stream from  Slave.
        :return:
        """
        self._begin = range['begin']
        self._end = range['end']

class SlaveResource(Object):
    """
    The Slave Resource, sent from Slave.
    """
    _type = None
    _scaler = None
    _ranges = []
    _role = None
    _name = None

    def __init__(self, resource):
        """
        :param resource: The JSON stream from Slave: Resource.
        :return:
        """
        self._type = resource['type']

        self._name = resource['name']
        self._role = resource['role']
        if self._type == 'SCALAR':
            self._scaler = resource['scalar']['value']
        else:
            if self._type == 'RANGES':
                for val in resource['ranges']['range']:
                    self._ranges.append(val)

class MesosOffer(Object):
    """
    The Mesos Offer from Slave.
    """
    url = None
    hostname = None
    id = None
    agent_id = None
    framework_id = None
    resources = []


    def __init__(self, offer):
        """
        :param offer: JSON Stream of constituting the offer.
        :return:None
        """
        self.url = SlaveURL(offer['url'])
        self.hostname = offer['hostname']
        self.agent_id = offer['agent_id']
        self.id = offer['id']
        self.framework_id = offer['framework_id']
        for res in offer['resources']:
            self.resources.append(SlaveResource(res))

        self.toString()