# Documentation for functions

This is a collection of functions used within the equipment classes, these functions include response check functions and wrappers for socket servers

---
---

# Response Check Functions

All response check functions can be accessed under .responseCheck and returns the response checker which is a function of the type

## responseCheck(Class, Command, ReturnLines)

Checks if the return value was good

- Class (class): the class which received the response
- Command (str): The command string which was sent
- ReturnLines (list-str): A list of all the return lines, in some cases like dll this may also be other types

Returns None on success and a string with the error message on error

---

## default(Line = 0)

Creates a response check function that checks if it received any response

- Line (int): The line of the return string to check

Returns the response check function

---

## getValue(Line = 0)

Creates a response check function that checks if the return string is a finite float

- Line (int): The line of the return string to check

Returns the response check function

---

## getNumber(Line = 0)

Creates a response check function that checks if the return string is a not nan

- Line (int): The line of the return string to check

Returns the response check function

---

## getBool(Line = 0)

Creates a response check function that checks if the return string is a bool

- Line (int): The line of the return string to check

Returns the response check function

---

## matchValue(Value, GetFunc, args = [], kwargs = {}, Tol = 0.01)

Creates a response check function to check if values has been set correctly

- Value (float): The value to check
- GetFunc (func): The function to get the value
- args (tuple): The args for the GetFunc function
- kwargs (dict): The kwargs for the GetFunc function
- Tol (float): The relative tolerance, must not be smaller than 0

Returns the response check function

---

## matchVar(Value, GetFunc, args = [], kwargs = {})

Creates a response check function to check if a variable is set correctly

- Value (any): The value to check
- GetFunc (func): The function to get the value
- args (tuple): The args for the GetFunc function
- kwargs (dict): The kwargs for the GetFunc function

Returns the response check function

---

## matchReturn(Value, Line = 0)

Creates a response check function to check if the return string has a specific value

- Value (str): The value to match with
- Line (int): The line of the return string to check

Returns the response check function

---

## inList(List, Line = 0)

Creates a response check function to check if the return string is in a list of values

- List (list of str): The list to match with
- Line (int): The line of the return string to check

Returns the response check function

---

## delimCount(Count, Delimiter = ":", Line = 0)

Creates a response check function to check that the return string has the correct number of parts

- Count (int): The number of parts it should have
- Delimiter (str): The delimiter to split the parts
- Line (int): The line of the return string to use

Returns the response check function

---

## wavemeter(Line = 0)

Checks if a wavemeter got a correct response

- Line (int): The line of the return string to use

Returns the response check function

---

## DLCPro()

Checks if a DLCPro got a correct response

Returns the response check function

---

## timeBanditHandShake()

Checks if a TimeBandit got a successful handshake

Returns the response check function

---

## timeBanditUpdate()

Checks if a TimeBandit updated its memory

Returns the response check function

---
---

# Socket functions

A collection of functions meant to make it easier to set up a socket server, all socket functions can be accessed by .socket

---

## returnWrapper(Function)

A wrapper function to add error identifiers for a socket server method

- Function (func): The function to wrap

Returns the wrapped function whose new return value will be True, OldReturn

---

## infoWrapper(Function)

A wrapper function to add error identifiers for a socket server info converter

- Function (func): The function to wrap

Returns the wrapped function whose new return value will be True, OldReturn

---
---

# settingHandlers

A collection of functions to create setting handlers for various devices, all setting handler functions can be accessed by .settingHandlers

---

## keithly(Keithly, Name = "", Overwrites = dict(), Pause = dict())

Creates a setting handler for a keithly

The possible settings include:

- currentLimit (float): The current limit
- currentRange (float): The current range
- voltageLimit (float): The voltage limit
- voltage (float): The voltage

Function arguments:

- Keithly (controllers.keithly): The keithly device to control
- Name (str): The name in from of each setting
- Overwrites (dict of list of str): A dict containing the lists of overwrites for each handler
- Pause (dict of floats): A dict containing the time to pause after setting each parameter, defaults to 0

Returns the settings handler as a lab.settingHandler

---
---

## laser(Laser, Lockable = True, Name = "", Overwrites = dict(), Pause = dict())

Creates a setting handler for a laser

The possible settings include:

- frequency (float): The frequency of the laser
- active (bool): If True attempt to lock the frequence

Function arguments:

- Laser (equipment.laser): The laser to control
- Lockable (bool): If false then it will not try to lock the frequence
- Name (str): The name in from of each setting
- Overwrites (dict of list of str): A dict containing the lists of overwrites for each handler
- Pause (dict of floats): A dict containing the time to pause after setting each parameter, defaults to 0

Returns the settings handler as a lab.settingHandler

---
---

## power(PowerControl, Name = "", Overwrites = dict(), Pause = dict())

Creates a setting handler for a power controller

The possible settings include:

- power (float): The power of the laser
- active (bool): If True attempt to lock the power

Function arguments:

- PowerControl (equipment.powerControl): The power controller to control
- Name (str): The name in from of each setting
- Overwrites (dict of list of str): A dict containing the lists of overwrites for each handler
- Pause (dict of floats): A dict containing the time to pause after setting each parameter, defaults to 0

Returns the settings handler as a lab.settingHandler

---
---

## PCLaser(Laser, Lockable = True, Name = "", Overwrites = dict(), Pause = dict())

Creates a setting handler for a power controlled laser

The possible settings include:

- frequency (float): The frequency of the laser
- power (float): The power of the laser
- active (bool): If True attempt to lock the frequence and power

