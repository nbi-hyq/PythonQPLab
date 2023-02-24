from .. import exceptions as e
from ..equipment import device

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
        from .. import controllers
        
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
        from .. import functions as f
        
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
        from .. import functions as f

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
    