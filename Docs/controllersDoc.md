# Documentation for equipment

This is a collection of controller classes for the lab equipment, all classes have an empty version which can be used for testing while the device is not connected to the computer

Unless stated otherwise kwargs include:
- UseQueue (bool): True if it should use the queue of the device


---

# Classes

---

## PID(OutputRange = (0, 1))

Generic PID class which defines the standard functions

- OutputRange (2-tuple of floats): The minimum and maximum allowed output signals for the PID

---

### method setSetPoint(Value)

Sets the set point of the PID

- Value (float): The value to set

---

### method getSetPoint()

Gets the set point of the PID

Returns the set point as a float

---

### method setOutputSignal(Value)

Sets the output signal of the PID

- Value (float): The value to set

---

### method getOutputSignal()

Gets the output signal of the PID

Returns the output signal as a float

---

### method getInputSignal()

Gets the input signal of the PID

Returns the input signal as a float

---

### method setP(Value)

Sets the P-factor of the PID

- Value (float): The value to set

---

### method getP()

Gets the P-factor of the PID

Returns the P-factor as a float

---

### method setI(Value)

Sets the I-factor of the PID

- Value (float): The value to set

---

### method getI()

Gets the I-factor of the PID

Returns the I-factor as a float

---

### method setD(Value)

Sets the D-factor of the PID

- Value (float): The value to set

---

### method getD()

Gets the D-factor of the PID

Returns the D-factor as a float

---

### method start()

Starts the PID

---

### method stop()

Stops the PID

---

### property minOutput (float)

The minimum possible output of the PID

---

### property maxOutput (float)

The maximum possible output of the PID

---
---

## powerPID(Port, ID = None, P = 15, I = 5, D = 0, MaxOutput = 4095, Timeout = 1, ReconnectTries = 100, ReconnectDelay = 1, MaxAttempts = 100, AttemptDelay = 1, UseQueue = True, Empty = False, DeviceName = f"PID {ID}")

Opens a power PID connection

- Port (str): The name of the COM port through which to access the serial connection
- P (float): The P-factor to initialize
- I (float): The I-factor to initialize
- D (float): The D-factor to initialize
- MaxOutput (float): The maximum possible output voltage
- Timeout (float): The timeout time for the connection, must not be negative
- ReconnectTries (int): How many times to attempt to reconnect if it disconnects, must not be smaller than 0
- ReconnectDelay (float): The delay in seconds between each reconnect attempt, must not be negative
- MaxAttempts (int): The maximum number attempts to send a command before giving up, must not be smaller than 1
- AttemptDelay (float): The delay in seconds between each attempt to send a command, must not be negative
- UseQueue (bool): If True then it will set up a queue which can be used in the sendCommand method, if False the UseQueue in sendCommand is ignored
- Empty (bool): If True then it will not communicate with the device
- DeviceName (str): The name of the device, only used for error messages
- ID (str): The ID name for the device, only used for displaying infomation

Inherits from PID and connections.serial

---

### method sendCommand(Command, UseQueue = True, ResponseCheck = None)

Send a command to the device

- Command (str): The command to send the device
- UseQueue (bool): Whether to run the command through the queue or not, ignored if the device was initialized with UseQueue = False
- ResponseCheck (Func): A function to check if the response was correct, None if no check should be used, the function must have the arguments (Class, Command, ReturnString) and must return None on succes or a string on failure with the error message

Returns the list of return lines as a list of strings

---

### method setSetPoint(Value, UseQueue = True)

Sets the set point of the PID

- Value (float): The value to set
- UseQueue (bool): Whether to run the command through the queue or not, ignored if the device was initialized with UseQueue = False

---

### method getSetPoint(UseQueue = True)

Gets the set point of the PID

- UseQueue (bool): Whether to run the command through the queue or not, ignored if the device was initialized with UseQueue = False

Returns the set point as a float

---

### method setOutputSignal(Value, UseQueue = True)

Sets the output signal of the PID

- Value (float): The value to set
- UseQueue (bool): Whether to run the command through the queue or not, ignored if the device was initialized with UseQueue = False

---

### method getOutputSignal(UseQueue = True)

Gets the output signal of the PID

- UseQueue (bool): Whether to run the command through the queue or not, ignored if the device was initialized with UseQueue = False

Returns the output signal as a float

---

### method getInputSignal(UseQueue = True)

Gets the input signal of the PID

- UseQueue (bool): Whether to run the command through the queue or not, ignored if the device was initialized with UseQueue = False

Returns the input signal as a float

---

### method setP(Value, UseQueue = True)

Sets the P-factor of the PID

- Value (float): The value to set
- UseQueue (bool): Whether to run the command through the queue or not, ignored if the device was initialized with UseQueue = False

---

### method getP(UseQueue = True)

Gets the P-factor of the PID

- UseQueue (bool): Whether to run the command through the queue or not, ignored if the device was initialized with UseQueue = False

Returns the P-factor as a float

---

### method setI(Value, UseQueue = True)

Sets the I-factor of the PID

- Value (float): The value to set
- UseQueue (bool): Whether to run the command through the queue or not, ignored if the device was initialized with UseQueue = False

---

### method getI(UseQueue = True)

Gets the I-factor of the PID

- UseQueue (bool): Whether to run the command through the queue or not, ignored if the device was initialized with UseQueue = False

Returns the I-factor as a float

---

### method setD(Value, UseQueue = True)

Sets the D-factor of the PID

- Value (float): The value to set
- UseQueue (bool): Whether to run the command through the queue or not, ignored if the device was initialized with UseQueue = False

---

### method getD(UseQueue = True)

Gets the D-factor of the PID

- UseQueue (bool): Whether to run the command through the queue or not, ignored if the device was initialized with UseQueue = False

Returns the D-factor as a float

---

### method start(UseQueue = True)

Starts the PID

- UseQueue (bool): Whether to run the command through the queue or not, ignored if the device was initialized with UseQueue = False

---

### method stop(UseQueue = True)

Stops the PID

- UseQueue (bool): Whether to run the command through the queue or not, ignored if the device was initialized with UseQueue = False

---

### method setVoltageOut

Alias for setOutputSignal

---

### method getVoltageOut

Alias for getOutputSignal

---

### method getVoltageIn

Alias for getInputSignal

---

### method setADCoffset(Value, UseQueue = True)

Set the ADC offset

- Value (float): The new value of the ADC offset
- UseQueue (bool): Whether to run the command through the queue or not, ignored if the device was initialized with UseQueue = False

---

### method getADCoffset(UseQueue = True)

Get the ADC offset

- UseQueue (bool): Whether to run the command through the queue or not, ignored if the device was initialized with UseQueue = False

Returns the ADC offset as a float

---

### method setSumError(Value, UseQueue = True)

Set the sum error

- Value (float): The new value of the sum error
- UseQueue (bool): Whether to run the command through the queue or not, ignored if the device was initialized with UseQueue = False

---

### method getSumError(UseQueue = True)

Get the sum error

- UseQueue (bool): Whether to run the command through the queue or not, ignored if the device was initialized with UseQueue = False

Returns the sum error as a float

---

### method status(UseQueue = True)

Get the status

- UseQueue (bool): Whether to run the command through the queue or not, ignored if the device was initialized with UseQueue = False

Returns True if it is running and False if it is not

---
---

## PTC10(Port, Name = "EOM", ID = None, OutputRange = (0, 1), Timeout = 1, ReconnectTries = 100, ReconnectDelay = 1, MaxAttempts = 100, AttemptDelay = 1, UseQueue = True, Empty = False, DeviceName = f"PTC10 {ID}")

A python controller for the PTC10, it can control the PID parameters of the devices connected to the PTC10, turn it on and off and read the applied current and the temperature.

- Port (str): The name of the COM port through which to access the serial connection
- Name (str): The name of the device to control, can be changed later with setName function
- OutputRange (2-tuple of floats): The minimum and maximum allowed output signals for the PID
- Timeout (float): The timeout time for the connection, must not be negative
- ReconnectTries (int): How many times to attempt to reconnect if it disconnects, must not be smaller than 0
- ReconnectDelay (float): The delay in seconds between each reconnect attempt, must not be negative
- MaxAttempts (int): The maximum number attempts to send a command before giving up, must not be smaller than 1
- AttemptDelay (float): The delay in seconds between each attempt to send a command, must not be negative
- UseQueue (bool): If True then it will set up a queue which can be used in the sendCommand method, if False the UseQueue in sendCommand is ignored
- Empty (bool): If True then it will not communicate with the device
- DeviceName (str): The name of the device, only used for error messages
- ID (str): The ID name for the device, only used for displaying infomation

Inherits from PID and connections.serial

---

### method setName(Name)

Sets the name of the equipment to use

- Name (str): The name of the equipment (EOM, ET1 or ET2 for ColdLab)

---

### method getName()

Gets the name of the equipment to use

---

### method setSetPoint(Value, UseQueue = True, Name = None)

Sets the set point of the PID

- Value (float): The value to set
- UseQueue (bool): Whether to run the command through the queue or not, ignored if the device was initialized with UseQueue = False
- Name (str): The name of the device to access, None to use the default device

---

### method getSetPoint(UseQueue = True, Name = None)

Gets the set point of the PID

- UseQueue (bool): Whether to run the command through the queue or not, ignored if the device was initialized with UseQueue = False
- Name (str): The name of the device to access, None to use the default device

Returns the set point as a float

---

### method setOutputSignal(Value, UseQueue = True, Name = None)

Sets the output signal of the PID

- Value (float): The value to set
- UseQueue (bool): Whether to run the command through the queue or not, ignored if the device was initialized with UseQueue = False
- Name (str): The name of the device to access, None to use the default device

---

### method getOutputSignal(UseQueue = True, Name = None)

Gets the output signal of the PID

- UseQueue (bool): Whether to run the command through the queue or not, ignored if the device was initialized with UseQueue = False
- Name (str): The name of the device to access, None to use the default device

Returns the output signal as a float

---

### method getInputSignal(UseQueue = True, Name = None)

Gets the input signal of the PID

- UseQueue (bool): Whether to run the command through the queue or not, ignored if the device was initialized with UseQueue = False
- Name (str): The name of the device to access, None to use the default device

Returns the input signal as a float

---

### method setP(Value, UseQueue = True, Name = None)

Sets the P-factor of the PID

- Value (float): The value to set
- UseQueue (bool): Whether to run the command through the queue or not, ignored if the device was initialized with UseQueue = False
- Name (str): The name of the device to access, None to use the default device

---

### method getP(UseQueue = True, Name = None)

Gets the P-factor of the PID

- UseQueue (bool): Whether to run the command through the queue or not, ignored if the device was initialized with UseQueue = False
- Name (str): The name of the device to access, None to use the default device

Returns the P-factor as a float

