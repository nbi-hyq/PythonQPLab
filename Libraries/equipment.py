import exceptions as e
import controllers as c
import functions as f

# The default equipment class
class device(object):
    # DeviceName (str): The name of the device
    # ID (str): The ID name for the device, only used for displaying infomation
    def __init__(self, *args, DeviceName = "Device", ID = None, **kwargs):
        import weakref
        
        super().__init__(*args, **kwargs)
        
        # Set the device name
        self.deviceName = str(DeviceName)
        self._isOpen = True
        
        if ID is not None:
            self.deviceName = f"{self.deviceName} {str(ID)}"
            
        weakref.finalize(self, self.close)
        
    # Checks if the device is open, may be overwritten by the sub class if it can be closed
    # Returns True if it is open
    def isOpen(self):
        return self._isOpen
        
    # Close the device, the method _close must be overwritten by the device
    def close(self):
        if self.isOpen():
            self._close()
            
        self._isOpen = False
        
    # Does the actual closing of the device
    def _close(self):
        pass


# Combines a laser with a wavementer to make locking possible
class laser(device):
    # Laser (controllers.laser): The laser to control
    # Wavemeter (controllers.WM): The wavemeter to read the frequency from
    # Redshift (float): The redshift of the laser due to AOM
    # LockInterval (float): The time in seconds between each locking attempt
    # LockWait (float): The time in seconds to wait when locking and using grating
    # LockTolerance (float): The tolerance of the error of the frequency in THz
    # LockSlope (float): Starting guess for the voltage over frequency for locking, this will be overwritten quite fast
    # LockSlopeRange (2-tuple of float): The minimum and maximum allowed slopes
    # PiezoAttempts (int): The number of attempts to stabalize using piezo, after this it will use grating
    # JumpAttempts (int): The number of attempts to use grating to stabilize the frequency
    # DeviceName (str): The name of the device
    # ID (str): The ID name for the device, only used for displaying infomation
    def __init__(self, Laser, Wavemeter, *args, Redshift = 0, LockInterval = 0.2, LockWait = 0.1, LockTolerance = 10e-6, LockSlope = 3804, LockSlopeRange = (2000, 4000), PiezoAttempts = 100, JumpAttempts = 4, **kwargs):
        import controllers
        
        # Make sure types are correct
        if not isinstance(Laser, controllers.laser):
            raise e.TypeDefError("Laser", Laser, controllers.laser)
            
        if not isinstance(Wavemeter, controllers.WM):
            raise e.TypeDefError("Wavemeter", Wavemeter, controllers.WM)
            
        if not "DeviceName" in kwargs:
            kwargs["DeviceName"] = "Laser"
            
        # Initialize super
        super().__init__(*args, **kwargs)
                
        # Save everything
        self.laser = Laser
        self.wm = Wavemeter
        self._lockFrequency = 0
        self._lockInterval = float(LockInterval)
        self._lockWait = float(LockWait)
        self._lockTolerance = float(LockTolerance)
        self._lockSlope = float(LockSlope)
        self._lockSlopeRange = (float(LockSlopeRange[0]), float(LockSlopeRange[1]))
        self._piezoAttempts = int(PiezoAttempts)
        self._jumpAttempts = int(JumpAttempts)
        self._lockTimer = None
        self._redshift = float(Redshift)
        
    # Sets the frequency to lock at
    # Value (float): The frequency to lock at    
    def setLockFrequency(self, Value):
        # Make sure it is within the range
        if not self.laser.frequencyAllowed(Value):
            raise e.RangeError("Lock frequency", Value, self.laser._frequencyRange[0], self.laser._frequencyRange[1])
            
        self._lockFrequency = float(Value)
        
    # Sets lock frequency and returns once it is locked
    # Value (float): The frequency to lock at    
    # UseQueue (bool): Whether to run the command through the queue or not, ignored if the device was initialized with UseQueue = False
    def setLockFrequencyPersistent(self, Value, **kwargs):        
        # Make sure it is locking
        if not self.isLocking():
            raise e.MethodError("Laser", self, "setLockFrequencyPersistent")
            
        self.setLockFrequency(Value)
        
        while not self.isLocked(**kwargs):
            f.time.sleep(self._lockInterval)
    
    # Get the frequency locking at
    def getLockFrequency(self):
        return self._lockFrequency
    
    # Checks if the laser is locked
    # UseQueue (bool): Whether to run the command through the queue or not, ignored if the device was initialized with UseQueue = False
    def isLocked(self, **kwargs):
        return abs(self._lockFrequency - self.getFrequency(**kwargs)) <= self._lockTolerance
        
    # Set the frequency of the laser
    # Value (float): The frequency to set
    # UseQueue (bool): Whether to run the command through the queue or not, ignored if the device was initialized with UseQueue = False
    def setLaserFrequency(self, Value, **kwargs):
        # Set piezo
        self.laser.setVoltage(self.laser.voltageBase)
        
        # Set laser frequency
        self.laser.setFrequency(Value, **kwargs)
    
    # Get the frequency from the laser
    # UseQueue (bool): Whether to run the command through the queue or not, ignored if the device was initialized with UseQueue = False
    def getLaserFrequency(self, **kwargs):
        return self.laser.getFrequency(**kwargs)
    
    # Set the frequency compensated using wavemeter
    # Value (float): The frequency to set
    # UseQueue (bool): Whether to run the command through the queue or not, ignored if the device was initialized with UseQueue = False
    def setFrequency(self, Value, **kwargs):
        # Get frequencies
        TrueFrequency = self.getFrequency(**kwargs)
        LaserFrequency = self.getLaserFrequency(**kwargs)
        
        # Set correct frequency
        self.setLaserFrequency(LaserFrequency + float(Value) - TrueFrequency, **kwargs)
    
    # Get the frequency from the wavemeter
    # UseQueue (bool): Whether to run the command through the queue or not, ignored if the device was initialized with UseQueue = False
    def getFrequency(self, **kwargs):
        # Make sure the channel is None
        kwargs["Channel"] = None
        
        return self.wm.getFrequency(**kwargs) - self._redshift
    
    # Reset the exposure time of the wavemeter
    # UseQueue (bool): Whether to run the command through the queue or not, ignored if the device was initialized with UseQueue = False
    def resetWM(self, **kwargs):
        # Make sure the channel is None
        kwargs["Channel"] = None
        
        return self.wm.resetExposure(**kwargs)
    
    # Attempts to compensate for drifts of the frequency
    # Count: The counter in the timer
    # UseQueue (bool): Whether to run the command through the queue or not, ignored if the device was initialized with UseQueue = False
    def _lockFunction(self, Count, **kwargs):            
        # Go through jump loop
        Stable = False
        
        for i in range(self._jumpAttempts + 1):            
            # Check if it is good
            DiffFrequency = self._lockFrequency - self.getFrequency(**kwargs)
            
            if abs(DiffFrequency) < self._lockTolerance:
                Stable = True
                break
            
            # Try with piezo
            for _ in range(self._piezoAttempts):
                # Make sure the slope is valid
                if self._lockSlope < self._lockSlopeRange[0] or self._lockSlope > self._lockSlopeRange[1]:
                    self._lockSlope = (self._lockSlopeRange[0] + self._lockSlopeRange[1]) / 2
                
                # Find the new voltage
                DiffVoltage = DiffFrequency * self._lockSlope
                NewVoltage = self.laser.getVoltage() + DiffVoltage
                
                # Make sure it is legal
                if not self.laser.voltageAllowed(NewVoltage):
                    print(f"Requested illigal voltage of {NewVoltage:.1f}, using grating to compensate for drift of {self.deviceName}")
                    break
                
                # Set new voltage
                self.laser.setVoltage(NewVoltage)
                
                # Wait
                f.time.sleep(self._lockWait)
                
                # Get the new frequency
                NewDiffFrequency = self.getFrequency(**kwargs) - (self._lockFrequency - DiffFrequency)
            
                # Calculate new slope
                if NewDiffFrequency != 0:
                    self._lockSlope = DiffVoltage / NewDiffFrequency
                    
                else:
                    self._lockSlope = (self._lockSlopeRange[0] + self._lockSlopeRange[1]) / 2
                
                # Find the true frequency difference and check if it has been set correctly
                DiffFrequency = self._lockFrequency - (NewDiffFrequency + (self._lockFrequency - DiffFrequency))
            
                if abs(DiffFrequency) < self._lockTolerance:
                    Stable = True
                    break
            
            if Stable:
                break
            
            # Set the frequency
            if i < self._jumpAttempts:
                print(f"Using grating to compensate for drift for {self.deviceName}")
                self.setFrequency(self._lockFrequency, **kwargs)
            
        # Tell if it did not work
        if not Stable:
            print(f"Unable to lock {self.deviceName}")
    
    # Locks the frequency
    # UseQueue (bool): Whether to run the command through the queue or not, ignored if the device was initialized with UseQueue = False
    def lock(self, **kwargs):
        import connections
        
        # Unlock if needed
        self.unlock()
        
        # Get lock frequency if not given
        if self._lockFrequency == 0:
            self._lockFrequency = self.getFrequency(**kwargs)
            
        # Start a timer
        self._lockTimer = connections.timer(self._lockInterval, self._lockFunction, TimerKwargs = kwargs)
        self._lockTimer.start()
    
    # Check if it is locked
    def isLocking(self):
        return (self._lockTimer is not None)
    
    # Unlocks the frequency
    def unlock(self):
        # Make sure it is locked
        if self.isLocking():
            # Stop time timer
            self._lockTimer.stop()
            
            # Overwrite it
            self._lockTimer = None
            
    def _close(self):
        self.unlock()
        
        super()._close()
    
    
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
    def __init__(self, PID, Powermeter, TimeBanditChannel, *args, PowerRangeFactor = 1.3, PowerTolerance = 0.01, MinPowerTolerance = 1e-9, LockAttempts = 20, LockDelay = 0.2, **kwargs):
        import controllers
        
        # Make sure the types are correct
        if not isinstance(PID, controllers.powerPID):
            raise e.TypeDefError("PID", PID, controllers.powerPID)
            
        if not isinstance(Powermeter, controllers.powermeter):
            raise e.TypeDefError("Powermeter", Powermeter, controllers.powermeter)
            
        if not isinstance(TimeBanditChannel, controllers.FPGAChannel):
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


