# Documentation for exceptions

This is a collection of exceptions used in all of the other scripts

---
---

# Exceptions

---

## TypeDefError(VariableName, Variable, Type)

Used when the type of an arg is not correct

- VariableName (str): The name of the variable to display in the error message
- Variable (any): The variable that has a wrong type
- Type (type): The correct type of the variable

---

### property var (any)

The variable

---

### property varName (str)

The variable name

---

### property type (type)

The type

---
---

## ElementTypeError(VariableName, Variable, ElementID, Type)

Used when an element of a variable has a wrong type

- VariableName (str): The name of the variable to display in the error message
- Variable (any): The variable which has an element with a wrong type
- ElementID (int): The ID of the element with a wrong type
- Type (type): The correct type of the variable    

---

### property var (any)

The variable

---

### property varName (str)

The variable name

---

### property id (int)

The ID

---

### property type (type)

The type

---
---

## LengthError(VariableName, Variable, Length)

Used when a variable has a wrong length

- VariableName (str): The name of the variable to display in the error message
- Variable (any): The variable which has a wrong length
- Length (int): The correct length of the variable

---

### property var (any)

The variable

---

### property varName (str)

The variable name

---

### property length (int)

The length

---
---

## MinLengthError(VariableName, Variable, Length)

Used when a variable has length smaller that the min length

- VariableName (str): The name of the variable to display in the error message
- Variable (any): The variable which has a wrong length
- Length (int): The correct length of the variable

---

### property var (any)

The variable

---

### property varName (str)

The variable name

---

### property length (int)

The length

---
---

## MaxLengthError(VariableName, Variable, Length)

Used when a variable has length larger that the max length

- VariableName (str): The name of the variable to display in the error message
- Variable (any): The variable which has a wrong length
- Length (int): The correct length of the variable

---

### property var (any)

The variable

---

### property varName (str)

The variable name

---

### property length (int)

The length

---
---

## PropagationError(Error, Reason)

Used when an error occured and it should be propagated

- Error (Exception): The exception that occured
- Reason (str): A string describing what happened when the error occured

---

### property error (Exception)

The error

---

### property reason (str)

The reason

---
---

## NotRunningError(ObjectName, Object)

Used when trying to use an object which is no longer running

- ObjectName (str): The name of the object to display in the error message
- Object (any): The object which is no longer running  

---

### property obj (any)

The object

---

### property objName (str)

The object name

---
---

## KeywordError(KeywordName, Keyword, Valid = None)

Used when a keyword is not recognized

- KeywordName (str): The name of the keyword
- Keyword (str): The unknown keyword
- Valid (list of str): The list of valid keywords

---

### property key (str)

The keyword

---

### property keyName (str)

The keyword name

---

### property valid (list of str)

The valid keywords

---
---

## LargerVarError(SmallVariableName, SmallVariable, LargeVariableName, LargeVariable)

Used when one variable must be larger than another

- SmallVariableName (str): The name of the smallest variable
- SmallVariable (num): The value of the smallest variable
- LargeVariableName (str): The name of the largest variable
- LargeVariable (num): The value of the largest variable

---

### property minVar (num)

The small variable

---

### property minVarName (str)

The name of the small variable

---

### property maxVar (num)

The large variable

---

### property maxVarName (str)

The name of the large variable

---
---

## MinValueError(VariableName, Variable, Value)

Used when a value is too small

- VariableName (str): The name of the variable to display in the error message
- Variable (num): The variable which is too small
- Value (num): The minimum number

---

### property var (num)

The variable

---

### property varName (str)

The name of the variable

---

### property value (num)

The minimum value

---
---

## SharpMinValueError(VariableName, Variable, Value)

Used when a value is too small

- VariableName (str): The name of the variable to display in the error message
- Variable (num): The variable which is too small
- Value (num): The minimum number

---

### property var (num)

The variable

---

### property varName (str)

The name of the variable

---

### property value (num)

The minimum value

---
---

## RangeError(VariableName, Variable, MinValue, MaxValue)

Used when a value is not within a range

- VariableName (str): The name of the variable to display in the error message
- Variable (num): The variable which is too small
- MinValue (num): The minimum number
- MaxValue (num): The maximum number

---

### property var (num)

The variable

---

### property varName (str)

The name of the variable

---

### property min (num)

The minimum value

---

### property max (num)

The maximum value

---
---

## SharpRangeError(VariableName, Variable, MinValue, MaxValue)

Used when a value is not within a range

- VariableName (str): The name of the variable to display in the error message
- Variable (num): The variable which is too small
- MinValue (num): The minimum number
- MaxValue (num): The maximum number

---

### property var (num)

The variable

---

### property varName (str)

The name of the variable

---

### property min (num)

The minimum value

---

### property max (num)

The maximum value

---
---

## OpenError(DeviceName, Device)

Used when unable to open a device

- DeviceName (str): The name of the device to display in the error message
- Device (device): The device that cannot be opened

---

### property device (device)

The device this error occured for

---

### property deviceName (str)

The name of the device

---

### property message (str)

The error message

---
---

## CommunicationError(DeviceName, Device, Command, Message)

Used when a communication error has occured

- DeviceName (str): The name of the device to display in the error message
- Device (device): The device with a communication error
- Command (str): The command sent to the device
- Message (str): The message describing the communication error

---

### property device (device)

The device this error occured for

---

### property deviceName (str)

The name of the device

---

### property command (str)

The command sent to the device

---

### propery oldMessage (str)

The message describing the communication error

---

### property message (str)

The error message

---
---

## TimeoutError(DeviceName, Device)

Used when a device has timed out

- DeviceName (str): The name of the device to display in the error message
- Device (device): The device which has timed out

---

### property device (device)

The device this error occured for

---

### property deviceName (str)

