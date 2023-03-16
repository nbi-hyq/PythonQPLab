from .. import exceptions as e
from ..equipment import device

# Allows for power control of a laser
class powerControl(device):
    # PID (controllers.powerPID): The PID to do the locking
    # Powermeter (controllers.powermeter): The powermeter used as reference
    # TimeBanditChannel (controllers.FPGAChannel) The FPGA channel used
    # DeviceName (st): The name of the device
    # PowerRangeFactor (float): How much higher than the locking power the powermeter should be peaking at
    # PowerTolerance (float): The maximum allowed relative error of the power
    # MinPowerTolerance (float): The minimum the tolerance can be
    # LockAttempts (int): The number of attempts to use locking
    # LockDelay (float): The time in seconds between each locking attempt
    # DeviceName (str): The name of the device
    # ID (str): The ID name for the device, only used for displaying infomation
    def __init__(self, PID, Powermeter, *args, TimeBanditChannel = None, PowerRangeFactor = 1.3, PowerTolerance = 0.01, MinPowerTolerance = 1e-9, LockAttempts = 20, LockDelay = 0.2, **kwargs):
        from .. import controllers
        from .. import interface
        
        # Make sure the types are correct
        if not isinstance(PID, controllers.powerPID):
            raise e.TypeDefError("PID", PID, controllers.powerPID)
            
        if not isinstance(Powermeter, interface.powermeter):
            raise e.TypeDefError("Powermeter", Powermeter, interface.powermeter)
            
        if TimeBanditChannel is not None and not isinstance(TimeBanditChannel, controllers.FPGAChannel):
            raise e.TypeDefError("TimeBanditChannel", TimeBanditChannel, controllers.FPGAChannel)

        if not "DeviceName" in kwargs:
            kwargs["DeviceName"] = "Power Control"
            
        # Init super
        super().__init__(*args, **kwargs)
        
        # Save the devices
        self.PID = PID
        self.powermeter = Powermeter
        self.timeBanditChannel = TimeBanditChannel
        
        # Save dettings
        self._powerRangeFactor = float(PowerRangeFactor)
        self._powerTolerance = float(PowerTolerance)
        self._minPowerTolerance = float(MinPowerTolerance)
        self._lockAttempts = int(LockAttempts)
        self._lockDelay = float(LockDelay)
        self._setPower = 0
        self.maxOutput = self.PID.maxOutput
        self.minOutput = self.PID.minOutput
        self.lock()
        
        # Initialize cache
        self.clearCache()
        
    # Start the PID
    # UseQueue (bool): Whether to run the command through the queue or not, ignored if the device was initialized with UseQueue = False
    def start(self, **kwargs):
        self.PID.start(**kwargs)
    
    # Stop the PID
    # UseQueue (bool): Whether to run the command through the queue or not, ignored if the device was initialized with UseQueue = False
    def stop(self, **kwargs):
        self.PID.stop(**kwargs)
        
    # Clear the cache
    def clearCache(self):
        self._cache = dict()
    
    # Set the setpoint of the PID
    # UseQueue (bool): Whether to run the command through the queue or not, ignored if the device was initialized with UseQueue = False
    def lock(self, **kwargs):
        import numpy as np
        from .. import functions as f
        
        Value = self._setPower
        
        # Disable autorange
        self.setAutoRange(False, **kwargs)
        
        # Set the power range
        self.setPowerRange(Value * self._powerRangeFactor, **kwargs)
        
        # Treat edge case of 0 power
        if Value == 0:
            self.setVoltageOut(0, **kwargs)
            return
        
        # Get the power range
        PowerRange = self.getPowerRange(**kwargs)
        
        # Start the PID
        self.start(**kwargs)
        
        # Set the slope
        Slope = (self.maxOutput - self.PID.getADCoffset(**kwargs)) / PowerRange
        
        # Set the initial setpoint
        if Value in self._cache:
            SetPoint = self._cache[Value]
        
        else:
            SetPoint = round(Value * Slope)
            
        # Attempt to lock
        for _ in range(self._lockAttempts):
            # Set the setpoint
            self.PID.setSetPoint(SetPoint, **kwargs)
            
            # Wait
            f.time.sleep(self._lockDelay)
            
            # Measure the power
            Power = self.getPower(**kwargs)
            
            # Check if it is locked
            if not np.isfinite(Power):
                SetPoint *= 0.9
                
            elif abs(Power - Value) / Value <= self._powerTolerance or abs(Power - Value) <= self._minPowerTolerance:
                # Save to cache
                self._cache[Value] = SetPoint
                return
            
            else:
                SetPoint += Slope * (Value - Power)
                
        # If it did not lock
        if self.getVoltageOut(**kwargs) == self.maxOutput:
            raise e.PowerRangeError(f"AOM {self.deviceName}", self)
        
        else:
            raise e.LockError(f"AOM {self.deviceName}", self)
    
    # Turns the PID off
    # UseQueue (bool): Whether to run the command through the queue or not, ignored if the device was initialized with UseQueue = False
    def off(self, **kwargs):
        self.stop(**kwargs)
        self.setVoltageOut(0, **kwargs)
        
    # Sets the setpoint of the PID, it must also be locked afterwards
    # Power (float): The power to set
    def setSetPower(self, Power):
        self._setPower = float(Power)
    
    # Get the setpoint of the PID
    def getSetPower(self):
        return self._setPower
    
    # Sets the power
    # Power (float): The power to set
    # UseQueue (bool): Whether to run the command through the queue or not, ignored if the device was initialized with UseQueue = False
    def setPower(self, Power, **kwargs):
        self.setSetPower(Power)
        self.lock(**kwargs)
    
    # Get the current power
    # UseQueue (bool): Whether to run the command through the queue or not, ignored if the device was initialized with UseQueue = False
    def getPower(self, **kwargs):
        return self.powermeter.getPower(**kwargs)
    
    # Gets several power measurements
    # Count (int): The number of measurements to get
    # SleepTime (float): The time to sleep between each point
    # UseQueue (bool): Whether to run the command through the queue or not, ignored if the device was initialized with UseQueue = False
    def getPowerMulti(self, Count, SleepTime = 0, **kwargs):
        return self.powermeter.getPowerMulti(Count, SleepTime = SleepTime, **kwargs)
    
    # Sets the output voltage
    # Value (float): The voltage to set
    # UseQueue (bool): Whether to run the command through the queue or not, ignored if the device was initialized with UseQueue = False
    def setVoltageOut(self, Value, **kwargs):
        self.PID.setOutputSignal(Value, **kwargs)
    
    # Gets the output voltage
    # UseQueue (bool): Whether to run the command through the queue or not, ignored if the device was initialized with UseQueue = False
    def getVoltageOut(self, **kwargs):
        return self.PID.getOutputSignal(**kwargs)
    
    # Check if the PID is locking
    # UseQueue (bool): Whether to run the command through the queue or not, ignored if the device was initialized with UseQueue = False
    def isLocked(self, **kwargs):
        import numpy as np
        
        # Get power
        Power = self.getPower(**kwargs)
        
        # Check if it is finite
        if not np.isfinite(Power):
            return False
        
        # Check special case of no power
        if self._setPower == 0:
            return abs(Power) <= self._minPowerTolerance
        
        # Check other cases
        return abs(self._setPower - Power) / self._setPower <= self._powerTolerance or abs(self._setPower - Power) <= self._minPowerTolerance
    
    # Check if the power is locked
    # UseQueue (bool): Whether to run the command through the queue or not, ignored if the device was initialized with UseQueue = False
    def isLocking(self, **kwargs):
        return self.PID.status(**kwargs) == "ON"
    
    # Sets the status of auto range
    # Value (bool): True to turn auto range on
    # UseQueue (bool): Whether to run the command through the queue or not, ignored if the device was initialized with UseQueue = False
    def setAutoRange(self, Value, **kwargs):
        self.powermeter.setPowerAutoRange(Value, **kwargs)
    
    # Gets the status of auto range
    # UseQueue (bool): Whether to run the command through the queue or not, ignored if the device was initialized with UseQueue = False
    def getAutoRange(self, **kwargs):
        return self.powermeter.getPowerAutoRange(**kwargs)
    
    # Sets the power range
    # Value (float): The maximum power
    # UseQueue (bool): Whether to run the command through the queue or not, ignored if the device was initialized with UseQueue = False
    def setPowerRange(self, Value, **kwargs):
        self.powermeter.setPowerRange(Value, **kwargs)
    
    # Gets the power range
    # UseQueue (bool): Whether to run the command through the queue or not, ignored if the device was initialized with UseQueue = False
    def getPowerRange(self, **kwargs):
        return self.powermeter.getPowerRange(**kwargs)
