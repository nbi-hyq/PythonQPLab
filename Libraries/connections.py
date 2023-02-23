# Classes to create connections to devices and other useful classes

import threading as th
import functions as f
import exceptions as e

class timerObj(th.Thread):
    # Initialise a timer object
    # Interval (float): The number of seconds between each function call
    # Function (func): The function to call every interval, the first argument must be the counter
    # Event (threading.Event): The stop event to stop the timer
    # FunctionArgs (set): The args to pass Function
    # FunctionKwargs (dict): The kwargs to pass Function
    def __init__(self, Interval, Function, Event, *args, FunctionArgs = set(), FunctionKwargs = dict(), **kwargs):
        super().__init__(*args, **kwargs)
    
        # Setup the event
        self._stopEvent = Event
        
        # Setup the interval and function
        self._int = float(Interval)
        self._f = Function
        self._args = FunctionArgs
        self._kwargs = FunctionKwargs
        
        # The count will increase by one everytime it is run
        self._count = 0
        
    # run the timer
    def run(self):
        import time
        import warnings
        
        # Record the start time
        StartTime = time.time()
        
        # Run the timer
        while not self._stopEvent.wait(max(StartTime + self._int * self._count - time.time(), 0)):
            # Run the function
            try:
                self._f(self._count, *self._args, **self._kwargs)
            
            except Exception as ErrorMes:
                # Print the error
                Mes = f"An exception occured in timer as count {self._count}: {ErrorMes}"
                warnings.warn(Mes)

            # Increase the count
            self._count += 1
            
    
class timer(object):
    # Initialize a timer which runs runs Function every Interval seconds
    # Interval (float): The number of seconds between each function call
    # Function (func): The function to call every interval, the first argument must be the counter   
    # TimerKwargs may include:
    # FunctionArgs (set): The args to pass Function
    # FunctionKwargs (dict): The kwargs to pass Function
    def __init__(self, Interval, Function, *args, TimerKwargs = dict(), **kwargs):
        import weakref
        
        super().__init__(*args, **kwargs)
        
        # Create the timer object
        self._stopEvent = th.Event()
        
        self._timer = timerObj(Interval, Function, self._stopEvent, **TimerKwargs)
        
        weakref.finalize(self, self.stop)
        
    # Starts the timer
    def start(self):
        self._timer.start()
        
    # Stops the timer
    def stop(self):
        self._stopEvent.set()


