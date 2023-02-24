# Defines exceptions used within other functions and classes

# Used when the type of an arg is not correct
class TypeDefError(Exception):
    # VariableName (str): The name of the variable to display in the error message
    # Variable (any): The variable that has a wrong type
    # Type (type): The correct type of the variable
    def __init__(self, VariableName, Variable, Type):
        self.var = Variable
        self.varName = str(VariableName)
        self.type = Type
        self.message = f"{self.varName} must be of type {self.type} but received {type(self.var)}"
        
        super().__init__(self.message)
        
# Used when an element of a variable has a wrong type
class ElementTypeError(Exception):
    # VariableName (str): The name of the variable to display in the error message
    # Variable (any): The variable which has an element with a wrong type
    # ElementID (int): The ID of the element with a wrong type
    # Type (type): The correct type of the variable    
    def __init__(self, VariableName, Variable, ElementID, Type):
        self.var = Variable
        self.varName = str(VariableName)
        self.id = int(ElementID)
        self.type = Type
        self.message = f"Element {self.id} of {self.varName} must be of type {self.type} but received {type(self.var[self.id])}"
        
        super().__init__(self.message)
        
# Used when a variable has a wrong length
class LengthError(Exception):
    # VariableName (str): The name of the variable to display in the error message
    # Variable (any): The variable which has a wrong length
    # Length (int): The correct length of the variable
    def __init__(self, VariableName, Variable, Length):
        self.var = Variable
        self.varName = str(VariableName)
        self.length = int(Length)
        self.message = f"{self.varName} must have length {self.length} but received length {len(self.var)}"
        
        super().__init__(self.message)
        
# Used when a variable has length smaller that the min length
class MinLengthError(Exception):
    # VariableName (str): The name of the variable to display in the error message
    # Variable (any): The variable which has a wrong length
    # Length (int): The correct length of the variable
    def __init__(self, VariableName, Variable, Length):
        self.var = Variable
        self.varName = str(VariableName)
        self.length = int(Length)
        self.message = f"{self.varName} must have minimum length {self.length} but received length {len(self.var)}"
     
        super().__init__(self.message)

# Used when a variable has length larger that the max length
class MaxLengthError(Exception):
    # VariableName (str): The name of the variable to display in the error message
    # Variable (any): The variable which has a wrong length
    # Length (int): The correct length of the variable
    def __init__(self, VariableName, Variable, Length):
        self.var = Variable
        self.varName = str(VariableName)
        self.length = int(Length)
        self.message = f"{self.varName} must have maximum length {self.length} but received length {len(self.var)}"
     
        super().__init__(self.message)

# Used when an error occured and it should be propagated
class PropagationError(Exception):
    # Error (Exception): The exception that occured
    # Reason (str): A string describing what happened when the error occured
    def __init__(self, Error, Reason):
        self.error = Error
        self.reason = str(Reason)
        self.message = f"An error occured while {self.reason}: {self.error}"
        
        super().__init__(self.message)
    
# Used when trying to use an object which is no longer running
class NotRunningError(Exception):
    # ObjectName (str): The name of the object to display in the error message
    # Object (any): The object which is no longer running  
    def __init__(self, ObjectName, Object):
        self.obj = Object
        self.objName = str(ObjectName)
        self.message = f"{self.objName} is not running an thus cannot be accessed"
        
        super().__init__(self.message)
    
# Used when a keyword is not recognized
class KeywordError(Exception):
    # KeywordName (str): The name of the keyword
    # Keyword (str): The unknown keyword
    # Valid (list of str): The list of valid keywords
    def __init__(self, KeywordName, Keyword, Valid = None):
        self.key = Keyword
        self.keyName = str(KeywordName)
        self.valid = Valid
        self.message = f"{self.keyName} has unknown keyword {self.key}"
        
        if Valid is not None:
            self.message += f" must be one of {Valid}"
        
        super().__init__(self.message)
    
# Used when one variable must be larger than another
class LargerVarError(Exception):
    # SmallVariableName (str): The name of the smallest variable
    # SmallVariable (num): The value of the smallest variable
    # LargeVariableName (str): The name of the largest variable
    # LargeVariable (num): The value of the largest variable
    def __init__(self, SmallVariableName, SmallVariable, LargeVariableName, LargeVariable):
        self.minVar = SmallVariable
        self.minVarName = str(SmallVariableName)
        self.maxVar = LargeVariable
        self.maxVarName = str(LargeVariableName)
        self.message = f"{self.minVarName} must be smaller than {self.maxVarName} but received {self.minVar} and {self.maxVar}"
        
        super().__init__(self.message)
  
# Used when a value is too small
class MinValueError(Exception):
    # VariableName (str): The name of the variable to display in the error message
    # Variable (num): The variable which is too small
    # Value (num): The minimum number
    def __init__(self, VariableName, Variable, Value):
        self.var = Variable
        self.varName = str(VariableName)
        self.value = Value
        self.message = f"{self.varName} is {self.var} but must be larger or equal to {self.value}"
        
        super().__init__(self.message)

