# Documentation for connections

This is a collection of connection classes for different methods of connecting to devices, all classes have an empty version which can be used for testing while the device is not connected to the computer. It also includes classes for multi threading as well

---

# Classes

---

## timerObj(Interval, Function, Event, FunctionArgs = set(), FunctionKwargs = dict())

Runs Function once every Interval seconds on a new thread until Event has been activated, must do .start() to start the thread

- Interval (float): The number of seconds between each function call
- Function (func): The function to call every interval, the first argument must be the counter
- Event (threading.Event): The stop event to stop the timer
- FunctionArgs (set): The args to pass Function
- FunctionKwargs (dict): The kwargs to pass Function

Inherits from threading.Thread

---
---

## timer(Interval, Function, *args, TimerKwargs, **kwargs)

Initialize a timer which runs runs Function every Interval seconds

- Interval (float): The number of seconds between each function call
- Function (func): The function to call every interval, the first argument must be the counter   
- TimerKwargs (dict): The kwargs to give to the timer

TimerKwargs may include:
- FunctionArgs (set): The args to pass Function
- FunctionKwargs (dict): The kwargs to pass Function

---

### method start()

Starts the timer, can only be run once

---

### method stop()

Kills the timer thread

---
---

## queue()

Implements a queue system while allowing plotting interactions by the user

Inherits from threading.Thread

---

### method call(Function, Args = tuple(), Kwargs = dict(), Wait = True)

Adds an item to the queue

- Function (callable): The function to run
- Args (tuple): The args of the function
- Kwargs (dict): The kwargs for the function
- Wait (bool): If True then it will wait until it has been processed and then return the return value, if False then it returns the ID

If Wait is True then it will return the return value of the function, otherwise it returns the ID of the item

---

### method kill()

Kills the queue thread after evaluating all leftover items in the queue

---

### method isAlive()

Returns True if the queue is still alive, False if it has been stopped or scheduled to be stopped

---

### method getSize()

Gets the number of calls in the queue

Returns the number of calls as an int

---
---

## queueNoThread()

An empty queue object which also has a call function but doesn't actually implement a queue, is meant to mimic a queue to use in devices that don't need one

---

### method call(Function, Args = tuple(), Kwargs = dict(), Wait = True)

Adds an item to the queue

- Function (callable): The function to run
- Args (tuple): The args of the function
- Kwargs (dict): The kwargs for the function
- Wait (bool): If True then it will wait until it has been processed and then return the return value, if False then it returns the ID

If Wait is True then it will return the return value of the function, otherwise it returns 0

---

### method kill()

Does nothing, only here for the sake of mimiking a real queue

---

### method isAlive()

Always returns True

### method getSize()

Always returns 0, kept for compatibility

---
---

## deviceBase(DeviceName = "Device", ID = None)

Defines the bare minimum for a device

- DeviceName (str): The name of the device
- ID (str): The ID name for the device, only used for displaying infomation

---

### method isOpen()

Checks if the device is open, may be overwritten by the sub class if it can be closed

Returns True if it is open and False if not

---

### method close()

Close the device, implement the closing of the device in the _close method, remember super()._close()

---

### property deviceName (str)

The name of the device

---
---

## device(ReconnectTries = 100, ReconnectDelay = 1, MaxAttempts = 100, AttemptDelay = 1, UseQueue = True, ForceClose = False, Empty = False, OpenArgs = set(), OpenKwargs = dict(), DeviceName = "Device", ID = None)

The base controller class for most devices

- ReconnectTries (int): How many times to attempt to reconnect if it disconnects, must not be smaller than 0
- ReconnectDelay (float): The delay in seconds between each reconnect attempt, must not be negative
- MaxAttempts (int): The maximum number attempts to send a command before giving up, must not be smaller than 1
- AttemptDelay (float): The delay in seconds between each attempt to send a command, must not be negative
- UseQueue (bool): If True then it will set up a queue which can be used in the sendCommand method, if False the UseQueue in sendCommand is ignored
- ForceClose (bool): If true then it should close the connection every time it sends a message and reopen
- Empty (bool): If True then it will not communicate with the device
- OpenArgs (set): Arguments sent to open
- OpenKwargs (dict): Arguments sent to open
- DeviceName (str): The name of the device, only used for error messages
- ID (str): The ID name for the device, only used for displaying infomation