# Implements a queue system while allowing plotting interactions by the user
class queue(th.Thread):
    # MaxLength (int): The maximum length of the queue
    # WaitInterval (float): The time in seconds to wait between checking for updates
    def __init__(self, *args, MaxLength = 1000, WaitInterval = 0.01, **kwargs):
        import weakref
        
        super().__init__(*args, **kwargs)
        
        self._alive = True
        self._size = int(MaxLength)
        self._q = [None] * int(MaxLength)
        self._getPos = 0
        self._putPos = 0
        self._waitTime = float(WaitInterval)
        
        self.start()
        weakref.finalize(self, self.kill)
        
    # Adds an item to the queue
    # Function (callable): The function to run
    # Args (tuple): The args of the function
    # Kwargs (dict): The kwargs for the function
    # Wait (bool): If True then it will wait until it has been processed and then return the return value, if False then it returns the ID
    def call(self, Function, Args = tuple(), Kwargs = dict(), Wait = True):
        if not self.is_alive():
            raise e.NotRunningError("Queue", self)

        Return = [None]

        # Make sure Function is a callable
        if not callable(Function):
            raise e.TypeDefError("Function", Function, "callable")
            
        Args = tuple(Args)
        Kwargs = dict(Kwargs)
        
        # Get the ID to put at
        ID = self._putPos
        
        if self._q[ID] is not None:
            raise e.QueueError()
        
        self._putPos = (self._putPos + 1) % self.size
        
        # Put the item
        self._q[ID] = (Function, Args, Kwargs, Return)
        
        # Wait
        if Wait:
            self.wait(ID)
            
        else:
            return ID
        
        # Check for error
        if Return[0][0]:
            return Return[0][1]
        
        else:
            raise Return[0][1]
            
    # Waits for an item to finish, still allows interactive plotting
    # ID (int): The ID of the item
    def wait(self, ID):
        import functions as f
        
        while self._q[ID] is not None:
            f.time.sleep(self._waitTime)
            
    def run(self):
        import warnings
        import functions as f
       
        while True:
            # If there is no task
            if self._q[self._getPos] is None:
                f.time.sleep(self._waitTime)
                continue
            
            # Run a taks
            Task = self._q[self._getPos]
            
            # Check if it should kill the queue
            if Task[0] == "kill":
                break
                
            # Run a function
            try:
                Result = Task[0](*Task[1], **Task[2])
                State = True
                
            except Exception as ErrorMes:
                Warn = e.PropagationError(ErrorMes, "processing an item in the queue")
                warnings.warn(Warn.message)
                Result = ErrorMes
                State = False
            
            # Send result
            Task[3][0] = (State, Result)

            # Mark the task as done
            self._q[self._getPos] = None
            self._getPos = (self._getPos + 1) % self._size
           
    # Kills the queue after finishing all tasks
    def kill(self):
        if self.isAlive():
            self._alive = False
            self.call("kill", Wait = False)
            
    # Checks if the queue is alive
    def isAlive(self):
        return self._alive and self.is_alive()
      
    # Returns the number of elements in the queue
    def getSize(self):
        Size = self._putPos - self._getPos
        
        if Size < 0:
            Size += self._size
            
        return Size


# A queue object for replacing queue if no new thread should be created
class queueNoThread:
    # MaxLength (int): The maximum length of the queue, kept for compatibility
    # WaitInterval (float): The time in seconds to wait between checking for updates, kept for compatibility
    def __init__(self, *args, MaxLength = 1000, WaitInterval = 0.01, **kwargs):
        import weakref
        
        super().__init__(*args, **kwargs)
        
        self._alive = True
        self._size = int(MaxLength)
        self._q = [None] * int(MaxLength)
        self._getPos = 0
        self._putPos = 0
        self._waitTime = float(WaitInterval)
        
        weakref.finalize(self, self.kill)
        
    # Adds an item to the queue
    # Function (callable): The function to run
    # Args (tuple): The args of the function
    # Kwargs (dict): The kwargs for the function
    # Wait (bool): If True then it will wait until it has been processed and then return the return value, if False then it returns the ID
    def call(self, Function, Args = tuple(), Kwargs = dict(), Wait = True):
        if not self.is_alive():
            raise e.NotRunningError("Queue", self)

        # Make sure Function is a callable
        if not callable(Function):
            raise e.TypeDefError("Function", Function, "callable")
            
        Args = tuple(Args)
        Kwargs = dict(Kwargs)
        
        # Handle error
        Result = Function(*Args, **Kwargs)
        
        # Wait
        if Wait:
            return Result
            
        else:
            return 0
            
    # Waits for an item to finish, still allows interactive plotting
    # ID (int): The ID of the item
    def wait(self, ID):
        pass
       
    # Kills the queue after finishing all tasks
    def kill(self):
        if self.isAlive():
            self._alive = False
            
    # Checks if the queue is alive
    def isAlive(self):
        return self._alive
      
    # Returns the number of elements in the queue
    def getSize(self):
        return 0
        
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
        import functions as f
        
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
    

