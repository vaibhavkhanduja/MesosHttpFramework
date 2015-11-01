# See LICENSE file for details.
# Copyright 2015-2015

__author__ = 'Vaibhav Khanduja - VK'

from abc import ABCMeta, abstractmethod

class Object:
    """
    The abstract base class for all classes in MesosHttpFramework.
    """
    __metaclass__ = ABCMeta

    @abstractmethod
    def __init__(self):
        """
        :return: None.
        """
        pass

    def toString(self):
        """
        Converts all object and its values to a string stream.
        :return: None
        """
        for attr in dir(self):
            if not callable(attr) and not attr.startswith("__"):
                print "%s = %s" % (attr, getattr(self, attr))
