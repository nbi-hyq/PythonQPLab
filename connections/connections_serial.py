from connections import device

# Class to control a serial device
class serial(device):
    # Port (str): The name of the COM port through which to access the serial connection
    # Baudrate (int): The baudrate of the connection
    # Timeout (float): The timeout time for the connection, must not be negative
    # ReadTermination (str): The termination character to look for when reading
    # WriteTermination (str): The termination character when writing a message
    # BytesMode (bool): If true it will just send and receive bytes (Then ReturnLines turns into the number of bytes to receive)
    # ReconnectTries (int): How many times to attempt to reconnect if it disconnects, must not be smaller than 0
    # ReconnectDelay (float): The delay in seconds between each reconnect attempt, must not be negative
    # MaxAttempts (int): The maximum number attempts to send a command before giving up, must not be smaller than 1
    # AttemptDelay (float): The delay in seconds between each attempt to send a command, must not be negative
    # UseQueue (bool): If True then it will set up a queue which can be used in the sendCommand method, if False the UseQueue in sendCommand is ignored
    # ForceClose (bool): If true then it should close the connection every time it sends a message and reopen
    # Empty (bool): If True then it will not communicate with the device
    # DeviceName (str): The name of the device, only used for error messages
    # ID (str): The ID name for the device, only used for displaying infomation
    def __init__(self, Port, *args, Baudrate = 9600, Timeout = 1, ReadTermination = "\r\n", WriteTermination = "\n", BytesMode = False, **kwargs):        
        # Set the name
        if not "DeviceName" in kwargs:
            kwargs["DeviceName"] = "Serial"
            
        kwargs["OpenArgs"] = (Port,)
        kwargs["OpenKwargs"] = {"Baudrate": Baudrate, "Timeout": Timeout}
            
        # Run the super init
        super().__init__(*args, **kwargs)
        
        self._readTermination = str(ReadTermination)
        self._writeTermination = str(WriteTermination)
        self._bytesMode = bool(BytesMode)
                            
    # Writes a message to the device
    # Message (str): The message to write
    def write(self, Message):
        if self._bytesMode:
            self._serial.write(Message)    
            
        else:
            self._serial.write((f"{str(Message)}{self._writeTermination}").encode("utf-8"))
    
    # Reads a message from a device
    # Returns a list of all the lines
    # Lines (int): The number of lines to read
    def read(self, Lines):
        if self._bytesMode:
            Return = self._serial.read(Lines)
            
        else:
            Return = []
            
            for _ in range(Lines):
                Return.append(self._serial.read_until().decode("utf-8").split(self._readTermination)[0])
            
        return Return
    
    # Flushes the device
    def flush(self):
        self._serial.reset_input_buffer()
        self._serial.reset_output_buffer()
    
    # Checks if the device is open
    # Returns True if it is open
    def isOpen(self):
        return self._serial.is_open
    
    # Opens the device again
    def _reopen(self):
        self._serial.open()
        
    # Opens a device
    def open(self, Port, Baudrate = 9600, Timeout = 1):
        import serial
        self._serial = serial.Serial(port = Port, baudrate = Baudrate, timeout = Timeout, write_timeout = Timeout)
    
    # Close the device
    def _close(self):
        self._serial.close()
        
        super()._close()
        
