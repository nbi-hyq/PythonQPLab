from .. import exceptions as e
from ..equipment import PID

# Controls a tempArduino PID and implements logging for it        
class tempArduino(PID):
    # Device (controllers.PID): The PID to control
    # WhiteSpaceIn (float): Defines the default white space for the input when plotting
    # WhiteSpaceOut (float): Defines the default white space for the output when plotting    
    # DeviceName (str): The name of the device
    # ID (str): The ID name for the device, only used for displaying infomation
    def __init__(self, Device, *args, **kwargs):
        from .. import controllers as c

        if not isinstance(Device, c.tempArduino):
            raise e.TypeDefError("Temperature Arduino", Device, c.tempArduino)
            
        if not "DeviceName" in kwargs:
            kwargs["DeviceName"] = "Temperature Arduino"
            
        super().__init__(Device, *args, **kwargs)
        
    # Retrieves the PID data for the logger: SignalIn, SetPoint, SignalOut
    def logDataRetriever(self):
        # Get the data
        Values = self.device.getStatus()
        
        SignalIn = Values["V_in"]
        SignalOut = Values["V_out"]
        SetPoint = Values["S"]
        
        return SignalIn, SetPoint, SignalOut
    
    # Logs the PID and does live plotting
    # File (str): The file path for where to save the log
    # MaxTime (float): The time in seconds to run the logging, 0 for infinity, must not be negative
    # Period (floar): The time in seconds between each measurement, must not be negative
    # MaxShow (int): The maximum number of data points to show at once, must be positive
    # Name (str): The name to display on the figures
    # figsize (tuple): A tuple of ints define the size of the figure
    # Plot (bool): If True then do live plotting
    # KeepFigure (bool): If False then it closes the live plotting when done
    # Wait (bool): If True then it will wait for the log to finish, if False then it will return immidiatly and return the stop event for the log for which to do .set() to stop the log
    def log(self, *args, **kwargs):
        if not "Name" in kwargs:
            kwargs["Name"] = "Temperature Arduino"

        super().log(*args, **kwargs)