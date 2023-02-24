from .. import connections as c
from .. import exceptions as e

# Controls the SNSPD
class SNSPD(c.socketClient):
    # IP (str): The IP of the socket connection
    # Group (str): A or B, the detector group to use
    # BufferSize (int): The size of the buffer when getting data
    # Timeout (float): The timeout in seconds
    # ReconnectTries (int): How many times to attempt to reconnect if it disconnects, must not be smaller than 0
    # ReconnectDelay (float): The delay in seconds between each reconnect attempt, must not be negative
    # MaxAttempts (int): The maximum number attempts to send a command before giving up, must not be smaller than 1
    # AttemptDelay (float): The delay in seconds between each attempt to send a command, must not be negative
    # UseQueue (bool): If True then it will set up a queue which can be used in the sendCommand method, if False the UseQueue in sendCommand is ignored
    # Empty (bool): If True then it will not communicate with the device
    # DeviceName (str): The name of the device, only used for error messages
    # ID (str): The ID name for the device, only used for displaying infomation
    def __init__(self, IP, Group, *args, **kwargs):
        if not "DeviceName" in kwargs:
            kwargs["DeviceName"] = "SNSPD"
        
        # Make sure types are correct
        if not isinstance(Group, str):
            raise e.TypeDefError("Group", Group, str)
            
        # Get the port
        if Group == "A":
            Port = 65432
            
        elif Group == "B":
            Port = 65433
            
        else:
            raise e.KeywordError("Group", Group, ["A", "B"])
            
        self.group = Group
        
        # Initialize socket
        super().__init__(IP, Port, *args, **kwargs)
        
    # Delatches a channel
    # Channel (int): The channel to delatch
    # UseQueue (bool): Whether to run the command through the queue or not, ignored if the device was initialized with UseQueue = False
    def delatch(self, Channel, **kwargs):
        self.sendWithoutResponse(f"Det-{int(Channel)}:Delatch = 0", **kwargs)
        
    # Sets the bias current of the SNSPD
    # Channel (int): The channel to delatch
    # Bias (float): The bias current to set
    # UseQueue (bool): Whether to run the command through the queue or not, ignored if the device was initialized with UseQueue = False
    def setBias(self, Channel, Bias, **kwargs):
        self.sendWithoutResponse(f"Det-{int(Channel)}:Bias = {float(Bias)}")
        