The name of the device

---

### property message (str)

The error message

---
---

## ImplementationError(Name)

Used when a function is run which has not been implemented

- Name (str): The name of the function which has not been implemented

---

### property name (str)

The name of the function

---

### property message (str)

The error message

---
---

## StabilizeError(DeviceName, Device, Stabilizer)

Used when unable to stabilize a value

- DeviceName (str): The name of the device to display in the error message
- Device (device): The device which cannot stabilize
- Stabilizer (str): The name of the thing to stabilize

---

### property device (device)

The device this error occured for

---

### property deviceName (str)

The name of the device

---

### property stabil (str)

The name of the thing to stabilize

---

### property message (str)

The error message

---
---

## MultipleError(VariableName, Variable, Base)

Used when a variable must be a multiple of another number

- VariableName (str): The name of the variable to display in the error message
- Variable (num): The variable which is not a multiple
- Base (num): The number Variable must be a multiple of

---

### property var (any)

The variable

---

### property varName (str)

The variable name

---

### property base (int)

The number the variable must be a multiple of

---

### property message (str)

The error message

---
---

## FinishMeasurementError(DeviceName, Device)

Used when a measurement does not finish

- DeviceName (str): The name of the device to display in the error message
- Device (device): The device which cannot finish the measurement  

---

### property device (device)

The device this error occured for

---

### property deviceName (str)

The name of the device

---

### property message (str)

The error message

---
---

## WrongValueError(VariableName, Variable)

Used when a variable has an illigal value

- VariableName (str): The name of the variable to display in the error message
- Variable (num): The variable which is not a multiple    

---

### property var (any)

The variable

---

### property varName (str)

The variable name

---

### property message (str)

The error message

---
---

## InitializeError(DeviceName, Device)

Used when a device has not been initialized

- DeviceName (str): The name of the device to display in the error message
- Device (device): The device which cannot initialize

---

### property device (device)

The device this error occured for

---

### property deviceName (str)

The name of the device

---

### property message (str)

The error message

---
---

## OverflowError(DeviceName, Device)

Used when a measurement does not finish

- DeviceName (str): The name of the device to display in the error message
- Device (device): The device which has overflowed

---

### property device (device)

The device this error occured for

---

### property deviceName (str)

The name of the device

---

### property message (str)

The error message

---
---

## ExistError(Parameter, DeviceName, Device)

Used when a parameter already exists and cannot be reinitialized

- Parameter (str): The name of the parameter
- DeviceName (str): The name of the device to display in the error message
- Device (device): The device which already has this parameter    

---

### property device (device)

The device this error occured for

---

### property deviceName (str)

The name of the device

---

### property param (str)

The name of the parameter

---

### property message (str)

The error message

---
---

## IlligalCharError(Character, Text)

Used when an illigal character is found in a string

- Character (str): The illigal character
- Text (str): The text with the illigal character within

---

### property char (str)

The illigal character

---

### property text (str)

The text with the illigal character within

---

### property message (str)

The error message

---
---

## MethodError(DeviceName, Device, MethodName)

Used when a method for a device is called when not allowed

- DeviceName (str): The name of the device to display in the error message
- Device (device): The device which has illigal method 
- MethodName (str): The name of the illigal method     

---

### property device (device)

The device this error occured for

---

### property deviceName (str)

The name of the device

---

### property method (str)

The name of the method

---

### property message (str)

The error message

---
---

## PowerRangeError(DeviceName, Device)

When an equipment is out of range of its power

- DeviceName (str): The name of the device to display in the error message
- Device (device): The device which does not have enough power     

---

### property device (device)

The device this error occured for

---

### property deviceName (str)

The name of the device

---

### property message (str)

The error message

---
---

## LockError(DeviceName, Device)

When an equipment is unable to lock

- DeviceName (str): The name of the device to display in the error message
- Device (device): The device which cannot lock     

---

### property device (device)

The device this error occured for

---

### property deviceName (str)

The name of the device

---

### property message (str)

The error message

---
---

## MinimizeError(DeviceName, Device)

When an equipment is unable to minimize

- DeviceName (str): The name of the device to display in the error message
- Device (device): The device which cannot minimize   

---

### property device (device)

The device this error occured for

---

### property deviceName (str)

The name of the device

---

### property message (str)

The error message

---
---

## LocateDeviceError(DeviceName, DeviceList)

Used when unable to locate a device

- DeviceName (str): The name of the device to display in the error message
- DeviceList (list of devices): The total list of devices      

---

### property deviceList (device)

The list of devices

---

### property deviceName (str)

The name of the device

---

### property message (str)

The error message

---
---

## MissingTagError(Equipment, Tag)

Used when a tag is missing from an equipment

- Equipment (lab.equipment): The equipment which is missing a tag
- Tag (str): The tag which is missing      

---

### property equipment (lab.equipment)

The equipment object

---

### property tag (str)

The missing tag

---

### property message (str)

The error message

---
---

## SettingError(Setup, Setting)

Used when a setting is wrong

- Setup (lab.setup): The setup with a wrong setting
- Setting (str): The setting which was needed

---

### property setup (lab.setup)

The setup object

---

### property setting (str)

The name of the setting

---

### property message (str)

The error message

---
---

## FileExistError(Path)

Used when a file already exists

- Path (str): The path of the file attempting to create

---

### property path (str)

The file path

---

### property message (str)

The error message

---
---

## ItemExistError(Item, Object)

Used when an item does not exist in a dict like object

- Item (str): The key of the item to locate
- Object (dict-like): The object the item should be found within

---

### property item (str)

The item key

---

### propert object (dict-like)

The object within which the item should be found

---

### property message (str)

The error message

---
---

## QueueError()

Signals that the queue is full

---

### property message (str)

The error message

---
---