from ..connections import device, deviceBase
from .. import exceptions as e

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
        from .. import functions as f
        
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
        import threading as th
        
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
        import threading as th
        
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