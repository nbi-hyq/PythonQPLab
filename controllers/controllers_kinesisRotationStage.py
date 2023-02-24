import connections as c
from controllers import rotationStage

# A controller for the KDC cube rotation cage
class kinesisRotationStage(rotationStage, c.external):
    # SerialNumber (str): The serial number of the device
    # Timeout (float): The timeout time in seconds
    # UseQueue (bool): If True then it will set up a queue which can be used in the sendCommand method, if False the UseQueue in sendCommand is ignored
    # Empty (bool): If True then it will not communicate with the device
    # DeviceName (str): The name of the device, only used for error messages
    # ID (str): The ID name for the device, only used for displaying infomation    
    def __init__(self, SerialNumber, *args, Timeout = 10, **kwargs):        
        if not "DeviceName" in kwargs:
            kwargs["DeviceName"] = "KDC101"
            
        kwargs["OpenArgs"] = (SerialNumber,)
            
        super().__init__(self, *args, **kwargs)

        # Load
        self._timeout = float(Timeout)
        
    def open(self, SerialNumber):
        from pylablib.devices.Thorlabs import KinesisMotor as m
        self._stage = m(SerialNumber, scale = "stage")
    
    # Homes the device     
    def _home(self):
        self._stage.home(timeout = self._timeout)
    
    # Moves the device to a specified position
    # Position (float): The position to set
    def _moveTo(self, Position):
        self._stage.move_to(Position % 360)
    
    # Gets the current position of the rotation stage
    def _getPosition(self):
        return self._stage.get_position()
    
    # Homes the device     
    # UseQueue (bool): Whether to run the command through the queue or not, ignored if the device was initialized with UseQueue = False
    def home(self, **kwargs):
        self.runFunction("_home", **kwargs)

    # Moves the device to a specified position
    # Position (float): The position to set
    # UseQueue (bool): Whether to run the command through the queue or not, ignored if the device was initialized with UseQueue = False
    def moveTo(self, Position, **kwargs):
        self.runFunction("_moveTo", Args = (Position,), **kwargs)
    
    # Gets the current position of the rotation stage
    # UseQueue (bool): Whether to run the command through the queue or not, ignored if the device was initialized with UseQueue = False
    def getPosition(self, **kwargs):
        return self.runFunction("_getPosition", **kwargs)
    
    def _close(self):
        self._stage.close()
        super()._close()
        