# Controls a socket connection
class socket(device):
    # IP (str): The IP of the connection
    # Port (int): The port to communicate through
    # BufferSize (int): The size of the buffer when getting data
    # Timeout (float): The timeout in seconds
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
    def __init__(self, IP, Port, *args, BufferSize = 4096, Timeout = 1, ReadTermination = "\n", WriteTermination = "\n", **kwargs):
        # Set the name
        if not "DeviceName" in kwargs:
            kwargs["DeviceName"] = "Socket"

        kwargs["OpenArgs"] = (IP, Port)
        kwargs["OpenKwargs"] = {"Timeout": Timeout}
            
        # Run the super init
        super().__init__(*args, **kwargs)

        # Set default values
        self._bufferSize = int(BufferSize)
        self._lines = []
        self._mes = b""
        self._timeout = float(Timeout)
        self._readTermination = str(ReadTermination).encode("utf-8")
        self._readTerminationLength = len(ReadTermination)
        self._writeTermination = str(WriteTermination)
        
    # Writes a message to the device
    # Message (str): The message to write
    def write(self, Message):
        self._socket.send(f"{str(Message)}{self._writeTermination}".encode("utf-8"))
    
    # Read until it has received a line and store everything
    def _readUntilLine(self):
        import time
        
        StartTime = time.time()
        
        while (time.time() - StartTime) < self._timeout:
            Read = self._socket.recv(self._bufferSize)
            
            # Append to the message
            self._mes += Read
            
            # Look for a newline
            if self._readTermination in Read:
                # Split the message
                FirstPos = 0
                i = 0
                
                while i <= len(self._mes) - self._readTerminationLength:
                    if self._mes[i:i + self._readTerminationLength] == self._readTermination:
                        Line = self._mes[FirstPos:i]
                        FirstPos = i + self._readTerminationLength
                        i += self._readTerminationLength - 1
                        
                        # Convert to text
                        self._lines.append(self.decode(Line))
                        
                    i += 1
                        
                self._mes = self._mes[FirstPos:]
                    
                return
        
        raise e.TimeoutError(self.deviceName, self)
        
    # Decodes bytes to data, may be overwritten by subclass
    # Mes (bytes): The bytes to decode
    def decode(self, Mes):
        return Mes.decode("utf-8")
    
    # Read one line from the device
    def _readLine(self):
        if len(self._lines) == 0:
            self._readUntilLine()
            
        Line = self._lines[0]
        self._lines = self._lines[1:]
        
        return Line
    
    # Reads a message from a device
    # Returns a list of all the lines
    # Lines (int): The number of lines to read
    def read(self, Lines):
        # Read all of the lines
        ReadLines = []
        for _ in range(Lines):
            ReadLines.append(self._readLine())
        
        if len(ReadLines) > Lines:
            ReadLines = ReadLines[:Lines]
            
        return ReadLines
    
    # Opens the device
    # IP (str): The IP of the connection
    # Port (int): The port to communicate through
    # Timeout (float): The timeout in seconds
    def open(self, IP, Port, Timeout = 1):        
        self._address = (str(IP), int(Port))
        self._timeout = float(Timeout)
        
        self.reopen()
    
    # Reopens a connection
    def _reopen(self):
        import socket

        self._socket = socket.create_connection(self._address, timeout = self._timeout)
    
    # Close the device
    def _close(self):
        self._socket.close()
        super()._close()

    # Forces a flush for the device
    def flush(self):
        # Send message
        self._socket.send(self._writeTermination.encode("utf-8"))
        
        # Empty res buffer
        self._socket.settimeout(0.01)
        
        while True:
            try:
                self._socket.recv(self._bufferSize)
            except:
                break
            
        self._socket.settimeout(self._timeout)
        self._lines = []
        self._mes = b""
        

