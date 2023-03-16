from .. import connections as c
from .. import exceptions as e
from ..interface import laser

# Class to control a CTL
class DLCPro(laser, c.socket):
    # IP (str): The IP of the connection
    # Port (int): The port to communicate through
    # FrequencyControl (bool): If False then it cannot set or get the frequency for this laser
    # SettleTime (float): The allowed time in seconds to set the wavelength
    # SleepTime (float): The time in seconds to sleep before each settle check when setting the wavelength
    # InitWait (float): The time in seconds to let it initialize
    # VoltageRange (2-tuple of float): Them minimum and maximum voltage allowed
    # FrequencyRange (2-tuple of float): The minimum and maximum frequencies allowed, if None then they are calculated from WavelengthRange
    # WavelengthRange (2-tuple of float): The minimum and maximum wavelengths allowed, calculated from FrequencyRange if that is given
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
    def __init__(self, *args, FrequencyControl = True, SettleTime = 25, SleepTime = 0.01, InitWait = 0.05, **kwargs):
        from .. import functions as f
        
        if not "WavelengthRange" in kwargs and not "FrequencyRange" in kwargs:
            kwargs["WavelengthRange"] = (910, 990)
            
        if not "VoltageRange" in kwargs:
            kwargs["VoltageRange"] = (20, 120)
            
        kwargs["WriteTermination"] = "\n"
        kwargs["ReadTermination"] = "> "

        if not "DeviceName" in kwargs:
            kwargs["DeviceName"] = "DLCPro"

        super().__init__(*args, **kwargs)

        # Flush
        f.time.sleep(float(InitWait))
        self.flush()
        
        # Set default parameters
        self._setBool("echo", True)
        self.setVoltage(self.voltageBase)
        
        self._settleTime = float(SettleTime)
        self._sleepTime = float(SleepTime)
        self._allowFrequency = bool(FrequencyControl)
        
    # Decodes a message
    # Mes (str): The message to decode
    def decode(self, Mes):
        # Split it into lines
        FirstPos = 0
        i = 0
        Lines = []
        FoundR = False
        
        for i in range(len(Mes)):
            if Mes[i:i + 1] == b"\r":
                FoundR = True
                continue
            
            if Mes[i:i + 1] == b"\n":
                Lines.append(Mes[FirstPos:i - FoundR])
                FirstPos = i + 1
                FoundR = False
                
            if FoundR is True:
                raise e.IlligalCharError("lonely \\r", Mes)
            
        if FirstPos < len(Mes):
            Lines.append(Mes[FirstPos:])
            
        # Decode text
        DecodeLines = []
        
        for Line in Lines:
            try:
                Decode = Line.decode("utf-8")
                
            except:
                try:
                    Num = f"0x{Line[:6]}"
                    Text = Line[6:].decode("utf-8")
                    Decode = f"{Num} {Text}"
                
                except:
                    Decode = Line
                
            DecodeLines.append(Decode)
                
        return DecodeLines
    
    # Sends a command to the device
    # Command (str): The command to send
    # UseQueue (bool): Whether to run the command through the queue or not
    def sendCommand(self, Command, **kwargs):
        from .. import functions as f
        
        kwargs["ReturnLines"] = 1
        
        if not "ResponseCheck" in kwargs:
            kwargs["ResponseCheck"] = f.responseCheck.DLCPro()
        
        ReturnString = super().sendCommand(Command, **kwargs)[0]
        
        # Remove echo
        if ReturnString[0] == str(Command):
            ReturnString = ReturnString[1:]
            
        return ReturnString[0]
        
    # Sets a parameter
    # Parameter (str): The name of the parameter to set
    # Value (str): The value to set
    # UseQueue (bool): Whether to run the command through the queue or not
    def _setParameter(self, Parameter, Value, **kwargs):
        self.sendCommand(f"(param-set! \'{Parameter} {Value})", **kwargs)
        
    # Gets a parameter
    # Parameter (str): The parameter to get
    # UseQueue (bool): Whether to run the command through the queue or not
    def _getParameter(self, Parameter, **kwargs):
        return self.sendCommand(f"(param-ref \'{Parameter})", **kwargs)
        
    # Sets the value of a parameter
    # Parameter (str): The name of the parameter to set
    # Value (float): The value to set
    # UseQueue (bool): Whether to run the command through the queue or not
    def _setValue(self, Parameter, Value, **kwargs):
        self._setParameter(f"{Parameter}-set", f"{float(Value):1.8g}", **kwargs)
 
    # Gets a value
    # Parameter (str): The parameter to get
    # UseQueue (bool): Whether to run the command through the queue or not
    def _getValue(self, Parameter, **kwargs):
        return float(self._getParameter(f"{Parameter}-act", **kwargs))
    
    # Sets a bool
    # Parameter (str): The parameter to set
    # UseQueue (bool): Whether to run the command through the queue or not
    def _setBool(self, Parameter, Value, **kwargs):
        # Get the mode
        if Value:
            Mode = "#t"
            
        else:
            Mode = "#f"

        self._setParameter(Parameter, Mode, **kwargs)
        
    # Excutes a command
    # Command (str): The command to execute
    # UseQueue (bool): Whether to run the command through the queue or not
    def _execute(self, Command, **kwargs):
        self.sendCommand(f"(exec \'{Command})", **kwargs)
                   
    # Sets the wavelength of the laser
    # Value (float): The value of the wavelength
    # UseQueue (bool): Whether to run the command through the queue or not
    def setWavelength(self, Value, **kwargs):
        import time
        from .. import functions as f
        
        if not self._allowFrequency:
            raise e.ImplementationError("DLCPro.setWavelength")
        
        Value = float(Value)
        
        # Make sure it is within the range
        if not self.wavelengthAllowed(Value):
            raise e.RangeError("Value", Value, self._wavelengthRange[0], self._wavelengthRange[1])
            
        # Reset the voltage
        self.setVoltage(self.voltageBase, **kwargs)
        
        # Set the wavelength
        self._setValue("laser1:ctl:wavelength", Value, **kwargs)
        
        # Wait until it is locked
        StartTime = time.time()
        
        while time.time() - StartTime < self._settleTime:
            # Get state
            State = self._getParameter("laser1:ctl:state", **kwargs)
            
            # Check for success
            if int(State) == 0:
                return
                        
            # Wait
            f.time.sleep(self._sleepTime)

        raise e.StabilizeError(self.deviceName, self, "wavelength")
        
    # Gets the wavelength set by the laser
    # UseQueue (bool): Whether to run the command through the queue or not
    def getWavelength(self, **kwargs):
        if not self._allowFrequency:
            raise e.ImplementationError("DLCPro.getWavelength")

        return self._getValue("laser1:ctl:wavelength", **kwargs)
                
    # Sets the scan parameters
    # StartWavelength (float): The start wavelength of the scan
    # StopWavelength (float): The stop wavelength of the scan
    # Speed (float): The speed of the scan
    # UseQueue (bool): Whether to run the command through the queue or not
    def scan(self, StartWavelength, StopWavelength, Speed, **kwargs):
        if not self._allowFrequency:
            raise e.ImplementationError("DLCPro.scan")

        # Make sure the wavelengths are correct
        if not self.wavelengthAllowed(StartWavelength):
            raise e.RangeError("StartWavelength", StartWavelength, self._wavelengthRange[0], self._wavelengthRange[1])

        if not self.wavelengthAllowed(StopWavelength):
            raise e.RangeError("StopWavelength", StopWavelength, self._wavelengthRange[0], self._wavelengthRange[1])
            
        # Set the scan parameters
        self._setParameter("laser1:ctl:scan:wavelength-begin", StartWavelength, **kwargs)
        self._setParameter("laser1:ctl:scan:wavelength-end", StopWavelength, **kwargs)
        self._setParameter("laser1:ctl:scan:speed", Speed, **kwargs)
    
    # Sets the state of the continuous scan
    # Mode (bool): True if it should do continuous scan
    # UseQueue (bool): Whether to run the command through the queue or not
    def scanContinuous(self, Mode, **kwargs):
        if not self._allowFrequency:
            raise e.ImplementationError("DLCPro.scanContinuous")

        self._setBool("laser1:ctl:scan:continuous-mode", Mode, **kwargs)
    
    # Enables continuous scanning
    # UseQueue (bool): Whether to run the command through the queue or not
    def enableScanContinuous(self, **kwargs):
        self.scanContinuous(True, **kwargs)
    
    # Disables continuous scanning
    # UseQueue (bool): Whether to run the command through the queue or not
    def disableScanContinuous(self, **kwargs):
        self.scanContinuous(False, **kwargs)
    
    # Starts scanning
    # UseQueue (bool): Whether to run the command through the queue or not
    def startScan(self, **kwargs):
        if not self._allowFrequency:
            raise e.ImplementationError("DLCPro.startScan")

        self._execute("laser1:ctl:scan:start", **kwargs)
        
    # Stops scanning
    # UseQueue (bool): Whether to run the command through the queue or not
    def stopScan(self, **kwargs):
        if not self._allowFrequency:
            raise e.ImplementationError("DLCPro.stopScan")

        self._execute("laser1:ctl:scan:stop", **kwargs)
    
    # Pauses scanning
    # UseQueue (bool): Whether to run the command through the queue or not
    def pauseScan(self, **kwargs):
        if not self._allowFrequency:
            raise e.ImplementationError("DLCPro.pauseScan")

        self._execute("laser1:ctl:scan:pause", **kwargs)
    
    # Continues scanning from last pause
    # UseQueue (bool): Whether to run the command through the queue or not
    def continueScan(self, **kwargs):
        if not self._allowFrequency:
            raise e.ImplementationError("DLCPro.continueScan")

        self._execute("laser1:ctl:scan:continue", **kwargs)
    
    # Sets the piezo voltage of the laser
    # Value (float): The voltage to set
    # UseQueue (bool): Whether to run the command through the queue or not
    def setVoltage(self, Value, **kwargs):
        # Save it internally
        super().setVoltage(Value, **kwargs)
        
        # Set the voltage
        self._setValue("laser1:dl:pc:voltage", float(Value))
        