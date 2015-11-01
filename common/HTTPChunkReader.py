# See LICENSE file for details.
# Copyright 2015-2015

__author__ = 'Vaibhav Khanduja - VK'

from Object import Object
import httplib

class HTTPChunkReader(Object):
    """
    Specialized class to read in chunks
    from the HTTP Stream.
    """
    _eventChannel = None

    def __init__(self, eventChannel):
        """
        :param eventChannel: The responce channel from HTTP Conection
        :return: None
        """
        self._eventChannel = eventChannel

    @staticmethod
    def getChunkSize(self):
        """
        :return: Parses the eventChannel( HTTP Responce Stream)
        to return the size of the valid chunk.
        """
        size_str = self._eventChannel.read(2)
        while size_str[-1:] != b"\n":
            size_str += self._eventChannel.read(1)
        return int(size_str)

    @staticmethod
    def getChunkData(self, chunk_size):
        """
        :param chunk_size: The size of data to be read from stream.
        :return: The chunk data.
        """
        data = self._eventChannel.read(chunk_size)
        return data

    def readChunkStream(self):
        """
        :return: The chuck data from the stream.
        """
        chunk_data = None
        try:
            chunk_size = self.getChunkSize(self=self)
            if chunk_size == 0:
                return chunk_data
            else:
                chunk_data = self.getChunkData(self=self, chunk_size=chunk_size)
        except httplib.HTTPException as e:
            print e
        return chunk_data