from .. import connections as c
from ..interface import powermeter

# Controls the powermeter
class PM100D(powermeter, c.visa):
    # SerialNumber (str): The serial number of the device
    # Timeout (float): The timeout time for the connection, must not be negative
    # ReconnectTries (int): How many times to attempt to reconnect if it disconnects, must not be smaller than 0
    # ReconnectDelay (float): The delay in seconds between each reconnect attempt, must not be negative
    # MaxAttempts (int): The maximum number attempts to send a command before giving up, must not be smaller than 1
    # AttemptDelay (float): The delay in seconds between each attempt to send a command, must not be negative
    # UseQueue (bool): If True then it will set up a queue which can be used in the sendCommand method, if False the UseQueue in sendCommand is ignored
    # Empty (bool): If True then it will not communicate with the device
    # DeviceName (str): The name of the device, only used for error messages
    # ID (str): The ID name for the device, only used for displaying infomation
    def __init__(self, SerialNumber, *args, **kwargs):
        if not "DeviceName" in kwargs:
            kwargs["DeviceName"] = "PM100D"
        
        super().__init__(f"USB0::0x1313::0x8078::{SerialNumber}::INSTR", *args, **kwargs)

    # Sets a bool value
    # Parameter (str): The parameter to set
    # Value (bool): The value to set
    # UseQueue (bool): True if it should use the command queue    
    def _setBool(self, Parameter, Value, **kwargs):
        self.sendWithoutResponse(f"{Parameter} {int(bool(Value))}", **kwargs)
        
    # Sets a float value
    # Parameter (str): The parameter to set
    # Value (bool): The value to set
    # UseQueue (bool): True if it should use the command queue    
    def _setFloat(self, Parameter, Value, **kwargs):
        self.sendWithoutResponse(f"{Parameter} {Value:g}", **kwargs)
        
    # Gets a bool value
    # Parameter (str): The parameter to get
    # UseQueue (bool): True if it should use the command queue    
    def _getBool(self, Parameter, **kwargs):
        from .. import functions as f
        
        kwargs["ResponseCheck"] = f.responseCheck.getBool()
        return bool(self.query(f"{Parameter}?", **kwargs))
    
    # Gets a float value
    # Parameter (str): The parameter to get
    # UseQueue (bool): True if it should use the command queue    
    def _getFloat(self, Parameter, **kwargs):
        from .. import functions as f
        
        kwargs["ResponseCheck"] = f.responseCheck.getNumber()
        return float(self.query(f"{Parameter}?", **kwargs))

    # Sets the power auto range
    # Value (bool): True if auto range should be enabled
    # UseQueue (bool): True if it should use the command queue    
    def setPowerAutoRange(self, Value, **kwargs):
        self._setBool("power:range:auto", Value, **kwargs)
    
    # Gets the status of the power auto range
    # UseQueue (bool): True if it should use the command queue    
    def getPowerAutoRange(self, **kwargs):
        return self._getBool("power:range:auto", **kwargs)
    
    # Sets the max power
    # Value (float): The value of the max power
    # UseQueue (bool): True if it should use the command queue    
    def setPowerRange(self, Value, **kwargs):
        self._setFloat("power:range", Value, **kwargs)
    
    # Gets the max power setting
    # UseQueue (bool): True if it should use the command queue    
    def getPowerRange(self, **kwargs):
        return self._getFloat("power:range", **kwargs)
    
    # Sets the max frequency
    # Value (float): The value of the max frequency
    # UseQueue (bool): True if it should use the command queue    
    def setFrequencyRange(self, Value, **kwargs):
        self._setFloat("frequency:range", Value, **kwargs)
    
    # Gets the max frequency setting
    # UseQueue (bool): True if it should use the command queue    
    def getFrequencyRange(self, Value, **kwargs):
        return self._getFloat("frequency:range", **kwargs)
    
    # Gets a power measurement
    # UseQueue (bool): True if it should use the command queue    
    def getPower(self, **kwargs):
        return self._getFloat("measure:power", **kwargs)
