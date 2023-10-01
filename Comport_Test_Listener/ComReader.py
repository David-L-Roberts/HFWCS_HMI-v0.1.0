from threading import Thread, Event
from MessageLib import msgTypeLookup
import time
import serial
import Logging as Log 


class ComReader():
    """   
    Starts a thread that will read data from serial.
    Will read for `maxWaitsec` time, then sleep. Will wake when `readSerial` method is called.

    Provides methods to read data from the serial.
    """
    def __init__(self, comPort: serial.Serial, filter: bool=True, maxWaitSec: float=3) -> None:
        self._comPort = comPort
        self._filter = filter
        self._currentMessage = ""
        self.maxWaitSec = maxWaitSec

        self._event = Event()
        self._readThread = Thread(target=self.__threadLoop, daemon=True)
        self._readThread.start()

    def readSerial(self):
        """Start thread to read data from serial."""
        self._event.set()
    
    def __threadLoop(self):
        while True:
            self.__readSerial()
            time.sleep(0.3)

    def __readSerial(self):
        """Try reading data from serial."""
        inputBytes = self.__readRaw() 
        if inputBytes == b'':
            return
        inputStr = inputBytes.hex(' ').upper()
        print(inputStr)


    def __readRaw(self):
        """Read raw serial data. For debugging purposes."""
        inputBytes = b''
        while(self._comPort.in_waiting > 0):
            inputBytes += self._comPort.read(10)
        return inputBytes


    def getMessageType(self):   # SS
        """Return the message type of the last read message."""
        try:
            controlCode = self._currentMessage[:2]
        except:
            Log.log("No message recieved.", logFlag="|Debug|")
        try:
            messageType = msgTypeLookup[controlCode]
        except:
            messageType = controlCode
            Log.log("Received invalid Control Code.", logFlag="|ERROR|")

        return messageType
