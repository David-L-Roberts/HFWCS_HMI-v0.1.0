from Logging import Log
from nicegui import ui

class DataProcessor:
    def __init__(self) -> None:
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
        Log.log("Processing: Auto Break Enabled", Log.DEBUG)
        ui.notify("Automatic Breaking Activated", type='warning', position='center')
    
    def __service_breakDisabled(self):
        Log.log("Processing: Auto Break Disabled", Log.DEBUG)
        ui.notify("Automatic Breaking Released", type='positive', position='center')
    
    def __service_stopEnabled(self):
        Log.log("Processing: Emergency Stop Enabled", Log.DEBUG)
        ui.notify("Emergency Stop Activated", type='negative', position='center')
    
    def __service_stopDisabled(self):
        Log.log("Processing: Emergency Stop Disabled", Log.DEBUG)
        ui.notify("Emergency Stop Deactivated", type='positive', position='center')
    
    def __service_DistSensor(self):
        Log.log(f"Processing: Distance Sensor Reading - {self.dataVal}", Log.DEBUG)
    