---

### method setI(Value, UseQueue = True, Name = None)

Sets the I-factor of the PID

- Value (float): The value to set
- UseQueue (bool): Whether to run the command through the queue or not, ignored if the device was initialized with UseQueue = False
- Name (str): The name of the device to access, None to use the default device

---

### method getI(UseQueue = True, Name = None)

Gets the I-factor of the PID

- UseQueue (bool): Whether to run the command through the queue or not, ignored if the device was initialized with UseQueue = False
- Name (str): The name of the device to access, None to use the default device

Returns the I-factor as a float

---

### method setD(Value, UseQueue = True, Name = None)

Sets the D-factor of the PID

- Value (float): The value to set
- UseQueue (bool): Whether to run the command through the queue or not, ignored if the device was initialized with UseQueue = False
- Name (str): The name of the device to access, None to use the default device

---

### method getD(UseQueue = True, Name = None)

Gets the D-factor of the PID

- UseQueue (bool): Whether to run the command through the queue or not, ignored if the device was initialized with UseQueue = False
- Name (str): The name of the device to access, None to use the default device

Returns the D-factor as a float

---

### method start(UseQueue = True, Name = None)

Starts the PID

- UseQueue (bool): Whether to run the command through the queue or not, ignored if the device was initialized with UseQueue = False
- Name (str): The name of the device to access, None to use the default device

---

### method stop(UseQueue = True, Name = None)

Stops the PID

- UseQueue (bool): Whether to run the command through the queue or not, ignored if the device was initialized with UseQueue = False
- Name (str): The name of the device to access, None to use the default device

---

### method setCurrent

Alias for setOutputSignal

---

### method getCurrent

Alias for getOutputSignal

---

### method getTemp

Alias for getInputSignal

---

### method status(UseQueue = True, Name = None)

Get the status of the PID

- UseQueue (bool): True if it should use the command queue
- Name (str): The name of the device to access, None to use the default device

Returns True if it is on, False if it is off, None if it is on Follow

---
---

## tempArduino(Port, ID = None, OutputRange = (0, 1), Timeout = 1, ReconnectTries = 100, ReconnectDelay = 1, MaxAttempts = 100, AttemptDelay = 1, UseQueue = True, Empty = False, DeviceName = f"Temperature Arduino {ID}")

A python controller for the arduino temperature PID, it can control the PID parameters of the arduino and get all infomation about it

- Port (str): The name of the COM port through which to access the serial connection
- Name (str): The name of the device to control, can be changed later with setName function
- OutputRange (2-tuple of floats): The minimum and maximum allowed output signals for the PID
- Timeout (float): The timeout time for the connection, must not be negative
- ReconnectTries (int): How many times to attempt to reconnect if it disconnects, must not be smaller than 0
- ReconnectDelay (float): The delay in seconds between each reconnect attempt, must not be negative
- MaxAttempts (int): The maximum number attempts to send a command before giving up, must not be smaller than 1
- AttemptDelay (float): The delay in seconds between each attempt to send a command, must not be negative
- UseQueue (bool): If True then it will set up a queue which can be used in the sendCommand method, if False the UseQueue in sendCommand is ignored
- Empty (bool): If True then it will not communicate with the device
- DeviceName (str): The name of the device, only used for error messages
- ID (str): The ID name for the device, only used for displaying infomation

Inherits from PID and connections.serial

---

### method setSetPoint(Value, UseQueue = True)

Sets the set point of the PID

- Value (float): The value to set
- UseQueue (bool): Whether to run the command through the queue or not, ignored if the device was initialized with UseQueue = False

---

### method getSetPoint(UseQueue = True)

Gets the set point of the PID

- UseQueue (bool): Whether to run the command through the queue or not, ignored if the device was initialized with UseQueue = False

Returns the set point as a float

---

### method setOutputSignal(Value, UseQueue = True)

Sets the output signal of the PID

- Value (float): The value to set
- UseQueue (bool): Whether to run the command through the queue or not, ignored if the device was initialized with UseQueue = False

---

### method getOutputSignal(UseQueue = True)

Gets the output signal of the PID

- UseQueue (bool): Whether to run the command through the queue or not, ignored if the device was initialized with UseQueue = False

Returns the output signal as a float

---

### method getInputSignal(UseQueue = True)

Gets the input signal of the PID

- UseQueue (bool): Whether to run the command through the queue or not, ignored if the device was initialized with UseQueue = False

Returns the input signal as a float

---

### method setP(Value, UseQueue = True)

Sets the P-factor of the PID

- Value (float): The value to set
- UseQueue (bool): Whether to run the command through the queue or not, ignored if the device was initialized with UseQueue = False

---

### method getP(UseQueue = True)

Gets the P-factor of the PID

- UseQueue (bool): Whether to run the command through the queue or not, ignored if the device was initialized with UseQueue = False

Returns the P-factor as a float

---

### method setI(Value, UseQueue = True)

Sets the I-factor of the PID

- Value (float): The value to set
- UseQueue (bool): Whether to run the command through the queue or not, ignored if the device was initialized with UseQueue = False

---

### method getI(UseQueue = True)

Gets the I-factor of the PID

- UseQueue (bool): Whether to run the command through the queue or not, ignored if the device was initialized with UseQueue = False

Returns the I-factor as a float

---

### method setD(Value, UseQueue = True)

Sets the D-factor of the PID

- Value (float): The value to set
- UseQueue (bool): Whether to run the command through the queue or not, ignored if the device was initialized with UseQueue = False

---

### method getD(UseQueue = True)

Gets the D-factor of the PID

- UseQueue (bool): Whether to run the command through the queue or not, ignored if the device was initialized with UseQueue = False

Returns the D-factor as a float

---

### method setIntegrand(Value, UseQueue = True)

Sets the integrand

- Value (float): The value to set
- UseQueue (bool): Whether to run the command through the queue or not, ignored if the device was initialized with UseQueue = False

---

### method setForceDac(Value, UseQueue = True)

Sets the force dac

- Value (float): The value to set
- UseQueue (bool): Whether to run the command through the queue or not, ignored if the device was initialized with UseQueue = False

---

### method getStatus(UseQueue = True)

Get all infomation about the arduino

- UseQueue (bool): Whether to run the command through the queue or not, ignored if the device was initialized with UseQueue = False

Returns a dictionary with all of the values

---
---

## keithly(SerialNumber, CurrentLimit = 0.001, VoltageLimit = 1.5, StableTries = 50, StableDelay = 0.05, Timeout = 1, ReconnectTries = 100, ReconnectDelay = 1, MaxAttempts = 100, AttemptDelay = 1, UseQueue = True, Empty = False, DeviceName = "Keithly", ID = None)

Controls a keithly voltage source

- SerialNumber (str): The serial number of the device
- CurrentLimit (float): The maximum allowed current
- VoltageLimit (float): The maximum allowed voltage
- StableTries (int): The maximum number of attempts to stabilize voltage
- StableDelay (float): The delay in seconds between each stabilization attempt
- Timeout (float): The timeout time for the connection, must not be negative
- ReconnectTries (int): How many times to attempt to reconnect if it disconnects, must not be smaller than 0
- ReconnectDelay (float): The delay in seconds between each reconnect attempt, must not be negative
- MaxAttempts (int): The maximum number attempts to send a command before giving up, must not be smaller than 1
- AttemptDelay (float): The delay in seconds between each attempt to send a command, must not be negative
- UseQueue (bool): If True then it will set up a queue which can be used in the sendCommand method, if False the UseQueue in sendCommand is ignored
- Empty (bool): If True then it will not communicate with the device
- DeviceName (str): The name of the device, only used for error messages
- ID (str): The ID name for the device, only used for displaying infomation

Inherits from connections.visa

---

### method setVoltage(Value, UseQueue = True)

Sets the voltage and waits until it is locked
    
- Value (float): The value of the voltage
- UseQueue (bool): Whether to run the command through the queue or not, ignored if the device was initialized with UseQueue = False

---

### method setVoltageFast(Value, UseQueue = True)

Sets the voltage without waiting for lock

- Value (float): The value of the voltage
- UseQueue (bool): Whether to run the command through the queue or not, ignored if the device was initialized with UseQueue = False

---

### method getVoltage(UseQueue = True)

Gets the voltage

- UseQueue (bool): Whether to run the command through the queue or not, ignored if the device was initialized with UseQueue = False

Returns the voltage as a float

---

### method getCurrent(UseQueue = True)

Gets the current

- UseQueue (bool): Whether to run the command through the queue or not, ignored if the device was initialized with UseQueue = False

Returns the current as a float

### method setCurrentLim(Value, UseQueue = True)

Sets the current limit

- Value (float): The value for the current limit
- UseQueue (bool): Whether to run the command through the queue or not, ignored if the device was initialized with UseQueue = False

---

### method getCurrentLim(UseQueue = True)

Gets the current limit

- UseQueue (bool): Whether to run the command through the queue or not, ignored if the device was initialized with UseQueue = False

Returns the current limit as a float

---

### method setVoltageLim(Value, UseQueue = True)

Sets the voltage limit

- Value (float): The value of the maximum voltage
- UseQueue (bool): Whether to run the command through the queue or not, ignored if the device was initialized with UseQueue = False

---

### method getVoltageLim(UseQueue = True)

Gets the voltage limit

- UseQueue (bool): Whether to run the command through the queue or not, ignored if the device was initialized with UseQueue = False

Returns the maximum allowed voltage as a float

---

### method setMeasureDelay(Value, UseQueue = True)

Sets the measure delay

- Value (float): The value of the measure delay
- UseQueue (bool): Whether to run the command through the queue or not, ignored if the device was initialized with UseQueue = False

---

### method getMeasureDelay(UseQueue = True)

Gets the measure delay

- UseQueue (bool): Whether to run the command through the queue or not, ignored if the device was initialized with UseQueue = False

Returns the measure delay as a float

---

### method getWireSense(UseQueue = True)

Gets the wire sense mode

- UseQueue (bool): Whether to run the command through the queue or not, ignored if the device was initialized with UseQueue = False

Returns the wire sense as a string

---

### method use2WireSense(UseQueue = True)

Sets the wire sense mode to 2wire

- UseQueue (bool): Whether to run the command through the queue or not, ignored if the device was initialized with UseQueue = False

---

### method start(UseQueue = True)

Turns on the voltage source

- UseQueue (bool): Whether to run the command through the queue or not, ignored if the device was initialized with UseQueue = False

---

### method stop(UseQueue = True)

Turns off the voltage source

- UseQueue (bool): Whether to run the command through the queue or not, ignored if the device was initialized with UseQueue = False

---

### method status(UseQueue = True)

Returns the activation status of the device

- UseQueue (bool): Whether to run the command through the queue or not, ignored if the device was initialized with UseQueue = False

