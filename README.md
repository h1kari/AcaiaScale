# AcaiaScale

This is a port of Bobby Powers's javascript implementation of code to talk to the Acaia BLE scale. The tare and weight reading functions have been tested on the Acaia Pearl. It needs some cleanup and additional code to make it useful but should work with pygatt as follows:

```
from pygatt import GATTToolBackend
from AcaiaScale.Packet import Packet
from time import sleep

# instantiate packet class
packet = Packet()

# create callback for printing received weight values
count = 0
def scale_cb(handle, value):
    global count
    packet.decodeWeight(value)
    if packet.weightReading():
        weight = packet.getWeight()
        print weight
        count += 1

# connect to scale
adapter = GATTToolBackend('hci0')
adapter.start(False)
device = adapter.connect('00:1C:97:11:B7:C6')

# subscribe to notifications
device.subscribe("00002a80-0000-1000-8000-00805f9b34fb", scale_cb)

# enable notifications and begin reading weight values
device.char_write_handle(0x0e, [0x01, 0x00])
device.char_write_handle(0x12, [0x01, 0x00])

# tare scale
device.char_write_handle(0x0d, packet.encodeTare())

# read 100 weight values
device.char_write_handle(0x0d, packet.encodeWeight())

while count < 100:
    sleep(1)
```

