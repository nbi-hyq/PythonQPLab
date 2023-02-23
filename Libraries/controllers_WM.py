import connections as c

# Controller for a wavemeter
class WM(c.dll):
    # DLLPath (str): The path to the dll to load
    # Channel (int): The default channel to use, can be set with the setChannel method
    # UseQueue (bool): If True then it will set up a queue which can be used in the sendCommand method, if False the UseQueue in sendCommand is ignored
    # Empty (bool): If True then it will not communicate with the device
    # DeviceName (str): The name of the device, only used for error messages
    # ID (str): The ID name for the device, only used for displaying infomation
    def __init__(self, *args, Channel = 1, **kwargs):
        import ctypes as c
        
        # Get the name
        if not "DeviceName" in kwargs:
            kwargs["DeviceName"] = "Wavelength Meter"
            
        # Initialize
        super().__init__(*args, **kwargs)
        
        # Set the channel
        self.setChannel(Channel)
        
        # Add header for used functions
        self.setupFunction("SetActiveChannel", c.c_long, [c.c_long, c.c_long, c.c_long, c.c_long])
        self.setupFunction("GetWavelengthNum", c.c_double, [c.c_long, c.c_double])
        self.setupFunction("GetFrequencyNum", c.c_double, [c.c_long, c.c_double])
        self.setupFunction("SetExposureNum", c.c_long, [c.c_long, c.c_long, c.c_long])

    # Runs a channel dependent function
    # Name (str): The name of the function
    # Args (set): The arguments to pass the function
    # UseQueue (bool): True if it should use the command queue
    # Channel (int): The channel to access, if None then it will use the default
    def _runChannelFunction(self, Name, Args = set(), Channel = None, **kwargs):
        if Channel is None:
            Channel = self._channel

        Args = (Channel,) + tuple(Args)
        
        self.runFunction("SetActiveChannel", Args = (1, 1, Channel, 0), **kwargs)
        return self.runFunction(Name, Args = Args, **kwargs)

    # Gets the wavelength from the device
    # UseQueue (bool): True if it should use the command queue
    # Channel (int): The channel to access, if None then it will use the default
    def getWavelength(self, **kwargs):
        return self._runChannelFunction("GetWavelengthNum", Args = (0,), **kwargs)
    
    # Gets the frequency from the device
    # UseQueue (bool): True if it should use the command queue
    # Channel (int): The channel to access, if None then it will use the default
    def getFrequency(self, **kwargs):
        return self._runChannelFunction("GetFrequencyNum", Args = (0,), **kwargs)
    
    # Sets the exposure time
    # Value (int): The value to set the exposure to
    # Index (int): The index of the exposure (0 or 1)
    # UseQueue (bool): True if it should use the command queue
    # Channel (int): The channel to access, if None then it will use the default
    def setExposure(self, Value, Index, **kwargs):
        self._runChannelFunction("SetExposureNum", Args = (Index, Value), **kwargs)
    
    # Resets the exposure time
    # UseQueue (bool): True if it should use the command queue
    # Channel (int): The channel to access, if None then it will use the default
    def resetExposure(self, **kwargs):
        self.setExposure(1, 1, **kwargs)
        self.setExposure(0, 2, **kwargs)
    
    # Sets the default channel to use
    # Channel (int): The channel to use
    def setChannel(self, Channel):
        self._channel = int(Channel)