Returns the status as a string

---

### method front(UseQueue = True)

Sets the front terminal and turns voltage source on

- UseQueue (bool): Whether to run the command through the queue or not, ignored if the device was initialized with UseQueue = False

---

### method rear(UseQueue = True)

Sets rear terminal and turns voltage source on

- UseQueue (bool): Whether to run the command through the queue or not, ignored if the device was initialized with UseQueue = False

---

### method getTerminal(UseQueue = True)

Get which terminal is showing

- UseQueue (bool): Whether to run the command through the queue or not, ignored if the device was initialized with UseQueue = False

Returns the terminal that is in use as a string

---

### method enableAutoDelay(UseQueue = True)

Enables auto delay

- UseQueue (bool): Whether to run the command through the queue or not, ignored if the device was initialized with UseQueue = False

---

### method disableAutoDelay(UseQueue = True)

Disables auto delay

- UseQueue (bool): Whether to run the command through the queue or not, ignored if the device was initialized with UseQueue = False

---

### method getAutoDelay(UseQueue = True)

Gets the auto delay status

- UseQueue (bool): Whether to run the command through the queue or not, ignored if the device was initialized with UseQueue = False

Returns the auto delay status as a string

---

### method exit(UseQueue = True)

shuts down the voltage source
    
- UseQueue (bool): Whether to run the command through the queue or not, ignored if the device was initialized with UseQueue = False

---

### method reset(UseQueue = True)

Resets the source to a known position

- UseQueue (bool): Whether to run the command through the queue or not, ignored if the device was initialized with UseQueue = False

---
---

## powermeter()

A generic powermeter controller

---

### method setPowerAutoRange(Value)

Sets the power auto range

- Value (bool): True if auto range should be enabled

---

### method enablePowerAutoRange()

Enables power auto range

---

### method disablePowerAutoRange()

Disables power auto range

---

### method getPowerAutoRange()

Gets the status of the power auto range
    
Returns True if auto range is on and False otherwise

---

### method setPowerRange(Value)

Sets the max power
    
- Value (float): The value of the max power

---

### method getPowerRange()

Gets the max power setting

Returns the maximum power the PM can measure as a float

---

### method setFrequencyRange(Value)

Sets the max frequency

- Value (float): The value of the max frequency

---

### method getFrequencyRange(Value)

Gets the max frequency setting

Returns the maximum frequency that it can measure as a float

---

### method getPower()

Gets a power measurement

Returns the measured power as a float

---

### method getPowerMulti(Count, SleepTime = 0)

Gets several power measurements

- Count (int): The number of measurements to get
- SleepTime (float): The time to sleep between each point

Returns a numpy array with the data

---
---

## PM100D(SerialNumber, Timeout = 1, ReconnectTries = 100, ReconnectDelay = 1, MaxAttempts = 100, AttemptDelay = 1, UseQueue = True, Empty = False, DeviceName = "PM100D", ID = None)

Controls a thorlabs PM100D powermeter

- SerialNumber (str): The serial number of the device
- Timeout (float): The timeout time for the connection, must not be negative
- ReconnectTries (int): How many times to attempt to reconnect if it disconnects, must not be smaller than 0
- ReconnectDelay (float): The delay in seconds between each reconnect attempt, must not be negative
- MaxAttempts (int): The maximum number attempts to send a command before giving up, must not be smaller than 1
- AttemptDelay (float): The delay in seconds between each attempt to send a command, must not be negative
- UseQueue (bool): If True then it will set up a queue which can be used in the sendCommand method, if False the UseQueue in sendCommand is ignored
- Empty (bool): If True then it will not communicate with the device
- DeviceName (str): The name of the device, only used for error messages
- ID (str): The ID name for the device, only used for displaying infomation

Inherits from powermeter and connections.visa

---

### method setPowerAutoRange(Value, UseQueue = True)

Sets the power auto range

- Value (bool): True if auto range should be enabled
- UseQueue (bool): Whether to run the command through the queue or not, ignored if the device was initialized with UseQueue = False

---

### method enablePowerAutoRange(UseQueue = True)

Enables power auto range

- UseQueue (bool): Whether to run the command through the queue or not, ignored if the device was initialized with UseQueue = False

---

### method disablePowerAutoRange(UseQueue = True)

Disables power auto range

- UseQueue (bool): Whether to run the command through the queue or not, ignored if the device was initialized with UseQueue = False

---

### method getPowerAutoRange(UseQueue = True)

Gets the status of the power auto range
    
- UseQueue (bool): Whether to run the command through the queue or not, ignored if the device was initialized with UseQueue = False

Returns True if auto range is on and False otherwise

---

### method setPowerRange(Value, UseQueue = True)

Sets the max power
    
- Value (float): The value of the max power
- UseQueue (bool): Whether to run the command through the queue or not, ignored if the device was initialized with UseQueue = False

---

### method getPowerRange(UseQueue = True)

Gets the max power setting

- UseQueue (bool): Whether to run the command through the queue or not, ignored if the device was initialized with UseQueue = False

Returns the maximum power the PM can measure as a float

---

### method setFrequencyRange(Value, UseQueue = True)

Sets the max frequency

- Value (float): The value of the max frequency
- UseQueue (bool): Whether to run the command through the queue or not, ignored if the device was initialized with UseQueue = False

---

### method getFrequencyRange(Value, UseQueue = True)

Gets the max frequency setting

- UseQueue (bool): Whether to run the command through the queue or not, ignored if the device was initialized with UseQueue = False

Returns the maximum frequency that it can measure as a float

---

### method getPower(UseQueue = True)

Gets a power measurement

- UseQueue (bool): Whether to run the command through the queue or not, ignored if the device was initialized with UseQueue = False

Returns the measured power as a float

---

### method getPowerMulti(Count, SleepTime = 0, UseQueue = True)

Gets several power measurements

- Count (int): The number of measurements to get
- SleepTime (float): The time to sleep between each point
- UseQueue (bool): Whether to run the command through the queue or not, ignored if the device was initialized with UseQueue = False

Returns a numpy array with the data


---
---

## WM(DLLPath, Channel = 1, UseQueue = True, Empty = False, DeviceName = "Wavelength Meter", ID = None)

Controller for a wavemeter

- DLLPath (str): The path to the dll to load
- Channel (int): The default channel to use, can be set with the setChannel method
- UseQueue (bool): If True then it will set up a queue which can be used in the sendCommand method, if False the UseQueue in sendCommand is ignored
- Empty (bool): If True then it will not communicate with the device
- DeviceName (str): The name of the device, only used for error messages
- ID (str): The ID name for the device, only used for displaying infomation

Inherits from connections.dll

---

### method getWavelength(UseQueue = True, Channel = None)

Gets the wavelength from the device

- UseQueue (bool): True if it should use the command queue
- Channel (int): The channel to access, if None then it will use the default

Returns the wavelength as a float in nm

---

### method getFrequency(UseQueue = True, Channel = None)

Gets the frequency from the device

- UseQueue (bool): True if it should use the command queue
- Channel (int): The channel to access, if None then it will use the default

Returns the frequency as a float in GHz

---

### method setExposure(Value, Index, UseQueue = True, Channel = None)

Sets the exposure time

- Value (int): The value to set the exposure to
- Index (int): The index of the exposure (0 or 1)
- UseQueue (bool): True if it should use the command queue
- Channel (int): The channel to access, if None then it will use the default

---

### method resetExposure(UseQueue = True, Channel = None)

Resets the exposure time

- UseQueue (bool): True if it should use the command queue
- Channel (int): The channel to access, if None then it will use the default

---

### method setChannel(Channel)

Sets the default channel to use

- Channel (int): The channel to use

---
---

## DAC(Name, InputChannels = [], OutputChannels = [], VoltageLimits = [], Timeout = 1, UseQueue = True, Empty = False, DeviceName = "DAC", ID = None)

Controls a DAC

- Name (str): The name of the device to connect to
- InputChannels (list of int): A list of all the input channels to use, may be empty
- OutputChannels (list of int): A list of all the output channels to use, may be empty, must have the same length as VoltageLimits
- VoltageLimits (list of float): A list of all the voltage limits of the output channels
- Timeout (float): The timeout in seconds
- UseQueue (bool): If True then it will set up a queue which can be used in the sendCommand method, if False the UseQueue in sendCommand is ignored
- Empty (bool): If True then it will not communicate with the device
- DeviceName (str): The name of the device, only used for error messages
- ID (str): The ID name for the device, only used for displaying infomation    

---

### method setVoltage(Value, Channel, UseQueue = True)

Set the voltage of an output channel

- Value (float): The voltage to set
- Channel (int): The ID of the channel to access    
- UseQueue (bool): Whether to run the command through the queue or not, ignored if the device was initialized with UseQueue = False

---

### method getVoltage(Channel, UseQueue = True)

Read the voltage from an input channel

- Channel (int): The ID of the channel to access    
- UseQueue (bool): Whether to run the command through the queue or not, ignored if the device was initialized with UseQueue = False

Returns the voltage as a float

---
---

## laser(VoltageRange = (0, 1), FrequencyRange = None, WavelengthRange = (900, 1000))

A generic laser class

- VoltageRange (2-tuple of float): Them minimum and maximum voltage allowed
- FrequencyRange (2-tuple of float): The minimum and maximum frequencies allowed, if None then they are calculated from WavelengthRange
- WavelengthRange (2-tuple of float): The minimum and maximum wavelengths allowed, calculated from FrequencyRange if that is given

---

### method frequencyToWavelength(Value)

Converts a frequency in THz to a wavelength in nm

- Value (float): The frequency to convert 

Returns the wavelength as a float

---

### method wavelengthToFrequency(Value)

Converts a wavelength in nm to a frequency in THz

- Value (float): The wavelength to convert

Returns the frequency as a float

---

### method frequencyAllowed(Value)

Checks if the frequency is in the allowed range

- Value (float): The frequency to check

Return True if it is within the Range, False otherwise

---

### method wavelengthAllowed(Value)

Checks if the wavelength is in the allowed range

- Value (float): The wavelength to check

Return True if it is within the Range, False otherwise

---

### method voltageAllowed(Value)

Checks if the voltage is in the allowed range

- Value (float): The voltage to check

Return True if it is within the Range, False otherwise

---

### method setWavelength(Value)

Sets the wavelength of the laser, this or setFrequency must be overwritten

- Value (float): The value of the wavelength

---

### method getWavelength()

Gets the wavelength set by the laser, this or getFrequency must be overwritten

Returns the wavelength as a float

---

### method setFrequency(Value)

Sets the frequency of the laser, this or setWavelength must be overwritten

- Value (float): The value of the frequency

---

### method getFrequency()

Gets the frequency set by the laser, this or getWavelength must be overwritten

Returns the frequency as a float

---

