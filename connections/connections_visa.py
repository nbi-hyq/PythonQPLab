from connections import device

# Class to control a visa device
class visa(device):
    # ResourceName (str): The resource name of the device to access
    # Baudrate (int): The baudrate of the connection
    # Timeout (float): The timeout time for the connection, must not be negative
    # ReadTermination (str): The termination character to look for when reading
    # WriteTermination (str): The termination character when writing a message
    # ReconnectTries (int): How many times to attempt to reconnect if it disconnects, must not be smaller than 0
    # ReconnectDelay (float): The delay in seconds between each reconnect attempt, must not be negative
    # MaxAttempts (int): The maximum number attempts to send a command before giving up, must not be smaller than 1
    # AttemptDelay (float): The delay in seconds between each attempt to send a command, must not be negative
    # UseQueue (bool): If True then it will set up a queue which can be used in the sendCommand method, if False the UseQueue in sendCommand is ignored
    # ForceClose (bool): If true then it should close the connection every time it sends a message and reopen
    # Empty (bool): If True then it will not communicate with the device
    # DeviceName (str): The name of the device, only used for error messages
    # ID (str): The ID name for the device, only used for displaying infomation
    def __init__(self, ResourceName, *args, Baudrate = 9600, Timeout = 1, ReadTermination = "\n", WriteTermination = "\n", **kwargs):
        # Set the name
        if not "DeviceName" in kwargs:
            kwargs["DeviceName"] = "Visa"
            
        kwargs["OpenArgs"] = (ResourceName,)
        kwargs["OpenKwargs"] = {"Baudrate": Baudrate, "Timeout": Timeout, "ReadTermination": ReadTermination, "WriteTermination": WriteTermination}
            
        # Run the super init
        super().__init__(*args, **kwargs)
                        
    # Writes a message to the device
    # Message (str): The message to write
    def write(self, Message):
        self._visa.write(str(Message))
    
    # Reads a message from a device
    # Returns a list of all the lines
    # Lines (int): The number of lines to read
    def read(self, Lines):
        Return = []
        
        for _ in range(Lines):
            Return.append(self._visa.read())
            
        return Return
    
    # Flushes the device
    def flush(self):
        import pyvisa
        self._visa.flush(pyvisa.constants.VI_READ_BUF | pyvisa.constants.VI_WRITE_BUF)
    
    # Checks if the device is open, must be overwritten by the sub class if it can be closed
    # Returns True if it is open
    def isOpen(self):
        try:
            self._visa.session
            return True
        except:
            return False
    
    # Opens the device again
    def _reopen(self):
        Visa = self._rm.open_resource(self._resourceName, open_timeout = self._visa.timeout)
        Visa.timeout = float(self._visa.timeout)
        Visa.baud_rate = int(self._visa.baud_rate)
        Visa.read_termination = str(self._visa.read_termination)
        Visa.write_termination = str(self._visa.write_termination)
        self._visa = Visa
    
    # Opens the device
    # ResourceName (str): The resource name of the device to access
    # Baudrate (int): The baudrate of the connection
    # Timeout (float): The timeout time for the connection, must not be negative
    # ReadTermination (str): The termination character to look for when reading
    # WriteTermination (str): The termination character when writing a message
    def open(self, ResourceName, Baudrate = 9600, Timeout = 1, ReadTermination = "\n", WriteTermination = "\n"):
        import pyvisa
        
        ResourceName = str(ResourceName)
        self._rm = pyvisa.ResourceManager()
        self._visa = self._rm.open_resource(ResourceName, open_timeout = int(Timeout))
        self._resourceName = ResourceName
        
        # Setup device
        self._visa.timeout = float(Timeout) * 1000
        self._visa.baud_rate = int(Baudrate)
        self._visa.read_termination = str(ReadTermination)
        self._visa.write_termination = str(WriteTermination)

    
    # Close the device
    def _close(self):
        self._visa.before_close()
        self._visa.close()
        super()._close()
       