# A socket object tailored to communicate with a socketServer
class socketClient(socket):
    # Command (str): The command to send the device
    # UseQueue (bool): Whether to run the command through the queue or not, ignored if the device was initialized with UseQueue = False
    # ResponseCheck (Func): A function to check if the response was correct, None if no check should be used, the function must have the arguments (Class, Command, ReturnString) and must return None on succes or a string on failure with the error message
    # WaitTime (float): The time in seconds to wait before reading
    def sendCommand(self, *args, **kwargs):
        # Set the return lines to be 1
        kwargs["ReturnLines"] = 1
        
        # Set the function to be correct
        if "ResponseCheck" in kwargs:
            kwargs["ResponseCheck"] = f.responseCheck.socketClient(kwargs["ResponseCheck"])
            
        else:
            kwargs["ResponseCheck"] = f.responseCheck.socketClient(None)
            
        return super().sendCommand(*args, **kwargs)[0][2:].split("|")
        
        
# A communication channel for a socket server to a single client
class socketChannel(object):
    # Connection (socket.connection): The connection through which to speak with the client
    # Address (2-tuple of str, int): A tuple containing the IP and the port of the client
    # ProcessFunc (func): The _process method from the server to process any incoming message
    # StopEvent (threading.Event): The stop event to signal that it should shut down
    # MaxSize (int): The maximum buffer size
    # ForceClose (bool): If True then it will force the connection to close after 1 message, should not be used
    # ReadTermination (str): The character to look for when reading to terminate a command
    # WriteTermination (str): The character to put at the end of a message when writing to the client
    # DisplayConnection (bool): If True then it will print when a client has connected or disconnected    
    def __init__(self, Connection, Address, ProcessFunc, StopEvent, *args, MaxSize = 4096, ForceClose = False, ReadTermination = "\n", WriteTermination = "\n", DisplayConnection = True, **kwargs):
        super().__init__(*args, **kwargs)
        
        self._connection = Connection
        self._address = Address
        self._maxSize = int(MaxSize)
        self._stopEvent = StopEvent
        self._readTermination = str(ReadTermination)
        self._writeTermination = str(WriteTermination)
        self._mes = ""
        self._process = ProcessFunc
        self._forceClose = bool(ForceClose)
        self._displayConnection = bool(DisplayConnection)
     
    def communicate(self):
        while not self._stopEvent.is_set():
            try:
                # Get information and do the task
                if not self.read():
                    break
                    
                # Break if it is forced to close
                if self._forceClose:
                    self._connection.close()
                    break
                
            except ConnectionResetError:
                break
                
            except Exception as m:
                print(f"An error occured while reading from {self._address}: {m}")
              
        if self._displayConnection:
            print(f"Closed connection to {self._address}")
     
    def read(self):
        import socket
        
        try:
            Data = self._connection.recv(self._maxSize).decode("utf-8")

            # Break if the connection has been closed
            if not Data:
                self._connection.close()
                return False
            
            # Merge with own message
            self._mes += Data
            
            # Process
            SplitData = self._mes.split(self._readTermination)
    
            self._mes = SplitData[-1]
            
            for DataLine in SplitData[:-1]:
                try:
                    self._connection.send(f"{self._process(DataLine)}{self._writeTermination}".encode("utf-8"))
                    
                except Exception as m:
                    print(f"An exception occured while processing the message \"{DataLine}\": {m}")
                    
                    self._connection.send(f"0|An exception occured{self._writeTermination}".encode("utf-8"))
            
        except socket.timeout:
            pass
        
        return True
    
    
