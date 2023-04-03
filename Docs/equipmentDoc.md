# Documentation for equipment

This is a collection of classes for the lab equipment, they consist of a collection of devices with added functionality like locking and plotting

---
---

# Classes

---

## device(DeviceName = "Device", ID = None)

The default equipment class

- DeviceName (str): The name of the device
- ID (str): The ID name for the device, only used for displaying infomation

---

### method close()

Closes the device, the _close method should be overwritten to implement own closing, remember super()._close()

---

### method isOpen()

Returns True if the device has not been closed, False otherwise

---

### property deviceName (str)

The name of the device

---
---

## laser(Laser, Wavemeter, LockInterval = 0.2, LockWait = 0.1, LockTolerance = 10e-6, LockSlope = 3804, LockSlopeRange = (2000, 4000), PiezoAttempts = 100, JumpAttempts = 4, DeviceName = "Laser", ID = None)

Allows locking of a laser to a specific frequency

- Laser (controllers.laser): The laser to control
- Wavemeter (controllers.WM): The wavemeter to read the frequency from
- LockInterval (float): The time in seconds between each locking attempt
- LockWait (float): The time in seconds to wait when locking and using grating
- LockTolerance (float): The tolerance of the error of the frequency in THz
- LockSlope (float): Starting guess for the voltage over frequency for locking, this will be overwritten quite fast
- LockSlopeRange (2-tuple of float): The minimum and maximum allowed slopes
- PiezoAttempts (int): The number of attempts to stabalize using piezo, after this it will use grating
- JumpAttempts (int): The number of attempts to use grating to stabilize the frequency
- DeviceName (str): The name of the device
- ID (str): The ID name for the device, only used for displaying infomation

Inherits from device

---

### method setLockFrequency(Value)

Sets the frequency to lock at

- Value (float): The frequency to lock at    

---

### method setLockFrequencyPersistent(Value, UseQueue = True)

Sets lock frequency and returns once it is locked

- Value (float): The frequency to lock at    
- UseQueue (bool): Whether to run the command through the queue or not, ignored if the device was initialized with UseQueue = False

---

### method getLockFrequency()

Get the frequency locking at

Returns the locking frequency as a float

---

### method isLocked(UseQueue = True)

Checks if the laser is locked

- UseQueue (bool): Whether to run the command through the queue or not, ignored if the device was initialized with UseQueue = False

Returns True if it is locked, False otherwise

---

### method setLaserFrequency(Value, UseQueue = True)

Set the frequency of the laser

- Value (float): The frequency to set
- UseQueue (bool): Whether to run the command through the queue or not, ignored if the device was initialized with UseQueue = False

---

### method getLaserFrequency(UseQueue = True)

Get the frequency from the laser

- UseQueue (bool): Whether to run the command through the queue or not, ignored if the device was initialized with UseQueue = False

Returns the laser frequency as a float

---

### method setFrequency(Value, UseQueue = True)

Set the frequency compensated using wavemeter

- Value (float): The frequency to set
- UseQueue (bool): Whether to run the command through the queue or not, ignored if the device was initialized with UseQueue = False

---

### method getFrequency(UseQueue = True)

Get the frequency from the wavemeter

- UseQueue (bool): Whether to run the command through the queue or not, ignored if the device was initialized with UseQueue = False

Returns the frequency as a float

---

### method resetWM(UseQueue = True)

Reset the exposure time of the wavemeter

- UseQueue (bool): Whether to run the command through the queue or not, ignored if the device was initialized with UseQueue = False

---

### method lock(UseQueue = True)

Locks the frequency

- UseQueue (bool): Whether to run the command through the queue or not, ignored if the device was initialized with UseQueue = False

---

### method isLocking()

Check if it is locked

Returns True if it is locking, False otherwise

---

### method unlock()

Unlocks the frequency

---

### property laser (controllers.laser)

The laser object

---

### property wm (controllers.WM)

The wavemeter object

---
---

## powerControl(PID, Powermeter, TimeBanditChannel = None, PowerRangeFactor = 1.3, PowerTolerance = 0.01, MinPowerTolerance = 1e-9, LockAttempts = 20, LockDelay = 0.2, DeviceName = "Power Control", ID = None)

Allows for power control of a laser path

- PID (controllers.powerPID): The PID to do the locking
- Powermeter (controllers.powermeter): The powermeter used as reference
- TimeBanditChannel (controllers.FPGAChannel) The FPGA channel used
- DeviceName (st): The name of the device
- PowerRangeFactor (float): How much higher than the locking power the powermeter should be peaking at
- PowerTolerance (float): The maximum allowed relative error of the power
- MinPowerTolerance (float): The minimum the tolerance can be
- LockAttempts (int): The number of attempts to use locking
- LockDelay (float): The time in seconds between each locking attempt
- DeviceName (str): The name of the device
- ID (str): The ID name for the device, only used for displaying infomation

