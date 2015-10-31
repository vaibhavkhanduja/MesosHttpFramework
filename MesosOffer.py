__author__ = 'khandv'


class SlaveAddress:
    _ip = None
    _hostname = None
    _port = None

    def __init__(self, address):
        self._ip = address['ip']
        self._hostname = address['hostname']
        self._port = address['port']

class SlaveURL:
    _path = None
    _scheme = None
    _address = None

    def __init__(self, url):
        self._path = url['path']
        self._scheme = url['scheme']
        self._address = SlaveAddress(url['address'])

class SlaveResourceRange:
    _begin = None
    _end = None

    def __init__(self, range):
        self._begin = range['begin']
        self._end = range['end']

class SlaveResource:
    _type = None
    _scaler = None
    _ranges = []
    _role = None
    _name = None

    def __init__(self, resource):
        self._type = resource['type']

        self._name = resource['name']
        self._role = resource['role']
        if self._type == 'SCALAR':
              self._scaler = resource['scalar']['value']
        else:
            if self._type == 'RANGES':
               for val in resource['ranges']['range']:
                   self._ranges.append(val)
class MesosOffer:
    url = None
    hostname = None
    id = None
    agent_id = None
    framework_id = None
    resources = []

    def __init__(self, offer):
        self.url = SlaveURL(offer['url'])
        self.hostname = offer['hostname']
        self.agent_id = offer['agent_id']
        self.id = offer['id']
        self.framework_id = offer['framework_id']
        for res in offer['resources']:
            self.resources.append(SlaveResource(res))