# The controller for a power controlled laser
class powerControlledLaser(device):
    # Laser (laser): The laser to control
    # PowerControl (powerControl) The power control of the laser
    # DeviceName (str): The name of the device
    # ID (str): The ID name for the device, only used for displaying infomation
    def __init__(self, Laser, PowerControl, *args, **kwargs):
        # Make sure the types are correct
        if not isinstance(Laser, laser):
            raise e.TypeDefError("Laser", Laser, laser)

        if not isinstance(PowerControl, powerControl):
            raise e.TypeDefError("PowerControl", PowerControl, powerControl)

        if not "DeviceName" in kwargs:
            kwargs["DeviceName"] = "Power Controlled Laser"

        super().__init__(*args, **kwargs)
        
        # Save the laser and power control
        self.laser = Laser
        self.power = PowerControl
        

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
        

# Controls a PTC10 PID and implements logging for it        
class PTC10(PID):
    # Device (controllers.PID): The PID to control
    # WhiteSpaceIn (float): Defines the default white space for the input when plotting
    # WhiteSpaceOut (float): Defines the default white space for the output when plotting    
    # DeviceName (str): The name of the device
    # ID (str): The ID name for the device, only used for displaying infomation
    def __init__(self, Device, *args, **kwargs):
        import controllers as c
        
        if not isinstance(Device, c.PTC10):
            raise e.TypeDefError("PTC10", Device, c.PTC10)
            
        if not "DeviceName" in kwargs:
            kwargs["DeviceName"] = "PTC10"
            
        super().__init__(Device, *args, **kwargs)
        
    # Retrieves the PID data for the logger: SignalIn, SetPoint, SignalOut
    # Name (str): The name of the PID to retrieve data from
    def logDataRetriever(self, Name = None):
        Current = self.device.getCurrent(Name = Name)
        Temp = self.device.getTemp(Name = Name)
        SetPoint = self.device.getSetPoint(Name = Name)
        
        return Temp, SetPoint, Current
    
    # Logs the PID and does live plotting
    # File (str): The file path for where to save the log
    # PIDName (str): The name of the PID to log, if None it will use the default which may change mid logging
    # MaxTime (float): The time in seconds to run the logging, 0 for infinity, must not be negative
    # Period (floar): The time in seconds between each measurement, must not be negative
    # MaxShow (int): The maximum number of data points to show at once, must be positive
    # Name (str): The name to display on the figures
    # figsize (tuple): A tuple of ints define the size of the figure
    # Plot (bool): If True then do live plotting
    # KeepFigure (bool): If False then it closes the live plotting when done
    # Wait (bool): If True then it will wait for the log to finish, if False then it will return immidiatly and return the stop event for the log for which to do .set() to stop the log
    def log(self, *args, PIDName = None, **kwargs):
        if not "Name" in kwargs:
            kwargs["Name"] = "PTC10"

        kwargs["DataKwargs"] = {"Name": PIDName}

        super().log(*args, **kwargs)


