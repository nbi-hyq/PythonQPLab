from .. import connections as c
from .. import exceptions as e
from ..controllers import rotationStage

# A controller for an ELLO control board
class ELLOControl(c.external):
    # SerialNumber (str): The serial number of the device
    # Timeout (float): The timeout in seconds
    # UseQueue (bool): If True then it will set up a queue which can be used in the sendCommand method, if False the UseQueue in sendCommand is ignored
    # Empty (bool): If True then it will not communicate with the device
    # DeviceName (str): The name of the device, only used for error messages
    # ID (str): The ID name for the device, only used for displaying infomation    
    def __init__(self, SerialNumber, *args, Timeout = 10, **kwargs):        
        if not "DeviceName" in kwargs:
            kwargs["DeviceName"] = "ELLO"
            
        kwargs["OpenArgs"] = (SerialNumber,)
        kwargs["OpenKwargs"] = {"Timeout": Timeout}
                    
        super().__init__(self, *args, **kwargs)
        
    def open(self, SerialNumber, Timeout = 10):
        from pylablib.devices.Thorlabs.elliptec import ElliptecMotor as m
        self._stage = m(SerialNumber, timeout = Timeout, scale = "stage")        
        
    # Creates a controller for a single rotation stage
    # Address (int): The address of the stage
    # DeviceName (str): The name of the device, only used for error messages
    # ID (str): The ID name for the device, only used for displaying infomation    
    def getControl(self, Address, *args, **kwargs):
        return ELLO(self, Address, *args, **kwargs)
    
    # Homes the device  
    # Address (int): The address of the device to access
    def _home(self, Address = 0):
        self._stage.home(addr = Address)
    
    # Moves the device to a specified position
    # Position (float): The position to set
    # Address (int): The address of the device to access
    def _moveTo(self, Position, Address = 0):
        self._stage.move_to(Position % 360, addr = Address)
    
    # Gets the current position of the rotation stage
    # Address (int): The address of the device to access
    def _getPosition(self, Address = 0):
        return self._stage.get_position(addr = Address)

    # Homes the device     
    # Address (int): The address of the device to access
    # UseQueue (bool): Whether to run the command through the queue or not, ignored if the device was initialized with UseQueue = False
    def home(self, Address = 0, **kwargs):
        self.runFunction("_home", Kwargs = {"Address": Address}, **kwargs)

    # Moves the device to a specified position
    # Position (float): The position to set
    # Address (int): The address of the device to access
    # UseQueue (bool): Whether to run the command through the queue or not, ignored if the device was initialized with UseQueue = False
    def moveTo(self, Position, Address = 0, **kwargs):
        self.runFunction("_moveTo", Kwargs = {"Address": Address}, Args = (Position,), **kwargs)
    
    # Gets the current position of the rotation stage
    # Address (int): The address of the device to access
    # UseQueue (bool): Whether to run the command through the queue or not, ignored if the device was initialized with UseQueue = False
    def getPosition(self, Address = 0, **kwargs):
        return self.runFunction("_getPosition", Kwargs = {"Address": Address}, **kwargs)
                
    def _close(self):
        self._stage.close()
        super()._close()

    
# A controller for a single ELLO rotation stage, should be initialized from ELLOControl.getControl
class ELLO(rotationStage, c.deviceBase):
    # Device (ELLOControl): The device to control
    # Address (int): The address of the stage
    # DeviceName (str): The name of the device, only used for error messages
    # ID (str): The ID name for the device, only used for displaying infomation    
    def __init__(self, Device, Address, *args, **kwargs):   
        if not isinstance(Device, ELLOControl):
            raise e.TypeDefError("Device", Device, ELLOControl)
        
        if not "DeviceName" in kwargs:
            kwargs["DeviceName"] = "ELLO"
            
        super().__init__(*args, **kwargs)

        self._device = Device
        self._addr = int(Address)
        
    # Homes the device     
    # UseQueue (bool): Whether to run the command through the queue or not, ignored if the device was initialized with UseQueue = False
    def home(self, **kwargs):
        self._device.home(Address = self._addr, **kwargs)
    
    # Moves the device to a specified position
    # Position (float): The position to set
    # UseQueue (bool): Whether to run the command through the queue or not, ignored if the device was initialized with UseQueue = False
    def moveTo(self, Position, **kwargs):
        self._device.moveTo(Position, Address = self._addr, **kwargs)
    
    # Gets the current position of the rotation stage
    # UseQueue (bool): Whether to run the command through the queue or not, ignored if the device was initialized with UseQueue = False
    def getPosition(self, **kwargs):
        return self._device.getPosition(Address = self._addr, **kwargs)
    