Inherits from deviceBase 

---

### method setEmptyReturn(Value)

Sets the return value if empty is true

- Value (str/list): If a list of strings then this will be the return value of the read, if a string the it will be repeated by the number of return lines

---

### method write(Message)

Writes a message to the device, must be overwritten by the sub class

- Message (str): The message to write

args and kwargs may be used for the device write command

---

### method read(Lines)

Reads a message from a device, must be overwritten by the sub class

- Lines (int): The number of lines to read

Returns a list of all the lines, args and kwargs may be used for the device read command

---

### method flush()

Flushes the device, must be overwritten by the sub class is flushing is posible

---

### method reopen()

Opens the device again, the _reopen method must be overwritten by the sub class if it can be reopened

---

### method open()

Opens the device, must be overwritten by the sub class

---

### method sendCommand(Command, UseQueue = True, WriteArgs = set(), WriteKwargs = dict(), ReadArgs = set(), ReadKwargs = dict(), ResponseCheck = None, ReturnLines = 1, WaitTime = 0)

Send a command to the device

- Command (str): The command to send the device
- UseQueue (bool): Whether to run the command through the queue or not, ignored if the device was initialized with UseQueue = False
- WriteArgs (set): The args sent to the write command
- WriteKwargs (dict): The kwargs sent to the write command
- ReadArgs (set): The args sent to the read command
- ReadKwargs (dict): The kwargs sent to the read command
- ResponseCheck (Func): A function to check if the response was correct, None if no check should be used, the function must have the arguments (Class, Command, ReturnString) and must return None on succes or a string on failure with the error message
- ReturnLines (int): The number of lines it expects to receive from the device
- WaitTime (float): The time in seconds to wait before reading

Returns the list of return lines as a list of strings

---

### method sendWithoutResponse(Command, UseQueue = True, WriteArgs = set(), WriteKwargs = dict(), ReadArgs = set(), ReadKwargs = dict(), ResponseCheck = None, WaitTime = 0)

Sends a command without expecting a response

- Command (str): The command to send the device
- UseQueue (bool): Whether to run the command through the queue or not, ignored if the device was initialized with UseQueue = False
- WriteArgs (set): The args sent to the write command
- WriteKwargs (dict): The kwargs sent to the write command
- ReadArgs (set): The args sent to the read command
- ReadKwargs (dict): The kwargs sent to the read command
- ResponseCheck (Func): A function to check if the response was correct, None if no check should be used, the function must have the arguments (Class, Command, ReturnString) and must return None on succes or a string on failure with the error message
- WaitTime (float): The time in seconds to wait before reading

---

### method query(Command, UseQueue = True, WriteArgs = set(), WriteKwargs = dict(), ReadArgs = set(), ReadKwargs = dict(), ResponseCheck = None, WaitTime = 0)

Sends a command expecting a single line of response

- Command (str): The command to send the device
- UseQueue (bool): Whether to run the command through the queue or not, ignored if the device was initialized with UseQueue = False
- WriteArgs (set): The args sent to the write command
- WriteKwargs (dict): The kwargs sent to the write command
- ReadArgs (set): The args sent to the read command
- ReadKwargs (dict): The kwargs sent to the read command
- ResponseCheck (Func): A function to check if the response was correct, None if no check should be used, the function must have the arguments (Class, Command, ReturnString) and must return None on succes or a string on failure with the error message
- WaitTime (float): The time in seconds to wait before reading

Returns the return string as a single string

---

### property empty (bool)

If True then it does not connect to the device but only acts as a shell

---

### property lastError (str)

The last error that occured doing writing

---
---