# Controls a tempArduino PID and implements logging for it        
class tempArduino(PID):
    # Device (controllers.PID): The PID to control
    # WhiteSpaceIn (float): Defines the default white space for the input when plotting
    # WhiteSpaceOut (float): Defines the default white space for the output when plotting    
    # DeviceName (str): The name of the device
    # ID (str): The ID name for the device, only used for displaying infomation
    def __init__(self, Device, *args, **kwargs):
        import controllers as c

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
            

# A generic rotation stage
class rotationStage(device, c.rotationStage):
    # Device (controllers.rotationStage): The rotation stage device
    # ZeroPos (float): The real position when the device is at position 0
    # DeviceName (str): The name of the device
    # ID (str): The ID name for the device, only used for displaying infomation
    def __init__(self, Device, *args, ZeroPos = 0, **kwargs):
        import controllers as c
        
        if not "DeviceName" in kwargs:
            kwargs["DeviceName"] = "Rotation Stage"
        
        super().__init__(*args, **kwargs)
        
        if not isinstance(Device, c.rotationStage):
            raise e.TypeDefError("Device", Device, c.rotationStage)
        
        # Save the device
        self.device = Device
        self._zeroPos = float(ZeroPos)
        
    # Homes the device     
    # UseQueue (bool): Whether to run the command through the queue or not, ignored if the device was initialized with UseQueue = False
    def home(self, **kwargs):
        self.device.home(**kwargs)
    
    # Moves the device to a specified position
    # Position (float): The position to set
    # UseQueue (bool): Whether to run the command through the queue or not, ignored if the device was initialized with UseQueue = False
    def moveTo(self, Position, **kwargs):
        self.device.moveTo(float(Position) - self._zeroPos, **kwargs)
    
    # Gets the current position of the rotation stage
    # UseQueue (bool): Whether to run the command through the queue or not, ignored if the device was initialized with UseQueue = False
    def getPosition(self, **kwargs):
        return self.device.getPosition(**kwargs) - self._zeroPos
    
    # Moves the rotation stage relative to its original position
    # Distance (float): The distance it should move by
    # UseQueue (bool): Whether to run the command through the queue or not, ignored if the device was initialized with UseQueue = False
    def move(self, Distance, **kwargs):
        self.device.move(Distance, **kwargs)
        
    # Sets the zero angle for this device
    # Value (float): The value for the zero angle
    def setZero(self, Value):
        self._zeroPos = float(Value)
        
    # Gets the zero angle for this device
    def getZero(self):
        return self._zeroPos
    