### method setVoltage(Value)

Sets the piezo voltage of the laser

- Value (float): The voltage to set

---

### method getVoltage()

Gets the last voltage set

Returns the voltage as a float

---

### property voltageBase (float)

The base voltage to return to when defaulting

---
---

## DLCPro(IP, Port, FrequencyControl = True, SettleTime = 25, SleepTime = 0.01, InitWait = 0.05, VoltageRange = (0, 1), FrequencyRange = None, WavelengthRange = (900, 1000), BufferSize = 4096, Timeout = 1, ReconnectTries = 100, ReconnectDelay = 1, MaxAttempts = 100, AttemptDelay = 1, UseQueue = True, Empty = False, DeviceName = "DLCPro", ID = None)

Controls a DLC pro controlled laser

- IP (str): The IP of the connection
- Port (int): The port to communicate through
- FrequencyControl (bool): If False then it cannot set or get the frequency for this laser
- SettleTime (float): The allowed time in seconds to set the wavelength
- SleepTime (float): The time in seconds to sleep before each settle check when setting the wavelength
- InitWait (float): The time in seconds to let it initialize
- VoltageRange (2-tuple of float): Them minimum and maximum voltage allowed
- FrequencyRange (2-tuple of float): The minimum and maximum frequencies allowed, if None then they are calculated from WavelengthRange
- WavelengthRange (2-tuple of float): The minimum and maximum wavelengths allowed, calculated from FrequencyRange if that is given
- BufferSize (int): The size of the buffer when getting data
- Timeout (float): The timeout in seconds
- ReconnectTries (int): How many times to attempt to reconnect if it disconnects, must not be smaller than 0
- ReconnectDelay (float): The delay in seconds between each reconnect attempt, must not be negative
- MaxAttempts (int): The maximum number attempts to send a command before giving up, must not be smaller than 1
- AttemptDelay (float): The delay in seconds between each attempt to send a command, must not be negative
- UseQueue (bool): If True then it will set up a queue which can be used in the sendCommand method, if False the UseQueue in sendCommand is ignored
- Empty (bool): If True then it will not communicate with the device
- DeviceName (str): The name of the device, only used for error messages
- ID (str): The ID name for the device, only used for displaying infomation

Inherits from laser and connections.socket

---

### method setWavelength(Value, UseQueue = True)

Sets the wavelength of the laser, this or setFrequency must be overwritten

- Value (float): The value of the wavelength
- UseQueue (bool): Whether to run the command through the queue or not, ignored if the device was initialized with UseQueue = False

---

### method getWavelength(UseQueue = True)

Gets the wavelength set by the laser, this or getFrequency must be overwritten

- UseQueue (bool): Whether to run the command through the queue or not, ignored if the device was initialized with UseQueue = False

Returns the wavelength as a float

---

### method setFrequency(Value, UseQueue = True)

Sets the frequency of the laser, this or setWavelength must be overwritten

- Value (float): The value of the frequency
- UseQueue (bool): Whether to run the command through the queue or not, ignored if the device was initialized with UseQueue = False

---

### method getFrequency(UseQueue = True)

Gets the frequency set by the laser, this or getWavelength must be overwritten

- UseQueue (bool): Whether to run the command through the queue or not, ignored if the device was initialized with UseQueue = False

Returns the frequency as a float

---

### method setVoltage(Value, UseQueue = True)

Sets the piezo voltage of the laser

- Value (float): The voltage to set
- UseQueue (bool): Whether to run the command through the queue or not, ignored if the device was initialized with UseQueue = False

---

### method getVoltage(UseQueue = True)

Gets the last voltage set

- UseQueue (bool): Whether to run the command through the queue or not, ignored if the device was initialized with UseQueue = False

Returns the voltage as a float

---

### method scan(StartWavelength, StopWavelength, Speed, UseQueue = True)

Sets the scan parameters

- StartWavelength (float): The start wavelength of the scan
- StopWavelength (float): The stop wavelength of the scan
- Speed (float): The speed of the scan
- UseQueue (bool): Whether to run the command through the queue or not, ignored if the device was initialized with UseQueue = False

---

### method scanContinuous(Mode, UseQueue = True)

Sets the state of the continuous scan

- Mode (bool): True if it should do continuous scan
- UseQueue (bool): Whether to run the command through the queue or not, ignored if the device was initialized with UseQueue = False

---

### method enableScanContinuous(UseQueue = True)

Enables continuous scanning

- UseQueue (bool): Whether to run the command through the queue or not, ignored if the device was initialized with UseQueue = False

---

### method disableScanContinuous(UseQueue = True)

Disables continuous scanning

- UseQueue (bool): Whether to run the command through the queue or not, ignored if the device was initialized with UseQueue = False

---

### method startScan(UseQueue = True)

Starts scanning

- UseQueue (bool): Whether to run the command through the queue or not, ignored if the device was initialized with UseQueue = False

---

### method stopScan(UseQueue = True)

Stops scanning

- UseQueue (bool): Whether to run the command through the queue or not, ignored if the device was initialized with UseQueue = False

---

### method pauseScan(UseQueue = True)

Pauses scanning

- UseQueue (bool): Whether to run the command through the queue or not, ignored if the device was initialized with UseQueue = False

---

### method continueScan(UseQueue = True)

Continues scanning from last pause

- UseQueue (bool): Whether to run the command through the queue or not, ignored if the device was initialized with UseQueue = False

---
---

## DACLaser(DACController, Channel, VoltageRange = (0, 1), DeviceName = "DAC Laser", ID = None)

A DAC controlled laser, this laser cannot set or get the frequency or wavelength

- DACController (DAC): The DAC to control the voltage
- Channel (int): The channel of the DAC to use
- VoltageRange (2-tuple of float): Them minimum and maximum voltage allowed
- DeviceName (str): The name of the device, only used for error messages
- ID (str): The ID name for the device, only used for displaying infomation

Inherits from laser and deviceBase

---

### method setVoltage(Value, UseQueue = True)

Sets the voltage using the DAC

- Value (float): The value of the voltage
- UseQueue (bool): Whether to run the command through the queue or not, ignored if the device was initialized with UseQueue = False

---

### method getVoltage(UseQueue = True)

Gets the voltage set for the DAC

- UseQueue (bool): Whether to run the command through the queue or not, ignored if the device was initialized with UseQueue = False

Returns the voltage as a float

---
---

## rigol(IP, VoltageLimit = 10, Timeout = 1, ReconnectTries = 100, ReconnectDelay = 1, MaxAttempts = 100, AttemptDelay = 1, UseQueue = True, Empty = False, DeviceName = "Rigol", ID = None)

Controls a rigol

- IP (str): The IP of the rigol device
- VoltageLimit (float): The maximum allowed output voltage
- Timeout (float): The timeout time for the connection, must not be negative
- ReconnectTries (int): How many times to attempt to reconnect if it disconnects, must not be smaller than 0
- ReconnectDelay (float): The delay in seconds between each reconnect attempt, must not be negative
- MaxAttempts (int): The maximum number attempts to send a command before giving up, must not be smaller than 1
- AttemptDelay (float): The delay in seconds between each attempt to send a command, must not be negative
- UseQueue (bool): If True then it will set up a queue which can be used in the sendCommand method, if False the UseQueue in sendCommand is ignored
- Empty (bool): If True then it will not communicate with the device
- DeviceName (str): The name of the device, only used for error messages
- ID (str): The ID name for the device, only used for displaying infomation

Inherits from connetions.visa

---

### method setDCOutput(Voltage, Channel, **kwargs)

Sets the output of a channel to DC

- Voltage (float): The voltage to set
- Channel (int): The channel to set
- UseQueue (bool): Whether to run the command through the queue or not, ignored if the device was initialized with UseQueue = False

---

### method setSineOutput(Frequency, Amplitude, Offset, Phase, Channel, **kwargs)

Sets the output of a channel to a sine

- Frequency (float): The frequency of the sine
- Amplitude (float): The amplitude of the sine
- Offset (float): The offset of the sine
- Phase (float): The phase of the sine
- Channel (int): The channel to set
- UseQueue (bool): Whether to run the command through the queue or not, ignored if the device was initialized with UseQueue = False

---
---

## FPGASequence(FPGA, SequenceLength = None)

A sequence for an FPGA

- FPGA (timeBandit): The TimeBandit to create sequence for
- SequenceLength (int): The length of the sequence in input clock cycles, if None then the current length will be used

---

### method addState(Channel, Start, Stop)

Adds an interval for the FPGA channel to be on, if the state was "dc" or "off", then it will overwrite

- Channel (int): The channel to add a state to
- Start (float): The start time in ns, this will be rounded down to nearest clock cycle
- Stop (float): The stop time in ns, this will be rounded up to nearest clock cycle

---

### method addStateWithDuration(Channel, Start, Duration)

Adds an interval for the FPGA channel to be on, if the state was "dc" or "off", then it will overwrite

- Channel (int): The channel to add a state to
- Start (float): The start time in ns, this will be rounded down to nearest clock cycle
- Duration (float): The duration in ns, this will be rounded up to nearest clock cycle

---

### method addBaseState(Channel, Start, Stop)

Adds an interval for the FPGA channel to be on, if the state was "dc" or "off", then it will overwrite

- Channel (int): The channel to add a state to
- Start (float): The start time in clock cycles
- Stop (float): The stop time in clock cycles

---

### method addBaseStateWithDuration(Channel, Start, Duration)

Adds an interval for the FPGA channel to be on, if the state was "dc" or "off", then it will overwrite

- Channel (int): The channel to add a state to
- Start (float): The start time in clock cycles
- Duration (float): The duration in clock cycles

---

### method addEmptyState(Channel)

- Adds an empty pulse
- Channel (int): The channel to add a state to

---

### method setState(Channel, State)

Sets the state of the FPGA channel
- Channel (int): The channel to set the state for
- State (str / list of 2-tuple of int): The state to set

---

### method setDC(Channel)

Sets the state to DC of the FPGA channel

- Channel (int): The channel to set the state for

---

### method setOff(Channel)

Sets the state to OFF of the FPGA channel

- Channel (int): The channel to set the state for

---

### method setCalibrationMode(Channel, Value)

Sets the calibration mode for a channel

- Channel (int): The channel to set the state for
- Value (bool): True if calibration mode should be on, False if it should be off and None if cannot enter this mode

---

### method setInvertClock(Channel, Value)

Sets the clock inversion for a channel

- Channel (int): The channel to set the state for
- Value (bool): True if clock inversion should be on, False if it should be off and None if cannot enter this mode

---

### method apply(UseQueue = True)

Apply the sequences to the FPGA channels

- UseQueue (bool): Whether to run the command through the queue or not    

---

### property FPGA (timeBandit)

The timeBandit associated with this sequence

---