# Used when a value is too small
class SharpMinValueError(Exception):
    # VariableName (str): The name of the variable to display in the error message
    # Variable (num): The variable which is too small
    # Value (num): The minimum number
    def __init__(self, VariableName, Variable, Value):
        self.var = Variable
        self.varName = str(VariableName)
        self.value = Value
        self.message = f"{self.varName} is {self.var} but must be larger than {self.value}"
        
        super().__init__(self.message)
        
# Used when a value is not within a range
class RangeError(Exception):
    # VariableName (str): The name of the variable to display in the error message
    # Variable (num): The variable which is too small
    # MinValue (num): The minimum number
    # MaxValue (num): The maximum number
    def __init__(self, VariableName, Variable, MinValue, MaxValue):
        self.var = Variable
        self.varName = str(VariableName)
        self.min = MinValue
        self.max = MaxValue
        self.message = f"{self.varName} is {self.var} but must be within the range ({self.min}, {self.max})"
        
        super().__init__(self.message)

# Used when a value is not within a range
class SharpRangeError(Exception):
    # VariableName (str): The name of the variable to display in the error message
    # Variable (num): The variable which is too small
    # MinValue (num): The minimum number
    # MaxValue (num): The maximum number
    def __init__(self, VariableName, Variable, MinValue, MaxValue):
        self.var = Variable
        self.varName = str(VariableName)
        self.min = MinValue
        self.max = MaxValue
        self.message = f"{self.varName} is {self.var} but must be within the range ({self.min}, {self.max}) exclusively"
        
        super().__init__(self.message)    
    
# Used when unable to open a device
class OpenError(Exception):
    # DeviceName (str): The name of the device to display in the error message
    # Device (device): The device that cannot be opened
    def __init__(self, DeviceName, Device):
        self.device = Device
        self.deviceName = str(DeviceName)
        self.message = f"Unable to open {self.deviceName}"
        
        super().__init__(self.message)
    
# Used when a communication error has occured
class CommunicationError(Exception):
    # DeviceName (str): The name of the device to display in the error message
    # Device (device): The device with a communication error
    # Command (str): The command sent to the device
    # Message (str): The message describing the communication error
    def __init__(self, DeviceName, Device, Command, Message):
        self.device = Device
        self.deviceName = str(DeviceName)
        self.command = str(Command)
        self.oldMessage = str(Message)
        self.message = f"Communication error for {self.deviceName} has occured with the command \"{self.command}\": {self.oldMessage}"
        
        super().__init__(self.message)

# Used when a device has timed out
class TimeoutError(Exception):
    # DeviceName (str): The name of the device to display in the error message
    # Device (device): The device which has timed out
    def __init__(self, DeviceName, Device):
        self.device = Device
        self.deviceName = str(DeviceName)
        self.message = f"Timeout error occured for {self.deviceName}"
        
        super().__init__(self.message)

# Used when a function is run which has not been implemented
class ImplementationError(Exception):
    # Name (str): The name of the function which has not been implemented
    def __init__(self, Name):
        self.name = str(Name)
        self.message = f"{self.name} has not been implemented yet"
        
        super().__init__(self.message)
        
# Used when unable to stabilize a value
class StabilizeError(Exception):
    # DeviceName (str): The name of the device to display in the error message
    # Device (device): The device which cannot stabilize
    # Stabilizer (str): The name of the thing to stabilize
    def __init__(self, DeviceName, Device, Stabilizer):
        self.device = Device
        self.deviceName = str(DeviceName)
        self.stabil = str(Stabilizer)
        self.message = f"{self.deviceName} was unable to stabilize {self.stabil}"
        
        super().__init__(self.message)

# Used when a variable must be a multiple of another number
class MultipleError(Exception):
    # VariableName (str): The name of the variable to display in the error message
    # Variable (num): The variable which is not a multiple
    # Base (num): The number Variable must be a multiple of
    def __init__(self, VariableName, Variable, Base):
        self.var = Variable
        self.varName = str(VariableName)
        self.base = Base
        self.message = f"{self.varName} is {self.var} but must be a multiple of {self.base}"
        
        super().__init__(self.message)
    
# Used when a measurement does not finish
class FinishMeasurementError(Exception):
    # DeviceName (str): The name of the device to display in the error message
    # Device (device): The device which cannot finish a measurement 
    def __init__(self, DeviceName, Device):
        self.device = Device
        self.deviceName = str(DeviceName)
        self.message = f"{self.deviceName} was unable to finish a measurement"
        
        super().__init__(self.message)

# Used when a variable has an illigal value
class WrongValueError(Exception):
    # VariableName (str): The name of the variable to display in the error message
    # Variable (num): The variable which is not a multiple    
    def __init__(self, VariableName, Variable):
        self.var = Variable
        self.varName = str(VariableName)
        self.message = f"{self.varName} is {self.var}"
        
        super().__init__(self.message)
        
