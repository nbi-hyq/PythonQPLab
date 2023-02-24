from .. import exceptions as e

# A generic powermeter class
class powermeter:
    # Sets the power auto range
    # Value (bool): True if auto range should be enabled
    def setPowerAutoRange(self, Value, **kwargs):
        raise e.ImplementationError("PM.setPowerAutoRange")

    # Enables power auto range
    def enablePowerAutoRange(self, **kwargs):
        self.setPowerAutoRange(True, **kwargs)
    
    # Disables power auto range
    def disablePowerAutoRange(self, **kwargs):
        self.setPowerAutoRange(False, **kwargs)
    
    # Gets the status of the power auto range
    def getPowerAutoRange(self):
        raise e.ImplementationError("PM.getPowerAutoRange")
    
    # Sets the max power
    # Value (float): The value of the max power
    def setPowerRange(self, Value):
        raise e.ImplementationError("PM.setPowerRange")
    
    # Gets the max power setting
    def getPowerRange(self):
        raise e.ImplementationError("PM.getPowerRange")
    
    # Sets the max frequency
    # Value (float): The value of the max frequency
    def setFrequencyRange(self, Value):
        raise e.ImplementationError("PM.setFrequencyRange")
    
    # Gets the max frequency setting
    def getFrequencyRange(self):
        raise e.ImplementationError("PM.getFrequencyRange")
    
    # Gets a power measurement
    def getPower(self):
        raise e.ImplementationError("PM.getPower")
        
    # Gets several power measurements
    # Count (int): The number of measurements to get
    # SleepTime (float): The time to sleep between each point
    def getPowerMulti(self, Count, SleepTime = 0, **kwargs):
        import numpy as np
        from .. import functions as f
        
        Count = int(Count)
        SleepTime = float(SleepTime)
        
        # Setup data
        Data = np.empty(Count, dtype = float)
        
        # Loop
        for i in range(Count - 1):
            Data[i] = self.getPower(**kwargs)
            
            # Wait
            f.time.sleep(SleepTime)
                
        Data[-1] = self.getPower(**kwargs)
        
        return Data