Inherits from device

---

### method start(UseQueue = True)

Start the PID

- UseQueue (bool): Whether to run the command through the queue or not, ignored if the device was initialized with UseQueue = False

---

### method stop(UseQueue = True)

Stops the PID

- UseQueue (bool): Whether to run the command through the queue or not, ignored if the device was initialized with UseQueue = False

---

### method clearCache()

Clear the cache

---

### method lock(UseQueue = True)

Locks the power

- UseQueue (bool): Whether to run the command through the queue or not, ignored if the device was initialized with UseQueue = False

---

### method lock(UseQueue = True)

Unlocks the power and sets it to 0

- UseQueue (bool): Whether to run the command through the queue or not, ignored if the device was initialized with UseQueue = False

---

### method off(UseQueue = True)

Turns the PID off

- UseQueue (bool): Whether to run the command through the queue or not, ignored if the device was initialized with UseQueue = False

---

### method setSetPower(Power)

Sets the setpoint of the PID, it must also be locked afterwards if it is not locked already

- Power (float): The power to set

---

### method getSetPower()

Get the setpoint of the PID

- UseQueue (bool): Whether to run the command through the queue or not, ignored if the device was initialized with UseQueue = False

Returns the locking power as a float

---

### method setPower(Power, UseQueue = True)

Sets the power

- Power (float): The power to set
- UseQueue (bool): Whether to run the command through the queue or not, ignored if the device was initialized with UseQueue = False

---

### method getPower(UseQueue = True)

Get the current power

- UseQueue (bool): Whether to run the command through the queue or not, ignored if the device was initialized with UseQueue = False

Returns the power as a float

---

### method getPowerMulti(Count, SleepTime = 0, UseQueue = True)

Gets several power measurements

- Count (int): The number of measurements to get
- SleepTime (float): The time to sleep between each point
- UseQueue (bool): Whether to run the command through the queue or not, ignored if the device was initialized with UseQueue = False

Returns the data in a numpy array

---

### method setVoltageOut(Value, UseQueue = True)

Sets the output voltage

- Value (float): The voltage to set
- UseQueue (bool): Whether to run the command through the queue or not, ignored if the device was initialized with UseQueue = False

---

### method getVoltageOut(UseQueue = True)

Gets the output voltage

- UseQueue (bool): Whether to run the command through the queue or not, ignored if the device was initialized with UseQueue = False

Returns the output voltage as a float

---

### method isLocked(UseQueue = True)

Check if the PID is locking

- UseQueue (bool): Whether to run the command through the queue or not, ignored if the device was initialized with UseQueue = False

Returns True if it is locked, False otherwise

---

### method isLocking(UseQueue = True)

Check if the power is locked

- UseQueue (bool): Whether to run the command through the queue or not, ignored if the device was initialized with UseQueue = False

Returns True if it is locking, False otherwise

---

### method setAutoRange(Value, UseQueue = True)

Sets the status of auto range

- Value (bool): True to turn auto range on
- UseQueue (bool): Whether to run the command through the queue or not, ignored if the device was initialized with UseQueue = False

---

### method getAutoRange(UseQueue = True)

Gets the status of auto range

- UseQueue (bool): Whether to run the command through the queue or not, ignored if the device was initialized with UseQueue = False

Returns True if auto range is on, False otherwise

---

### method setPowerRange(Value, UseQueue = True)

Sets the power range

- Value (float): The maximum power
- UseQueue (bool): Whether to run the command through the queue or not, ignored if the device was initialized with UseQueue = False

---

### method getPowerRange(UseQueue = True)

Gets the power range

- UseQueue (bool): Whether to run the command through the queue or not, ignored if the device was initialized with UseQueue = False

Returns the maximum power which can be measured as a float

---

### property PID (controllers.powerPID)

The PID object

---

### property powermeter (controllers.powermeter)

The powermeter object

---

### property timeBanditChannel (controllers.FPGAChannel)

The TimeBandit channel to control the power

---

### property minOutput (float)

The minimum allowed output voltage

---

### property maxOutput (float)

The maximum allowed output voltage

---
---

## powerControlledLaser(Laser, PowerControl, DeviceName = "Power Controlled Laser", ID = None)

The controller for a power controlled laser

- Laser (laser): The laser to control
- PowerControl (powerControl) The power control of the laser
- DeviceName (str): The name of the device
- ID (str): The ID name for the device, only used for displaying infomation

Inherits from device

---

### property laser (laser)

The laser object

---

### property power (powerControl)

The powerControl object

---
---

## PID(Device, WhiteSpaceIn = 0, WhiteSpaceOut = 0, DeviceName = "PID", ID = None)

A generic PID class with logging

