from ..connections import queue, queueNoThread
from .. import exceptions as e

# Defines the base of a device
class deviceBase(object):
    # DeviceName (str): The name of the device, only used for error messages
    # ID (str): The ID name for the device, only used for displaying infomation
    def __init__(self, *args, DeviceName = "Device", ID = None, **kwargs):
        import weakref
        
        super().__init__(*args, **kwargs)
        
        self.deviceName = str(DeviceName)
        
        if ID is not None:
            self.deviceName = f"{self.deviceName} {str(ID)}"
            
        self._isOpen = True
        
        weakref.finalize(self, self.close)

    # Checks if the device is open, may be overwritten by the sub class if it can be closed
    # Returns True if it is open
    def isOpen(self):
        return self._isOpen
        
    # Close the device, the method _close must be overwritten by the device
    def close(self):
        if self.isOpen():
            self._close()
            
        self._isOpen = False
        
    # Does the actual closing of the device
    def _close(self):
        pass


# The base class for any device
class device(deviceBase):
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
    def __init__(self, *args, ReconnectTries = 100, ReconnectDelay = 1, MaxAttempts = 100, AttemptDelay = 1, UseQueue = True, ForceClose = False, Empty = False, OpenArgs = set(), OpenKwargs = dict(), **kwargs):
        super().__init__(*args, **kwargs)
            
        # Set default values
        self._reconnectTries = int(ReconnectTries)
        self._reconnectDelay = float(ReconnectDelay)
        self._maxAttempts = int(MaxAttempts)
        self._attemptDelay = float(AttemptDelay)
        self._forceClose = bool(ForceClose)
        self.lastError = ""

        # Make sure max attempts is not too low
        if self._reconnectTries < 0:
            raise e.MinValueError("ReconnectTries", self._reconnectTries, 0)
            
        if self._maxAttempts < 1:
            raise e.MinValueError("MaxAttempts", self._maxAttempts, 1)
            
        if self._reconnectDelay < 0:
            raise e.MinValueError("ReconnectDelay", self._reconnectDelay, 0)

        if self._attemptDelay < 0:
            raise e.MinValueError("AttemptDelay", self._attemptDelay, 0)

        # Setup for empty
        self.empty = bool(Empty)
        self.setEmptyReturn("0")
        
        # Setup a queue
        self._useQueue = bool(UseQueue)
        
        if self._useQueue:
            self._q = queue()
            
        else:
            self._q = queueNoThread()
        
        # Opens device
        if not bool(Empty):
            self.open(*OpenArgs, **OpenKwargs)
            
            if not self.isOpen():
                raise e.OpenError(self.deviceName, self)

        
    # Sets the return value if empty is true
    # Value (str/list): If a list of strings then this will be the return value of the read, if a string the it will be repeated by the number of return lines
    def setEmptyReturn(self, Value):
        if isinstance(Value, str):
            Value = [Value]
            
        else:
            Value = list(Value)
            
        self._emptyReturn = Value
        
    # Writes a message to the device, must be overwritten by the sub class
    # Message (str): The message to write
    def write(self, Message):
        raise e.ImplementationError("device.write")
    
    # Reads a message from a device, must be overwritten by the sub class
    # Returns a list of all the lines
    # Lines (int): The number of lines to read
    def read(self, Lines):
        raise e.ImplementationError("device.read")
    
    # Flushes the device, must be overwritten by the sub class is flushing is posible
    def flush(self):
        pass
        
    # Opens the device again, must be overwritten by the sub class if it can be reopened
    def _reopen(self):
        raise e.ImplementationError("device.reopen")
    
    # Reopens the device, implement own reopen in _reopen method
    def reopen(self, *args, **kwargs):
        self._reopen(*args, **kwargs)
        
        if not self._q.isAlive():
            if self._useQueue:
                self._q = queue()
                
            else:
                self._q = queueNoThread()
    
    # Opens a device, must be overwritten by the sub class
    def open(self):
        raise e.ImplementationError("device.open")
        
    # Send a command to the device
    # Command (str): The command to send the device
    # WriteArgs (set): The args sent to the write command
    # WriteKwargs (dict): The kwargs sent to the write command
    # ReadArgs (set): The args sent to the read command
    # ReadKwargs (dict): The kwargs sent to the read command
    # ResponseCheck (Func): A function to check if the response was correct, None if no check should be used, the function must have the arguments (Class, ReturnString) and must return None on succes or a string on failure with the error message
    # ReturnLines (int): The number of lines it expects to receive from the device
    # WaitTime (float): The time in seconds to wait before reading
    def _sendCommand(self, Command, WriteArgs = set(), WriteKwargs = dict(), ReadArgs = set(), ReadKwargs = dict(), ResponseCheck = None, ReturnLines = 1, WaitTime = 0):
        from .. import functions as f
        
        # Check if it is empty
        if self.empty:
            ReturnString = self._emptyReturn.copy()
            
            if len(ReturnString) > ReturnLines:
                ReturnString = ReturnString[:ReturnLines]
                
            elif len(ReturnString) < ReturnLines:
                ReturnString += [ReturnString[-1]] * (ReturnLines - len(ReturnString))
                
            return ReturnString
        
        # Reopen if forced to close
        if self._forceClose:
            self.reopen()
        
        # Check that the device is open
        if not self.isOpen():
            for _ in range(self._reconnectTries):
                print(f"{self.deviceName} is disconnected attempting to reconnect")
                
                self.reopen()
                if self.isOpen():
                    print("Reconnected")
                    break
               
                # Sleep for a bit
                f.time.sleep(self._reconnectDelay)
                
            # Make sure it is connected
            if not self.isOpen():
                raise e.OpenError(self.deviceName, self)
            
        # Send the new command
        try:
            for _ in range(self._maxAttempts):
                # Write command
                try:
                    self.write(Command, *WriteArgs, **WriteKwargs)
                
                except Exception as ErrorMes:
                    self.lastError = ErrorMes                
                    print(f"Unable to write to {self.deviceName}, trying again")
                    f.time.sleep(self._attemptDelay)    
                    Check = ErrorMes
                    continue
                
                if float(WaitTime) > 0:
                    f.time.sleep(float(WaitTime))
                
                # Get the return value
                try:
                    ReturnString = self.read(ReturnLines, *ReadArgs, **ReadKwargs)
                
                except Exception as ErrorMes:
                    self.lastError = ErrorMes                
                    print(f"Unable to read from {self.deviceName}, trying again")
                    f.time.sleep(self._attemptDelay) 
                    Check = ErrorMes
                    continue
           
                # Check if it worked
                if ResponseCheck is not None:
                    Check = ResponseCheck(self, Command, ReturnString)
                else:
                    Check = None
                    
                if Check is None:
                    break
       
                # Flush the input buffer to make sure it is ready for a new command
                self.flush()
                 
                # Wait
                self.lastError = Check
                print(Check)
                f.time.sleep(self._attemptDelay)
            
            # Check that it got a response
            if Check is not None:
                raise e.CommunicationError(self.deviceName, self, Command, Check)
            
        except Exception as m:
            if self._forceClose:
                self.close()
            
            raise m
            
        if self._forceClose:
            self.close()
            
        return ReturnString
    
    # Send a command to the device
    # Command (str): The command to send the device
    # UseQueue (bool): Whether to run the command through the queue or not
    # WriteArgs (set): The args sent to the write command
    # WriteKwargs (dict): The kwargs sent to the write command
    # ReadArgs (set): The args sent to the read command
    # ReadKwargs (dict): The kwargs sent to the read command
    # ResponseCheck (Func): A function to check if the response was correct, None if no check should be used, the function must have the arguments (Class, Command, ReturnString) and must return None on succes or a string on failure with the error message
    # ReturnLines (int): The number of lines it expects to receive from the device
    # WaitTime (float): The time in seconds to wait before reading
    def sendCommand(self, Command, *args, UseQueue = True, **kwargs):
        if UseQueue:
            return self._q.call((self._sendCommand, (Command,) + args, kwargs), Wait = True)
            
        else:
            return self._sendCommand(Command, *args, **kwargs)
        
    # Sends a command without expecting a response
    # Command (str): The command to send the device
    # UseQueue (bool): Whether to run the command through the queue or not
    # WriteArgs (set): The args sent to the write command
    # WriteKwargs (dict): The kwargs sent to the write command
    # ReadArgs (set): The args sent to the read command
    # ReadKwargs (dict): The kwargs sent to the read command
    # ResponseCheck (Func): A function to check if the response was correct, None if no check should be used, the function must have the arguments (Class, ReturnString) and must return None on succes or a string on failure with the error message
    # WaitTime (float): The time in seconds to wait before reading
    def sendWithoutResponse(self, *args, **kwargs):
        # Change the return lines
        kwargs["ReturnLines"] = 0
        self.sendCommand(*args, **kwargs)
 
    # Sends a command expecting a single line of response
    # Command (str): The command to send the device
    # UseQueue (bool): Whether to run the command through the queue or not
    # WriteArgs (set): The args sent to the write command
    # WriteKwargs (dict): The kwargs sent to the write command
    # ReadArgs (set): The args sent to the read command
    # ReadKwargs (dict): The kwargs sent to the read command
    # ResponseCheck (Func): A function to check if the response was correct, None if no check should be used, the function must have the arguments (Class, ReturnString) and must return None on succes or a string on failure with the error message
    # WaitTime (float): The time in seconds to wait before reading
    def query(self, *args, **kwargs):
        # Change the return lines
        kwargs["ReturnLines"] = 1
        return self.sendCommand(*args, **kwargs)[0]
        
    def _close(self):
        self._q.kill()   
        super()._close()
    
    def close(self):
        if not self.empty:
            super().close()
