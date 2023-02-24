import exceptions as e
from equipment import device

# A generic PID class with logging
class PID(device):
    # Device (controllers.PID): The PID to control
    # WhiteSpaceIn (float): Defines the default white space for the input when plotting
    # WhiteSpaceOut (float): Defines the default white space for the output when plotting    
    # DeviceName (str): The name of the device
    # ID (str): The ID name for the device, only used for displaying infomation
    def __init__(self, Device, *args, WhiteSpaceIn = 0.1, WhiteSpaceOut = 0.1, **kwargs):
        import controllers
        import loggers
        
        if not "DeviceName" in kwargs:
            kwargs["DeviceName"] = "TempArduino"
        
        super().__init__(*args, **kwargs)
        
        if not isinstance(Device, controllers.PID):
            raise e.TypeDefError("PID", Device, controllers.PID)
        
        # Save the settings
        self.device = Device
        self._whiteSpaceIn = float(WhiteSpaceIn)
        self._whiteSpaceOut = float(WhiteSpaceOut)
        
        # Initialize the logger
        self.logger = loggers.PIDLogger(self.logDataRetriever)
        
    # Retrieves the PID data for the logger: SignalIn, SetPoint, SignalOut, this must be defined
    def logDataRetriever(self):
        pass
        
    # Logs the PID and does live plotting
    # File (str): The file path for where to save the log
    # MaxTime (float): The time in seconds to run the logging, 0 for infinity, must not be negative
    # Period (floar): The time in seconds between each measurement, must not be negative
    # MaxShow (int): The maximum number of data points to show at once, must be positive
    # Name (str): The name to display on the figures
    # figsize (tuple): A tuple of ints define the size of the figure
    # Plot (bool): If True then do live plotting
    # KeepFigure (bool): If False then it closes the live plotting when done
    # Wait (bool): If True then it will wait for the log to finish and then return the data, if False then it will return immidiatly and return the stop event for the log for which to do .set() to stop the log
    def log(self, *args, **kwargs):
        # Overwrite white space
        if not "WhiteSpaceIn" in kwargs:
            kwargs["WhiteSpaceIn"] = self._whiteSpaceIn
            
        if not "WhiteSpaceOut" in kwargs:
            kwargs["WhiteSpaceOut"] = self._whiteSpaceOut
            
        # Overwrite name
        if not "Name" in kwargs:
            kwargs["Name"] = "PID"
        
        return self.logger.log(*args, **kwargs)
        
    def _close(self):
        self.logger.killLogs()
        super()._close()