# A minimizer for the EOM
class EOM(device):
    # PowerControl (powerControl): The power control unit connected to the EOM
    # TimeTagger (controllers.timeTagger): The time tagger object
    # DACController (controllers.DAC): The DAC object
    # DACChannel (int): The DAC channel
    # VoltageGuess (float): The initial guess for the optimal voltage
    # ScanRange (float): The range of each voltage scan
    # ScanPoints (int): The number of measurement points in each scan
    # IntegrationTime (float): The integration time per point
    # MaxAttempts (int): The maximum number of attempts to minimize the EOM
    # Gate (2-tuple of float): The gate for use to get time tagger counts
    # InitialPause (float): The time to pause at the beginning of each tagger scan
    # RepetitionCount (int): The number of measurement points to get for each powermeter measurement
    # ScanPause (float): The time to pause between each measurement in a scan
    # Figsize (dict): The size of the figure
    # ShowBuffer (float): The white space buffer in the plot in percentage
    # DeviceName (str): The name of the device
    # ID (str): The ID name for the device, only used for displaying infomation
    def __init__(self, PowerControl, TimeTagger, DACController, DACChannel, *args, VoltageGuess = 3.4, ScanRange = 4 / 5, ScanPoints = 20, IntegrationTime = 0.1, RepetitionCount = 5, MaxAttempts = 100, Gate = None, InitialPause = 0.3, ScanPause = 0.1, Figsize = (8, 8), ShowBuffer = 0.1, **kwargs):
        import controllers as c
        import plotting
        
        if not "DeviceName" in kwargs:
            kwargs["DeviceName"] = "EOM"
            
        super().__init__(*args, **kwargs)
        
        if not isinstance(PowerControl, powerControl):
            raise e.TypeDefError("Powermeter", PowerControl, powerControl)

        if not isinstance(TimeTagger, c.timeTagger):
            raise e.TypeDefError("TimeTagger", TimeTagger, c.timeTagger)
            
        if not isinstance(DACController, c.DAC):
            raise e.TypeDefError("DACController", DACController, c.DAC)
            
        self._powerControl = PowerControl
        self._timeTagger = TimeTagger
        self._timeTaggerChannel = 1
        self._DAC = DACController
        self._channel = int(DACChannel)
        
        # Setup figure
        self._maxAttempts = int(MaxAttempts)
        self._voltageGuess = float(VoltageGuess)
        self._scanRange = float(ScanRange)
        self._scanPoints = int(ScanPoints)
        self._intTime = float(IntegrationTime)
        self._repCount = int(RepetitionCount)
        self._initPause = float(InitialPause)
        self._scanPause = float(ScanPause)
        self._gate = Gate
        
        self._plot = plotting.plot(self._scanPoints, 1, "o", Colors = "blue", Labels = "Data", Figsize = Figsize, Titles = "Minimizing EOM power", xLabels = "Voltage", yLabels = "Power", ShowBuffers = ShowBuffer)
        
    def _close(self):
        if self._plot is not None:
            self._plot.close()
            
        super()._close()
        
    # Sets the voltage for the EOM
    # Voltage (float): The voltage to set
    # UseQueue (bool): Whether to run the command through the queue or not, ignored if the device was initialized with UseQueue = False
    def setVoltage(self, Voltage, **kwargs):
        self._DAC.setVoltage(Voltage, self._channel, **kwargs)
            
    # Minimize the laser through the EOM
    # MeasureFunc (callable): The function to measure the power
    # InitFunc (callable): The function to run before starting
    # ExitFunc (callable): The function to run after it is done
    # UseQueue (bool): Whether to run the command through the queue or not, ignored if the device was initialized with UseQueue = False
    def minimize(self, MeasureFunc, InitFunc = None, ExitFunc = None, **kwargs):
        import numpy as np
        import plotting
                
        # Run initialization function
        if InitFunc is not None:
            InitFunc(**kwargs)
            
        # Set state to DC
        TimeBanditState = self._powerControl.timeBanditChannel.getState()
        self._powerControl.timeBanditChannel.setDC(**kwargs)
                
        # Start minimizing
        Success = False
        BestVoltage = self._voltageGuess
        
        for _ in range(self._maxAttempts):
            # Start plotting
            self._plot.reset()

            # Get the voltages to scan
            VoltageList = np.linspace(BestVoltage - self._scanRange / 2, BestVoltage + self._scanRange / 2, self._scanPoints)

            # Create array for measurements
            PowerDataMean = np.empty(self._scanPoints, dtype = float)
            PowerDataStd = np.empty(self._scanPoints, dtype = float)
            
            # Go to starting voltage and wait
            self.setVoltage(VoltageList[0], **kwargs)
            f.time.sleep(self._initPause)
            
            # Get measurements
            for i, Voltage in enumerate(VoltageList):
                # Set voltage and pause
                self._DAC.setVoltage(Voltage, self._channel, **kwargs)
                f.time.sleep(self._scanPause)
                
                # Measure
                PowerDataMean[i], PowerDataStd[i] = MeasureFunc(**kwargs)

                # Plot it
                self._plot.update(Voltage, PowerDataMean[i])
                            
            # Create voltage matrix
            PolyVar = np.polyfit(VoltageList, PowerDataMean, 2, w = 1 / PowerDataStd)
            NewBestVoltage = -PolyVar[1] / (2 * PolyVar[0])

            # Plot it
            x = np.linspace(np.min(VoltageList), np.max(VoltageList), 1000)
            self._plot.axes[0].plot(x, PolyVar[2] + PolyVar[1] * x + PolyVar[0] * x ** 2, "-", color = "Red", label = "Fit")
            plotting.livePlot.update(self._plot)
            
            # Determine if it was good enough
            OldBestVoltage = BestVoltage
            BestVoltage = NewBestVoltage
            
            if abs(BestVoltage - OldBestVoltage) < self._scanRange / 4:
                Success = True
                break
            
        # Run exit function
        if ExitFunc is not None:
            ExitFunc(**kwargs)
            
        # Set time bandit state back
        self._powerControl.timeBanditChannel.applyState(TimeBanditState)
        
        # Make sure that is has been minimized
        if not Success:
            raise e.MinimizeError(self.deviceName, self)
            
        # Set best voltage
        self._DAC.setVoltage(BestVoltage, self._channel, **kwargs)
            
        # Update guess
        self._voltageGuess = BestVoltage
        
        return BestVoltage 
    
    # Initialization function for power minimization
    # UseQueue (bool): Whether to run the command through the queue or not, ignored if the device was initialized with UseQueue = False
    def _powerInit(self, **kwargs):
        # Get old data
        self._locking = self._powerControl.isLocking(**kwargs)
        
        if self._locking:
            self._lockPower = self._powerControl.getSetPower()
            
        else:
            self._oldSetPoint = self._powerControl.PID.getSetPoint(**kwargs)
            
        # Stop PID
        self._powerControl.stop(**kwargs)
        self._powerControl.setAutoRange(True, **kwargs)
        
    # Finalizer function for power minimization
    # UseQueue (bool): Whether to run the command through the queue or not, ignored if the device was initialized with UseQueue = False
    def _powerExit(self, **kwargs):
        # Start PID
        if self._locking:
            self._powerControl.setPower(self._lockPower, **kwargs)
            
        else:
            self._powerControl.PID.setSetPoint(self._oldSetPoint, **kwargs)
        
    # Measure function for power minimization
    # UseQueue (bool): Whether to run the command through the queue or not, ignored if the device was initialized with UseQueue = False
    def _powerMeasure(self, **kwargs):
        import numpy as np
        
        Power = self._powerControl.getPowerMulti(self._repCount)
        Filter = np.isfinite(Power)
        Power = Power[Filter]
        return np.mean(Power), np.std(Power, ddof = 1)
        
    # Minimize the power of a power meter
    # UseQueue (bool): Whether to run the command through the queue or not, ignored if the device was initialized with UseQueue = False
    def minimizePower(self, **kwargs):
        return self.minimize(self._powerMeasure, InitFunc = self._powerInit, ExitFunc = self._powerExit, **kwargs)
    
    # Measure function for power minimization
    # UseQueue (bool): Whether to run the command through the queue or not, ignored if the device was initialized with UseQueue = False
    def _countsMeasure(self, **kwargs):
        import numpy as np
        
        Counts = self._timeTagger.getGatedCount(Channel = self._timeTaggerChannel, IntegrationTime = self._intTime, Gates = self._gate, **kwargs)
        return float(Counts), np.sqrt(float(Counts))
    
    # Minimize the counts of a time tagger
    # Channel (int): The channel to get data from
    # UseQueue (bool): Whether to run the command through the queue or not, ignored if the device was initialized with UseQueue = False
    def minimizeCounts(self, Channel, **kwargs):
        self._timeTaggerChannel = int(Channel)
        return self.minimize(self._countsMeasure, **kwargs)
    