### property states (list of (list of 2-tuple of float / str))

The list of the states for each channel

---

### property calibrationModes (list of bool)

The calibration modes for each channel

---

### property invertClocks (list of bool)

The clock inversion modes for each channel

---

### property sequenceLength (int)

The sequence length for this sequence

---
---

## FPGAChannel(FPGA, Channel, MemoryOffset, ClockPartition = 1, ModeMemoryOffset = 0, MaxLength = 4)

A generic FPGA channel for the TimeBandit

- FPGA (timeBandit): The FPGA it is connected to
- Channel (int): The channel ID of this channel
- MemoryOffset (int): The memory offset on the FPGA
- ClockPartition (int): The number of partitions that each lock cycle can be divided into
- ModeMemoryOffset (int): The offset relative to MemoryOffset of the configuration bits
- MaxLength (int): The maximum number of pulses

---

### method generateState(Start, Stop, SequenceLength = None, Calibrating = None)

Generates a single pulse

- Start (float): The start time in ns, will be rounded down to nearest clock cycle
- Stop (float): The stop time in ns, will be rounded up to nearest clock cycle
- SequenceLength (int): The length of the sequence in input clock cycles, if None then the current length will be used
- Calibrating (bool); If True then it will create calibration pulses

Returns the pulse as a 2-tuple of float

---

### method generateStateWithDuration(Start, Duration, SequenceLength = None, Calibrating = None)

Generates a single pulse

- Start (float): The start time in ns, will be rounded down to nearest clock cycle
- Duration (float): The duration in ns, will be rounded up to nearest clock cycle
- SequenceLength (int): The length of the sequence in input clock cycles, if None then the current length will be used
- Calibrating (bool); If True then it will create calibration pulses

Returns the pulse as a 2-tuple of float

---

### method generateBaseState(Start, Stop, SequenceLength = None, Calibrating = None)

Generates a single pulse

- Start (float): The start time in clock cycles, will be rounded down to nearest clock cycle
- Stop (float): The stop time in clock cycles, will be rounded up to nearest clock cycle
- SequenceLength (int): The length of the sequence in input clock cycles, if None then the current length will be used
- Calibrating (bool); If True then it will create calibration pulses

Returns the pulse as a 2-tuple of float

---

### method generateBaseStateWithDuration(Start, Duration, SequenceLength = None, Calibrating = None)

Generates a single pulse

- Start (float): The start time in clock cycles, will be rounded down to nearest clock cycle
- Duration (float): The duration in clock cycles, will be rounded up to nearest clock cycle
- SequenceLength (int): The length of the sequence in input clock cycles, if None then the current length will be used
- Calibrating (bool); If True then it will create calibration pulses

Returns the pulse as a 2-tuple of float

---

### method setState(Values, UseQueue = True)

Sets the state of the channel

- Values (list of 2-tuple of float): The state, a list of start, stop times in ns
- UseQueue (bool): Whether to run the command through the queue or not, ignored if the device was initialized with UseQueue = False

---

### method setStateWithDuration(Values, UseQueue = True)

Sets the state of the channel

- Values (list of 2-tuple of float): The state, a list of start, duration times in ns
- UseQueue (bool): Whether to run the command through the queue or not, ignored if the device was initialized with UseQueue = False

---

### method setBaseState(Values, UseQueue = True)

Sets the state of the channel

- Values (list of 2-tuple of float): The state, a list of start, stop in clock cycles
- UseQueue (bool): Whether to run the command through the queue or not, ignored if the device was initialized with UseQueue = False

---

### method setBaseStateWithDuration(Values, UseQueue = True)

Sets the state of the channel

- Values (list of 2-tuple of float): The state, a list of start, duration in clock cycles
- UseQueue (bool): Whether to run the command through the queue or not, ignored if the device was initialized with UseQueue = False

---

### method setDC(UseQueue = True)

Sets the state to be DC

- UseQueue (bool): Whether to run the command through the queue or not, ignored if the device was initialized with UseQueue = False

---

### method setOff(UseQueue = True)

Sets the state to be off

- UseQueue (bool): Whether to run the command through the queue or not, ignored if the device was initialized with UseQueue = False

---

### method applyState(State, UseQueue = True)

Applies a final state

- State (list of 2-tuple of float): The list of pulses, each containing start and stop times in clock cycles
- UseQueue (bool): Whether to run the command through the queue or not, ignored if the device was initialized with UseQueue = False

---

### method getState()

Gets the currently applied state

Returns the state as a list

---

### method update(UseQueue = True)

Updates the state of the channel

- UseQueue (bool): Whether to run the command through the queue or not, ignored if the device was initialized with UseQueue = False

---

### property FPGA (timeBandit)

The FPGA this channel is a part of

---

### property channel (int)

The channel ID of this channel

---

### property clockPartition (int)

The number of partitions it splits each clock into

---
---

## FPGAChannelPulse(FPGA, Channel, MemoryOffset)

A pulsed FPGA channel for the timeBandit. A maximum of 4 pulses are allowed and start/stop must be given in integer values corresponding to clock cycles (4 clock cycles per input pulse)

- FPGA (timeBandit): The FPGA it is connected to
- Channel (int): The channel ID of this channel
- MemoryOffset (int): The memory offset on the FPGA

Inherits from FPGAChannel

---

### method setInvertClock(Value, UseQueue = True)

Inverts the clock

- Value (bool): True if the clock should be inverted
- UseQueue (bool): Whether to run the command through the queue or not, ignored if the device was initialized with UseQueue = False

---

### method getInvertClock()

Gets the invert clock

Returns the invert clock as a bool

---
---

## FPGAChannelPhasedPulse(FPGA, Channel, MemoryOffset, PhaseMemoryOffset, CalibrationData, *args, **kwargs)

A phased pulsed FPGA channel for the timeBandit.A maximum of 8 pulses are allowed and start/stop must be given in steps of 1/24 where 24/24 corresponding to a clock cycle (4 clock cycles per input pulse)

- FPGA (timeBandit): The FPGA it is connected to
- Channel (int): The channel ID of this channel
- MemoryOffset (int): The memory offset on the FPGA
- PhaseMemoryOffset (int): The memory offset for 
- CalibrationData (16-tuple of int): The phase calibration data

Inherits from FPGAChannel

---

### method startCalibration()

Enter calibration mode, here the step size is 1/256 and the decimal part is the uint8 given as the phase

---

### method stopCalibration()

Exits calibration mode

---
---

## timeBandit(Port, CalibrationData = (0,) * 16, Channel = 1, ClockFrequency = 50e6, ClocksPerBase = 4, Timeout = 1, ReconnectTries = 100, ReconnectDelay = 1, MaxAttempts = 100, AttemptDelay = 1, UseQueue = True, Empty = False, DeviceName = "TimeBandit", ID = None)

Controls the time bandit FPGA

- Port (str): The name of the COM port through which to access the serial connection
- CalibrationData (16-tuple of int): The calibration data for the phase channel
- Channel (int): The default counter channel, must be 0 or 1
- ClockFrequency (float): The frequency of the base clock
- ClocksPerBase (int): The number of clock cycles per base clock
- Timeout (float): The timeout time for the connection, must not be negative
- ReconnectTries (int): How many times to attempt to reconnect if it disconnects, must not be smaller than 0
- ReconnectDelay (float): The delay in seconds between each reconnect attempt, must not be negative
- MaxAttempts (int): The maximum number attempts to send a command before giving up, must not be smaller than 1
- AttemptDelay (float): The delay in seconds between each attempt to send a command, must not be negative
- UseQueue (bool): If True then it will set up a queue which can be used in the sendCommand method, if False the UseQueue in sendCommand is ignored
- Empty (bool): If True then it will not communicate with the device
- DeviceName (str): The name of the device, only used for error messages
- ID (str): The ID name for the device, only used for displaying infomation

Inherits from connections.serial

---

### method setDefaultChannel(Channel)

Sets the default channel, it must be 0 or 1

- Channel (int): The channel to set

---

### method getDefaultChannel()

Gets the default channel

Returns the default channel as an int

---

### method updateMemory(Address, Byte, UseQueue = True)

Updates one byte of memory on the FPGA

- Address (int): The address to write to, must be smaller than 256
- Byte (int): The byte to set, must be smaller than 256
- UseQueue (bool): Whether to run the command through the queue or not, ignored if the device was initialized with UseQueue = False

---

### method updateMemory2(Address, Bytes, UseQueue = True)

Updates two bytes of memory on the FPGA

- Address (int): The address to write to, must be smaller than 256
- Bytes (int): The bytes to set, must be smaller than 256^2
- UseQueue (bool): Whether to run the command through the queue or not, ignored if the device was initialized with UseQueue = False

---

### method resync(UseQueue = True)

Resynchronizes the FPGA to the external clock

- UseQueue (bool): Whether to run the command through the queue or not, ignored if the device was initialized with UseQueue = False

---

### method setIntegrationTime(Value, UseQueue = True)

Sets the integration time of the FPGA

- Value (float): The time in seconds, must be a multiple of 0.01 and be maximally 2.55
- UseQueue (bool): Whether to run the command through the queue or not, ignored if the device was initialized with UseQueue = False

---

### method getIntegrationTime()

Gets the last integration time set

Returns the integration time as a float

---

### method getCounts(UseQueue = True)

Gets the counts from both channels

- UseQueue (bool): Whether to run the command through the queue or not, ignored if the device was initialized with UseQueue = False

Returns a list of ints of length 2 with the counts

---

### method getDefaultCount(UseQueue = True)

Gets counts from default channel

- UseQueue (bool): Whether to run the command through the queue or not, ignored if the device was initialized with UseQueue = False

Returns the counts as an int

---

### method setSequenceLength(Value, UseQueue = True)

The length of a sequence in units of clock cycles

- Value (int): The number of clock cycles per sequence
- UseQueue (bool): Whether to run the command through the queue or not, ignored if the device was initialized with UseQueue = False

---

### method getSequenceLength()

Gets the last selected sequence length

Returns the sequence length as an int

---

### method getClockFrequency()

Gets the base clock frequency

Returns the base clock frequency as a float

---

### method getClocksPerBase()

Gets the number of clocks per base clock cycle

Returns the clocks per base period as an int

---

### method sendSettings(UseQueue = True)

Resend all settings, useful for when FPGA lost power

- UseQueue (bool): Whether to run the command through the queue or not, ignored if the device was initialized with UseQueue = False

---

### method setOutputClockLevel(Level, UseQueue = True)

Sets the output clock level

- Level (str): Either off, safe_on or always_on
- UseQueue (bool): Whether to run the command through the queue or not, ignored if the device was initialized with UseQueue = False

---

### method setOutputClockPhase(Phase, UseQueue = True)

Sets the phase of the output clock