Function arguments:

- Laser (equipment.powerControlledLaser): The laser to control
- Lockable (bool): If false then it will not try to lock the frequence
- Name (str): The name in from of each setting
- Overwrites (dict of list of str): A dict containing the lists of overwrites for each handler
- Pause (dict of floats): A dict containing the time to pause after setting each parameter, defaults to 0

Returns the settings handler as a lab.settingHandler

---
---

## rotationStage(RotationStage, Name = "", Overwrites = dict(), Pause = dict())

Creates  a setting handler for a rotation stage

The possible settings include:

- zeroPosition (float): The position where angle 0 is
- position (float): The position to set the device to

Function arguments:

- RotationStage (controllers.rotationStage): The stage to control
- Name (str): The name in from of each setting
- Overwrites (dict of list of str): A dict containing the lists of overwrites for each handler
- Pause (dict of floats): A dict containing the time to pause after setting each parameter, defaults to 0

Returns the settings handler as a lab.settingHandler

---
---

## timeTagger(TimeTagger, ChannelCount, Name = "", Overwrites = dict(), Pause = dict())

Creates a setting handler for a time tagger

The possible settings include:

- channel (int): The default channel to use when getting counts
- integrationTime (float): The default integration time in ns
- clockChannel (int): The clock channel
- binWidth (int): The width of the bins in ps
- correlationBins (int): The number of default correlation bins, mutually exclusive with correlationTime
- correlationTime (float): The period in ns to use for max default correlation time, mutually exclusive with correlationBins
- CH[ID].triggerLevel (float): The trigger level in volts of channel ID
- CH[ID].triggerMode (str): "rising" or "falling" depending on how to trigger
- CH[ID].deadTime (float): The dead time in ns
- CH[ID].delay (float): The delay of the channel in ns

Function arguments:

- TimeTagger (controllers.timeTagger): The time tagger to control
- ChannelCount (int): The number of channels accessable
- Name (str): The name in from of each setting
- Overwrites (dict of list of str): A dict containing the lists of overwrites for each handler
- Pause (dict of floats): A dict containing the time to pause after setting each parameter, defaults to 0

Returns the settings handler as a lab.settingHandler

---
---

## photonSpot(SNSPD, ChannelCount, Name = "", Overwrites = dict(), Pause = dict())

Creates a setting handler for a Photon Spot SNSPD

The possible settings include:

- [A/B][ID].bias (float): The bias current of channel ID

Function arguments:

- SNSPD (controllers.SNSPD): The SNSPD device to control
- ChannelCount (int): The number of channels accessable
- Name (str): The name in from of each setting
- Overwrites (dict of list of str): A dict containing the lists of overwrites for each handler
- Pause (dict of floats): A dict containing the time to pause after setting each parameter, defaults to 0

Returns the settings handler as a lab.settingHandler

---
---

## timeBandit(FPGA, Sequences, SequenceArgs = tuple(), Name = "", Overwrites = dict(), Pause = dict())

Creates a setting handler for a timeBandit FPGA

The possible settings include:

- sequence (str): The sequence to run, "Name_Arg1_Arg2" will run Sequences["Name"](*SequenceArgs, Arg1, Arg2)

Function arguments:

- FPGA (equipment.timeBandit): The FPGA object
- Sequences (dict): Dictionary with all the possible sequences
- SequenceArgs (tuple): The first arguments to give the sequence function 
- Name (str): The name in from of each setting
- Overwrites (dict of list of str): A dict containing the lists of overwrites for each handler
- Pause (dict of floats): A dict containing the time to pause after setting each parameter, defaults to 0

Returns the settings handler as a lab.settingHandler

---
---

## AWG(Device, Sequences, SequenceArgs = tuple(), Name = "", Overwrites = dict(), Pause = dict())

Creates a setting handler for an AWG

The possible settings include:

- sequence (str): The sequence to run, "Name_Arg1_Arg2" will run Sequences["Name"](*SequenceArgs, Arg1, Arg2)

Function arguments:

- Device (equipment.AWG): The AWG object
- Sequences (dict): Dictionary with all the possible sequences
- SequenceArgs (tuple): The first arguments to give the sequence function 
- Name (str): The name in from of each setting
- Overwrites (dict of list of str): A dict containing the lists of overwrites for each handler
- Pause (dict of floats): A dict containing the time to pause after setting each parameter, defaults to 0

Returns the settings handler as a lab.settingHandler

---
---

## getSubDict(Dict, Name)

Gets a sub dict, extracts all items from a dict with key starting with Name and saves them in a new dict with the remainder of the key as the new key

- Dict (dict): The dictionary to look through
- Name (str): The name to be at the start of the keys to extract

Returns the new dictionary

---
---

# settingFinalizers

A collection of functions to create setting finalizers, all setting finalizer functions can be accessed by .settingFinalizers

---

## formatString(Value, Key, Settings)

Formats a string by taking every "{FormatName}" and looking up this field in "name1.name2" if key is "name1.name2.name3" and inserting this instead

- Value (str): The string to format
- Key (str): The key for this string
- Settings (lab.setting): The setting which this is found in

---
---

# time

A collection of functions to handle time events, can be accessed with .time

---

## sleep(Time)

Sleeps while still allowing plots to be controlled

- Time (float): The time to sleep, if negative or 0 then it will not sleep

---
---

## getCurrentTime()

Gets the current time as a string for saving files

Returns the current time as a string

---
---