## serial(Port, Baudrate = 9600, Timeout = 1, ReadTermination = "\r\n", WriteTermination = "\n", BytesMode = False, ReconnectTries = 100, ReconnectDelay = 1, MaxAttempts = 100, AttemptDelay = 1, UseQueue = True, ForceClose = False, Empty = False, DeviceName = "Serial", ID = None)

A python controller for a serial connection

- Port (str): The name of the COM port through which to access the serial connection
- Baudrate (int): The baudrate of the connection
- Timeout (float): The timeout time for the connection, must not be negative
- ReadTermination (str): The termination character to look for when reading
- WriteTermination (str): The termination character when writing a message
- BytesMode (bool): If true it will just send and receive bytes (Then ReturnLines turns into the number of bytes to receive)
- ReconnectTries (int): How many times to attempt to reconnect if it disconnects, must not be smaller than 0
- ReconnectDelay (float): The delay in seconds between each reconnect attempt, must not be negative
- MaxAttempts (int): The maximum number attempts to send a command before giving up, must not be smaller than 1
- AttemptDelay (float): The delay in seconds between each attempt to send a command, must not be negative
- UseQueue (bool): If True then it will set up a queue which can be used in the sendCommand method, if False the UseQueue in sendCommand is ignored
- ForceClose (bool): If true then it should close the connection every time it sends a message and reopen
- Empty (bool): If True then it will not communicate with the device
- DeviceName (str): The name of the device, only used for error messages
- ID (str): The ID name for the device, only used for displaying infomation

Inherits from the device class

---
---

## visa(ResourceName, Baudrate = 9600, Timeout = 1, ReadTermination = "\n", WriteTermination = "\n", ReconnectTries = 100, ReconnectDelay = 1, MaxAttempts = 100, AttemptDelay = 1, UseQueue = True, ForceClose = False, Empty = False, DeviceName = "Visa", ID = None)

A python controller for a visa connection

- ResourceName (str): The resource name of the device to access
- Baudrate (int): The baudrate of the connection
- Timeout (float): The timeout time for the connection, must not be negative
- ReadTermination (str): The termination character to look for when reading
- WriteTermination (str): The termination character when writing a message
- ReconnectTries (int): How many times to attempt to reconnect if it disconnects, must not be smaller than 0
- ReconnectDelay (float): The delay in seconds between each reconnect attempt, must not be negative
- MaxAttempts (int): The maximum number attempts to send a command before giving up, must not be smaller than 1
- AttemptDelay (float): The delay in seconds between each attempt to send a command, must not be negative
- UseQueue (bool): If True then it will set up a queue which can be used in the sendCommand method, if False the UseQueue in sendCommand is ignored
- ForceClose (bool): If true then it should close the connection every time it sends a message and reopen
- Empty (bool): If True then it will not communicate with the device
- DeviceName (str): The name of the device, only used for error messages
- ID (str): The ID name for the device, only used for displaying infomation

Inherits from the device class

---
---

## dll(DLLPath, ReconnectTries = 100, ReconnectDelay = 1, MaxAttempts = 100, AttemptDelay = 1, UseQueue = True, ForceClose = False, Empty = False, DeviceName = "DLL", ID = None)

A python controller for a device accessed via a dll

- DLLPath (str): The path to the dll to load
- ReconnectTries (int): How many times to attempt to reconnect if it disconnects, must not be smaller than 0
- ReconnectDelay (float): The delay in seconds between each reconnect attempt, must not be negative
- MaxAttempts (int): The maximum number attempts to send a command before giving up, must not be smaller than 1
- AttemptDelay (float): The delay in seconds between each attempt to send a command, must not be negative
- UseQueue (bool): If True then it will set up a queue which can be used in the sendCommand method, if False the UseQueue in sendCommand is ignored
- ForceClose (bool): If true then it should close the connection every time it sends a message and reopen
- Empty (bool): If True then it will not communicate with the device
- DeviceName (str): The name of the device, only used for error messages
- ID (str): The ID name for the device, only used for displaying infomation