# Controls a socket server
class socketServer(deviceBase):
    # Port (int): The port to use
    # Methods (serverFunction): The possible methods to use
    # IP (str): The IP address of the device to run it on
    # Mode (str): The mode of the server, single: Only allow a single client at the time, multi: Allow multiple clients at the time this is a bit slower than single, threaded: Same as multi but with every client on its own thread, this is as fast as single
    # MaxClients (int): The maximum number of clients allowed to wait
    # MaxSize (int): The maximum number of bytes per message
    # ReadTermination (str): The character to look for when reading to terminate a command
    # WriteTermination (str): The character to put at the end of a message when writing to the client
    # DisplayConnection (bool): If True then it will print when a client has connected or disconnected
    # Timeout (float): How long it will wait for new clients or messages before moving on to the next task
    # ForceClose (bool): Not recommended, if True, then it will force a connection to close after one call
    # DeviceName (str): The name of the device, only used for error messages
    # ID (str): The ID name for the device, only used for displaying infomation
    def __init__(self, Port, Methods, *args, IP = None, Mode = "Single", MaxClients = 100, MaxSize = 4096, ReadTermination = "\n", WriteTermination = "\n", Timeout = 0.01, DisplayConnection = True, ForceClose = False, **kwargs):
        import socket
        
        if not "DeviceName" in kwargs:
            kwargs["DeviceName"] = "Socket Server"
            
        super().__init__(*args, **kwargs)
        
        # Get IP
        if IP is None:
            IP = socket.gethostname()
        
        # Create the server
        if not str(Mode).lower() in ["single", "multi", "threaded"]:
            raise e.KeywordError("Mode", str(Mode).lower(), ["single", "multi", "threaded"])
        
        self._mode = str(Mode).lower()
        self._server = socket.create_server((str(IP), int(Port)), backlog = int(MaxClients))            
        self._timeout = Timeout
        self._server.settimeout(Timeout)
        self._maxSize = int(MaxSize)
        self._readTermination = str(ReadTermination)
        self._writeTermination = str(WriteTermination)
        self._forceClose = bool(ForceClose)
        self._methods = Methods
        self._displayConnection = bool(DisplayConnection)
        self._IP = str(IP)
        self._port = int(Port)
        
        # Create stop event
        self._stopEvent = th.Event()
        self._thread = th.Thread(target = self._listen)
        self._thread.start()
        
    # Listen for connections
    def _listen(self):
        import socket
        
        try:
            # Listen
            self._server.listen()
            Channels = []
            
            # Keep looking for clients
            while not self._stopEvent.is_set():
                try:
                    Connection, Address = self._server.accept()
                    Connection.settimeout(self._timeout)
                    NewChannel = socketChannel(Connection, Address, self._process, self._stopEvent, MaxSize = self._maxSize, ForceClose = self._forceClose, ReadTermination = self._readTermination, WriteTermination = self._writeTermination, DisplayConnection = self._displayConnection)
                       
                    if self._displayConnection:
                        print(f"Established connection to {Address}")
                        
                # Correct when multi
                except socket.timeout:
                    if self._mode == "multi":
                        Length = len(Channels) - 1
                        for i, Channel in enumerate(Channels[::-1]):
                            try:
                                Result = Channel.read()
                                
                            except ConnectionResetError:
                                Result = False

                            except Exception as m:
                                print(f"An error occured while reading from {Channel._address}: {m}")
                                Result = True
                                
                            if not Result:
                                print(f"Closed connection to {Channel._address}")
                                Channels.pop(Length - i)
                                    
                    continue
                
                # Perform task
                if self._mode == "single":
                    NewChannel.communicate()
                    
                # Add to list of channels
                elif self._mode == "multi":
                    Channels.append(NewChannel)
                    
                else: # threaded
                    Thread = th.Thread(target = NewChannel.communicate)
                    Thread.start()
                
        except Exception as m:
            print(m)
            
        self._server.close()
    
    # Process a message
    # Message (str): The message to process
    def _process(self, Message):
        return self._methods.run(Message)
    
    # Returns the IP and port of the server
    def getIP(self):
        return self._IP, self._port
        
    # Close the server
    def _close(self):
        self._stopEvent.set()
        super()._close()
        
        