- Device (controllers.PID): The PID to control
- WhiteSpaceIn (float): Defines the default white space for the input when plotting
- WhiteSpaceOut (float): Defines the default white space for the output when plotting    
- DeviceName (str): The name of the device
- ID (str): The ID name for the device, only used for displaying infomation

Inherits from device

---

### method logDataRetriever()

Retrieves the PID data for the logger this must be overwritten by a subclass

Returns (SignalIn, SetPoint, SignalOut)

---

### method log(File, MaxTime = 0, Period = 1, MaxShow = 10000, Name = None, figsize = (10, 10), Plot = True, KeepFigure = True, Wait = False)

Logs the PID and does live plotting

- File (str): The file path for where to save the log
- MaxTime (float): The time in seconds to run the logging, 0 for infinity, must not be negative
- Period (floar): The time in seconds between each measurement, must not be negative
- MaxShow (int): The maximum number of data points to show at once, must be positive
- Name (str): The name to display on the figures
- figsize (tuple): A tuple of ints define the size of the figure
- Plot (bool): If True then do live plotting
- KeepFigure (bool): If False then it closes the live plotting when done
- Wait (bool): If True then it will wait for the log to finish and then return the data, if False then it will return immidiatly and return the stop event for the log for which to do .set() to stop the log

If Wait = True it returns the log results, if Wait = False it returns the stop event (threading.Event) for the log

---

### property device (controllers.PID)

The PID controller

### property logger (loggers.PIDLogger)

A logger object to log data with

---
---

## PTC10(Device, WhiteSpaceIn = 0.005, WhiteSpaceOut = 0.01, DeviceName = "PTC10", ID = None)

Controls a PTC10 PID and implements logging for it        

- Device (controllers.PTC10): The PID to control
- WhiteSpaceIn (float): Defines the default white space for the input when plotting
- WhiteSpaceOut (float): Defines the default white space for the output when plotting    
- DeviceName (str): The name of the device
- ID (str): The ID name for the device, only used for displaying infomation

Inherits from PID

---

### method log(File, PIDName = None, MaxTime = 0, Period = 1, MaxShow = 10000, Name = "PTC10", figsize = (10, 10), Plot = True, KeepFigure = True, Wait = False)

Logs the PID and does live plotting

- File (str): The file path for where to save the log
- PIDName (str): The name of the PID to log, if None it will use the default which may change mid logging
- MaxTime (float): The time in seconds to run the logging, 0 for infinity, must not be negative
- Period (floar): The time in seconds between each measurement, must not be negative
- MaxShow (int): The maximum number of data points to show at once, must be positive
- Name (str): The name to display on the figures
- figsize (tuple): A tuple of ints define the size of the figure
- Plot (bool): If True then do live plotting
- KeepFigure (bool): If False then it closes the live plotting when done
- Wait (bool): If True then it will wait for the log to finish and then return the data, if False then it will return immidiatly and return the stop event for the log for which to do .set() to stop the log

If Wait it True then it will return None. If False then it will return the stop event for the log

---

### property device (controllers.PTC10)

The PID controller

---
---

## tempArduino(Device, WhiteSpaceIn = 0.05, WhiteSpaceOut = 0.02, DeviceName = "Temperature Arduino", ID = None)

Controls a tempArduino PID and implements logging for it        

- Device (controllers.tempArduino): The PID to control
- WhiteSpaceIn (float): Defines the default white space for the input when plotting
- WhiteSpaceOut (float): Defines the default white space for the output when plotting    
- DeviceName (str): The name of the device
- ID (str): The ID name for the device, only used for displaying infomation

Inherits from PID

---

### method log(File, MaxTime = 0, Period = 1, MaxShow = 10000, Name = "PTC10", figsize = (10, 10), Plot = True, KeepFigure = True, Wait = False)

Logs the PID and does live plotting

- File (str): The file path for where to save the log
- MaxTime (float): The time in seconds to run the logging, 0 for infinity, must not be negative
- Period (floar): The time in seconds between each measurement, must not be negative
- MaxShow (int): The maximum number of data points to show at once, must be positive
- Name (str): The name to display on the figures
- figsize (tuple): A tuple of ints define the size of the figure
- Plot (bool): If True then do live plotting
- KeepFigure (bool): If False then it closes the live plotting when done
- Wait (bool): If True then it will wait for the log to finish and then return the data, if False then it will return immidiatly and return the stop event for the log for which to do .set() to stop the log

If Wait it True then it will return None. If False then it will return the stop event for the log

---

### property device (controllers.tempArduino)

The PID controller

---
---

## rotationStage(Device, ZeroPos = 0, DeviceName = "Rotation Stage", ID = None)

A generic rotation stage

- Device (controllers.rotationStage): The rotation stage device
- ZeroPos (float): The real position when the device is at position 0
- DeviceName (str): The name of the device
- ID (str): The ID name for the device, only used for displaying infomation