Inherits from the device class

---

### method runFunction(Name, Args = set(), UseQueue = True, ResponseCheck = None, ReturnLines = 1, WaitTime = 0)

Runs a function from the dll, the sendCommand, sendWithoutResponse and query methods should not be used

- Name (str): The name of the function
- Args (set): The arguments of the function
- UseQueue (bool): Whether to run the command through the queue or not, ignored if the device was initialized with UseQueue = False
- ResponseCheck (Func): A function to check if the response was correct, None if no check should be used, the function must have the arguments (Class, Command, ReturnString) and must return None on succes or a string on failure with the error message
- ReturnLines (int): The number of lines it expects to receive from the device
- WaitTime (float): The time in seconds to wait before reading


Returns the return value of the dll function

---

### method setupFunction(Function, ReturnType, ArgTypes)

Sets up a function from lib, must be run once before using the function, preferably in the init function

- Function (str): The name of the function
- ReturnType (ctypes.PyCSimpleType): The return type of the function
- ArgTypes (list of ctypes.PyCSimpleType): A list with the types of all the arguments

---
---

## external(Library, ReconnectTries = 100, ReconnectDelay = 1, MaxAttempts = 100, AttemptDelay = 1, UseQueue = True, ForceClose = False, Empty = False, OpenArgs = set(), OpenKwargs = dict(), DeviceName = "External", ID = None)

A controller for a device which is controlled by other python functions

- Library (object): The object containing all the external functions
- ReconnectTries (int): How many times to attempt to reconnect if it disconnects, must not be smaller than 0
- ReconnectDelay (float): The delay in seconds between each reconnect attempt, must not be negative
- MaxAttempts (int): The maximum number attempts to send a command before giving up, must not be smaller than 1
- AttemptDelay (float): The delay in seconds between each attempt to send a command, must not be negative
- UseQueue (bool): If True then it will set up a queue which can be used in the sendCommand method, if False the UseQueue in sendCommand is ignored
- Empty (bool): If True then it will not communicate with the device
- ForceClose (bool): If true then it should close the connection every time it sends a message and reopen
- OpenArgs (set): Arguments sent to open
- OpenKwargs (dict): Arguments sent to open
- DeviceName (str): The name of the device, only used for error messages
- ID (str): The ID name for the device, only used for displaying infomation    

Inherits from the device class

---

### method runFunction(Name, Args = set(), Kwargs = dict(), UseQueue = True, ResponseCheck = None, ReturnLines = 1, WaitTime = 0)

Runs a function from the library

- Name (str): The name of the function
- Args (set): The arguments of the function
- Kwargs (dict): The kwargs for the function
- UseQueue (bool): Whether to run the command through the queue or not
- ResponseCheck (Func): A function to check if the response was correct, None if no check should be used, the function must have the arguments (Class, Command, ReturnString) and must return None on succes or a string on failure with the error message
- ReturnLines (int): The number of lines it expects to receive from the device, this is uniused unless implemented by the device
- WaitTime (float): The time in seconds to wait before reading

Returns the return value of the function

---
---

## socket(IP, Port, BufferSize = 4096, Timeout = 1, ReadTermination = "\n", WriteTermination = "\n", ReconnectTries = 100, ReconnectDelay = 1, MaxAttempts = 100, AttemptDelay = 1, UseQueue = True, ForceClose = False, Empty = False, DeviceName = "Socket", ID = None)

A python controller for a device using a socket connection

