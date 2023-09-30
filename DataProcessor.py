from Logging import Log

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

        func = self.processorDict[charCode]
        func()
    
    def __service_ACK(self):
        Log.log("Processing: ACK", Log.DEBUG)
        pass
    
    def __service_breakEnabled(self):
        Log.log("Processing: Auto Break Enabled", Log.DEBUG)
        pass
    
    def __service_breakDisabled(self):
        Log.log("Processing: Auto Break Disabled", Log.DEBUG)
        pass
    
    def __service_stopEnabled(self):
        Log.log("Processing: Emergency Stop Enabled", Log.DEBUG)
        pass
    
    def __service_stopDisabled(self):
        Log.log("Processing: Emergency Stop Disabled", Log.DEBUG)
        pass
    
    def __service_DistSensor(self):
        Log.log(f"Processing: Distance Sensor Reading - {self.dataVal}", Log.DEBUG)
        pass