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
            if self._event.is_set():
                self.__readSerial()
                # self._event.clear()
            else:
                time.sleep(0.1)

    def __readSerial(self):
        """Try reading data from serial."""
        if self._filter:
            readFunc = self.__readFiltered
        else:
            readFunc = self.__readRaw

        # reading from serial
        self._currentMessage = ""
        endTime = time.time() + self.maxWaitSec
        while (endTime - time.time()) > 0:
        # while True:
            readFunc()
        if self._currentMessage == "":
            # Log.log(f"|!!!| No Data Recieved after {self.maxWaitSec} sec")
            pass
        else:
            Log.log(f"From serial: {self._currentMessage}")
            Log.log(f"Rx Message Type: {self.getMessageType()}")


    def __readRaw(self):
        """Read raw serial data. For debugging purposes."""
        while(self._comPort.in_waiting > 0):
            print(self._comPort.read(10))
    

    def __readFiltered(self):
        """Read and filter data from the serial."""
        inputByteArray: bytes = b''
        time.sleep(0.05)
        if(self._comPort.in_waiting > 0):
            time.sleep(0.1)
            Log.log(f"Bytes Recieved: {self._comPort.in_waiting}")
        else: 
            return
        while(self._comPort.in_waiting > 0):
            inputByteArray += self._comPort.read(size=50)

        # updated current message if new data has been read
        if inputByteArray:
            for byte in inputByteArray:
                byteFormatted: str = hex(byte)[2:].upper()
                if len(byteFormatted) < 2:
                    byteFormatted = "0" + byteFormatted
                self._currentMessage += byteFormatted + " "


    def getMessageType(self):
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