- Phase (int): The phase to set, must be bewteen 0 and 255
- UseQueue (bool): Whether to run the command through the queue or not, ignored if the device was initialized with UseQueue = False

---

### method updateOutputClock(UseQueue = True)

Updates the output clock

- UseQueue (bool): Whether to run the command through the queue or not, ignored if the device was initialized with UseQueue = False

---

### property CH (list of FPGAChannel)

The channels for the timeBandit

---
---

## SNSPD(IP, Group, BufferSize = 4096, Timeout = 1, ReconnectTries = 100, ReconnectDelay = 1, MaxAttempts = 100, AttemptDelay = 1, UseQueue = True, Empty = False, DeviceName = "SNSPD", ID = None)

Controls the delatching and bias current of the SNSPD detector

- IP (str): The IP of the socket connection
- Group (str): A or B, the detector group to use
- BufferSize (int): The size of the buffer when getting data
- Timeout (float): The timeout in seconds
- ReconnectTries (int): How many times to attempt to reconnect if it disconnects, must not be smaller than 0
- ReconnectDelay (float): The delay in seconds between each reconnect attempt, must not be negative
- MaxAttempts (int): The maximum number attempts to send a command before giving up, must not be smaller than 1
- AttemptDelay (float): The delay in seconds between each attempt to send a command, must not be negative
- UseQueue (bool): If True then it will set up a queue which can be used in the sendCommand method, if False the UseQueue in sendCommand is ignored
- Empty (bool): If True then it will not communicate with the device
- DeviceName (str): The name of the device, only used for error messages
- ID (str): The ID name for the device, only used for displaying infomation

Inherits from connections.socket

---

### method delatch(Channel, UseQueue = True)

Delatches a channel

- Channel (int): The channel to delatch
- UseQueue (bool): Whether to run the command through the queue or not, ignored if the device was initialized with UseQueue = False

---

### method setBias(Channel, Bias, UseQueue = True)

Sets the bias current of the SNSPD

- Channel (int): The channel to delatch
- Bias (float): The bias current to set
- UseQueue (bool): Whether to run the command through the queue or not, ignored if the device was initialized with UseQueue = False

---
---

## rotationStage()

A generic rotation stage controller

---

### method home()

Homes the device

---

### method moveTo(Position)

Moves the device to a specified position

- Position (float): The position to set

---

### method getPosition()

Gets the current position of the rotation stage

Returns the position as a float

---

### method move(Distance)

Moves the rotation stage relative to its original position

- Distance (float): The distance it should move by

---
---

## kinesisRotationStage(SerialNumber, Timeout = 10, UseQueue = True, Empty = False, DeviceName = "KDC101", ID = None)

A controller for a thorlabs kinesis rotation stage

- SerialNumber (str): The serial number of the device
- Timeout (float): The timeout time in seconds
- UseQueue (bool): If True then it will set up a queue which can be used in the sendCommand method, if False the UseQueue in sendCommand is ignored
- Empty (bool): If True then it will not communicate with the device
- DeviceName (str): The name of the device, only used for error messages
- ID (str): The ID name for the device, only used for displaying infomation    

Inherits from rotationStage and connections.external

---

### method home(UseQueue = True)

Homes the device

- UseQueue (bool): Whether to run the command through the queue or not, ignored if the device was initialized with UseQueue = False

---

### method moveTo(Position, UseQueue = True)

Moves the device to a specified position

- Position (float): The position to set
- UseQueue (bool): Whether to run the command through the queue or not, ignored if the device was initialized with UseQueue = False

---

### method getPosition(UseQueue = True)

Gets the current position of the rotation stage

- UseQueue (bool): Whether to run the command through the queue or not, ignored if the device was initialized with UseQueue = False

Returns the position as a float

---

### method move(Distance, UseQueue = True)

Moves the rotation stage relative to its original position

- Distance (float): The distance it should move by
- UseQueue (bool): Whether to run the command through the queue or not, ignored if the device was initialized with UseQueue = False

---
---

## ELLOControl(SerialNumber, Timeout = 10, UseQueue = True, Empty = False, DeviceName = "ELLO", ID = None)

A controller for an ELLO control board

- SerialNumber (str): The serial number of the device
- Timeout (float): The timeout in seconds
- UseQueue (bool): If True then it will set up a queue which can be used in the sendCommand method, if False the UseQueue in sendCommand is ignored
- Empty (bool): If True then it will not communicate with the device
- DeviceName (str): The name of the device, only used for error messages
- ID (str): The ID name for the device, only used for displaying infomation    

Inherits from connections.external

---

### method getControl(Address, DeviceName = "ELLO", ID = None)

Creates a controller for a single rotation stage

- Address (int): The address of the stage
- DeviceName (str): The name of the device, only used for error messages
- ID (str): The ID name for the device, only used for displaying infomation    

Returns the ELLO controller

---

### method home(Address = 0, UseQueue = True)

Homes the device

- Address (int): The address of the device to access
- UseQueue (bool): Whether to run the command through the queue or not, ignored if the device was initialized with UseQueue = False

---

### method moveTo(Position, Address = 0, UseQueue = True)

Moves the device to a specified position

- Position (float): The position to set
- Address (int): The address of the device to access
- UseQueue (bool): Whether to run the command through the queue or not, ignored if the device was initialized with UseQueue = False

---

### method getPosition(Address = 0, UseQueue = True)

Gets the current position of the rotation stage

- Address (int): The address of the device to access
- UseQueue (bool): Whether to run the command through the queue or not, ignored if the device was initialized with UseQueue = False

Returns the position as a float

---

### method move(Distance, Address = 0, UseQueue = True)

Moves the rotation stage relative to its original position

- Distance (float): The distance it should move by
- Address (int): The address of the device to access
- UseQueue (bool): Whether to run the command through the queue or not, ignored if the device was initialized with UseQueue = False

---
---

## ELLO(Device, Address, DeviceName = "ELLO", ID = None)

A controller for a single ELLO rotation stage, should be initialized from ELLOControl.getControl

- Device (ELLOControl): The device to control
- Address (int): The address of the stage
- DeviceName (str): The name of the device, only used for error messages
- ID (str): The ID name for the device, only used for displaying infomation    

Inherits from rotationStage and connections.deviceBase

---

### method home(UseQueue = True)

Homes the device

- UseQueue (bool): Whether to run the command through the queue or not, ignored if the device was initialized with UseQueue = False

---

### method moveTo(Position, UseQueue = True)

Moves the device to a specified position

- Position (float): The position to set
- UseQueue (bool): Whether to run the command through the queue or not, ignored if the device was initialized with UseQueue = False

---

### method getPosition(UseQueue = True)

Gets the current position of the rotation stage

- UseQueue (bool): Whether to run the command through the queue or not, ignored if the device was initialized with UseQueue = False

Returns the position as a float

---

### method move(Distance, UseQueue = True)

Moves the rotation stage relative to its original position

- Distance (float): The distance it should move by
- UseQueue (bool): Whether to run the command through the queue or not, ignored if the device was initialized with UseQueue = False

---
---

## timeTagger(DefaultChannel = 1, DefaultIntegrationTime = 1, ClockChannel = 1, DefaultGates = [], BinWidth = 4, DefaultCorrelationBins = 2500, UseQueue = True, Empty = False, DeviceName = "TimeTagger", ID = None)

Controls the time tagger

- DefaultChannel (int): The default channel to get data from
- DefaultIntegrationTime (float): The default integration time in seconds
- ClockChannel (int): The default clock channel
- DefaultGates (list of 2-tuple of int): The default gates in pico seconds
- BinWidth (int): The width of a bin in ps
- DefaultCorrelationBins (int): The number of correlation bins to use by default
- UseQueue (bool): If True then it will set up a queue which can be used in the sendCommand method, if False the UseQueue in sendCommand is ignored
- Empty (bool): If True then it will not communicate with the device
- DeviceName (str): The name of the device, only used for error messages
- ID (str): The ID name for the device, only used for displaying infomation    

Inherits from connections.external

---

### method sample(Sampler, IntegrationTime, UseQueue = True)

Samples from a sampler and waits until it is done

- Sampler (TimeTagger aquisition class): A class with .isRunning() and .startFor(IntTime) function
- IntegrationTime (float): The integration time in seconds
- UseQueue (bool): Whether to run the command through the queue or not, ignored if the device was initialized with UseQueue = False

---

### method calibrate(UseQueue = True)

Gets the jitters of all the channels

- UseQueue (bool): Whether to run the command through the queue or not, ignored if the device was initialized with UseQueue = False

Returns the jitters of all the channels as a list of ints

---

### method checkOverflows(UseQueue = True)

Checks if any overflows occured and prints if they have

- UseQueue (bool): Whether to run the command through the queue or not, ignored if the device was initialized with UseQueue = False

---

### method getCount(Channels = None, IntegrationTime = None, UseQueue = True)

Gets the count rates of some channels

- Channels (int/list of int): The channel or channels to use, if None it will use the default
- IntegrationTime (float): The integration time in seconds, if None it will use the default
- UseQueue (bool): Whether to run the command through the queue or not, ignored if the device was initialized with UseQueue = False

Returns the counts for all channels as a list of ints

---

### method getGatedCount(ClockChannel = None, Channel = None, IntegrationTime = None, Gates = None, UseQueue = True)

Gets the count within the specified gates

- ClockChannel (int): The channel to use for the clock
- Channel (int): The channel to get data from
- IntegrationTime (float): The integration time for the histogram
- Gates (list of 2-tuple of int): List of gates where each gate defines the start and end time of data aquisition
- UseQueue (bool): Whether to run the command through the queue or not, ignored if the device was initialized with UseQueue = False

Returns the gated count for the channel as an int

---

### method setDefaultChannel(Channel, UseQueue = True)

Sets the default channel to use

- Channel (int): The channel to set
- UseQueue (bool): Whether to run the command through the queue or not, ignored if the device was initialized with UseQueue = False

---

### method getDefaultChannel(UseQueue = True)

Gets the default channel

- UseQueue (bool): Whether to run the command through the queue or not, ignored if the device was initialized with UseQueue = False

Returns the default channel as an int

---

### method setClockChannel(Channel, UseQueue = True)

Sets the default clock channel

- Channel (int): The channel to set
- UseQueue (bool): Whether to run the command through the queue or not, ignored if the device was initialized with UseQueue = False

---

### method getClockChannel(UseQueue = True)

Gets the default clock channel

- UseQueue (bool): Whether to run the command through the queue or not, ignored if the device was initialized with UseQueue = False

Return the clock channel as an int

---

### method setDefaultIntegrationTime(IntegrationTime, UseQueue = True)

Sets the default integration time

- IntegrationTime (float): The integration time in seconds
- UseQueue (bool): Whether to run the command through the queue or not, ignored if the device was initialized with UseQueue = False