- IP (str): The IP of the connection
- Port (int): The port to communicate through
- BufferSize (int): The size of the buffer when getting data
- Timeout (float): The timeout in seconds
- ReadTermination (str): The termination character to look for when reading
- WriteTermination (str): The termination character when writing a message
- ReconnectTries (int): How many times to attempt to reconnect if it disconnects, must not be smaller than 0
- ReconnectDelay (float): The delay in seconds between each reconnect attempt, must not be negative
- MaxAttempts (int): The maximum number attempts to send a command before giving up, must not be smaller than 1
- AttemptDelay (float): The delay in seconds between each attempt to send a command, must not be negative
- UseQueue (bool): If True then it will set up a queue which can be used in the sendCommand method, if False the UseQueue in sendCommand is ignored
- ForceClose (bool): If true then it should close the connection every time it sends a message and reopen
- Empty (bool): If True then it will not communicate with the device
- DeviceName (str): The name of the device, only used for error messages
- ID (str): The ID name for the device, only used for displaying infomation

Inherits from the device class

---

### method decode(Mes)

Decodes bytes to data, may be overwritten by subclass

- Mes (bytes): The bytes to decode

---
---

## socketClient(IP, Port, BufferSize = 4096, Timeout = 1, ReadTermination = "\n", WriteTermination = "\n", ReconnectTries = 100, ReconnectDelay = 1, MaxAttempts = 100, AttemptDelay = 1, UseQueue = True, ForceClose = False, Empty = False, DeviceName = "Socket", ID = None)

A socket class with a modified sendCommand method to match the return signature of the socketServer

- IP (str): The IP of the connection
- Port (int): The port to communicate through
- BufferSize (int): The size of the buffer when getting data
- Timeout (float): The timeout in seconds
- ReadTermination (str): The termination character to look for when reading
- WriteTermination (str): The termination character when writing a message
- ReconnectTries (int): How many times to attempt to reconnect if it disconnects, must not be smaller than 0
- ReconnectDelay (float): The delay in seconds between each reconnect attempt, must not be negative
- MaxAttempts (int): The maximum number attempts to send a command before giving up, must not be smaller than 1
- AttemptDelay (float): The delay in seconds between each attempt to send a command, must not be negative
- UseQueue (bool): If True then it will set up a queue which can be used in the sendCommand method, if False the UseQueue in sendCommand is ignored
- ForceClose (bool): If true then it should close the connection every time it sends a message and reopen
- Empty (bool): If True then it will not communicate with the device
- DeviceName (str): The name of the device, only used for error messages
- ID (str): The ID name for the device, only used for displaying infomation

Inherits from the socket class

---

### method sendCommand(Command, UseQueue = True, ResponseCheck = None, WaitTime = 0)

Send a command to the device

- Command (str): The command to send the device
- UseQueue (bool): Whether to run the command through the queue or not, ignored if the device was initialized with UseQueue = False
- ResponseCheck (Func): A function to check if the response was correct, None if no check should be used, the function must have the arguments (Class, Command, ReturnString) and must return None on succes or a string on failure with the error message
- WaitTime (float): The time in seconds to wait before reading

Returns the list of return lines as a list of strings

---

### method sendWithoutResponse(Command, UseQueue = True, ResponseCheck = None, WaitTime = 0)

Sends a command without expecting a response

- Command (str): The command to send the device
- UseQueue (bool): Whether to run the command through the queue or not, ignored if the device was initialized with UseQueue = False
- ResponseCheck (Func): A function to check if the response was correct, None if no check should be used, the function must have the arguments (Class, Command, ReturnString) and must return None on succes or a string on failure with the error message
- WaitTime (float): The time in seconds to wait before reading

---

### method query(Command, UseQueue = True, ResponseCheck = None, WaitTime = 0)

Sends a command expecting a single line of response

- Command (str): The command to send the device
- UseQueue (bool): Whether to run the command through the queue or not, ignored if the device was initialized with UseQueue = False
- ResponseCheck (Func): A function to check if the response was correct, None if no check should be used, the function must have the arguments (Class, Command, ReturnString) and must return None on succes or a string on failure with the error message
- WaitTime (float): The time in seconds to wait before reading

Returns the return string as a single string

---
---

## socketServer(Port, Methods, IP = None, Mode = "Single", MaxClients = 100, MaxSize = 4096, ReadTermination = "\n", WriteTermination = "\n", Timeout = 0.01, DisplayConnection = True, ForceClose = False, DeviceName = "Socket Server", ID = None)

