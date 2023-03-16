from .. import exceptions as e
from .. import interface
from ..equipment import device

# A generic rotation stage
class rotationStage(device, interface.rotationStage):
    # Device (controllers.rotationStage): The rotation stage device
    # ZeroPos (float): The real position when the device is at position 0
    # DeviceName (str): The name of the device
    # ID (str): The ID name for the device, only used for displaying infomation
    def __init__(self, Device, *args, ZeroPos = 0, **kwargs):
        if not "DeviceName" in kwargs:
            kwargs["DeviceName"] = "Rotation Stage"
        
        super().__init__(*args, **kwargs)
        
        if not isinstance(Device, interface.rotationStage):
            raise e.TypeDefError("Device", Device, interface.rotationStage)
        
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