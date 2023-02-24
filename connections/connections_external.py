from ..connections import device
    
# A controller for a device which is controlled by other python functions
class external(device):
    # Library (object): The object containing all the external functions
    # ReconnectTries (int): How many times to attempt to reconnect if it disconnects, must not be smaller than 0
    # ReconnectDelay (float): The delay in seconds between each reconnect attempt, must not be negative
    # MaxAttempts (int): The maximum number attempts to send a command before giving up, must not be smaller than 1
    # AttemptDelay (float): The delay in seconds between each attempt to send a command, must not be negative
    # UseQueue (bool): If True then it will set up a queue which can be used in the sendCommand method, if False the UseQueue in sendCommand is ignored
    # ForceClose (bool): If true then it should close the connection every time it sends a message and reopen
    # Empty (bool): If True then it will not communicate with the device
    # OpenArgs (set): Arguments sent to open
    # OpenKwargs (dict): Arguments sent to open
    # DeviceName (str): The name of the device, only used for error messages
    # ID (str): The ID name for the device, only used for displaying infomation    
    def __init__(self, Library, *args, **kwargs):
        # Set the name
        if not "DeviceName" in kwargs:
            kwargs["DeviceName"] = "External"
            
        # Run the super init
        super().__init__(*args, **kwargs)
        
        self._lib = Library
        self._returnValue = None
        
    # Runs a function from the library
    # Name (str): The function to run
    # args and kwargs are used for the function
    def write(self, Name, *args, **kwargs):
        self._returnVal = getattr(self._lib, str(Name))(*args, **kwargs)
    
    # Returns the return value of the last function call
    # Lines (int): Unused
    def read(self, Lines):
        ReturnVal = self._returnVal
        self._returnVal = None
        return ReturnVal
        
    # Runs a function from the library
    # Name (str): The name of the function
    # Args (set): The arguments of the function
    # Kwargs (dict): The kwargs for the function
    # UseQueue (bool): Whether to run the command through the queue or not
    # ResponseCheck (Func): A function to check if the response was correct, None if no check should be used, the function must have the arguments (Class, Command, ReturnString) and must return None on succes or a string on failure with the error message
    # ReturnLines (int): The number of lines it expects to receive from the device
    # WaitTime (float): The time in seconds to wait before reading
    def runFunction(self, Name, Args = set(), Kwargs = dict(), **kwargs):
        kwargs["WriteArgs"] = Args
        kwargs["WriteKwargs"] = Kwargs
        
        return self.sendCommand(Name, **kwargs)
    