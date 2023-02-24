from .. import connections as c
from ..controllers import PID

# Used to control a power controller PID
class powerPID(PID, c.serial):
    # Port (str): The name of the COM port through which to access the serial connection
    # P (float): The P-factor to initialize
    # I (float): The I-factor to initialize
    # D (float): The D-factor to initialize
    # MaxOutput (float): The maximum possible output voltage
    # Timeout (float): The timeout time for the connection, must not be negative
    # ReconnectTries (int): How many times to attempt to reconnect if it disconnects, must not be smaller than 0
    # ReconnectDelay (float): The delay in seconds between each reconnect attempt, must not be negative
    # MaxAttempts (int): The maximum number attempts to send a command before giving up, must not be smaller than 1
    # AttemptDelay (float): The delay in seconds between each attempt to send a command, must not be negative
    # UseQueue (bool): If True then it will set up a queue which can be used in the sendCommand method, if False the UseQueue in sendCommand is ignored
    # Empty (bool): If True then it will not communicate with the device
    # DeviceName (str): The name of the device, only used for error messages
    # ID (str): The ID name for the device, only used for displaying infomation
    def __init__(self, *args, P = 15, I = 5, D = 0, MaxOutput = 4095, **kwargs):
        if not "DeviceName" in kwargs:
            kwargs["DeviceName"] = "Power PID"
            
        kwargs["OutputRange"] = (0, MaxOutput)
        
        if not "Baudrate" in kwargs:
            kwargs["Baudrate"] = 115200
        
        super().__init__(*args, **kwargs)
            
        # Set default values
        self.setP(P)
        self.setI(I)
        self.setD(D)
        
    # Send a command to the PID
    # Command (str): The command to send the device
    # UseQueue (bool): Whether to run the command through the queue or not
    # ResponseCheck (Func): A function to check if the response was correct, None if no check should be used, the function must have the arguments (Class, Command, ReturnString) and must return None on succes or a string on failure with the error message
    # WaitTime (float): The time in seconds to wait before reading
    def sendCommand(self, *args, **kwargs):
        # Set the number of return lines
        kwargs["ReturnLines"] = 2
        return super().sendCommand(*args, **kwargs)[1]
        
    # Set a parameter of the PID
    # Parameter (str): The name of the parameter to set
    # Value (): The value of the parameter
    # Type (type): The type to cast to
    # UseQueue (bool): Whether to run the command through the queue or not
    def _setParameter(self, Parameter, Value, Type, **kwargs):
        from .. import functions as f
        
        Parameter = str(Parameter)
        
        # Attempt to type cast
        CorrectValue = Type(Value)
            
        # Send the command
        kwargs["ResponseCheck"] = f.responseCheck.matchReturn("OK", Line = 1)
        return self.sendCommand(f"{Parameter}={CorrectValue}", **kwargs)

        
    # Get a parameter from the PID
    # Parameter (str): The name of the parameter to get
    # UseQueue (bool): Whether to run the command through the queue or not
    def _getParameter(self, Parameter, **kwargs):
        from .. import functions as f
        
        Parameter = str(Parameter)
        
        # Send command to get the value and read it
        kwargs["ResponseCheck"] = f.responseCheck.delimCount(2, Delimiter = ":", Line = 1)
        ReturnString = self.sendCommand(f"{Parameter}?", **kwargs)
        
        # Split the string
        return float(ReturnString.split(":")[1])
        
    # Set the SetPoint
    # Value (uint16): The new value of the SetPoint
    # UseQueue (bool): Whether to run the command through the queue or not
    def setSetPoint(self, Value, **kwargs):
        import numpy as np
        self._setParameter("S", Value, np.uint16, **kwargs)
        
    # Get the SetPoint
    # UseQueue (bool): Whether to run the command through the queue or not
    def getSetPoint(self, **kwargs):
        return self._getParameter("S", **kwargs)
        
    # Set the voltage out
    # Value (uint16): The new value of the VoltageOut
    # UseQueue (bool): Whether to run the command through the queue or not
    def setOutputSignal(self, Value, **kwargs):
        import numpy as np
        self._setParameter("O", Value, np.uint16, **kwargs)
        
    # Alias for setOutputSignal
    # UseQueue (bool): Whether to run the command through the queue or not
    def setVoltageOut(self, *args, **kwargs):
        return self.setOutputSignal(*args, **kwargs)
        
    # Get the voltage out
    # UseQueue (bool): Whether to run the command through the queue or not
    def getOutputSignal(self, **kwargs):
        return self._getParameter("O", **kwargs)
      
    # Alias for getOutputSignal
    # UseQueue (bool): Whether to run the command through the queue or not
    def getVoltageOut(self, *args, **kwargs):
        return self.getOutputSignal(*args, **kwargs)
    
    # Get the voltage in
    # UseQueue (bool): Whether to run the command through the queue or not
    def getInputSignal(self, **kwargs):
        return self._getParameter("V", **kwargs)

    # Alias for getInputSignal
    # UseQueue (bool): Whether to run the command through the queue or not
    def getVoltageIn(self, *args, **kwargs):
        return self.getInputSignal(*args, **kwargs)
        
    # Set the P factor
    # Value (uint16): The new value of the P factor
    # UseQueue (bool): Whether to run the command through the queue or not
    def setP(self, Value, **kwargs):
        import numpy as np
        self._setParameter("P", Value, np.uint16, **kwargs)

    # Get the P factor
    # UseQueue (bool): Whether to run the command through the queue or not
    def getP(self, **kwargs):
        return self._getParameter("P", **kwargs)

    # Set the I factor
    # Value (int16): The new value of the I factor
    # UseQueue (bool): Whether to run the command through the queue or not
    def setI(self, Value, **kwargs):
        import numpy as np
        self._setParameter("I", Value, np.uint16, **kwargs)

    # Get the I factor
    # UseQueue (bool): Whether to run the command through the queue or not
    def getI(self, **kwargs):
        return self._getParameter("I", **kwargs)
        
    # Set the D factor
    # Value (uint16): The new value of the D factor
    # UseQueue (bool): Whether to run the command through the queue or not
    def setD(self, Value, **kwargs):
        import numpy as np
        self._setParameter("D", Value, np.uint16, **kwargs)

    # Get the D factor
    # UseQueue (bool): Whether to run the command through the queue or not
    def getD(self, **kwargs):
        return self._getParameter("D", **kwargs)

    # Set the ADC offset
    # Value (uint16): The new value of the ADC offset
    # UseQueue (bool): Whether to run the command through the queue or not
    def setADCoffset(self, Value, **kwargs):
        import numpy as np
        self._setParameter("A", Value, np.uint16, **kwargs)

    # Get the ADC offset
    # UseQueue (bool): Whether to run the command through the queue or not
    def getADCoffset(self, **kwargs):
        return self._getParameter("A", **kwargs)

    # Set the sum error
    # Value (int32): The new value of the sum error
    # UseQueue (bool): Whether to run the command through the queue or not
    def setSumError(self, Value, **kwargs):
        import numpy as np
        self._setParameter("E", Value, np.int32, **kwargs)

    # Get the sum error
    # UseQueue (bool): Whether to run the command through the queue or not
    def getSumError(self, **kwargs):
        return self._getParameter("E", **kwargs)
                
    # Get the status
    # UseQueue (bool): Whether to run the command through the queue or not
    def status(self, **kwargs):     
        from .. import functions as f
        
        # Ask for status and get result
        kwargs["ResponseCheck"] = f.responseCheck.default(Line = 1)
        return self.sendCommand("R?", **kwargs).strip()
        
    # Start the PID
    # UseQueue (bool): Whether to run the command through the queue or not
    def start(self, **kwargs):
        from .. import functions as f
        
        # Send the command to run and get result
        kwargs["ResponseCheck"] = f.responseCheck.matchReturn("PID RUN", Line = 1)
        self.sendCommand("R+", **kwargs)
        
    # Stop the PID
    # UseQueue (bool): Whether to run the command through the queue or not
    def stop(self, **kwargs):
        from .. import functions as f
        
        # Send command and receive answer
        kwargs["ResponseCheck"] = f.responseCheck.matchReturn("PID STOP", Line = 1)
        self.sendCommand("R-", **kwargs)
      