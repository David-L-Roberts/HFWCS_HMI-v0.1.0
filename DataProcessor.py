from Logging import Log
from nicegui import ui
import time

C_HEADER_DEFAULT = "bg-stone-900"
C_HEADER_STOP = "bg-rose-900"

class DataProcessor:
    def __init__(self, headerRow: ui.header) -> None:
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
    
    def __service_breakEnabled(self):
        ui.notify("Automatic Breaking Activated", type='warning', position='center', progress=True)
    
    def __service_breakDisabled(self):
        ui.notify("Automatic Breaking Released", type='positive', position='center', progress=True)
    
    def __service_stopEnabled(self):
        ui.notify("Emergency Stop Activated", type='negative', position='center', progress=True, timeout=7_000)
        self.headerRow.classes(remove=C_HEADER_DEFAULT, add=C_HEADER_STOP)
    
    def __service_stopDisabled(self):
        ui.notify("Emergency Stop Deactivated", type='positive', position='center', progress=True)
        self.headerRow.classes(remove=C_HEADER_STOP, add=C_HEADER_DEFAULT)
    
    def __service_DistSensor(self):
        Log.log(f"Processing: Distance Sensor Reading - 0x{self.dataVal}", Log.DEBUG)

    