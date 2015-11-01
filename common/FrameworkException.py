# See LICENSE file for details.
# Copyright 2015-2015

__author__ = 'Vaibhav Khanduja - VK'

from abc import ABCMeta, abstractmethod

from Object import Object
import exceptions

class FrameworkException(Object):
    """
    Abstract class acting as base of all exceptions.
    """
    __metaclass__ = ABCMeta

    @abstractmethod
    def __init__(self, exception):
        pass