Inherits from device and controllers.rotationStage

---

### method home(UseQueue = True)

Homes the device     

- UseQueue (bool): Whether to run the command through the queue or not, ignored if the device was initialized with UseQueue = False

---

### method moveTo(Position, UseQueue = True)

Moves the device to a specified position in degrees

- Position (float): The position to set in degrees
- UseQueue (bool): Whether to run the command through the queue or not, ignored if the device was initialized with UseQueue = False

---

### method getPosition(UseQueue = True)

Gets the current position of the rotation stage

- UseQueue (bool): Whether to run the command through the queue or not, ignored if the device was initialized with UseQueue = False

Returns the current rotation angle in degrees as a float

---

### method move(Distance, UseQueue = True)

Moves the rotation stage relative to its original position in degrees

- Distance (float): The distance it should move by in degrees
- UseQueue (bool): Whether to run the command through the queue or not, ignored if the device was initialized with UseQueue = False

---

### method setZero(Value)

Sets the zero angle for this device

- Value (float): The value for the zero angle in degrees

---

### method getZero()

Gets the zero angle for this device in degrees

Returns the zero angle in degrees as a float

---

### property device (controllers.rotationStage)

The rotation stage controller

---
---

## EOM(PowerControl, TimeTagger, DACController, DACChannel, VoltageGuess = 3.4, ScanRange = 4 / 5, ScanPoints = 20, IntegrationTime = 0.1, RepetitionCount = 5, MaxAttempts = 100, Gate = None, InitialPause = 0.3, ScanPause = 0.1, Figsize = (8, 8), ShowBuffer = 0.1, DeviceName = "EOM", ID = None)

A minimizer for the EOM

- PowerControl (powerControl): The power control unit connected to the EOM
- TimeTagger (controllers.timeTagger): The time tagger object
- DACController (controllers.DAC): The DAC object
- DACChannel (int): The DAC channel
- VoltageGuess (float): The initial guess for the optimal voltage
- ScanRange (float): The range of each voltage scan
- ScanPoints (int): The number of measurement points in each scan
- IntegrationTime (float): The integration time per point
- MaxAttempts (int): The maximum number of attempts to minimize the EOM
- Gate (2-tuple of float): The gate for use to get time tagger counts
- InitialPause (float): The time to pause at the beginning of each tagger scan
- RepetitionCount (int): The number of measurement points to get for each powermeter measurement
- ScanPause (float): The time to pause between each measurement in a scan
- Figsize (dict): The size of the figure
- ShowBuffer (float): The white space buffer in the plot in percentage
- DeviceName (str): The name of the device
- ID (str): The ID name for the device, only used for displaying infomation

Inherits from device

---

### method setVoltage(Voltage, UseQueue = True)

Sets the voltage for the EOM

- Voltage (float): The voltage to set
- UseQueue (bool): Whether to run the command through the queue or not, ignored if the device was initialized with UseQueue = False

---

### method minimize(MeasureFunc, InitFunc = None, ExitFunc = None, UseQueue = True)

Minimize the laser through the EOM

 MeasureFunc (callable): The function to measure the power
 InitFunc (callable): The function to run before starting
 ExitFunc (callable): The function to run after it is done
 UseQueue (bool): Whether to run the command through the queue or not, ignored if the device was initialized with UseQueue = False

Returns the voltage where it is minimized

---

### method minimizePower(UseQueue = True)

Minimize the power of a power meter

- UseQueue (bool): Whether to run the command through the queue or not, ignored if the device was initialized with UseQueue = False

Returns the voltage where the power is minimized

---

### method minimizeCounts(Channel, UseQueue = True)

Minimize the counts of a time tagger

- Channel (int): The channel to get data from
- UseQueue (bool): Whether to run the command through the queue or not, ignored if the device was initialized with UseQueue = False

Returns the voltage where the counts is minimized

---
---

## timeBandit(FPGA, Figsize = (8, 4), DeviceName = "TimeBandit", ID = None)

Adds plotting to the time bandit

- FPGA (controllers.timeBandit): The FPGA to control
- Figsize (2-tuple of int): The size of the figure to plot the sequences on
- DeviceName (str): The name of the device
- ID (str): The ID name for the device, only used for displaying infomation

Inherits from device

---

### method show()

Shows the sequences

---

### property FPGA (controllers.timeBandit)

The time bandit to do plotting for

---
---

## AWG(Device, Figsize = (8, 4), DeviceName = "AWG", ID = None)

Adds plotting to the AWG

- Device (controllers.AWG): The AWG to control
- Figsize (2-tuple of int): The size of the figure to plot the sequences on

Inherits from device

---

### method show()

Shows the sequences

---

### property device (controllers.AWG)

The AWG controller

---
---