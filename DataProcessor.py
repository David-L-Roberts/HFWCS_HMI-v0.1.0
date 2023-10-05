from Logging import Log
from nicegui import ui
import time

C_HEADER_DEFAULT = "bg-[#0d1117]"
C_HEADER_STOP = "bg-rose-900"

MAX_DIST_VAL = 500  # max distance reading of sensor, in cm
CONV_FACT = MAX_DIST_VAL/255    # conversion factor for distance reading

class DataProcessor:
    def __init__(self, headerRow: ui.header, distanceLabel: ui.label) -> None:
        # match action codes to service functions
        self.processorDict = {
            "D2": self.__service_ACK,
            "FB": self.__service_breakEnabled,
            "FC": self.__service_breakDisabled,
            "FA": self.__service_stopEnabled,
            "FE": self.__service_stopDisabled,
            "FD": self.__service_DistSensor
            }
        # var for holding distance sensor reading
        self.dataVal = ""
        # store reference to header row element
        self.headerRow = headerRow
        # store reference to distance label element
        self.distlabel = distanceLabel
        # flag for acknowledgement reception
        self.recACK = False

    def processCharCode(self, charCode: str):
        if type(charCode) == tuple:
            charCode, self.dataVal = charCode
        try:
            func = self.processorDict[charCode]
        except KeyError:
            Log.log(f"Cannot process char code ({charCode}) in {DataProcessor}.", Log.WARNING)
        else:
            func()
    
    def __service_ACK(self):
        Log.log("Processing: ACK", Log.DEBUG)
        self.recACK = True

    def checkACK(self):
        """Returns `True` if an ACK was received. Will reset ACK flag."""
        response = self.recACK
        self.recACK = False
        return response
    
    def __service_breakEnabled(self):
        Log.log("Automatic Breaking ACTIVATED.")
        ui.notify("Automatic Breaking Activated. Forward movement prevented.", type='warning', position='center', progress=True, timeout=5_000)
    
    def __service_breakDisabled(self):
        Log.log("Automatic Breaking RELEASED.")
        ui.notify("Automatic Breaking Released.", type='positive', position='center', progress=True, timeout=4_000)
    
    def __service_stopEnabled(self):
        Log.log("Emergency Stop ACTIVATED.")
        ui.notify("Emergency Stop Activated. All movement is disabled.", type='negative', position='center', progress=True, timeout=5_000)
        self.headerRow.classes(remove=C_HEADER_DEFAULT, add=C_HEADER_STOP)
    
    def __service_stopDisabled(self):
        Log.log("Emergency Stop DEACTIVATED.")
        ui.notify("Emergency Stop Deactivated. Movement enabled.", type='positive', position='center', progress=True, timeout=4_000)
        self.headerRow.classes(remove=C_HEADER_STOP, add=C_HEADER_DEFAULT)
    
    def __service_DistSensor(self):
        Log.log(f"Processing: Distance Sensor Reading - 0x{self.dataVal}", Log.DEBUG)
        # convert hex str to int val
        dataInt: int = int.from_bytes(bytes.fromhex(self.dataVal), byteorder='big')
        # convert Int to distance (in cm)
        distanceFloat: float = round(dataInt*CONV_FACT, 1)
        # conver to string. format with 3 sig figs
        distStr: str = str(distanceFloat)
        self.distlabel.set_text(f"{distStr} cm")