# Adds plotting to the time bandit
class timeBandit(device):
    # FPGA (controllers.timeBandit): The FPGA to control
    # Figsize (2-tuple of int): The size of the figure to plot the sequences on
    # DeviceName (str): The name of the device
    # ID (str): The ID name for the device, only used for displaying infomation
    def __init__(self, FPGA, *args, Figsize = (8, 4), **kwargs):
        import plotting as pl

        if not "DeviceName" in kwargs:
            kwargs["DeviceName"] = "TimeBandit"
        
        super().__init__(*args, **kwargs)
        
        if not isinstance(FPGA, c.timeBandit):
            raise e.TypeDefError("FPGA", FPGA, c.timeBandit)
        
        # Save the FPGA
        self.FPGA = FPGA
        
        # Setup plotting
        ChannelCount = len(FPGA.CH)
        Labels = [f"CH {i + 1}" for i in range(ChannelCount)]
        Shapes = ["-"] * ChannelCount
        
        self._plot = pl.renewPlot(1, Shapes, Labels = Labels, Figsize = Figsize, Titles = "TimeBandit sequence", xLabels = "Time (ns)", yLabels = "Voltage")
        
    def _close(self):
        self._plot.close()
        super()._close()
        
    # Shows the sequences
    def show(self):
        import numpy as np
        import math
        
        # Get clock division
        ClockDivision = 1
        
        for Channel in self.FPGA.CH:
            ClockDivision *= Channel.clockPartition // math.gcd(ClockDivision, Channel.clockPartition)
        
        # Get the x values
        Length = self.FPGA.getSequenceLength() * self.FPGA.getClocksPerBase() * ClockDivision
        x = np.arange(Length, dtype = float) / (self.FPGA.getClockFrequency() * self.FPGA.getClocksPerBase() * ClockDivision)
        
        # Go through each channel and get the sequence
        Values = [None] * len(self.FPGA.CH)
        
        for i, Channel in enumerate(self.FPGA.CH):
            # Get the state and partition
            State = Channel.getState()
            Partition = Channel.clockPartition
            Multiplier = ClockDivision // Partition
            
            # Set off
            Values[i] = np.zeros_like(x)
            if State == "off":
                pass
                
            elif State == "dc":
                Values[i][:] = 1
                
            else:
                for Pulse in State:
                    if Pulse is None:
                        continue
                    
                    Start, Stop = Pulse
                    Start = int(Start * Partition) % (Length * Partition // ClockDivision)
                    Stop = int(Stop * Partition) % (Length * Partition // ClockDivision)
                    
                    if Start >= Stop:
                        Values[i][Start * Multiplier:] = 1
                        Values[i][:(Stop - 1) * Multiplier] = 1
                        
                    else:
                        Values[i][Start * Multiplier:(Stop - 1) * Multiplier] = 1
                        
        # Plot it
        self._plot.update(x, Values)
    
    
# Adds plotting to the AWG
class AWG(device):
    # Device (controllers.AWG): The AWG to control
    # Figsize (2-tuple of int): The size of the figure to plot the sequences on
    # DeviceName (str): The name of the device
    # ID (str): The ID name for the device, only used for displaying infomation
    def __init__(self, Device, *args, Figsize = (8, 4), **kwargs):
        import plotting as pl

        if not "DeviceName" in kwargs:
            kwargs["DeviceName"] = "AWG"
        
        super().__init__(*args, **kwargs)
        
        if not isinstance(Device, c.AWG):
            raise e.TypeDefError("Device", Device, c.AWG)
        
        # Save the FPGA
        self.device = Device
        
        # Setup plotting
        ChannelCount = Device.channelCount
        Labels = [f"CH {i + 1}" for i in range(ChannelCount)]
        Shapes = ["-"] * ChannelCount
        
        self._plotAmplitude = pl.renewPlot(1, Shapes, Labels = Labels, Figsize = Figsize, Titles = "AWG sequence amplitude", xLabels = "Time (ns)", yLabels = "Amplitude")
        self._plotPhase = pl.renewPlot(1, Shapes, Labels = Labels, Figsize = Figsize, Titles = "AWG sequence phase", xLabels = "Time (ns)", yLabels = "Phase")
        
    def _close(self):
        self._plot.close()
        super()._close()
        
    # Shows the sequences
    def show(self):
        import numpy as np
        
        # If nothing is active
        if self.device.currentSequence is None:
            x = np.array([0, 1], dtype = float)
            Values = [np.array([0, 0], dtype = float)] * self.device.channelCount
            PhaseValue = [np.array([0, 0], dtype = float)] * self.device.channelCount
            
        else:
            # Get the sequences
            Sequence = self.device.sequences[self.device.currentSequence]
            
            # Get the length
            Length = Sequence.entryCount * Sequence.length
            
            x = np.arange(Length, dtype = float) / Sequence.sampleFreq
            
            Values = [None] * Sequence.channelCount
            PhaseValues = [None] * Sequence.channelCount
            
            for i in range(Sequence.channelCount):
                Values[i] = np.empty(Length)
                PhaseValues[i] = np.zeros(Length)
                
                # Fill the values
                for j in range(Sequence.entryCount):
                    if Sequence.mode == "BB":
                        Values[i][Sequence.length * j: Sequence.length * (j + 1)] = Sequence.sequences[j][i].waveform
                        
                    else:
                        A, P = Sequence.fromIQ(Sequence.sequences[j][i][0].waveform, Sequence.sequences[j][i][1].waveform)
                        
                        Values[i][Sequence.length * j: Sequence.length * (j + 1)] = A
                        PhaseValues[i][Sequence.length * j: Sequence.length * (j + 1)] = P                      
                        
        self._plotAmplitude.update(x, Values)
        self._plotPhase.update(x, PhaseValue)
            