---

### method getDefaultIntegrationTime(UseQueue = True)

Gets the default integration time

- UseQueue (bool): Whether to run the command through the queue or not, ignored if the device was initialized with UseQueue = False

Returns the integration time in seconds as a float

---

### method setDefaultGates(Gates, UseQueue = True)

Sets the default gates

- Gates (list of 2-tuple of float): List of gates of (StartTime, EndTime) in nano seconds
- UseQueue (bool): Whether to run the command through the queue or not, ignored if the device was initialized with UseQueue = False

---

### method getDefaultGates(UseQueue = True)

Gets the default gates

- UseQueue (bool): Whether to run the command through the queue or not, ignored if the device was initialized with UseQueue = False

Returns the default gates as a list of 2-tuple of float

---

### method setDefaultCorrelationBins(BinCount, UseQueue = True)

Sets the default correlation bin count

- BinCount (int): The number of bins
- UseQueue (bool): Whether to run the command through the queue or not, ignored if the device was initialized with UseQueue = False

---

### method getDefaultCorrelationBins(UseQueue = True)

Gets the default correlation bin count

- UseQueue (bool): Whether to run the command through the queue or not, ignored if the device was initialized with UseQueue = False

Returns the default correlation bin count as an int

---

### method setBinWidth(Value, UseQueue = True)

Sets the bin width (resolution)

- Value (int): The bin width in ps
- UseQueue (bool): Whether to run the command through the queue or not, ignored if the device was initialized with UseQueue = False

---

### method getBinWidth(UseQueue = True)

Gets the bin width (resolution)

- UseQueue (bool): Whether to run the command through the queue or not, ignored if the device was initialized with UseQueue = False

Returns the bin width in ps as an int

---

### method setTriggerLevel(Channel, Level, UseQueue = True)

Sets the trigger level of a channel

- Channel (int): The channel to apply to
- Level (float): The voltage level for the trigger
- UseQueue (bool): Whether to run the command through the queue or not, ignored if the device was initialized with UseQueue = False

---

### method getTriggerLevel(Channel, UseQueue = True)

Gets the trigger level of a channel

- Channel (int): The channel to get it from
- UseQueue (bool): Whether to run the command through the queue or not, ignored if the device was initialized with UseQueue = False

Returns the trigger level for the specified channel as a float

---

### method setTriggerMode(Channel, Mode, UseQueue = True)

Sets the trigger mode for a channel

- Channel (int): The channel to set the trigger mode for
- Mode (str): The mode of the channel, either "rising" or "falling"
- UseQueue (bool): Whether to run the command through the queue or not, ignored if the device was initialized with UseQueue = False

---

### method getTriggerMode(Channel, UseQueue = True)

Gets the trigger mode for a channel

- Channel (int): The channel to get the trigger mode for
- UseQueue (bool): Whether to run the command through the queue or not, ignored if the device was initialized with UseQueue = False

Returns the trigger mode as a string

---

### method setDeadTime(Channel, DeadTime, UseQueue = True)

Sets the dead time of a channel

- Channel (int): The channel to apply it to
- DeadTime (float): The dead time in nano seconds
- UseQueue (bool): Whether to run the command through the queue or not, ignored if the device was initialized with UseQueue = False

---

### method getDeadTime(Channel, UseQueue = True)

Gets the dead time of a channel

- Channel (int): The channel to get it from
- UseQueue (bool): Whether to run the command through the queue or not, ignored if the device was initialized with UseQueue = False

Returns the dead time in ns for the specified channel as a float

---

### method setChannelDelay(Channel, Delay, UseQueue = True)

Sets an artificial delay of a channel

- Channel (int): The channel to set it for
- Delay (float): The delay time in nano seconds
- UseQueue (bool): Whether to run the command through the queue or not, ignored if the device was initialized with UseQueue = False

---

### method getChannelDelay(Channel, UseQueue = True)

Gets the delay of a channel

- Channel (int): The channel to get it from
- UseQueue (bool): Whether to run the command through the queue or not, ignored if the device was initialized with UseQueue = False

Returns the delay in ns of the specified channel as a float

---

### method getClockRate(ClockChannel = None, IntegrationTime = 0.05, UseQueue = True)

Gets the clock rate

- ClockChannel (int): The channel to use for the clock
- ClockRate (float): The clock rate for the histogram, if not given then it will calculate it itself    
- UseQueue (bool): Whether to run the command through the queue or not, ignored if the device was initialized with UseQueue = False

Returns the clock rate as a float in Hz

---

### method getHistogram(ClockChannel = None, Channel = None, IntegrationTime = None, Gates = None, UseQueue = True)

Gets a histogram

- ClockChannel (int): The channel to use for the clock
- Channel (int): The channel to get data from
- IntegrationTime (float): The integration time for the histogram
- Gates (list of 2-tuple of int): List of gates where each gate defines the start and end time of data aquisition
- ClockRate (float): The clock rate for the histogram, if not given then it will calculate it itself
- UseQueue (bool): Whether to run the command through the queue or not, ignored if the device was initialized with UseQueue = False

Returns (Bins, Times) where Bins is a list of ints of the counts in each bin and Times is a list of floats of the times for each bin in ns

---

### method getHistogramBins(ClockChannel = None)

Gets the histogram bins times

- ClockChannel (int): The channel to use for the clock
- ClockRate (float): The clock rate for the histogram, if not given then it will calculate it itself
- UseQueue (bool): Whether to run the command through the queue or not, ignored if the device was initialized with UseQueue = False

Returns a numpy array with the times of each bin

---

### method getCorrelations(ChannelStart = None, ChannelStop = None, BinCount = None, IntegrationTime = None, UseQueue = True)

Gets the correlation between 2 channels, set them equal for autocorrelations

- ChannelStart (int): The channel for which start clicks are detected, if None it will use the default channel
- ChannelStop (int): The channel for which stop clicks are detected, if None it will use the default channel
- BinCount (int): The number of bins to use in the correlations, if None it will use the default bin count
- IntegrationTime (float): The time to run the experiment for in seconds, if None use the default integration time
- UseQueue (bool): Whether to run the command through the queue or not, ignored if the device was initialized with UseQueue = False

Returns (Counts (list of int), NormCounts (list of float), Delays (list of float)) where Counts is the number of correlations in each bin, NormCounts is the number of correlations in each bin normalized to the total number of single detection events, Delays is the delay time in ns between the 2 signals for each bin

---

### method initStream(MaxSize = 1000000, Channels = [], UseQueue = True)

Initialize a stream to gather data through

- MaxSize (int): The maximum allowed number of events within the stream
- Channels (list of int): A list of all the channels to get data from, leave empty for all channels
- UseQueue (bool): Whether to run the command through the queue or not, ignored if the device was initialized with UseQueue = False

---

### method startStream(IntegrationTime = None, UseQueue = True)

Starts the stream and notes down when it is done

- IntegrationTime (float): The integration time in seconds, None to use default
- UseQueue (bool): Whether to run the command through the queue or not, ignored if the device was initialized with UseQueue = False

---

### method getData(UseQueue = True)

Gets the data from the stream after waiting for it to finish, returns Timestamps, Channels which are both lists as long as the number of events

- UseQueue (bool): Whether to run the command through the queue or not, ignored if the device was initialized with UseQueue = False

Returns (Timestamps (list of float), Channels (list of int)) where Timestamps is a list of timestamps for each event and Channels is a list of same length with the channel ID that triggered each event

---
---

## AWG(IP, DefaultChannel = 1, TriggerLevel = 0.4, TriggerDelay = 0, MaxSampleFrequency = 6.16, ChannelCount = 4, Timeout = 1, ReconnectTries = 100, ReconnectDelay = 1, MaxAttempts = 100, AttemptDelay = 1, UseQueue = True, Empty = False, DeviceName = "AWG", ID = None)

Controller for an Active Technologies AWG

- IP (str): The IP of the AWG
- DefaultChannel (int): The default channel to use
- TriggerLevel (float): The trigger level for the external clock
- TriggerDelay (float): The delay of the trigger in seconds
- MaxSampleFrequency (float): The maximum allowed sampling frequency
- ChannelCount (int): The number of channels
- Timeout (float): The timeout time for the connection, must not be negative
- ReconnectTries (int): How many times to attempt to reconnect if it disconnects, must not be smaller than 0
- ReconnectDelay (float): The delay in seconds between each reconnect attempt, must not be negative
- MaxAttempts (int): The maximum number attempts to send a command before giving up, must not be smaller than 1
- AttemptDelay (float): The delay in seconds between each attempt to send a command, must not be negative
- UseQueue (bool): If True then it will set up a queue which can be used in the sendCommand method, if False the UseQueue in sendCommand is ignored
- Empty (bool): If True then it will not communicate with the device
- DeviceName (str): The name of the device, only used for error messages
- ID (str): The ID name for the device, only used for displaying infomation

Inherits from connections.visa

---

### method setDefaultChannel(Channel)

Sets the default channel

- Channel (int): The default channel

---

### method getDefaultChannel()

Gets the default channel

Returns the default channel as an int

---

### method setMode(Mode, UseQueue = True)

Sets the run mode

- Mode (str): The new mode
- UseQueue (bool): Whether to run the command through the queue or not, ignored if the device was initialized with UseQueue = False

---

### method getMode(UseQueue = True)

Gets the run mode

- UseQueue (bool): Whether to run the command through the queue or not, ignored if the device was initialized with UseQueue = False

Returns the run mode as a string

---

### method setSampleFrequency(Value, UseQueue = True)

Sets the sampling frequency in GHz

- Value (float): The sampling frequency
- UseQueue (bool): Whether to run the command through the queue or not, ignored if the device was initialized with UseQueue = False

---

### method getSampleFrequency(UseQueue = True)

Gets the sampling frequency in GHz
    
- UseQueue (bool): Whether to run the command through the queue or not, ignored if the device was initialized with UseQueue = False

Returns the sample frequency as a float

---

### method setRefClockRate(Value, UseQueue = True)

Sets the reference clock rate

- Value (float): The clock rate to set
- UseQueue (bool): Whether to run the command through the queue or not, ignored if the device was initialized with UseQueue = False

---

### method syncRefClock(UseQueue = True)

Syncs with the reference clock

- UseQueue (bool): Whether to run the command through the queue or not, ignored if the device was initialized with UseQueue = False

---

### method setTriggerValues(TriggerLevel, TriggerDelay = 0, UseQueue = True)

Sets all the trigger variables

- TriggerLevel (float): The trigger level for the external clock
- TriggerDelay (float): The delay for the trigger in seconds
- UseQueue (bool): Whether to run the command through the queue or not, ignored if the device was initialized with UseQueue = False

---

### method setOperatingMode(Mode, UseQueue = True)

Sets the operating mode
    
