"""
A class that implements formation of the Acaia BLE packet functions

CREDIT: Based on Bobby Powers's js implementation at https://github.com/bpowers/btscale
"""

__author__    = "David Hulton"
__license__   = "BSD"
__copyright__ = "Copyright 2016, David Hulton"

from AcaiaScale.Encode import Encode

class Packet(Encode):
    def __init__(self):
        self._weightReading = 0
        Encode.__init__(self)

    def encodeWeight(self, weightPeriod = 1, weightTime = 100, weightType = 1):
        payload = [weightPeriod & 0xff, weightTime & 0xff, weightType & 0xff]
        return self.encode(4, 0, payload)

    def encodeTare(self):
        payload = [0x0, 0x0]
        return self.encode(12, 0, payload)

    def encodeStartTimer(self):
        payload = [0x5]
        return self.encode(12, 0, payload)

    def encodePauseTimer(self):
        payload = [0x6]
        return self.encode(12, 0, payload)

    def encodeStopTimer(self):
        payload = [0x7]
        return self.encode(12, 0, payload)

    def encodeGetTimer(self, count = 20):
        payload = [0x8, count & 0xff]
        return self.encode(12, 0, payload)

    def encodeGetBattery(self):
        return self.encode(2, 0, [])

    def decodeWeight(self, data):
        self.decode(data)
        self._weightReading = False
        if self._msgType == 5:
            value = float((self._payload[1] << 8) | self._payload[0])
            for i in range(self._payload[4]):
                value /= 10

            if self._payload[6] & 0x2 == 0x2:
                value *= -1

            self._weightReading = True
            self._weightValue = value

    def weightReading(self):
        return self._weightReading

    def getWeight(self):
        if self._weightReading:
            return self._weightValue
        else:
            return False