# Used when a device has not been initialized
class InitializeError(Exception):
    # DeviceName (str): The name of the device to display in the error message
    # Device (device): The device which cannot initialize 
    def __init__(self, DeviceName, Device):
        self.device = Device
        self.deviceName = str(DeviceName)
        self.message = f"{self.deviceName} has not been initialized"
        
        super().__init__(self.message)
        
# Used when a measurement does not finish
class OverflowError(Exception):
    # DeviceName (str): The name of the device to display in the error message
    # Device (device): The device which has overflowed
    def __init__(self, DeviceName, Device):
        self.device = Device
        self.deviceName = str(DeviceName)
        self.message = f"{self.deviceName} encountered an overflow"
        
        super().__init__(self.message)
      
# Used when a parameter already exists and cannot be reinitialized
class ExistError(Exception):
    # Parameter (str): The name of the parameter
    # DeviceName (str): The name of the device to display in the error message
    # Device (device): The device which already has this parameter    
    def __init__(self, Parameter, DeviceName, Device):
        self.device = Device
        self.deviceName = str(DeviceName)
        self.param = str(Parameter)
        self.message = f"{self.param} already exists for {self.deviceName}"
        
        super().__init__(self.message)
        
# Used when an illigal character is found in a string
class IlligalCharError(Exception):
    # Character (str): The illigal character
    # Text (str): The text with the illigal character within
    def __init__(self, Character, Text):
        self.char = str(Character)
        self.text = str(Text)
        self.message = f"Found illigal character {self.char} in text"
        
        super().__init__(self.message)

# Used when a method for a device is called when not allowed
class MethodError(Exception):
    # DeviceName (str): The name of the device to display in the error message
    # Device (device): The device which has illigal method 
    # MethodName (str): The name of the illigal method     
    def __init__(self, DeviceName, Device, MethodName):
        self.device = Device
        self.deviceName = str(DeviceName)
        self.method = str(MethodName)
        self.message = f"{self.deviceName} must be {self.require} to use {self.method}"
        
        super().__init__(self.message)

# When an equipment is out of range of its power
class PowerRangeError(Exception):
    # DeviceName (str): The name of the device to display in the error message
    # Device (device): The device which does not have enough power     
    def __init__(self, DeviceName, Device):
        self.device = Device
        self.deviceName = str(DeviceName)
        self.message = f"{self.deviceName} is at maximum power. Desired power out of range of {self.deviceName}"
        
        super().__init__(self.message)

# When an equipment is unable to lock
class LockError(Exception):
    # DeviceName (str): The name of the device to display in the error message
    # Device (device): The device which cannot lock     
    def __init__(self, DeviceName, Device):
        self.device = Device
        self.deviceName = str(DeviceName)
        self.message = f"{self.deviceName} is unable to lock"
        
        super().__init__(self.message)
        
# When an equipment is unable to minimize
class MinimizeError(Exception):
    # DeviceName (str): The name of the device to display in the error message
    # Device (device): The device which cannot minimize   
    def __init__(self, DeviceName, Device):
        self.device = Device
        self.deviceName = str(DeviceName)
        self.message = f"{self.deviceName} is unable to minimize"
        
        super().__init__(self.message)

# Used when unable to locate a device
class LocateDeviceError(Exception):
    # DeviceName (str): The name of the device to display in the error message
    # DeviceList (list of devices): The total list of devices      
    def __init__(self, DeviceName, DeviceList):
        self.deviceList = DeviceList
        self.deviceName = str(DeviceName)
        self.message = f"Unable to locate {self.deviceName}"
        
        super().__init__(self.message)
        
# Used when a tag is missing from an equipment
class MissingTagError(Exception):
    # Equipment (lab.equipment): The equipment which is missing a tag
    # Tag (str): The tag which is missing      
    def __init__(self, Equipment, Tag):
        self.equipment = Equipment
        self.tag = str(Tag)
        self.message = f"Equipment ({self.equipment.setting}) does not have the tag {self.tag}"
        
        super().__init__(self.message)
        
# Used when a setting is wrong
class SettingError(Exception):
    # Setup (lab.setup): The setup with a wrong setting
    # Setting (str): The setting which was needed
    def __init__(self, Setup, Setting):
        self.setup = Setup
        self.setting = str(Setting)
        self.message = f"Setup has setting {self.setup.setting} but {self.setting} is required"
        
        super().__init__(self.message)
        
# Used when a file already exists
class FileExistError(Exception):
    # Path (str): The path of the file attempting to create
    def __init__(self, Path):
        self.path = str(Path)
        self.message = f"Unable to create file \"{self.path}\" because is already exists"
        
        super().__init__(self.message)
        
# Used when an item does not exist in a dict like object
class ItemExistError(Exception):
    # Item (str): The key of the item to locate
    # Object (dict-like): The object the item should be found within
    def __init__(self, Item, Object):
        self.item = str(Item)
        self.object = Object
        self.message = f"Unable to locate {Item}"
        
        super().__init__(self.message)
        
# Signals that the queue is full
class QueueError(Exception):
    def __init__(self):
        self.message = "The queue is full"
        
        super().__init__(self.message)