- Port (int): The port to use
- Methods (serverFunction): The possible methods to use
- IP (str): The IP address of the device to run it on
- Mode (str): The mode of the server, single: Only allow a single client at the time, multi: Allow multiple clients at the time this is a bit slower than single, threaded: Same as multi but with every client on its own thread, this is as fast as single
- MaxClients (int): The maximum number of clients allowed to wait
- MaxSize (int): The maximum number of bytes per message
- ReadTermination (str): The character to look for when reading to terminate a command
- WriteTermination (str): The character to put at the end of a message when writing to the client
- DisplayConnection (bool): If True then it will print when a client has connected or disconnected
- Timeout (float): How long it will wait for new clients or messages before moving on to the next task
- ForceClose (bool): Not recommended, if True, then it will force a connection to close after one call
- DeviceName (str): The name of the device, only used for error messages
- ID (str): The ID name for the device, only used for displaying infomation

Inherits from deviceBase

---

### method getIP()

Gets the IP and host of the server

Returns (IP (str), Host (int)) of the server

---
---

## socketChannel(Connection, Address, ProcessFunc, StopEvent, MaxSize = 4096, ForceClose = False, ReadTermination = "\n", WriteTermination = "\n", DisplayConnection = True)

A communication channel for a socket server to a single client

- Connection (socket.connection): The connection through which to speak with the client
- Address (2-tuple of str, int): A tuple containing the IP and the port of the client
- ProcessFunc (func): The _process method from the server to process any incoming message
- StopEvent (threading.Event): The stop event to signal that it should shut down
- MaxSize (int): The maximum buffer size
- ForceClose (bool): If True then it will force the connection to close after 1 message, should not be used
- ReadTermination (str): The character to look for when reading to terminate a command
- WriteTermination (str): The character to put at the end of a message when writing to the client
- DisplayConnection (bool): If True then it will print when a client has connected or disconnected    

---

### method communicate()

Starts communicating with the client until the connection is broken

---

### method read()

Reads all data that has been received up until this point and processes each line

Returns False if the connection is closed, True otherwise

---
---

## serverFunction(SetFunction = None, GetFunction = None, ToggleFunction = None, ParameterDict = dict(), InfoConverter = None)

A method used for a socket server to process a message, the wrapper functions from functions.socket may be useful along with lambda functions for writing compact function interfaces

- SetFunction (func): The function to run when setting a parameter value, the function must take the parameters (Message [str], Data [list])
- GetFunction (func): The function to run when getting a parameter value, the function must take the parameters (Data [list]) and return (ErrorIdentifier [bool], ReturnValue [str]) where ErrorIdentifier is False when an error occured and in that case the ReturnValue is the error message
- ToggleFunction (func): The function to run when toggling a parameter, the function must take the parameters (Data [list])
- InfoConverter (func): A function which must be given if info is expected, it will take the info string and return (ErrorIdentifier [bool], Data [any/str]) where ErrorIdentifier is False on error and then Data is an error message, on success Data is the converted info
- ParameterDict (dict): A dictionary containing all of the sub parameters which are all serverFunction, upper or lower case letters does not matter here

---

### method run(Message, Info = None, Data = None, Set = False, Get = False, Name = None)

Runs the function, spaces and upper/lower cases does not matter, if the message is ":<Field><RestMes>" then it will attempt to find <Field> in the subParameters and run this function on <RestMes>. If the message is "=<Value>" then the Set function is run on <Value>. If the message is "?" then the Get function is run and the return value is returned. If there are no more message then the Toggle function is run

- Message (str): The command to run
- Info (str): The extra data it gets, None if no info, external calls should pass None
- Data (list): A list of all previous info, external calls should pass None
- Set (bool): True if this function is a setter, external calls should pass None
- Get (bool): True if this function is a getter, external calls should pass None
- Name (str): The name of the previous fields, used for error handling, external calls should pass None

Returns the return string

---
---