# Methods for a socket server
class serverFunction(object):
    # SetFunction (func): The function to run when setting a parameter, the function must take the parameters (Message [str], Data [list])
    # GetFunction (func): The function to run when getting a parameter, the function must take the parameters (Data [list])
    # ToggleFunction (func): The function to run when toggling a parameter, the function must take the parameters (Data [list])
    # InfoConverter (func): A function which must be given if info is expected, it will take the info string and return (bool, Value) where bool is False on error and then Value is an error message, on success value is the converted info
    # ParameterDict (dict): A dictionary containing all of the sub parameters which are all serverFunction
    def __init__(self, *args, SetFunction = None, GetFunction = None, ToggleFunction = None, ParameterDict = dict(), InfoConverter = None, **kwargs):
        super().__init__(*args, **kwargs)
        
        self._setFunction = SetFunction
        self._getFunction = GetFunction
        self._toggleFunction = ToggleFunction
        self._subParameters = {}
        self._infoConverter = InfoConverter
        
        for Key in ParameterDict:
            self._subParameters[Key.lower()] = ParameterDict[Key]
        
    def _errorMessage(self, Message):
        return f"0|{Message}"
    
    def _correctMessage(self, Message):
        return f"1|{Message}"
        
    # Runs the function
    # Message (str): The command to run
    # Info (str): The extra data it gets, None if no info
    # Data (list): A list of all previous info
    # Set (bool): True if this function is a setter
    # Get (bool): True if this function is a getter
    def run(self, Message, Info = None, Data = None, Set = False, Get = False, Name = None):
        if Data is None:
            Data = []
            
        Message = str(Message).strip()
        
        # Save the info
        if Info is not None and self._infoConverter is None:
            return self._errorMessage(f"Received info {Info} for {Name} when not needed, remaining message: {Message}")
        
        elif Info is None and self._infoConverter is not None:
            return self._errorMessage(f"Did not receive info for {Name} when needed, remaining message: {Message}")
        
        elif self._infoConverter is not None:
            Code, Value = self._infoConverter(str(Info))
            
            if not Code:
                return self._errorMessage(Value)
            
            Data.append(Value)
            
        # Run get function
        if Get:
            if self._getFunction is None:
                return self._errorMessage(f"Requested get function for {Name} but this does not exist, remaining message: {Message}")
            
            Code, Message = self._getFunction(Data)
        
        # Run the set function
        elif Set:
            if self._setFunction is None:
                return self._errorMessage(f"Requested set function for {Name} but this does not exist, remaining message: {Message}")

            Code, Message = self._setFunction(Message, Data)

        # Run the toggle function
        elif len(Message) == 0:
            if self._toggleFunction is None:
                return self._errorMessage(f"Requested toggle function for {Name} but this does not exist, remaining message: {Message}")
                
            Code, Message = self._toggleFunction(Data)
        
        # New parameter
        else:
            NextPar = Message.find(":")
            NextSet = Message.find("=")
            NextGet = Message.find("?")
            
            if NextPar == -1:
                NextPar = len(Message)

            if NextSet == -1:
                NextSet = len(Message)
                
            if NextGet == -1:
                NextGet = len(Message)
            
            if NextSet < NextPar and NextSet < NextGet:
                Set = True
                NextPar = NextSet
                
            elif NextGet < NextPar and NextGet < NextSet:
                Get = True
                NextPar = NextGet
                
            # Figure out if there is info
            NextInfo = Message.find("-")
            
            if NextInfo == -1 or NextInfo > NextPar:
                Info = None
                NextInfo = NextPar
                
            else:
                Info = Message[NextInfo + 1:NextPar]
                
            # Find the parameter
            Parameter = Message[:NextInfo].replace(" ", "")
            
            if Parameter.lower() not in self._subParameters:
                return self._errorMessage(f"Parameter \"{Parameter}\" for {Name} does not exist, remaining message: {Message}")
            
            # Run the function
            if Name is None:
                NewName = f"{Parameter}"
                
            else:
                NewName = Name + f":{Parameter}"
                
            return self._subParameters[Parameter.lower()].run(Message[NextPar + 1:], Info = Info, Data = Data, Set = Set, Get = Get, Name = NewName)
            
        if Code:
            return self._correctMessage(Message)
        
        else:
            return self._errorMessage(Message)