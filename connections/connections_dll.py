from ..connections import device
    
# Class to control a dll controled device
class dll(device):
    # DLLPath (str): The path to the dll to load
    # ReconnectTries (int): How many times to attempt to reconnect if it disconnects, must not be smaller than 0
    # ReconnectDelay (float): The delay in seconds between each reconnect attempt, must not be negative
    # MaxAttempts (int): The maximum number attempts to send a command before giving up, must not be smaller than 1
    # AttemptDelay (float): The delay in seconds between each attempt to send a command, must not be negative
    # UseQueue (bool): If True then it will set up a queue which can be used in the sendCommand method, if False the UseQueue in sendCommand is ignored
    # ForceClose (bool): If true then it should close the connection every time it sends a message and reopen
    # Empty (bool): If True then it will not communicate with the device
    # DeviceName (str): The name of the device, only used for error messages
    # ID (str): The ID name for the device, only used for displaying infomation
    def __init__(self, DLLPath, *args, **kwargs):
        # Set the name
        if not "DeviceName" in kwargs:
            kwargs["DeviceName"] = "DLL"
            
        kwargs["OpenArgs"] = (DLLPath,)
        kwargs["OpenKwargs"] = dict()
            
        # Run the super init
        super().__init__(*args, **kwargs)
        
        self._returnVal = None
        
    # Runs a function from the dll
    # Name (str): The function to run
    def write(self, Name, *args):
        self._returnVal = getattr(self._lib, str(Name))(*args)
    
    # Returns the return value of the last function call
    # Lines (int): Unused
    def read(self, Lines):
        ReturnVal = self._returnVal
        self._returnVal = None
        return ReturnVal
    
    # Opens the device
    # DLLPath (str): The path to the dll to load
    def open(self, DLLPath):
        import ctypes as c
        
        self._lib = c.cdll.LoadLibrary(str(DLLPath))

    # Frees the dll
    def _close(self):
        import _ctypes as c
        
        c.FreeLibrary(self._lib._handle)
        super()._close()
        
    # Runs a function from the dll
    # Name (str): The name of the function
    # Args (set): The arguments of the function
    def runFunction(self, Name, Args = set(), **kwargs):
        kwargs["WriteArgs"] = Args
        
        return self.sendCommand(Name, **kwargs)
    
    # Sets up a function from lib, must be run once before using the function, preferably in the init function
    # Function (str): The name of the function
    # ReturnType (ctypes.PyCSimpleType): The return type of the function
    # ArgTypes (list of ctypes.PyCSimpleType): A list with the types of all the arguments
    def setupFunction(self, Function, ReturnType, ArgTypes):
        if not self.empty:
            getattr(self._lib, str(Function)).restype = ReturnType
            getattr(self._lib, str(Function)).argtypes = ArgTypes
    