- Mode (str): The operating mode, either BB or RF
- UseQueue (bool): Whether to run the command through the queue or not, ignored if the device was initialized with UseQueue = False

---

### method getOperatingMode(UseQueue = True)

Gets the operating mode

- UseQueue (bool): Whether to run the command through the queue or not, ignored if the device was initialized with UseQueue = False

Returns the operating mode as a string


---

### method setBBAmplitude(Value, Channel = None, Entry = 1, UseQueue = True)

Sets the output amplitude in BB mode

- Value (float): The value of the amplitude
- Channel (int): The channel to set it for, None if it should use the default
- Entry (int): The entry to set it for
- UseQueue (bool): Whether to run the command through the queue or not, ignored if the device was initialized with UseQueue = False

---

### method setBBOffset(Value, Channel = None, Entry = 1, UseQueue = True)

Sets the output offset in BB mode

- Value (float): The value of the offset
- Channel (int): The channel to set it for, None if it should use the default
- Entry (int): The entry to set it for
- UseQueue (bool): Whether to run the command through the queue or not, ignored if the device was initialized with UseQueue = False

---

### method setBBMin(Value, Channel = None, Entry = 1, UseQueue = True)

Sets the output minimum voltage in BB mode

- Value (float): The value of the min voltage
- Channel (int): The channel to set it for, None if it should use the default
- Entry (int): The entry to set it for
- UseQueue (bool): Whether to run the command through the queue or not, ignored if the device was initialized with UseQueue = False

---

### method setBBMax(Value, Channel = None, Entry = 1, UseQueue = True)

Sets the output maximum voltage in BB mode

- Value (float): The value of the max voltage
- Channel (int): The channel to set it for, None if it should use the default
- Entry (int): The entry to set it for
- UseQueue (bool): Whether to run the command through the queue or not, ignored if the device was initialized with UseQueue = False

---

### method setRFAmplitude(IValue, QValue, Channel = None, Entry = 1, UseQueue = True)

Sets the output amplitude in RF mode

- IValue (float): The value of the I amplitude
- QValue (float): The value of the Q amplitude
- Channel (int): The channel to set it for, None if it should use the default
- Entry (int): The entry to set it for
- UseQueue (bool): Whether to run the command through the queue or not, ignored if the device was initialized with UseQueue = False

---

### method setRFOffset(IValue, QValue, Channel = None, Entry = 1, UseQueue = True)

Sets the output offset in RF mode

- IValue (float): The value of the I offset
- QValue (float): The value of the Q offset
- Channel (int): The channel to set it for, None if it should use the default
- Entry (int): The entry to set it for
- UseQueue (bool): Whether to run the command through the queue or not, ignored if the device was initialized with UseQueue = False

---

### method setRFMin(IValue, QValue, Channel = None, Entry = 1, UseQueue = True)

Sets the output minimum voltage in RF mode

- IValue (float): The value of the I min voltage
- QValue (float): The value of the Q min voltage
- Channel (int): The channel to set it for, None if it should use the default
- Entry (int): The entry to set it for
- UseQueue (bool): Whether to run the command through the queue or not, ignored if the device was initialized with UseQueue = False

---

### method setRFMax(IValue, QValue, Channel = None, Entry = 1, UseQueue = True)

Sets the output maximum voltage in RF mode

- IValue (float): The value of the I max voltage
- QValue (float): The value of the Q max voltage
- Channel (int): The channel to set it for, None if it should use the default
- Entry (int): The entry to set it for
- UseQueue (bool): Whether to run the command through the queue or not, ignored if the device was initialized with UseQueue = False

---

### method reset(UseQueue = True)

Removes all the waveforms

- UseQueue (bool): Whether to run the command through the queue or not, ignored if the device was initialized with UseQueue = False

---

### method on(Channel = None, UseQueue = True)

Turns a channel on

- Channel (int): The channel to set it for, None if it should use the default
- UseQueue (bool): Whether to run the command through the queue or not, ignored if the device was initialized with UseQueue = False

---

### method off(Channel = None, UseQueue = True)

Turns a channel off

- Channel (int): The channel to set it for, None if it should use the default
- UseQueue (bool): Whether to run the command through the queue or not, ignored if the device was initialized with UseQueue = False

---

### method run(UseQueue = True)

Sets the AWG to run

- UseQueue (bool): Whether to run the command through the queue or not, ignored if the device was initialized with UseQueue = False

---

### method stop(UseQueue = True)

Sets the AWG to stop

- UseQueue (bool): Whether to run the command through the queue or not, ignored if the device was initialized with UseQueue = False

---

### method wait(UseQueue = True)

Sets the AWG to wait

- UseQueue (bool): Whether to run the command through the queue or not, ignored if the device was initialized with UseQueue = False

Returns the wait flag

---

### method importWaveform(Waveform, Name, UseQueue = True)

- Send a waveform to the AWG
- Waveform (numpy.ndarray of uint16): The waveform to send
- Name (str): The name of the waveform

---

### method loadBBSequence(Sequence, UseQueue = True)

Loads an arbitrary waveform for baseband mode

- Sequence (AWGSequence): The sequence to load
- UseQueue (bool): Whether to run the command through the queue or not, ignored if the device was initialized with UseQueue = False

---

### method loadRFSequence(Sequence, UseQueue = True)

Loads an arbitrary waveform for RF mode

- Sequence (AWGSingleSequence): The sequence to load
- UseQueue (bool): Whether to run the command through the queue or not, ignored if the device was initialized with UseQueue = False

---

### method loadSequence(Sequence, UseQueue = True)

Loads an arbitrary waveform

- Sequence (AWGSingleSequence): The sequence to load
- UseQueue (bool): Whether to run the command through the queue or not, ignored if the device was initialized with UseQueue = False

---

### property maxSampleFrequency (float)

The maximum possible sampling frequency in GHz

---

### property currentSequence (str)

The name of the sequence applied, None if nothing is applied

---

### property channelCount (int)

The number of accessable channels

---

### property sequences (dict)

A dict with all the saved sequences of type AWGSequence

---
---

## AWGSingleSequence(Waveform)

A sequence for a single channel for the AWG

- Waveform (numpy.ndarray of float): The waveform of the sequence

---

### property waveform (numpy.ndarray of float)

The original data

---

### property normWaveform (numpy.ndarray of uint16)

The data scaled to an integer value with the lowest being 0 and the highest being 2^15-1

---

### min (float)

The minimum value of the data

---

### max (float)

The maximum value of the data

---
---

## AWGSequence(Device, Name, Period, *args, Mode = "BB", Entries = 1)

A sequence for an AWG

- Device (AWG): The AWG device
- Name (str): The name of this sequence, must be unique
- Period (float): The period of the sequence in ns
- Mode (str): BB: baseband mode, RF: radio frequency mode
- Entries (int): The number of entries to use

---

### staticmethod toIQ(Amplitude, Phase)

Converts amplitude and phase to I and Q

- Amplitude (float/numpy.ndarray of float): The amplitude value
- Phase (float/numpy.ndarray of float): The phase value

Returns (I, Q) both as floats/numpy.ndarray of float

---

### staticmethod fromIQ(I, Q)

Converts I and Q to amplitude and phase

- I (float/numpy.ndarray of float): The I value
- Q (float/numpy.ndarray of float): The Q value

Returns (amplitude, phase) both as floats/numpy.ndarray of float

---

### method apply(USeQueue = True)

Applies this sequence

- UseQueue (bool): Whether to run the command through the queue or not, ignored if the device was initialized with UseQueue = False    

---

### method addBasePulse(Start, Stop, Amplitude = 1, Phase = 0, Channel = 1, Entry = 1)

Adds a pulse to the sequence in units of clock cycles, Start is rounded down, Stop is rounded up

- Start (float): The start clock cycle of the pulse, it is rounded down to nearest clock cycle
- Stop (float): The stop clock cyle of the pulse, it is rounded up to nearest clock cycle
- Amplitude (float): The amplitude of the pulse in volts
- Phase (float): The phase of the RF signal, ignored on BB mode
- Channel (int): The channel to apply this to
- Entry (int): The entry to apply this to

---

### method addPulse(self, Start, Stop, Amplitude = 1, Phase = 0, Channel = 1, Entry = 1)

Adds a pulse to the sequence in units of ns, Start is rounded down, Stop is rounded up

- Start (float): The start time of the pulse, it is rounded down to nearest clock cycle
- Stop (float): The stop time of the pulse, it is rounded up to nearest clock cycle
- Amplitude (float): The amplitude of the pulse in volts
- Phase (float): The phase of the RF signal, ignored on BB mode
- Channel (int): The channel to apply this to
- Entry (int): The entry to apply this to

---

### method addBasePulseWithDuration(Start, Duration, Amplitude = 1, Phase = 0, Channel = 1, Entry = 1)

Adds a pulse to the sequence in units of clock cycles, Start is rounded down, Duration is rounded up

- Start (float): The start clock cycle of the pulse, it is rounded down to nearest clock cycle
- Duration (float): The duration cyle of the pulse, it is rounded up to nearest clock cycle
- Amplitude (float): The amplitude of the pulse in volts
- Phase (float): The phase of the RF signal, ignored on BB mode
- Channel (int): The channel to apply this to
- Entry (int): The entry to apply this to

---

### method addPulseWithDuration(Start, Duration, Amplitude = 1, Phase = 0, Channel = 1, Entry = 1)

Adds a pulse to the sequence in units of ns, Start is rounded down, Duration is rounded up

- Start (float): The start time of the pulse, it is rounded down to nearest clock cycle
- Duration (float): The duration of the pulse, it is rounded up to nearest clock cycle
- Amplitude (float): The amplitude of the pulse in volts
- Phase (float): The phase of the RF signal, ignored on BB mode
- Channel (int): The channel to apply this to
- Entry (int): The entry to apply this to

---

### method addDC(Amplitude = 1, Phase = 0, Channel = 1, Entry = 1)

Adds a DC signal in units of clock cycles

- Amplitude (float): The amplitude of the signal in volts
- Phase (float): The phase of the RF signal, ignored on BB mode
- Channel (int): The channel to apply this to
- Entry (int): The entry to apply this to

---

### property name (str)

The name of the sequence

---

### property device (AWG)

The AWG controller

---

### property sampleFreq (float)

The AWG sampling frequency in GHz

---

### property length (int)

The length of the sequence

---

### property mode (str)

The mode of the sequence

---

### property channelCount (int)

The number of channels

---

### property entryCount (int)

The number of entries

---

### property sequences (list of list of AWGSingleSequence/list of list of 2-tuple of AWGSingleSequence)

A list of all the sequences for each channel and entry, the outer list determine the entry and the inner list the channel. In BB mode it stores the waveforms, in RF mode in stores the (I, Q) waveforms

---
---
