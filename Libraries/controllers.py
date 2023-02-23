import connections as c
import functions as f
import exceptions as e

# Unless stated otherwise kwargs include:
# UseQueue (bool): True if it should use the queue of the device

# Used to control a PID
class PID(object):
    # OutputRange (2-tuple of floats): The minimum and maximum allowed output signals for the PID
    def __init__(self, *args, OutputRange = (0, 1), **kwargs):
        super().__init__(*args, **kwargs)
        
        # Set the minimum and maximum output
        self.minOutput = float(OutputRange[0])
        self.maxOutput = float(OutputRange[1])
    
    # Sets the set point of the PID
    # Value (float): The value to set
    def setSetPoint(self, Value):
        raise e.ImplementationError("PID.setSetPoint")
        
    # Gets the set point from the PID
    def getSetPoint(self):
        raise e.ImplementationError("PID.getSetPoint")
        
    # Gets the input signal from the PID
    def getInputSignal(self):
        raise e.ImplementationError("PID.getInputSignal")

    # Sets the output signal of the PID
    # Value (float): The value to set
    def setOutputSignal(self, Value):
        raise e.ImplementationError("PID.setOutputSignal")
        
    # Gets the output signal from the PID
    def getOutputSignal(self):
        raise e.ImplementationError("PID.getOutputSignal")

    # Sets the P factor of the PID
    # Value (float): The value to set
    def setP(self, Value):
        raise e.ImplementationError("PID.setP")
        
    # Gets the P factor from the PID
    def getP(self):
        raise e.ImplementationError("PID.getP")

    # Sets the I factor of the PID
    # Value (float): The value to set
    def setI(self, Value):
        raise e.ImplementationError("PID.setI")
        
    # Gets the I factor from the PID
    def getI(self):
        raise e.ImplementationError("PID.getI")

    # Sets the D factor of the PID
    # Value (float): The value to set
    def setD(self, Value):
        raise e.ImplementationError("PID.setD")
        
    # Gets the D factor from the PID
    def getD(self):
        raise e.ImplementationError("PID.getD")
        
    # Starts the PID
    def start(self):
        raise e.ImplementationError("PID.start")
        
    # Stops the PID
    def stop(self):
        raise e.ImplementationError("PID.stop")
        

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
        # Ask for status and get result
        kwargs["ResponseCheck"] = f.responseCheck.default(Line = 1)
        return self.sendCommand("R?", **kwargs).strip()
        
    # Start the PID
    # UseQueue (bool): Whether to run the command through the queue or not
    def start(self, **kwargs):
        # Send the command to run and get result
        kwargs["ResponseCheck"] = f.responseCheck.matchReturn("PID RUN", Line = 1)
        self.sendCommand("R+", **kwargs)
        
    # Stop the PID
    # UseQueue (bool): Whether to run the command through the queue or not
    def stop(self, **kwargs):
        # Send command and receive answer
        kwargs["ResponseCheck"] = f.responseCheck.matchReturn("PID STOP", Line = 1)
        self.sendCommand("R-", **kwargs)
                        

# A PTC10 controller class
class PTC10(PID, c.serial): # Look at page 94 in manual
    # Port (str): The name of the COM port through which to access the serial connection
    # Name (str): The name of the device to control, can be changed later with setName function
    # OutputRange (2-tuple of floats): The minimum and maximum allowed output signals for the PID
    # Timeout (float): The timeout time for the connection, must not be negative
    # ReconnectTries (int): How many times to attempt to reconnect if it disconnects, must not be smaller than 0
    # ReconnectDelay (float): The delay in seconds between each reconnect attempt, must not be negative
    # MaxAttempts (int): The maximum number attempts to send a command before giving up, must not be smaller than 1
    # AttemptDelay (float): The delay in seconds between each attempt to send a command, must not be negative
    # UseQueue (bool): If True then it will set up a queue which can be used in the sendCommand method, if False the UseQueue in sendCommand is ignored
    # Empty (bool): If True then it will not communicate with the device
    # DeviceName (str): The name of the device, only used for error messages
    # ID (str): The ID name for the device, only used for displaying infomation
    def __init__(self, *args, Name = "EOM", **kwargs):            
        if not "DeviceName" in kwargs:
            kwargs["DeviceName"] = "PTC10"
        
        super().__init__(*args, **kwargs)
            
        # Set default values
        self._name = str(Name)
    
    # Sets the name of the equipment to use
    # Name (str): The name of the equipment (EOM, ET1 or ET2 for ColdLab)
    def setName(self, Name):
        self._name = str(Name)
        
    # Gets the name of the equipment to use
    def getName(self):
        return self._name
        
    # Send a command with a given name ID
    # Command (str): The command that must be send
    # Name (str): The name of the system (EOM, ET1 or ET2 for ColdLab), if None then it uses the self.name
    # UseQueue (bool): True if it should use the command queue
    # ResponseCheck (func): The response check function
    def _sendNamedCommand(self, Command, Name = None, **kwargs):
        # Use default name
        if Name is None:
            Name = self._name

        return self.query(f"{Name}{Command}", **kwargs)
         
    # Set a paramter
    # Parameter (str): The parameter to set
    # Value (float): The value to set
    # GetFunction (func): The function to retrieve the same value from the PID
    # Name (str): The name of the system (EOM, ET1 or ET2 for ColdLab), if None then it uses the self.name
    # UseQueue (bool): True if it should use the command queue    
    def _setParameter(self, Parameter, Value, GetFunction, **kwargs):
        ResponseKwargs = kwargs.copy()
        ResponseKwargs["UseQueue"] = False
        kwargs["ResponseCheck"] = f.responseCheck.matchValue(float(Value), GetFunction, kwargs = ResponseKwargs)
        self._sendNamedCommand(f"{Parameter}={float(Value)}", **kwargs)
        
    # Get a paramter
    # Param (str): The parameter to get
    # Name (str): The name of the system (EOM, ET1 or ET2 for ColdLab), if None then it uses the self.name
    # UseQueue (bool): True if it should use the command queue    
    def _getParameter(self, Param, **kwargs):
        kwargs["ResponseCheck"] = f.responseCheck.getValue()
        return float(self._sendNamedCommand(f"{Param}?", **kwargs))
    
    # Set the SetPoint
    # Value (float): The value to set
    # Name (str): The name of the system (EOM, ET1 or ET2 for ColdLab), if None then it uses the self.name
    # UseQueue (bool): True if it should use the command queue    
    def setSetPoint(self, Value, **kwargs):
        self._setParameter("A.PID.setpoint", Value, self.getSetPoint, **kwargs)

    # Get the SetPoint
    # Name (str): The name of the system (EOM, ET1 or ET2 for ColdLab), if None then it uses the self.name
    # UseQueue (bool): True if it should use the command queue    
    def getSetPoint(self, **kwargs):
        return self._getParameter("A.PID.setpoint", **kwargs)

    # Set the current
    # Value (float): The value to set
    # Name (str): The name of the system (EOM, ET1 or ET2 for ColdLab), if None then it uses the self.name
    # UseQueue (bool): True if it should use the command queue    
    def setOutputSignal(self, Value, **kwargs):
        self._setParameter("A.value", Value, self.getCurrent, **kwargs)

    # Alias for setOutputSignal
    # Name (str): The name of the system (EOM, ET1 or ET2 for ColdLab), if None then it uses the self.name
    # UseQueue (bool): True if it should use the command queue    
    def setCurrent(self, *args, **kwargs):
        return self.setOutputSignal(*args, **kwargs)

    # Get the current
    # Name (str): The name of the system (EOM, ET1 or ET2 for ColdLab), if None then it uses the self.name
    # UseQueue (bool): True if it should use the command queue    
    def getOutputSignal(self, **kwargs):
        return self._getParameter("A.value", **kwargs)
    
    # Alias for getOutputSignal
    # Name (str): The name of the system (EOM, ET1 or ET2 for ColdLab), if None then it uses the self.name
    # UseQueue (bool): True if it should use the command queue    
    def getCurrent(self, *args, **kwargs):
        return self.getOutputSignal(*args, **kwargs)

    # Get the temperature
    # Name (str): The name of the system (EOM, ET1 or ET2 for ColdLab), if None then it uses the self.name
    # UseQueue (bool): True if it should use the command queue    
    def getInputSignal(self, **kwargs):
        return self._getParameter("B.value", **kwargs)
    
    # Alias for getInputSignal
    # Name (str): The name of the system (EOM, ET1 or ET2 for ColdLab), if None then it uses the self.name
    # UseQueue (bool): True if it should use the command queue    
    def getTemp(self, *args, **kwargs):
        return self.getInputSignal(*args, **kwargs)

    # Set the P value
    # Value (float): The value to set
    # Name (str): The name of the system (EOM, ET1 or ET2 for ColdLab), if None then it uses the self.name
    # UseQueue (bool): True if it should use the command queue    
    def setP(self, Value, **kwargs):
        self._setParameter("A.PID.P", Value, self.getP, **kwargs)

    # Get the P value
    # Name (str): The name of the system (EOM, ET1 or ET2 for ColdLab), if None then it uses the self.name
    # UseQueue (bool): True if it should use the command queue    
    def getP(self, **kwargs):
        return self._getParameter("A.PID.P", **kwargs)

    # Set the I value
    # Value (float): The value to set
    # Name (str): The name of the system (EOM, ET1 or ET2 for ColdLab), if None then it uses the self.name
    # UseQueue (bool): True if it should use the command queue    
    def setI(self, Value, **kwargs):
        self._setParameter("A.PID.I", Value, self.getI, **kwargs)

    # Get the I value
    # Name (str): The name of the system (EOM, ET1 or ET2 for ColdLab), if None then it uses the self.name
    # UseQueue (bool): True if it should use the command queue    
    def getI(self, **kwargs):
        return self._getParameter("A.PID.I", **kwargs)

    # Set the D value
    # Value (float): The value to set
    # Name (str): The name of the system (EOM, ET1 or ET2 for ColdLab), if None then it uses the self.name
    # UseQueue (bool): True if it should use the command queue    
    def setD(self, Value, **kwargs):
        self._setParameter("A.PID.D", Value, self.getD, **kwargs)

    # Get the D value
    # Name (str): The name of the system (EOM, ET1 or ET2 for ColdLab), if None then it uses the self.name
    # UseQueue (bool): True if it should use the command queue    
    def getD(self, **kwargs):
        return self._getParameter("A.PID.D", **kwargs)
    
    # Starts the PID
    # Name (str): The name of the system (EOM, ET1 or ET2 for ColdLab), if None then it uses the self.name
    # UseQueue (bool): True if it should use the command queue    
    def start(self, **kwargs):
        ResponseKwargs = kwargs.copy()
        ResponseKwargs["UseQueue"] = False
        kwargs["ResponseCheck"] = f.responseCheck.matchVar(True, self.status, kwargs = ResponseKwargs)
        self._sendNamedCommand("A.PID.mode=On", **kwargs)
        
    # Stop the PID
    # Name (str): The name of the system (EOM, ET1 or ET2 for ColdLab), if None then it uses the self.name
    # UseQueue (bool): True if it should use the command queue    
    def stop(self, **kwargs):
        ResponseKwargs = kwargs.copy()
        ResponseKwargs["UseQueue"] = False
        kwargs["ResponseCheck"] = f.responseCheck.matchVar(False, self.status, kwargs = ResponseKwargs)
        self._sendNamedCommand("A.off", **kwargs)
        
    # Get the status of the PID, True if it is on, False if it is off, None if it is on Follow
    # Name (str): The name of the system (EOM, ET1 or ET2 for ColdLab), if None then it uses the self.name
    # UseQueue (bool): True if it should use the command queue    
    def status(self, **kwargs):
        kwargs["ResponseCheck"] = f.responseCheck.inList(["Off", "On", "Follow"])
        ReturnString = self._sendNamedCommand("A.PID.mode?", **kwargs)
        
        if ReturnString == "On":
            return True
        
        elif ReturnString == "Off":
            return False
        
        else:
            return None
          
    
# Controls the temperature arduino
class tempArduino(PID, c.serial):
    # Port (str): The name of the COM port through which to access the serial connection
    # Name (str): The name of the device to control, can be changed later with setName function
    # OutputRange (2-tuple of floats): The minimum and maximum allowed output signals for the PID
    # Timeout (float): The timeout time for the connection, must not be negative
    # ReconnectTries (int): How many times to attempt to reconnect if it disconnects, must not be smaller than 0
    # ReconnectDelay (float): The delay in seconds between each reconnect attempt, must not be negative
    # MaxAttempts (int): The maximum number attempts to send a command before giving up, must not be smaller than 1
    # AttemptDelay (float): The delay in seconds between each attempt to send a command, must not be negative
    # UseQueue (bool): If True then it will set up a queue which can be used in the sendCommand method, if False the UseQueue in sendCommand is ignored
    # Empty (bool): If True then it will not communicate with the device
    # DeviceName (str): The name of the device, only used for error messages
    # ID (str): The ID name for the device, only used for displaying infomation
    def __init__(self, *args, **kwargs):
        if not "DeviceName" in kwargs:
            kwargs["DeviceName"] = "Temperature Arduino"
        
        kwargs["Baudrate"] = 115200
        
        super().__init__(*args, **kwargs)

    # Sets the value of a parameter
    # Parameter (str): The parameter to set
    # Value (float): The value of the parameter
    # UseQueue (bool): True if it should use the command queue    
    def _setParameter(self, Parameter, Value, **kwargs):
        kwargs["ResponseCheck"] = f.responseCheck.default()
        return self.query(f"{Parameter}{float(Value)}", **kwargs)

    # Gets the signal in
    # UseQueue (bool): True if it should use the command queue    
    def getInputSignal(self, **kwargs):
        return self.getStatus(**kwargs)["V_in"]
    
    # Gets the signal out
    # UseQueue (bool): True if it should use the command queue    
    def getOutputSignal(self, **kwargs):
        return self.getStatus(**kwargs)["V_out"]

    # Sets the SetPoint
    # Value (float): The value to set
    # UseQueue (bool): True if it should use the command queue    
    def setSetPoint(self, Value, **kwargs):
        return self._setParameter("S", Value, **kwargs)
    
    # Gets the set point
    # UseQueue (bool): True if it should use the command queue    
    def getSetPoint(self, **kwargs):
        return self.getStatus(**kwargs)["S"]
    
    # Sets the P factor
    # Value (float): The value to set
    # UseQueue (bool): True if it should use the command queue    
    def setP(self, Value, **kwargs):
        return self._setParameter("P", Value, **kwargs)
    
    # Gets the P factor
    # UseQueue (bool): True if it should use the command queue    
    def getP(self, **kwargs):
        return self.getStatus(**kwargs)["P"]

    # Sets the I factor
    # Value (float): The value to set
    # UseQueue (bool): True if it should use the command queue    
    def setI(self, Value, **kwargs):
        return self._setParameter("I", Value, **kwargs)

    # Gets the I factor
    # UseQueue (bool): True if it should use the command queue    
    def getI(self, **kwargs):
        return self.getStatus(**kwargs)["I"]

    # Sets the D factor
    # Value (float): The value to set
    # UseQueue (bool): True if it should use the command queue    
    def setD(self, Value, **kwargs):
        return self._setParameter("D", Value, **kwargs)

    # Gets the D factor
    # UseQueue (bool): True if it should use the command queue    
    def getD(self, **kwargs):
        return self.getStatus(**kwargs)["D"]

    # Sets the integrand
    # Value (float): The value to set
    # UseQueue (bool): True if it should use the command queue    
    def setIntegrand(self, Value, **kwargs):
        return self._setParameter("C", Value, **kwargs)

    # Sets the force dac
    # Value (float): The value to set
    # UseQueue (bool): True if it should use the command queue    
    def setForceDac(self, Value, **kwargs):
        return self._setParameter("A", Value, **kwargs)

    # Get all infomation about the arduino
    # Returns a dictionary with all of the values
    # UseQueue (bool): True if it should use the command queue    
    def getStatus(self, **kwargs):
        kwargs["ReturnLines"] = 9
        kwargs["ResponseCheck"] = f.responseCheck.default()
        Status = self.sendCommand("H0", **kwargs)
        
        # Get values
        Dict = {}
        
        Dict["V_in"] = float(Status[0].split(":")[1])
        Dict["dVdT"] = float(Status[1].split(":")[1])
        Dict["S"] = float(Status[2].split(":")[1])
        Dict["Lock"] = float(Status[3].split(":")[1].replace(" ", ""))
        Dict["V_out"] = float(Status[7].split(":")[1])
        
        P = Status[4].split(":")[1].replace(" ", "").split("(")
        I = Status[5].split(":")[1].replace(" ", "").split("(")
        D = Status[6].split(":")[1].replace(" ", "").split("(")

        Dict["P_out"] = float(P[0])
        Dict["P"] = float(P[1][:-1])
        Dict["I_out"] = float(I[0])
        Dict["I"] = float(I[1][:-1])
        Dict["D_out"] = float(D[0])
        Dict["D"] = float(D[1][:-1])
        
        return Dict


# Controls the keithly
class keithly(c.visa):
    # SerialNumber (str): The serial number of the device
    # CurrentLimit (float): The maximum allowed current
    # VoltageLimit (float): The maximum allowed voltage
    # StableTries (int): The maximum number of attempts to stabilize voltage
    # StableDelay (float): The delay in seconds between each stabilization attempt
    # Timeout (float): The timeout time for the connection, must not be negative
    # ReconnectTries (int): How many times to attempt to reconnect if it disconnects, must not be smaller than 0
    # ReconnectDelay (float): The delay in seconds between each reconnect attempt, must not be negative
    # MaxAttempts (int): The maximum number attempts to send a command before giving up, must not be smaller than 1
    # AttemptDelay (float): The delay in seconds between each attempt to send a command, must not be negative
    # UseQueue (bool): If True then it will set up a queue which can be used in the sendCommand method, if False the UseQueue in sendCommand is ignored
    # Empty (bool): If True then it will not communicate with the device
    # DeviceName (str): The name of the device, only used for error messages
    # ID (str): The ID name for the device, only used for displaying infomation
    def __init__(self, SerialNumber, *args, CurrentLimit = 0.001, VoltageLimit = 1.5, StableTries = 50, StableDelay = 0.05, **kwargs):
        if not "DeviceName" in kwargs:
            kwargs["DeviceName"] = "Keithly"
        
        super().__init__(f"USB0::0x05E6::0x2450::{SerialNumber}::INSTR", *args, **kwargs)
        
        self._voltageLim = 0
        
        # Initialize
        self.reset()
        self.setCurrentLim(float(CurrentLimit), UseQueue = True)
        self.setVoltageLim(float(VoltageLimit))
        self.setCurrentRange(1e-5)
        
        self._stableTries = int(StableTries)
        self._stableDelay = float(StableDelay)
        
    # Retrieves a parameter
    # Parameter (str): The parameter to retrieve
    # UseQueue (bool): True if it should use the command queue    
    def _getParameter(self, Parameter, **kwargs):
        kwargs["ResponseCheck"] = f.responseCheck.default()
        return self.query(f"print({Parameter})", **kwargs)
    
    # Retrieves a float
    # Parameter (str): The parameter to retrieve
    # UseQueue (bool): True if it should use the command queue    
    def _getValue(self, Parameter, **kwargs):
        kwargs["ResponseCheck"] = f.responseCheck.getValue()
        return float(self.query(f"print({Parameter})", **kwargs))
    
    # Sets a parameter
    # Parameter (str): The parameter to set
    # Value (str): The value to set the parameter to
    # UseQueue (bool): True if it should use the command queue    
    def _setParameter(self, Parameter, Value, **kwargs):
        self.sendWithoutResponse(f"{Parameter}={Value}", **kwargs)
        
    # Sets a float
    # Parameter (str): The parameter to set
    # Value (float): The value to set the parameter to
    # UseQueue (bool): True if it should use the command queue    
    def _setValue(self, Parameter, Value, **kwargs):
        self.sendWithoutResponse(f"{Parameter}={float(Value):1.6g}", **kwargs)

    # Sets the voltage and waits until it is locked
    # Value (float): The value of the voltage
    # UseQueue (bool): True if it should use the command queue    
    def setVoltage(self, Value, **kwargs):
        self.setVoltageFast(Value, **kwargs)
        
        # Make sure it was set
        self._setParameter("smu.measure.func", "smu.FUNC_DC_VOLTAGE", **kwargs)
        
        Success = False
        for i in range(self._stableTries):
            if abs(self._getValue("smu.measure.read()", **kwargs) - float(Value)) < 1e-4:
                Success = True
                break
        
        if not Success:
            raise e.StabilizeError(self.deviceName, self, "voltage")
    
    # Sets the voltage without waiting for lock
    # Value (float): The value of the voltage
    # UseQueue (bool): True if it should use the command queue    
    def setVoltageFast(self, Value, **kwargs):
        # Check that it is within the limits
        if abs(float(Value)) > self.getVoltageLim():
            raise e.RangeError("Voltage", float(Value), -self.getVoltageLim(), self.getVoltageLim())
            
        # Set the level
        self._setValue("smu.source.level", Value, **kwargs)
    
    # Gets the voltage
    # UseQueue (bool): True if it should use the command queue    
    def getVoltage(self, **kwargs):
        self._setParameter("smu.measure.func", "smu.FUNC_DC_VOLTAGE", **kwargs)
        return self._getValue("smu.measure.read()", **kwargs)
    
    # Gets the current
    # UseQueue (bool): True if it should use the command queue    
    def getCurrent(self, **kwargs):
        self._setParameter("smu.measure.func", "smu.FUNC_DC_CURRENT", **kwargs)
        return self._getValue("smu.measure.read()", **kwargs)
    
    # Sets the current limit
    # Value (float): The value for the current limit
    # UseQueue (bool): True if it should use the command queue    
    def setCurrentLim(self, Value, **kwargs):
        self._setValue("smu.source.ilimit.level", Value, **kwargs)
    
    # Gets the current limit
    # UseQueue (bool): True if it should use the command queue    
    def getCurrentLim(self, **kwargs):
        return self._getValue("smu.source.ilimit.level", **kwargs)
    
    # Sets the current range
    # Value (float): The maximum current allowed
    # UseQueue (bool): True if it should use the command queue    
    def setCurrentRange(self, Value, **kwargs):
        self._setParameter("smu.measure.func", "smu.FUNC_DC_CURRENT", **kwargs)
        self._setValue("smu.measure.range", Value, **kwargs)
    
    # Sets the voltage limit
    # Value (float): The value of the maximum voltage
    # UseQueue (bool): True if it should use the command queue    
    def setVoltageLim(self, Value, **kwargs):
        self._voltageLim = float(Value)
        
    # Gets the voltage limit
    # UseQueue (bool): True if it should use the command queue    
    def getVoltageLim(self, **kwargs):
        return float(self._voltageLim)
    
    # Sets the measure delay
    # Value (float): The value of the measure delay
    # UseQueue (bool): True if it should use the command queue    
    def setMeasureDelay(self, Value, **kwargs):
        self._setValue("smu.source.delay", Value, **kwargs)
    
    # Gets the measure delay
    # UseQueue (bool): True if it should use the command queue    
    def getMeasureDelay(self, **kwargs):
        return self._getValue("smu.source.delay", **kwargs)
    
    # Gets the wire sense mode
    # UseQueue (bool): True if it should use the command queue    
    def getWireSense(self, **kwargs):
        return self._getParameter("smu.measure.sense")
    
    # Sets the wire sense mode to 2wire
    # UseQueue (bool): True if it should use the command queue    
    def use2WireSense(self, **kwargs):
        self._setParameter("smu.measure.sense", "smu.SENSE_2WIRE", **kwargs)
    
    # Turns on the voltage source
    # UseQueue (bool): True if it should use the command queue    
    def start(self, **kwargs):
        self._setParameter("smu.source.output", "smu.ON", **kwargs)
    
    # Turns off the voltage source
    # UseQueue (bool): True if it should use the command queue    
    def stop(self, **kwargs):
        self._setParameter("smu.source.output", "smu.OFF", **kwargs)

    # Returns the activation status of the device
    # UseQueue (bool): True if it should use the command queue    
    def status(self, **kwargs):
        return self._getParameter("smu.source.output", **kwargs)
    
    # Sets the front terminal and turns voltage source on
    # UseQueue (bool): True if it should use the command queue    
    def front(self, **kwargs):
        self._setParameter("smu.measure.terminals", "smu.TERMINALS_FRONT", **kwargs)    
        self.start(**kwargs)
    
    # Sets rear terminal and turns voltage source on
    # UseQueue (bool): True if it should use the command queue    
    def rear(self, **kwargs):
        self._setParameter("smu.measure.terminals", "smu.TERMINALS_REAR", **kwargs)    
        self.start(**kwargs)
        
    # Get which terminal is showing
    # UseQueue (bool): True if it should use the command queue    
    def getTerminal(self, **kwargs):
        return self._getParameter("smu.measure.terminals", **kwargs)
    
    # Enables auto delay
    # UseQueue (bool): True if it should use the command queue    
    def enableAutoDelay(self, **kwargs):
        self._setParameter("smu.source.autodelay", "smu.ON", **kwargs)
    
    # Disables auto delay
    # UseQueue (bool): True if it should use the command queue    
    def disableAutoDelay(self, **kwargs):
        self._setParameter("smu.source.autodelay", "smu.OFF", **kwargs)
    
    # Gets the auto delay status
    # UseQueue (bool): True if it should use the command queue    
    def getAutoDelay(self, **kwargs):
        return self._getParameter("smu.source.autodelay", **kwargs)
    
    # shuts down the voltage source
    # UseQueue (bool): True if it should use the command queue    
    def exit(self, **kwargs):
        self.sendWithoutResponse("exit()", **kwargs)
    
    # Resets the source to a known position
    # UseQueue (bool): True if it should use the command queue    
    def reset(self, **kwargs):
        self.sendWithoutResponse("smu.reset()", **kwargs)
        
        self._setParameter("smu.source.func", "smu.FUNC_DC_VOLTAGE", **kwargs)
        self._setParameter("smu.source.protect.level", "smu.PROTECT_5V", **kwargs)
        self._setParameter("smu.source.offmode", "smu.OFFMODE_ZERO", **kwargs)
        self._setParameter("smu.source.readback", "smu.ON", **kwargs)
        self._setParameter("smu.source.autorange", "smu.ON", **kwargs)
        self._setParameter("smu.source.level", "0", **kwargs)
        self._setParameter("smu.source.output", "smu.OFF", **kwargs)
        self._setParameter("smu.source.autodelay", "smu.ON", **kwargs)


# A generic powermeter class
class powermeter(object):
    # Sets the power auto range
    # Value (bool): True if auto range should be enabled
    def setPowerAutoRange(self, Value, **kwargs):
        raise e.ImplementationError("PM.setPowerAutoRange")

    # Enables power auto range
    def enablePowerAutoRange(self, **kwargs):
        self.setPowerAutoRange(True, **kwargs)
    
    # Disables power auto range
    def disablePowerAutoRange(self, **kwargs):
        self.setPowerAutoRange(False, **kwargs)
    
    # Gets the status of the power auto range
    def getPowerAutoRange(self):
        raise e.ImplementationError("PM.getPowerAutoRange")
    
    # Sets the max power
    # Value (float): The value of the max power
    def setPowerRange(self, Value):
        raise e.ImplementationError("PM.setPowerRange")
    
    # Gets the max power setting
    def getPowerRange(self):
        raise e.ImplementationError("PM.getPowerRange")
    
    # Sets the max frequency
    # Value (float): The value of the max frequency
    def setFrequencyRange(self, Value):
        raise e.ImplementationError("PM.setFrequencyRange")
    
    # Gets the max frequency setting
    def getFrequencyRange(self):
        raise e.ImplementationError("PM.getFrequencyRange")
    
    # Gets a power measurement
    def getPower(self):
        raise e.ImplementationError("PM.getPower")
        
    # Gets several power measurements
    # Count (int): The number of measurements to get
    # SleepTime (float): The time to sleep between each point
    def getPowerMulti(self, Count, SleepTime = 0, **kwargs):
        import numpy as np
        
        Count = int(Count)
        SleepTime = float(SleepTime)
        
        # Setup data
        Data = np.empty(Count, dtype = float)
        
        # Loop
        for i in range(Count - 1):
            Data[i] = self.getPower(**kwargs)
            
            # Wait
            f.time.sleep(SleepTime)
                
        Data[-1] = self.getPower(**kwargs)
        
        return Data


# Controls the powermeter
class PM100D(powermeter, c.visa):
    # SerialNumber (str): The serial number of the device
    # Timeout (float): The timeout time for the connection, must not be negative
    # ReconnectTries (int): How many times to attempt to reconnect if it disconnects, must not be smaller than 0
    # ReconnectDelay (float): The delay in seconds between each reconnect attempt, must not be negative
    # MaxAttempts (int): The maximum number attempts to send a command before giving up, must not be smaller than 1
    # AttemptDelay (float): The delay in seconds between each attempt to send a command, must not be negative
    # UseQueue (bool): If True then it will set up a queue which can be used in the sendCommand method, if False the UseQueue in sendCommand is ignored
    # Empty (bool): If True then it will not communicate with the device
    # DeviceName (str): The name of the device, only used for error messages
    # ID (str): The ID name for the device, only used for displaying infomation
    def __init__(self, SerialNumber, *args, **kwargs):
        if not "DeviceName" in kwargs:
            kwargs["DeviceName"] = "PM100D"
        
        super().__init__(f"USB0::0x1313::0x8078::{SerialNumber}::INSTR", *args, **kwargs)

    # Sets a bool value
    # Parameter (str): The parameter to set
    # Value (bool): The value to set
    # UseQueue (bool): True if it should use the command queue    
    def _setBool(self, Parameter, Value, **kwargs):
        self.sendWithoutResponse(f"{Parameter} {int(bool(Value))}", **kwargs)
        
    # Sets a float value
    # Parameter (str): The parameter to set
    # Value (bool): The value to set
    # UseQueue (bool): True if it should use the command queue    
    def _setFloat(self, Parameter, Value, **kwargs):
        self.sendWithoutResponse(f"{Parameter} {Value:g}", **kwargs)
        
    # Gets a bool value
    # Parameter (str): The parameter to get
    # UseQueue (bool): True if it should use the command queue    
    def _getBool(self, Parameter, **kwargs):
        kwargs["ResponseCheck"] = f.responseCheck.getBool()
        return bool(self.query(f"{Parameter}?", **kwargs))
    
    # Gets a float value
    # Parameter (str): The parameter to get
    # UseQueue (bool): True if it should use the command queue    
    def _getFloat(self, Parameter, **kwargs):
        kwargs["ResponseCheck"] = f.responseCheck.getNumber()
        return float(self.query(f"{Parameter}?", **kwargs))

    # Sets the power auto range
    # Value (bool): True if auto range should be enabled
    # UseQueue (bool): True if it should use the command queue    
    def setPowerAutoRange(self, Value, **kwargs):
        self._setBool("power:range:auto", Value, **kwargs)
    
    # Gets the status of the power auto range
    # UseQueue (bool): True if it should use the command queue    
    def getPowerAutoRange(self, **kwargs):
        return self._getBool("power:range:auto", **kwargs)
    
    # Sets the max power
    # Value (float): The value of the max power
    # UseQueue (bool): True if it should use the command queue    
    def setPowerRange(self, Value, **kwargs):
        self._setFloat("power:range", Value, **kwargs)
    
    # Gets the max power setting
    # UseQueue (bool): True if it should use the command queue    
    def getPowerRange(self, **kwargs):
        return self._getFloat("power:range", **kwargs)
    
    # Sets the max frequency
    # Value (float): The value of the max frequency
    # UseQueue (bool): True if it should use the command queue    
    def setFrequencyRange(self, Value, **kwargs):
        self._setFloat("frequency:range", Value, **kwargs)
    
    # Gets the max frequency setting
    # UseQueue (bool): True if it should use the command queue    
    def getFrequencyRange(self, Value, **kwargs):
        return self._getFloat("frequency:range", **kwargs)
    
    # Gets a power measurement
    # UseQueue (bool): True if it should use the command queue    
    def getPower(self, **kwargs):
        return self._getFloat("measure:power", **kwargs)

# Controller for a wavemeter
# kwargs of methods in this class may include:
class WM(c.dll):
    # DLLPath (str): The path to the dll to load
    # Channel (int): The default channel to use, can be set with the setChannel method
    # UseQueue (bool): If True then it will set up a queue which can be used in the sendCommand method, if False the UseQueue in sendCommand is ignored
    # Empty (bool): If True then it will not communicate with the device
    # DeviceName (str): The name of the device, only used for error messages
    # ID (str): The ID name for the device, only used for displaying infomation
    def __init__(self, *args, Channel = 1, **kwargs):
        import ctypes as c
        
        # Get the name
        if not "DeviceName" in kwargs:
            kwargs["DeviceName"] = "Wavelength Meter"
            
        # Initialize
        super().__init__(*args, **kwargs)
        
        # Set the channel
        self.setChannel(Channel)
        
        # Add header for used functions
        self.setupFunction("SetActiveChannel", c.c_long, [c.c_long, c.c_long, c.c_long, c.c_long])
        self.setupFunction("GetWavelengthNum", c.c_double, [c.c_long, c.c_double])
        self.setupFunction("GetFrequencyNum", c.c_double, [c.c_long, c.c_double])
        self.setupFunction("SetExposureNum", c.c_long, [c.c_long, c.c_long, c.c_long])

    # Runs a channel dependent function
    # Name (str): The name of the function
    # Args (set): The arguments to pass the function
    # UseQueue (bool): True if it should use the command queue
    # Channel (int): The channel to access, if None then it will use the default
    def _runChannelFunction(self, Name, Args = set(), Channel = None, **kwargs):
        if Channel is None:
            Channel = self._channel

        Args = (Channel,) + tuple(Args)
        
        self.runFunction("SetActiveChannel", Args = (1, 1, Channel, 0), **kwargs)
        return self.runFunction(Name, Args = Args, **kwargs)

    # Gets the wavelength from the device
    # UseQueue (bool): True if it should use the command queue
    # Channel (int): The channel to access, if None then it will use the default
    def getWavelength(self, **kwargs):
        return self._runChannelFunction("GetWavelengthNum", Args = (0,), **kwargs)
    
    # Gets the frequency from the device
    # UseQueue (bool): True if it should use the command queue
    # Channel (int): The channel to access, if None then it will use the default
    def getFrequency(self, **kwargs):
        return self._runChannelFunction("GetFrequencyNum", Args = (0,), **kwargs)
    
    # Sets the exposure time
    # Value (int): The value to set the exposure to
    # Index (int): The index of the exposure (0 or 1)
    # UseQueue (bool): True if it should use the command queue
    # Channel (int): The channel to access, if None then it will use the default
    def setExposure(self, Value, Index, **kwargs):
        self._runChannelFunction("SetExposureNum", Args = (Index, Value), **kwargs)
    
    # Resets the exposure time
    # UseQueue (bool): True if it should use the command queue
    # Channel (int): The channel to access, if None then it will use the default
    def resetExposure(self, **kwargs):
        self.setExposure(1, 1, **kwargs)
        self.setExposure(0, 2, **kwargs)
    
    # Sets the default channel to use
    # Channel (int): The channel to use
    def setChannel(self, Channel):
        self._channel = int(Channel)


# Controls a DAC
class DAC(c.external):
    # Name (str): The name of the device to connect to
    # InputChannels (list of int): A list of all the input channels to use, may be empty
    # OutputChannels (list of int): A list of all the output channels to use, may be empty, must have the same length as VoltageLimits
    # VoltageLimits (list of float): A list of all the voltage limits of the output channels
    # Timeout (float): The timeout in seconds
    # UseQueue (bool): If True then it will set up a queue which can be used in the sendCommand method, if False the UseQueue in sendCommand is ignored
    # Empty (bool): If True then it will not communicate with the device
    # DeviceName (str): The name of the device, only used for error messages
    # ID (str): The ID name for the device, only used for displaying infomation    
    def __init__(self, Name, *args, InputChannels = [], OutputChannels = [], VoltageLimits = [], Timeout = 1, **kwargs):        
        if not "DeviceName" in kwargs:
            kwargs["DeviceName"] = "DAC"

        # Save the name
        self._name = str(Name)
        
        # Save the timeout
        self._timeout = float(Timeout)

        kwargs["OpenKwargs"] = {"InputChannels": InputChannels, "OutputChannels": OutputChannels, "VoltageLimits": VoltageLimits}
            
        super().__init__(self, *args, **kwargs)
                            
    def open(self, InputChannels = [], OutputChannels = [], VoltageLimits = []):
        # Save the channel lists
        self._inputChannels = []
        self._outputChannels = []
        self._voltageLimits = []
        
        # Open the channels
        for Channel in InputChannels:
            self._addInputChannel(Channel)
            
        for Channel, VoltageLimit in zip(OutputChannels, VoltageLimits):
            self._addOutputChannel(Channel, VoltageLimit = VoltageLimit)

        
    # Adds an output channel
    # Channel (int): The ID of the channel to access
    # ColtageLimit (float): The maximum voltage allowed on the channel
    def _addOutputChannel(self, Channel, VoltageLimit = 0):
        import nidaqmx as daq
        
        # Make sure Channel is correct
        Channel = int(Channel)
        
        if Channel < 0:
            raise e.MinValueError("Channel", Channel, 0)
            
        # Make sure the channel is not in the list
        if len(self._outputChannels) > Channel and self._outputChannels[Channel] is not None:
            raise e.ExistError(f"Channel {Channel}", self.deviceName, self)
           
        # Get the name
        Name = f"{self._name}/ao{Channel}"
           
        # Create the channel
        Device = daq.Task()
        Device.ao_channels.add_ao_voltage_chan(Name)
        
        # Add to the list
        if len(self._outputChannels) <= Channel:
            self._outputChannels += [None] * (Channel + 1 - len(self._outputChannels))
        
        self._outputChannels[Channel] = Device
        
        if len(self._voltageLimits) <= Channel:
            self._voltageLimits += [0.] * (Channel + 1 - len(self._voltageLimits))
        
        self._voltageLimits[Channel] = float(VoltageLimit)
        
    # Adds an input channel
    # Channel (int): The ID of the channel to access
    def _addInputChannel(self, Channel):
        import nidaqmx as daq
        
        # Make sure Channel is correct            
        Channel = int(Channel)
        
        if Channel < 0:
            raise e.MinValueError("Channel", Channel, 0)
            
        # Make sure the channel is not in the list
        if len(self._inputChannels) > Channel and self._inputChannels[Channel] is not None:
            raise e.ExistError(f"Channel {Channel}", self.deviceName, self)
           
        # Get the name
        Name = f"{self._name}/ai{Channel}"
           
        # Create the channel
        Device = daq.Task()
        Device.ai_channels.add_ai_voltage_chan(Name)
        
        # Add to the list
        if len(self._inputChannels) <= Channel:
            self._inputChannels += [None] * (Channel + 1 - len(self._inputChannels))
        
        self._inputChannels[Channel] = Device
    
    # Set the voltage of an output channel
    # Value (float): The voltage to set
    # Channel (int): The ID of the channel to access    
    def _setVoltage(self, Value, Channel):
        # Make sure the channel is correct
        Channel = int(Channel)
        
        if Channel < 0:
            raise e.MinValueError("Channel", Channel, 0)
            
        # Make sure the channel is open
        if len(self._outputChannels) <= Channel or self._outputChannels[Channel] is None:
            raise e.ExistError(f"Channel {Channel}", self.deviceName, self)

        # Make sure the value is within the limits
        if abs(float(Value)) > self._voltageLimits[Channel]:
            raise e.RangeError("Voltage", float(Value), -self._voltageLimits[Channel], self._voltageLimits[Channel])
            
        self._outputChannels[Channel].write(float(Value), timeout = self._timeout)
        
    # Read the voltage from an input channel
    # Channel (int): The ID of the channel to access    
    def _getVoltage(self, Channel):
        # Make sure the channel is correct
        Channel = int(Channel)
        
        if Channel < 0:
            raise e.MinValueError("Channel", Channel, 0)
            
        # Make sure the channel is open
        if len(self._inputChannels) <= Channel or self._inputChannels[Channel] is None:
            raise e.ExistError(f"Channel {Channel}", self.deviceName, self)
            
        return float(self._inputChannels[Channel].read(timeout = self._timeout))
            
    # Set the voltage of an output channel
    # Value (float): The voltage to set
    # Channel (int): The ID of the channel to access    
    # UseQueue (bool): Whether to run the command through the queue or not
    def setVoltage(self, Value, Channel, **kwargs):
        self.runFunction("_setVoltage", Args = (Value, Channel), **kwargs)
    
    # Read the voltage from an input channel
    # Channel (int): The ID of the channel to access    
    # UseQueue (bool): Whether to run the command through the queue or not
    def getVoltage(self, Channel, **kwargs):
        return self.runFunction("_getVoltage", Args = (Channel,), **kwargs)
    
    # Close the device
    def _close(self):
        # Close input channels
        for Channel in self._inputChannels:
            if Channel is not None:
                Channel.close()
                
        # Close output channels
        for Channel in self._outputChannels:
            if Channel is not None:
                Channel.close()
                
        # Reset
        self._inputChannel = []
        self._outputChannel = []
        self._voltageLimits = []
        
        super()._close()

# A generic class to control lasers, cannot be used on its own
class laser(object):
    # VoltageRange (2-tuple of float): Them minimum and maximum voltage allowed
    # FrequencyRange (2-tuple of float): The minimum and maximum frequencies allowed, if None then they are calculated from WavelengthRange
    # WavelengthRange (2-tuple of float): The minimum and maximum wavelengths allowed, calculated from FrequencyRange if that is given
    def __init__(self, *args, VoltageRange = (0, 1), FrequencyRange = None, WavelengthRange = (900, 1000), **kwargs):
        super().__init__(*args, **kwargs)
        
        self._voltageRange = (float(VoltageRange[0]), float(VoltageRange[1]))
        
        if FrequencyRange is not None:
            self._frequencyRange = (float(FrequencyRange[0]), float(FrequencyRange[1]))
            self._wavelengthRange = (self.frequencyToWavelength(FrequencyRange[1]), self.frequencyToWavelength(FrequencyRange[0]))
        else:
            self._frequencyRange = (self.wavelengthToFrequency(WavelengthRange[1]), self.wavelengthToFrequency(WavelengthRange[0]))
            self._wavelengthRange = (float(WavelengthRange[0]), float(WavelengthRange[1]))

        self.voltageBase = (self._voltageRange[0] + self._voltageRange[1]) / 2

    # Converts a frequency in THz to a wavelength in nm
    # Value (float): The frequency to convert        
    def frequencyToWavelength(self, Value):
        return 299792458 / (float(Value) * 1e12) * 1e9
    
    # Converts a wavelength in nm to a frequency in THz
    # Value (float): The wavelength to convert
    def wavelengthToFrequency(self, Value):
        return 299792458 / (float(Value) * 1e-9) * 1e-12
    
    # Checks if the frequency is in the allowed range
    # Value (float): The frequency to check
    def frequencyAllowed(self, Value):
        return float(Value) >= self._frequencyRange[0] and float(Value) <= self._frequencyRange[1]
    
    # Checks if the wavelength is in the allowed range
    # Value (float): The wavelength to check
    def wavelengthAllowed(self, Value):
        return float(Value) >= self._wavelengthRange[0] and float(Value) <= self._wavelengthRange[1]
        
    # Checks if the voltage is in the allowed range
    # Value (float): The voltage to check
    def voltageAllowed(self, Value):
        return float(Value) >= self._voltageRange[0] and float(Value) <= self._voltageRange[1]
    
    # Sets the wavelength of the laser, this or setFrequency must be overwritten
    # Value (float): The value of the wavelength
    def setWavelength(self, Value, **kwargs):
        # Make sure it is within the range
        if not self.wavelengthAllowed(Value):
            raise e.RangeError("Value", Value, self._wavelengthRange[0], self._wavelengthRange[1])
        
        self.setFrequency(self.wavelengthToFrequency(Value), **kwargs)
    
    # Gets the wavelength set by the laser, this or getFrequency must be overwritten
    def getWavelength(self, **kwargs):
        return self.frequencyToWavelength(self.getFrequency(**kwargs))
    
    # Sets the frequency of the laser, this or setWavelength must be overwritten
    # Value (float): The value of the frequency
    def setFrequency(self, Value, **kwargs):
        if not self.frequencyAllowed(Value):
            raise e.RangeError("Value", Value, self._frequencyRange[0], self._frequencyRange[1])

        self.setWavelength(self.frequencyToWavelength(Value), **kwargs)
    
    # Gets the frequency set by the laser, this or getWavelength must be overwritten
    def getFrequency(self, **kwargs):
        return self.wavelengthToFrequency(self.getWavelength(**kwargs))
        
    # Sets the piezo voltage of the laser
    # Value (float): The voltage to set
    def setVoltage(self, Value):
        # Check that the voltage is within the limits
        if not self.voltageAllowed(Value):
            raise e.RangeError("Value", Value, self._voltageRange[0], self._voltageRange[1])

        # Save it internally
        self._voltage = float(Value)
        
    # Gets the last voltage set
    def getVoltage(self):
        return self._voltage
    
    
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
        

# A laser class controlled by a DAC
class DACLaser(c.deviceBase, laser): # If used with the equipment.laser remember to set the JumpAttempts to 0
    # DACController (DAC): The DAC to control the voltage
    # Channel (int): The channel of the DAC to use
    # VoltageRange (2-tuple of float): Them minimum and maximum voltage allowed
    # DeviceName (str): The name of the device, only used for error messages
    # ID (str): The ID name for the device, only used for displaying infomation
    def __init__(self, DACController, Channel, *args, **kwargs):
        # Make sure it is a DAC
        if not isinstance(DACController, DAC):
            raise e.TypeDefError("DACController", DACController, DAC)
        
        # Set the voltage range
        if not "VoltageRange" in kwargs:
            kwargs["VoltageRange"] = (-3, 3)

        if not "DeviceName" in kwargs:
            kwargs["DeviceName"] = "DAC Laser"
            
        # Initialize the laser
        super().__init__(*args, **kwargs)
        
        # Save the DAC
        self._DAC = DACController
        self._channel = int(Channel)
        
    # This cannot set the wavelength
    # Value (float): The value of the wavelength
    def setWavelength(self, Value, **kwargs):
        raise e.ImplementationError("DACLaser.setWavelength")

    # This cannot get the wavelength
    def getWavelength(self, **kwargs):
        raise e.ImplementationError("DACLaser.getWavelength")
        
    # This cannot set the frequency
    # Value (float): Tje value of the frequency
    def setFrequency(self, Value, **kwargs):
        raise e.ImplementationError("DACLaser.setFrequency")

    # This cannot get the frequency
    def getFrequency(self, **kwargs):
        raise e.ImplementationError("DACLaser.getFrequency")

    # Sets the voltage using the DAC
    # Value (float): The value of the voltage
    # UseQueue (bool): Whether to run the command through the queue or not
    def setVoltage(self, Value, **kwargs):
        # Save it internally
        super().setVoltage(Value)
        
        # Set voltage
        self._DAC.setVoltage(float(Value), self._channel, **kwargs)   
        
    # Gets the voltage set for the DAC
    # UseQueue (bool): Whether to run the command through the queue or not
    def getVoltage(self, **kwargs):
        return super().getVoltage()
        

# Controls a rigol
class rigol(c.visa):
    # IP (str): The IP of the rigol device
    # VoltageLimit (float): The maximum allowed output voltage
    # Timeout (float): The timeout time for the connection, must not be negative
    # ReconnectTries (int): How many times to attempt to reconnect if it disconnects, must not be smaller than 0
    # ReconnectDelay (float): The delay in seconds between each reconnect attempt, must not be negative
    # MaxAttempts (int): The maximum number attempts to send a command before giving up, must not be smaller than 1
    # AttemptDelay (float): The delay in seconds between each attempt to send a command, must not be negative
    # UseQueue (bool): If True then it will set up a queue which can be used in the sendCommand method, if False the UseQueue in sendCommand is ignored
    # Empty (bool): If True then it will not communicate with the device
    # DeviceName (str): The name of the device, only used for error messages
    # ID (str): The ID name for the device, only used for displaying infomation
    def __init__(self, IP, *args, VoltageLimit = 10, **kwargs):        
        if not "DeviceName" in kwargs:
            kwargs["DeviceName"] = "Rigol"
        
        super().__init__(f"TCPIP0::{IP}::INSTR", *args, **kwargs)
        
        self._voltageLimit = float(VoltageLimit)
        
    def sendCommand(self, *args, **kwargs):
        kwargs["ReturnLines"] = 0
        super().sendCommand(*args, **kwargs)
        
    # Sets the output of a channel to DC
    # Voltage (float): The voltage to set
    # Channel (int): The channel to set
    # UseQueue (bool): Whether to run the command through the queue or not
    def setDCOutput(self, Voltage, Channel, **kwargs):
        Voltage = float(Voltage)
        Channel = int(Channel)

        # Make sure it is within the range
        if abs(Voltage) > self._voltageLimit:
            raise e.RangeError("Voltage", Voltage, -self._voltageLimit, self._voltageLimit)
            
        self.sendCommand(f":SOUR{Channel}:APPL:DC 1,1,{Voltage}", **kwargs)
    
    # Sets the output of a channel to a sine
    # Frequency (float): The frequency of the sine
    # Amplitude (float): The amplitude of the sine
    # Offset (float): The offset of the sine
    # Phase (float): The phase of the sine
    # Channel (int): The channel to set
    # UseQueue (bool): Whether to run the command through the queue or not
    def setSineOutput(self, Frequency, Amplitude, Offset, Phase, Channel, **kwargs):
        Frequency = float(Frequency)
        Amplitude = 2 * float(Amplitude)
        Offset = float(Offset)
        Phase = float(Phase)        
        Channel = int(Channel)

        # Make sure it is within the range
        MaxVoltage = abs(Amplitude) + abs(Offset)
        if MaxVoltage > self._voltageLimit:
            raise e.RangeError("MaxVoltage", MaxVoltage, -self._voltageLimit, self._voltageLimit)
    
        self.sendCommand(f":SOUR{Channel}:APPL:SIN {Frequency},{Amplitude},{Offset},{Phase}", **kwargs)


# A sequence for an FPGA
class FPGASequence:
    # FPGA (timeBandit): The TimeBandit to create sequence for
    # SequenceLength (int): The length of the sequence in input clock cycles, if None then the current length will be used
    def __init__(self, FPGA, SequenceLength, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Make sure the FPGA is a timeBandit
        if not isinstance(FPGA, timeBandit):
            raise e.TypeDefError("FPGA", FPGA, timeBandit)
                
        # Save the FPGA and set up the different channels
        self.FPGA = FPGA
        self.states = ["off"] * len(FPGA.CH)
        self.calibrationModes = [None] * len(FPGA.CH)
        self.invertClocks = [None] * len(FPGA.CH)
        self.sequenceLength = int(SequenceLength)
        
        for i in range(len(FPGA.CH)):
            if isinstance(FPGA.CH[i], FPGAChannelPulse):
                self.invertClocks[i] = False
            
            elif isinstance(FPGA.CH[i], FPGAChannelPhasedPulse):
                self.calibrationModes[i] = False
            
    # Adds an interval for the FPGA channel to be on, if the state was "dc" or "off", then it will overwrite
    # Channel (int): The channel to add a state to
    # Start (float): The start time in ns, this will be rounded down to nearest clock cycle
    # Stop (float): The stop time in ns, this will be rounded up to nearest clock cycle
    def addState(self, Channel, Start, Stop):
        # Get old state state
        State = self.states[Channel]
        
        if isinstance(State, str):
            State = []

        # Add new state
        State.append(self.FPGA.CH[Channel].generateState(Start, Stop, SequenceLength = self.sequenceLength, Calibrating = self.calibrationModes[Channel]))

        self.setState(Channel, State)
    
    # Adds an interval for the FPGA channel to be on, if the state was "dc" or "off", then it will overwrite
    # Channel (int): The channel to add a state to
    # Start (float): The start time in ns, this will be rounded down to nearest clock cycle
    # Duration (float): The duration in ns, this will be rounded up to nearest clock cycle
    def addStateWithDuration(self, Channel, Start, Duration):
        # Get old state state
        State = self.states[Channel]
        
        if isinstance(State, str):
            State = []
            
        # Add new state
        State.append(self.FPGA.CH[Channel].generateStateWithDuration(Start, Duration, SequenceLength = self.sequenceLength, Calibrating = self.calibrationModes[Channel]))

        self.setState(Channel, State)
    
    # Adds an interval for the FPGA channel to be on, if the state was "dc" or "off", then it will overwrite
    # Channel (int): The channel to add a state to
    # Start (float): The start time in clock cycles
    # Stop (float): The stop time in clock cycles
    def addBaseState(self, Channel, Start, Stop):
        # Get old state state
        State = self.states[Channel]
        
        if isinstance(State, str):
            State = []
            
        # Add new state
        State.append(self.FPGA.CH[Channel].generateBaseState(Start, Stop, SequenceLength = self.sequenceLength, Calibrating = self.calibrationModes[Channel]))

        self.setState(Channel, State)
    
    # Adds an interval for the FPGA channel to be on, if the state was "dc" or "off", then it will overwrite
    # Channel (int): The channel to add a state to
    # Start (float): The start time in clock cycles
    # Duration (float): The duration in clock cycles
    def addBaseStateWithDuration(self, Channel, Start, Duration):
        # Get old state state
        State = self.states[Channel]
        
        if isinstance(State, str):
            State = []
            
        # Add new state
        State.append(self.FPGA.CH[Channel].generateBaseStateWithDuration(Start, Duration, SequenceLength = self.sequenceLength, Calibrating = self.calibrationModes[Channel]))

        self.setState(Channel, State)
        
    # Adds an empty pulse
    # Channel (int): The channel to add a state to
    def addEmptyState(self, Channel):
        State = self.states[Channel]
        
        if isinstance(State, str):
            State = []
            
        # Add new state
        State.append(None)

        self.setState(Channel, State)
    
    # Sets the state of the FPGA channel
    # Channel (int): The channel to set the state for
    # State (str / list of 2-tuple of int): The state to set
    def setState(self, Channel, State):
        self.states[Channel] = State
    
    # Sets the state to DC of the FPGA channel
    # Channel (int): The channel to set the state for
    def setDC(self, Channel):
        self.setState(Channel, "dc")
    
    # Sets the state to OFF of the FPGA channel
    # Channel (int): The channel to set the state for
    def setOff(self, Channel):
        self.setState(Channel, "off")
        
    # Sets the calibration mode for a channel
    # Channel (int): The channel to set the state for
    # Value (bool): True if calibration mode should be on, False if it should be off and None if cannot enter this mode
    def setCalibrationMode(self, Channel, Value):
        if Value is not None:
            Value = bool(Value)
        
        self.calibrationModes[Channel] = Value

    # Sets the clock inversion for a channel
    # Channel (int): The channel to set the state for
    # Value (bool): True if clock inversion should be on, False if it should be off and None if cannot enter this mode
    def setInvertClock(self, Channel, Value):
        if Value is not None:
            Value = bool(Value)
        
        self.invertClocks[Channel] = Value
    
    # Apply the sequences to the FPGA channels
    # UseQueue (bool): Whether to run the command through the queue or not    
    def apply(self, **kwargs):
        self.FPGA.resync(**kwargs)

        # Set sequence length
        self.FPGA.setSequenceLength(self.sequenceLength)

        # Set the calibration modes
        for Channel, Mode in zip(self.FPGA.CH, self.calibrationModes):
            if Mode is True:
                Channel.startCalibration()
                
            elif Mode is False:
                Channel.stopCalibration()
        
        # Set clock inversion
        for Channel, Mode in zip(self.FPGA.CH, self.invertClocks):
            if Mode is not None:
                Channel.setInvertClock(Mode, **kwargs)
        
        for Channel, State in zip(self.FPGA.CH, self.states):
            Channel.applyState(State, **kwargs)


# A generic FPGA channel
class FPGAChannel:
    # FPGA (timeBandit): The FPGA it is connected to
    # Channel (int): The channel ID of this channel
    # MemoryOffset (int): The memory offset on the FPGA
    # ClockPartition (int): The number of partitions that each lock cycle can be divided into
    # ModeMemoryOffset (int): The offset relative to MemoryOffset of the configuration bits
    # MaxLength (int): The maximum number of pulses
    def __init__(self, FPGA, Channel, MemoryOffset, *args, ClockPartition = 1, ModeMemoryOffset = 0, MaxLength = 4, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Make sure the FPGA is a timeBandit
        if not isinstance(FPGA, timeBandit):
            raise e.TypeDefError("FPGA", FPGA, timeBandit)
                  
        # Save the data
        self.FPGA = FPGA
        self._memoryOffset = int(MemoryOffset)
        self._modeMemoryOffset = int(ModeMemoryOffset)
        self._maxLength = int(MaxLength)
        self._state = "off"
        self.clockPartition = int(ClockPartition)
        self.channel = int(Channel)
        self._calibrationMode = False
        
    # Generates a single pulse
    # Start (float): The start time in ns, will be rounded down to nearest clock cycle
    # Stop (float): The stop time in ns, will be rounded up to nearest clock cycle
    # SequenceLength (int): The length of the sequence in input clock cycles, if None then the current length will be used
    # Calibrating (bool); If True then it will create calibration pulses
    def generateState(self, Start, Stop, **kwargs):
        return self.generateBaseState(float(Start) * 1e-9 * self.FPGA.getClockFrequency() * self.FPGA.getClocksPerBase(), float(Stop) * 1e-9 * self.FPGA.getClockFrequency() * self.FPGA.getClocksPerBase(), **kwargs)
    
    # Generates a single pulse
    # Start (float): The start time in ns, will be rounded down to nearest clock cycle
    # Duration (float): The duration in ns, will be rounded up to nearest clock cycle
    # SequenceLength (int): The length of the sequence in input clock cycles, if None then the current length will be used
    # Calibrating (bool); If True then it will create calibration pulses
    def generateStateWithDuration(self, Start, Duration, **kwargs):
        return self.generateBaseState(float(Start) * 1e-9 * self.FPGA.getClockFrequency() * self.FPGA.getClocksPerBase(), float(Duration) * 1e-9 * self.FPGA.getClockFrequency() * self.FPGA.getClocksPerBase(), **kwargs)

    # Generates a single pulse
    # Start (float): The start time in clock cycles, will be rounded down to nearest clock cycle
    # Stop (float): The stop time in clock cycles, will be rounded up to nearest clock cycle
    # SequenceLength (int): The length of the sequence in input clock cycles, if None then the current length will be used
    # Calibrating (bool); If True then it will create calibration pulses
    def generateBaseState(self, Start, Stop, SequenceLength = None, Calibrating = None):
        import numpy as np
        
        if SequenceLength is None:
            SequenceLength = self.FPGA.getSequenceLength()
            
        if Calibrating is None:
            Calibrating = self._calibrationMode
        
        # Convert to ints
        if Calibrating:
            Start = (int(float(Start) * 256) / 256) % (SequenceLength * self.FPGA.getClocksPerBase())
            Stop = (int(np.ceil(float(Stop) * 256)) / 256) % (SequenceLength * self.FPGA.getClocksPerBase())
            
        else:
            Start = (int(float(Start) * self.clockPartition) / self.clockPartition) % (SequenceLength * self.FPGA.getClocksPerBase())
            Stop = (int(np.ceil(float(Stop) * self.clockPartition)) / self.clockPartition) % (SequenceLength * self.FPGA.getClocksPerBase())
        
        return (Start, Stop)
    
    # Generates a single pulse
    # Start (float): The start time in clock cycles, will be rounded down to nearest clock cycle
    # Duration (float): The duration in clock cycles, will be rounded up to nearest clock cycle
    # SequenceLength (int): The length of the sequence in input clock cycles, if None then the current length will be used
    # Calibrating (bool); If True then it will create calibration pulses
    def generateBaseStateWithDuration(self, Start, Duration, SequenceLength = None, Calibrating = None):
        import numpy as np
        
        if SequenceLength() is None:
            SequenceLength = self.FPGA.getSequenceLength()

        if Calibrating is None:
            Calibrating = self._calibrationMode

        # Convert to ints
        if Calibrating:
            Start = (int(float(Start) * 256) / 256) % (SequenceLength * self.FPGA.getClocksPerBase())
            Duration = int(np.ceil(float(Duration) * 256)) / 256

        else:
            Start = (int(float(Start) * self.clockPartition) / self.clockPartition) % (SequenceLength * self.FPGA.getClocksPerBase())
            Duration = int(np.ceil(float(Duration) * self.clockPartition)) / self.clockPartition
        
        Stop = (Start + Duration) % (SequenceLength * self.FPGA.getClocksPerBase())
        
        return (Start, Stop)
        
    # Sets the state of the channel
    # Values (list of 2-tuple of float): The state, a list of start, stop times in ns
    # UseQueue (bool): Whether to run the command through the queue or not, ignored if the device was initialized with UseQueue = False
    def setState(self, Values, **kwargs):
        State = []
        
        # Run through all the values
        for Value in Values:
            if Value is None:
                State.append(None)
                
            else:
                State.append(self.generateState(*Value))
            
        self.applyState(State, **kwargs)
    
    # Sets the state of the channel
    # Values (list of 2-tuple of float): The state, a list of start, duration times in ns
    # UseQueue (bool): Whether to run the command through the queue or not, ignored if the device was initialized with UseQueue = False
    def setStateWithDuration(self, Values, **kwargs):
        State = []
        
        # Run through all the values
        for Value in Values:
            if Value is None:
                State.append(None)
                
            else:
                State.append(self.generateStateWithDuration(*Value))
            
        self.applyState(State, **kwargs)
    
    # Sets the state of the channel
    # Values (list of 2-tuple of float): The state, a list of start, stop in clock cycles
    # UseQueue (bool): Whether to run the command through the queue or not, ignored if the device was initialized with UseQueue = False
    def setBaseState(self, Values, **kwargs):
        State = []
        
        # Run through all the values
        for Value in Values:
            if Value is None:
                State.append(None)
                
            else:
                State.append(self.generateBaseState(*Value))
            
        self.applyState(State, **kwargs)
    
    # Sets the state of the channel
    # Values (list of 2-tuple of float): The state, a list of start, duration in clock cycles
    # UseQueue (bool): Whether to run the command through the queue or not, ignored if the device was initialized with UseQueue = False
    def setBaseStateWithDuration(self, Values, **kwargs):
        State = []
        
        # Run through all the values
        for Value in Values:
            if Value is None:
                State.append(None)
                
            else:
                State.append(self.generateBaseStateWithDuration(*Value))
            
        self.applyState(State, **kwargs)
    
    # Sets the state to be DC
    # UseQueue (bool): Whether to run the command through the queue or not, ignored if the device was initialized with UseQueue = False
    def setDC(self, **kwargs):
        self.applyState("dc", **kwargs)
    
    # Sets the state to be off
    # UseQueue (bool): Whether to run the command through the queue or not, ignored if the device was initialized with UseQueue = False
    def setOff(self, **kwargs):
        self.applyState("off", **kwargs)
    
    # Applies a final state
    # State (list of 2-tuple of float): The list of pulses, each containing start and stop times in clock cycles
    # UseQueue (bool): Whether to run the command through the queue or not, ignored if the device was initialized with UseQueue = False
    def applyState(self, State, **kwargs):
        self._state = State
        self.update(**kwargs)
        
    # Gets the currently applied state
    def getState(self):
        return self._state
    
    # Updates the state of the channel
    # UseQueue (bool): Whether to run the command through the queue or not, ignored if the device was initialized with UseQueue = False
    def update(self, **kwargs):
        # Turn the channel off
        if self._state == "off":
            self.FPGA.updateMemory(self._memoryOffset + self._modeMemoryOffset, 0, **kwargs)
            
        # Set channel to DC
        elif self._state == "dc":
            self.FPGA.updateMemory(self._memoryOffset + self._modeMemoryOffset, 16, **kwargs)
            
        # Add pulses
        else:
            # Make sure there are not too many
            if len(self._state) > self._maxLength:
                raise e.MaxLengthError("State", self.state, 8)
                
            ConfigurationBits = self._configurationBits()
                
            # Do the pulses
            for i, Pulse in enumerate(self._state):
                if Pulse is None:
                    continue
                
                if len(Pulse) != 2:
                    raise e.LengthError("Each pulse", Pulse, 2)

                # Add configuration bit to declare the pulse
                ConfigurationBits += int(2 ** i)

                self._update(*Pulse, i, **kwargs)
                                
            # Write the configuration bits
            self.FPGA.updateMemory(self._memoryOffset + self._modeMemoryOffset, ConfigurationBits, **kwargs)
                
    # Updates a single pulse
    # Start (float): The start time in clock cycles
    # Stop (float): The stop time in clock cycles
    # i (int): The pulse ID
    # UseQueue (bool): Whether to run the command through the queue or not, ignored if the device was initialized with UseQueue = False
    def _update(self, Start, Stop, i, **kwargs):
        pass
            
    # Returns a number to add to the configuration bit when updating
    def _configurationBits(self):
        return 0
        
        
# A pulsed FPGA channel
class FPGAChannelPulse(FPGAChannel):
    # FPGA (timeBandit): The FPGA it is connected to
    # Channel (int): The channel ID of this channel
    # MemoryOffset (int): The memory offset on the FPGA    
    def __init__(self, *args, **kwargs):
        kwargs["ClockPartition"] = 1
        kwargs["ModeMemoryOffset"] = 16
        kwargs["MaxLength"] = 4
        
        super().__init__(*args, **kwargs)
        
        self._invertClock = False
    
    # Updates a single pulse
    # Start (float): The start time in clock cycles
    # Stop (float): The stop time in clock cycles
    # i (int): The pulse ID
    # UseQueue (bool): Whether to run the command through the queue or not, ignored if the device was initialized with UseQueue = False
    def _update(self, Start, Stop, i, **kwargs):
        Start = int(Start) % (self.FPGA.getSequenceLength() * self.FPGA.getClocksPerBase())
        Stop = int(Stop) % (self.FPGA.getSequenceLength() * self.FPGA.getClocksPerBase())

        # Update memory
        self.FPGA.updateMemory2(self._memoryOffset + 4 * i, Start, **kwargs)
        self.FPGA.updateMemory2(self._memoryOffset + 4 * i + 2, Stop, **kwargs)
    
    # Returns a number to add to the configuration bit when updating
    def _configurationBits(self):
        if self._invertClock:
            return int(2 ** 5)
        
        return 0
    
    # Sets the invert clock
    # Value (bool): True if the clock should be inverted
    # UseQueue (bool): Whether to run the command through the queue or not, ignored if the device was initialized with UseQueue = False
    def setInvertClock(self, Value, **kwargs):
        self._invertClock = bool(Value)
        self.update(**kwargs)
        
    # Gets the invert clock
    def getInvertClock(self):
        return self._invertClock
                
    
# A phased pulsed FPGA channel
class FPGAChannelPhasedPulse(FPGAChannel):
    # FPGA (timeBandit): The FPGA it is connected to
    # Channel (int): The channel ID of this channel
    # MemoryOffset (int): The memory offset on the FPGA
    # PhaseMemoryOffset (int): The memory offset for 
    # CalibrationData (16-tuple of int): The phase calibration data
    def __init__(self, FPGA, Channel, MemoryOffset, PhaseMemoryOffset, CalibrationData, *args, **kwargs):
        kwargs["ClockPartition"] = 24
        kwargs["ModeMemoryOffset"] = 32
        kwargs["MaxLength"] = 8

        super().__init__(FPGA, Channel, MemoryOffset, *args, **kwargs)
        
        self._phaseMemoryOffset = int(PhaseMemoryOffset)
        self._phaseCalibration = tuple(CalibrationData)
        self.stopCalibration()
        
    # Updates a single pulse
    # Start (float): The start time in clock cycles
    # Stop (float): The stop time in clock cycles
    # i (int): The pulse ID
    # UseQueue (bool): Whether to run the command through the queue or not, ignored if the device was initialized with UseQueue = False
    def _update(self, Start, Stop, i, **kwargs):
        # Get the pulse information bits
        UseStart = (int(Start) - 1) % (self.FPGA.getSequenceLength() * self.FPGA.getClocksPerBase())
        UseStop = (int(Stop) + 1) % (self.FPGA.getSequenceLength() * self.FPGA.getClocksPerBase())
        
        # Update memory
        self.FPGA.updateMemory2(self._memoryOffset + 4 * i, UseStart, **kwargs)
        self.FPGA.updateMemory2(self._memoryOffset + 4 * i + 2, UseStop, **kwargs)
                        
        # Find phases
        if self._calibrationMode:
            PhaseStart = int((Start % 1) * 256)
            PhaseStop = int((Stop % 1) * 256)
            
        else:
            PhaseStart = self._phaseCalibration[2 * i] + int((Start % self.FPGA.getClocksPerBase()) * self.clockPartition)
            PhaseStop = self._phaseCalibration[2 * i + 1] + int((Stop % self.FPGA.getClocksPerBase()) * self.clockPartition)

        # Update memory
        self.FPGA.updateMemory(self._phaseMemoryOffset + 2 * i, PhaseStart, **kwargs)
        self.FPGA.updateMemory(self._phaseMemoryOffset + 2 * i + 1, PhaseStop, **kwargs)                
        
    # Enter calibration mode
    def startCalibration(self):
        self._calibrationMode = True

    # Exit calibration mode
    def stopCalibration(self):
        self._calibrationMode = False

# Controls the time bandit FPGA
class timeBandit(c.serial):
    # Port (str): The name of the COM port through which to access the serial connection
    # CalibrationData (16-tuple of int): The calibration data for the phase channel
    # Channel (int): The default counter channel, must be 0 or 1
    # ClockFrequency (float): The frequency of the base clock
    # ClocksPerBase (int): The number of clock cycles per base clock
    # Timeout (float): The timeout time for the connection, must not be negative
    # ReconnectTries (int): How many times to attempt to reconnect if it disconnects, must not be smaller than 0
    # ReconnectDelay (float): The delay in seconds between each reconnect attempt, must not be negative
    # MaxAttempts (int): The maximum number attempts to send a command before giving up, must not be smaller than 1
    # AttemptDelay (float): The delay in seconds between each attempt to send a command, must not be negative
    # UseQueue (bool): If True then it will set up a queue which can be used in the sendCommand method, if False the UseQueue in sendCommand is ignored
    # Empty (bool): If True then it will not communicate with the device
    # DeviceName (str): The name of the device, only used for error messages
    # ID (str): The ID name for the device, only used for displaying infomation
    def __init__(self, *args, CalibrationData = (0,) * 16, Channel = 1, ClockFrequency = 50e6, ClocksPerBase = 4, **kwargs):
        if not "DeviceName" in kwargs:
            kwargs["DeviceName"] = "TimeBandit"
            
        kwargs["Baudrate"] = 115200
        kwargs["BytesMode"] = True
        
        super().__init__(*args, **kwargs)
                
        self._intTime = 0.1
        self._sequenceLength = 2
        self._clockFrequency = float(ClockFrequency)
        self._clocksPerBase = int(ClocksPerBase)
        self._outputLevel = "off"
        self._outputPhase = 0
        
        self.setDefaultChannel(Channel)
        
        # Add all of the channels
        self.CH = [None] * 7
        self.CH[0] = FPGAChannelPhasedPulse(self, 0, 24, 8, CalibrationData)
        self.CH[1] = FPGAChannelPulse(self, 1, 57)
        self.CH[2] = FPGAChannelPulse(self, 2, 74)
        self.CH[3] = FPGAChannelPulse(self, 3, 91)
        self.CH[4] = FPGAChannelPulse(self, 4, 108)
        self.CH[5] = FPGAChannelPulse(self, 5, 125)
        self.CH[6] = FPGAChannelPulse(self, 6, 142)
        
        self.sendSettings()
        
    # Sets the default channel, it must be 0 or 1
    # Channel (int): The channel to set
    def setDefaultChannel(self, Channel):
        if int(Channel) < 0 or int(Channel) > 1:
            raise e.RangeError("Channel", Channel, 0, 1)
        
        self._channel = int(Channel)
        
    # Gets the default channel
    def getDefaultChannel(self):
        return self._channel
        
    # Updates one byte of memory on the FPGA
    # Address (int): The address to write to, must be smaller than 256
    # Byte (int): The byte to set, must be smaller than 256
    # UseQueue (bool): Whether to run the command through the queue or not, ignored if the device was initialized with UseQueue = False
    def updateMemory(self, Address, Byte, **kwargs):
        # Convert to bytes and write
        self.sendCommand(int(Address % 256).to_bytes(1, "little") + int(Byte).to_bytes(1, "little"), ReturnLines = 2, ResponseCheck = f.responseCheck.timeBanditUpdate(), **kwargs)
        
    # Updates two bytes of memory on the FPGA
    # Address (int): The address to write to, must be smaller than 256
    # Bytes (int): The bytes to set, must be smaller than 256^2
    # UseQueue (bool): Whether to run the command through the queue or not, ignored if the device was initialized with UseQueue = False
    def updateMemory2(self, Address, Bytes, **kwargs):
        # Get the bytes
        Byte1 = Bytes % 256
        Byte2 = Bytes // 256
        
        # Update the memory
        self.updateMemory(Address, Byte1, **kwargs)
        self.updateMemory(Address + 1, Byte2, **kwargs)
        
    # Sets the integration time of the FPGA
    # Value (float): The time in seconds, must be a multiple of 0.01 and be maximally 2.55
    # UseQueue (bool): Whether to run the command through the queue or not, ignored if the device was initialized with UseQueue = False
    def setIntegrationTime(self, Value, **kwargs):
        Value = float(Value)
        
        # Make sure the integration time is correct
        if 100 * Value != int(100 * Value):
            raise e.MultipleError("Integration time", Value, 0.01)
            
        # Make sure it is in the correct interval
        Byte = int(Value * 100)
        
        if Byte <= 0 or Byte >= 256:
            raise e.RangeError("Integration time", Value, 0.01, 2.55)
            
        # Send the infomation
        self.updateMemory(254, Byte, **kwargs)
        
        self._intTime = Value
        
    # Resynchronizes the FPGA to the external clock
    # UseQueue (bool): Whether to run the command through the queue or not, ignored if the device was initialized with UseQueue = False
    def resync(self, **kwargs):
        # Write the message and check for response
        self.sendCommand(b"\x01\x01", ReturnLines = 2, ResponseCheck = f.responseCheck.timeBanditHandShake(), **kwargs)

        
    # Gets the last integration time set
    def getIntegrationTime(self):
        return self._intTime
        
    # Gets the counts
    # UseQueue (bool): Whether to run the command through the queue or not, ignored if the device was initialized with UseQueue = False
    def getCounts(self, **kwargs):
        # Make sure integration time has been set
        if not self._intTime > 0:
            raise e.SharpMinValueError("Integration time", self._intTime, 0)
            
        # Write command and get result
        Result = self.sendCommand(int(253).to_bytes(1, "little") + int(253).to_bytes(1, "little"), ReturnLines = 6, **kwargs)
        return [int.from_bytes(Result[:3], "little"), int.from_bytes(Result[3:], "little")]
    
    # Gets counts from default channel
    # UseQueue (bool): Whether to run the command through the queue or not, ignored if the device was initialized with UseQueue = False
    def getDefaultCount(self, **kwargs):
        Counts = self.getCounts(**kwargs)
        
        return Counts[self._channel]
    
    # The length of a sequence in units of clock cycles
    # Value (int): The number of clock cycles per sequence
    # UseQueue (bool): Whether to run the command through the queue or not, ignored if the device was initialized with UseQueue = False
    def setSequenceLength(self, Value, **kwargs):
        Value = int(Value)
        
        # Make sure it is valid
        if Value <= 0 or Value >= 2 ** 14:
            raise e.SharpRangeError("Sequence length", Value, 0, "2^14")
            
        if Value % 2 != 0:
            raise e.MultipleError("Sequence length", Value, 2)
            
        # Write it
        self.updateMemory2(1, Value // 2 - 1)
        
        self._sequenceLength = Value
         
    # Gets the last selected sequence length
    def getSequenceLength(self):
        return self._sequenceLength
            
    # Gets the base clock frequency
    def getClockFrequency(self):
        return self._clockFrequency
    
    # Gets the number of clocks per base clock cycle
    def getClocksPerBase(self):
        return self._clocksPerBase
    
    # Resend all settings, useful for when FPGA lost power
    # UseQueue (bool): Whether to run the command through the queue or not, ignored if the device was initialized with UseQueue = False
    def sendSettings(self, **kwargs):
        # self.resync(**kwargs)
        self.setSequenceLength(self._sequenceLength, **kwargs)
        self.setIntegrationTime(self._intTime, **kwargs)
        
        # Update the channels
        for CH in self.CH:
            CH.update(**kwargs)
        
        # Update the clock
        self.updateOutputClock(**kwargs)
            
    # Sets the output clock level
    # Level (str): Either off, safe_on or always_on
    # UseQueue (bool): Whether to run the command through the queue or not, ignored if the device was initialized with UseQueue = False
    def setOutputClockLevel(self, Level, **kwargs):
        Level = str(Level).lower()
        
        if not (Level == "off" or Level == "safe_on" or Level == "always_on"):
            raise e.KeywordError("Level", Level, ["off", "safe_on", "always_on"])
            
        self._outputLevel = Level
        self.updateOutputClock(**kwargs)
    
    # Sets the phase of the output clock
    # Phase (int): The phase to set, must be bewteen 0 and 255
    # UseQueue (bool): Whether to run the command through the queue or not, ignored if the device was initialized with UseQueue = False
    def setOutputClockPhase(self, Phase, **kwargs):
        Phase = int(Phase)
        
        if Phase < 0 or Phase > 255:
            raise e.RangeError("Phase", Phase, 0, 255)
            
        self._outputPhase = Phase
        self.updateOutputClock(**kwargs)
    
    # Updates the output clock
    # UseQueue (bool): Whether to run the command through the queue or not, ignored if the device was initialized with UseQueue = False
    def updateOutputClock(self, **kwargs):
        # Update the phase
        self.updateMemory(6, self._outputPhase, **kwargs)
        self.updateMemory(7, self._outputPhase, **kwargs)
        
        # Get the bits
        Bits = 0
        
        # Add for level
        if self._outputLevel == "safe_on":
            Bits += 4
            
        elif self._outputLevel == "always_on":
            Bits += 12
            
        # Update the memory
        self.updateMemory(0, Bits, **kwargs)
        
        
# Controls the SNSPD
class SNSPD(c.socketClient):
    # IP (str): The IP of the socket connection
    # Group (str): A or B, the detector group to use
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
    def __init__(self, IP, Group, *args, **kwargs):
        if not "DeviceName" in kwargs:
            kwargs["DeviceName"] = "SNSPD"
        
        # Make sure types are correct
        if not isinstance(Group, str):
            raise e.TypeDefError("Group", Group, str)
            
        # Get the port
        if Group == "A":
            Port = 65432
            
        elif Group == "B":
            Port = 65433
            
        else:
            raise e.KeywordError("Group", Group, ["A", "B"])
            
        self.group = Group
        
        # Initialize socket
        super().__init__(IP, Port, *args, **kwargs)
        
    # Delatches a channel
    # Channel (int): The channel to delatch
    # UseQueue (bool): Whether to run the command through the queue or not, ignored if the device was initialized with UseQueue = False
    def delatch(self, Channel, **kwargs):
        self.sendWithoutResponse(f"Det-{int(Channel)}:Delatch = 0", **kwargs)
        
    # Sets the bias current of the SNSPD
    # Channel (int): The channel to delatch
    # Bias (float): The bias current to set
    # UseQueue (bool): Whether to run the command through the queue or not, ignored if the device was initialized with UseQueue = False
    def setBias(self, Channel, Bias, **kwargs):
        self.sendWithoutResponse(f"Det-{int(Channel)}:Bias = {float(Bias)}")
        
        
# A generic rotation stage controller
class rotationStage(object):   
    # Homes the device     
    def home(self):
        raise e.ImplementationError("rotationStage.home")
    
    # Moves the device to a specified position
    # Position (float): The position to set
    def moveTo(self, Position):
        raise e.ImplementationError("rotationStage.moveTo")
    
    # Gets the current position of the rotation stage
    def getPosition(self):
        raise e.ImplementationError("rotationStage.getPosition")
    
    # Moves the rotation stage relative to its original position
    # Distance (float): The distance it should move by
    def move(self, Distance, **kwargs):
        # Get new position
        Pos = self.getPosition(**kwargs) + Distance
        
        # Move
        self.moveTo(Pos, **kwargs)
        
        
# A controller for the KDC cube rotation cage
class kinesisRotationStage(rotationStage, c.external):
    # SerialNumber (str): The serial number of the device
    # Timeout (float): The timeout time in seconds
    # UseQueue (bool): If True then it will set up a queue which can be used in the sendCommand method, if False the UseQueue in sendCommand is ignored
    # Empty (bool): If True then it will not communicate with the device
    # DeviceName (str): The name of the device, only used for error messages
    # ID (str): The ID name for the device, only used for displaying infomation    
    def __init__(self, SerialNumber, *args, Timeout = 10, **kwargs):        
        if not "DeviceName" in kwargs:
            kwargs["DeviceName"] = "KDC101"
            
        kwargs["OpenArgs"] = (SerialNumber,)
            
        super().__init__(self, *args, **kwargs)

        # Load
        self._timeout = float(Timeout)
        
    def open(self, SerialNumber):
        from pylablib.devices.Thorlabs import KinesisMotor as m
        self._stage = m(SerialNumber, scale = "stage")
    
    # Homes the device     
    def _home(self):
        self._stage.home(timeout = self._timeout)
    
    # Moves the device to a specified position
    # Position (float): The position to set
    def _moveTo(self, Position):
        self._stage.move_to(Position % 360)
    
    # Gets the current position of the rotation stage
    def _getPosition(self):
        return self._stage.get_position()
    
    # Homes the device     
    # UseQueue (bool): Whether to run the command through the queue or not, ignored if the device was initialized with UseQueue = False
    def home(self, **kwargs):
        self.runFunction("_home", **kwargs)

    # Moves the device to a specified position
    # Position (float): The position to set
    # UseQueue (bool): Whether to run the command through the queue or not, ignored if the device was initialized with UseQueue = False
    def moveTo(self, Position, **kwargs):
        self.runFunction("_moveTo", Args = (Position,), **kwargs)
    
    # Gets the current position of the rotation stage
    # UseQueue (bool): Whether to run the command through the queue or not, ignored if the device was initialized with UseQueue = False
    def getPosition(self, **kwargs):
        return self.runFunction("_getPosition", **kwargs)
    
    def _close(self):
        self._stage.close()
        super()._close()
        
        
# A controller for an ELLO control board
class ELLOControl(c.external):
    # SerialNumber (str): The serial number of the device
    # Timeout (float): The timeout in seconds
    # UseQueue (bool): If True then it will set up a queue which can be used in the sendCommand method, if False the UseQueue in sendCommand is ignored
    # Empty (bool): If True then it will not communicate with the device
    # DeviceName (str): The name of the device, only used for error messages
    # ID (str): The ID name for the device, only used for displaying infomation    
    def __init__(self, SerialNumber, *args, Timeout = 10, **kwargs):        
        if not "DeviceName" in kwargs:
            kwargs["DeviceName"] = "ELLO"
            
        kwargs["OpenArgs"] = (SerialNumber,)
        kwargs["OpenKwargs"] = {"Timeout": Timeout}
                    
        super().__init__(self, *args, **kwargs)
        
    def open(self, SerialNumber, Timeout = 10):
        from pylablib.devices.Thorlabs.elliptec import ElliptecMotor as m
        self._stage = m(SerialNumber, timeout = Timeout, scale = "stage")        
        
    # Creates a controller for a single rotation stage
    # Address (int): The address of the stage
    # DeviceName (str): The name of the device, only used for error messages
    # ID (str): The ID name for the device, only used for displaying infomation    
    def getControl(self, Address, *args, **kwargs):
        return ELLO(self, Address, *args, **kwargs)
    
    # Homes the device  
    # Address (int): The address of the device to access
    def _home(self, Address = 0):
        self._stage.home(addr = Address)
    
    # Moves the device to a specified position
    # Position (float): The position to set
    # Address (int): The address of the device to access
    def _moveTo(self, Position, Address = 0):
        self._stage.move_to(Position % 360, addr = Address)
    
    # Gets the current position of the rotation stage
    # Address (int): The address of the device to access
    def _getPosition(self, Address = 0):
        return self._stage.get_position(addr = Address)

    # Homes the device     
    # Address (int): The address of the device to access
    # UseQueue (bool): Whether to run the command through the queue or not, ignored if the device was initialized with UseQueue = False
    def home(self, Address = 0, **kwargs):
        self.runFunction("_home", Kwargs = {"Address": Address}, **kwargs)

    # Moves the device to a specified position
    # Position (float): The position to set
    # Address (int): The address of the device to access
    # UseQueue (bool): Whether to run the command through the queue or not, ignored if the device was initialized with UseQueue = False
    def moveTo(self, Position, Address = 0, **kwargs):
        self.runFunction("_moveTo", Kwargs = {"Address": Address}, Args = (Position,), **kwargs)
    
    # Gets the current position of the rotation stage
    # Address (int): The address of the device to access
    # UseQueue (bool): Whether to run the command through the queue or not, ignored if the device was initialized with UseQueue = False
    def getPosition(self, Address = 0, **kwargs):
        return self.runFunction("_getPosition", Kwargs = {"Address": Address}, **kwargs)
                
    def _close(self):
        self._stage.close()
        super()._close()

    
# A controller for a single ELLO rotation stage, should be initialized from ELLOControl.getControl
class ELLO(rotationStage, c.deviceBase):
    # Device (ELLOControl): The device to control
    # Address (int): The address of the stage
    # DeviceName (str): The name of the device, only used for error messages
    # ID (str): The ID name for the device, only used for displaying infomation    
    def __init__(self, Device, Address, *args, **kwargs):   
        if not isinstance(Device, ELLOControl):
            raise e.TypeDefError("Device", Device, ELLOControl)
        
        if not "DeviceName" in kwargs:
            kwargs["DeviceName"] = "ELLO"
            
        super().__init__(*args, **kwargs)

        self._device = Device
        self._addr = int(Address)
        
    # Homes the device     
    # UseQueue (bool): Whether to run the command through the queue or not, ignored if the device was initialized with UseQueue = False
    def home(self, **kwargs):
        self._device.home(Address = self._addr, **kwargs)
    
    # Moves the device to a specified position
    # Position (float): The position to set
    # UseQueue (bool): Whether to run the command through the queue or not, ignored if the device was initialized with UseQueue = False
    def moveTo(self, Position, **kwargs):
        self._device.moveTo(Position, Address = self._addr, **kwargs)
    
    # Gets the current position of the rotation stage
    # UseQueue (bool): Whether to run the command through the queue or not, ignored if the device was initialized with UseQueue = False
    def getPosition(self, **kwargs):
        return self._device.getPosition(Address = self._addr, **kwargs)
    
    
# Controls the time tagger
class timeTagger(c.external):
    # DefaultChannel (int): The default channel to get data from
    # DefaultIntegrationTime (float): The default integration time in seconds
    # ClockChannel (int): The default clock channel
    # DefaultGates (list of 2-tuple of int): The default gates in pico seconds
    # BinWidth (int): The width of a bin in ps
    # DefaultCorrelationBins (int): The number of correlation bins to use by default
    # ChannelCount (int): The number of channels accessable
    # UseQueue (bool): If True then it will set up a queue which can be used in the sendCommand method, if False the UseQueue in sendCommand is ignored
    # Empty (bool): If True then it will not communicate with the device
    # DeviceName (str): The name of the device, only used for error messages
    # ID (str): The ID name for the device, only used for displaying infomation    
    def __init__(self, *args, DefaultChannel = 1, DefaultIntegrationTime = 1, ClockChannel = 1, DefaultGates = [], BinWidth = 4, DefaultCorrelationBins = 2500, ChannelCount = 8, **kwargs):        
        import TimeTagger as TT
        self._TT = TT
        
        if not "DeviceName" in kwargs:
            kwargs["DeviceName"] = "TimeTagger"
            
        super().__init__(self, *args, **kwargs)
        
        # Set settings
        self.setDefaultChannel(DefaultChannel)
        self.setDefaultIntegrationTime(DefaultIntegrationTime)
        self.setClockChannel(ClockChannel)
        self.setDefaultGates(DefaultGates)
        self.setDefaultCorrelationBins(DefaultCorrelationBins)
        self._binWidth = int(BinWidth)
        self._device.clearConditionalFilter()
        self._stream = None
        self._streamEnd = 0.
        self._triggerMode = [1] * int(ChannelCount)
        
    def open(self):
        self._device = self._TT.createTimeTagger()
        self._device.reset()
        self._device.sync()
                
    def _close(self):
        self._TT.freeTimeTagger(self._device)
        super()._close()
        
    # Samples from a sampler and waits until it is done
    # Sampler (TimeTagger aquisition class): A class with .isRunning() and .startFor(IntTime) function
    # IntegrationTime (float): The integration time in seconds
    # UseQueue (bool): Whether to run the command through the queue or not, ignored if the device was initialized with UseQueue = False
    def sample(self, Sampler, IntegrationTime, **kwargs):
        self.runFunction("_sample", Args = (Sampler, IntegrationTime), **kwargs)
        
    # Samples from a sampler and waits until it is done
    # Sampler (TimeTagger aquisition class): A class with .isRunning() and .startFor(IntTime) function
    # IntegrationTime (float): The integration time in seconds
    def _sample(self, Sampler, IntegrationTime):
        IntegrationTime = float(IntegrationTime)

        # Start sampling
        Sampler.startFor(int(IntegrationTime * 1e12))
        
        # Wait
        f.time.sleep(IntegrationTime)
        
        Finished = False
        for _ in range(int(IntegrationTime * 100) + 1):
            if not Sampler.isRunning():
                Finished = True
                break
            f.time.sleep(0.01)
            
        if not Finished:
            raise e.FinishMeasurementError(self.deviceName, self)
            
        # Check for overflows
        self._checkOverflows()
        
    # Gets the jitters of all the channels
    # UseQueue (bool): Whether to run the command through the queue or not, ignored if the device was initialized with UseQueue = False
    def calibrate(self, **kwargs):
        return self.runFunction("_calibrate", **kwargs)
        
    # Gets the jitters of all the channels
    def _calibrate(self):
        return self._device.autoCalibration()

    # Checks if any overflows occured
    # UseQueue (bool): Whether to run the command through the queue or not, ignored if the device was initialized with UseQueue = False
    def checkOverflows(self, **kwargs):
        self.runFunction("_checkOverflows", **kwargs)
        
    # Checks if any overflows occured
    def _checkOverflows(self):
        Overflows = self._device.getOverflowsAndClear()
        if Overflows > 0:
            print(f"{self.deviceName} had {Overflows} overflows in the last measurement")

    # Gets the count rates of some channels
    # Channels (int/list of int): The channel or channels to use, if None it will use the default
    # IntegrationTime (float): The integration time in seconds, if None it will use the default
    # UseQueue (bool): Whether to run the command through the queue or not, ignored if the device was initialized with UseQueue = False
    def getCount(self, Channels = None, IntegrationTime = None, **kwargs):
        return self.runFunction("_getCount", Kwargs = {"Channels": Channels, "IntegrationTime": IntegrationTime}, **kwargs)
    
    # Gets the count rates of some channels
    # Channels (int/list of int): The channel or channels to use, if None it will use the default
    # IntegrationTime (float): The integration time in seconds, if None it will use the default
    def _getCount(self, Channels = None, IntegrationTime = None):
        # Get parameters
        if Channels is None:
            Channels = self._channel
                        
        if IntegrationTime is None:
            IntegrationTime = self._intTime
            
        ToInt = False
        if isinstance(Channels, int):
            Channels = [Channels]
            ToInt = True
            
        for i in range(len(Channels)):
            Channels[i] *= self._triggerMode[Channels[i] - 1]
        
        # Setup counter
        Sampler = self._TT.Counter(self._device, Channels, int(float(IntegrationTime) * 1e12), 1)

        # Get counts
        self._sample(Sampler, IntegrationTime)
        
        # Get data
        Data = Sampler.getData()
        
        if ToInt:
            Data = int(Data)
            
        return Data

    # Gets the count within the specified gates
    # ClockChannel (int): The channel to use for the clock
    # Channel (int): The channel to get data from
    # IntegrationTime (float): The integration time for the histogram
    # Gates (list of 2-tuple of int): List of gates where each gate defines the start and end time of data aquisition
    # UseQueue (bool): Whether to run the command through the queue or not, ignored if the device was initialized with UseQueue = False
    def getGatedCount(self, ClockChannel = None, Channel = None, IntegrationTime = None, Gates = None, **kwargs):
        return self.runFunction("_getGatedCount", Kwargs = {"ClockChannel": ClockChannel, "Channel": Channel, "IntegrationTime": IntegrationTime, "Gates": Gates}, **kwargs)

    # Gets the count within the specified gates
    # ClockChannel (int): The channel to use for the clock
    # Channel (int): The channel to get data from
    # IntegrationTime (float): The integration time for the histogram
    # Gates (list of 2-tuple of int): List of gates where each gate defines the start and end time of data aquisition
    def _getGatedCount(self, **kwargs):
        import numpy as np
        
        # Get histogram
        Data, _ = self._getHistogram(**kwargs)
        
        # Sum them
        return np.sum(Data)
    
    # Sets the default channel to use
    # Channel (int): The channel to set
    # UseQueue (bool): Whether to run the command through the queue or not, ignored if the device was initialized with UseQueue = False
    def setDefaultChannel(self, Channel, **kwargs):
        self.runFunction("_setDefaultChannel", Args = (Channel,), **kwargs)

    # Sets the default channel to use
    # Channel (int): The channel to set
    def _setDefaultChannel(self, Channel):
        self._channel = int(Channel)
    
    # Gets the default channel
    # UseQueue (bool): Whether to run the command through the queue or not, ignored if the device was initialized with UseQueue = False
    def getDefaultChannel(self, **kwargs):
        return self.runFunction("_getDefaultChannel", **kwargs)

    # Gets the default channel
    def _getDefaultChannel(self):
        return self._channel
    
    # Sets the default clock channel
    # Channel (int): The channel to set
    # UseQueue (bool): Whether to run the command through the queue or not, ignored if the device was initialized with UseQueue = False
    def setClockChannel(self, Channel, **kwargs):
        self.runFunction("_setClockChannel", Args = (Channel,), **kwargs)
    
    # Sets the default clock channel
    # Channel (int): The channel to set
    def _setClockChannel(self, Channel):
        self._clockChannel = int(Channel)

    # Gets the default clock channel
    # UseQueue (bool): Whether to run the command through the queue or not, ignored if the device was initialized with UseQueue = False
    def getClockChannel(self, **kwargs):
        return self.runFunction("_getClockChannel", **kwargs)
    
    # Gets the default clock channel
    def _getClockChannel(self):
        return self._clockChannel

    # Sets the default integration time
    # IntegrationTime (float): The integration time in seconds
    # UseQueue (bool): Whether to run the command through the queue or not, ignored if the device was initialized with UseQueue = False
    def setDefaultIntegrationTime(self, IntegrationTime, **kwargs):
        self.runFunction("_setDefaultIntegrationTime", Args = (IntegrationTime,), **kwargs)
    
    # Sets the default integration time
    # IntegrationTime (float): The integration time in seconds
    def _setDefaultIntegrationTime(self, IntegrationTime):
        self._intTime = float(IntegrationTime)

    # Gets the default integration time
    # UseQueue (bool): Whether to run the command through the queue or not, ignored if the device was initialized with UseQueue = False
    def getDefaultIntegrationTime(self, **kwargs):
        return self.runFunction("_getDefaultIntegrationTime", **kwargs)
    
    # Gets the default integration time
    def _getDefaultIntegrationTime(self):
        return self._intTime

    # Sets the default gates
    # Gates (list of 2-tuple of float): List of gates of (StartTime, EndTime) in nano seconds
    # UseQueue (bool): Whether to run the command through the queue or not, ignored if the device was initialized with UseQueue = False
    def setDefaultGates(self, Gates, **kwargs):
        self.runFunction("_setDefaultGates", Args = (Gates,), **kwargs)
    
    # Sets the default gates
    # Gates (list of 2-tuple of float): List of gates of (StartTime, EndTime) in nano seconds
    def _setDefaultGates(self, Gates):
        CorrectGates = []
        
        for Gate in Gates:
            CorrectGates.append((float(Gate[0]), float(Gate[1])))
            
        self._gates = CorrectGates

    # Gets the default gates
    # UseQueue (bool): Whether to run the command through the queue or not, ignored if the device was initialized with UseQueue = False
    def getDefaultGates(self, **kwargs):
        return self.runFunction("_getDefaultGates", **kwargs)
    
    # Gets the default gates
    def _getDefaultGates(self):
        return self._gates
    
    # Sets the bin width
    # Value (int): The bin width in ps
    # UseQueue (bool): Whether to run the command through the queue or not, ignored if the device was initialized with UseQueue = False
    def setBinWidth(self, Value, **kwargs):
        self.runFunction("_setBinWidth", Args = (Value,), **kwargs)
    
    # Sets the bin width
    # Value (int): The bin width in ps
    def _setBinWidth(self, Value):
        self._binWidth = int(Value)
    
    # Gets the bin width in ps
    # UseQueue (bool): Whether to run the command through the queue or not, ignored if the device was initialized with UseQueue = False
    def getBinWidth(self, **kwargs):
        return self.runFunction("_getBinWidth", **kwargs)        
    
    # Gets the bin width in ps
    def _getBinWidth(self):
        return self._binWidth

    # Sets the default correlation bin count
    # BinCount (int): The number of bins
    # UseQueue (bool): Whether to run the command through the queue or not, ignored if the device was initialized with UseQueue = False
    def setDefaultCorrelationBins(self, BinCount, **kwargs):
        self.runFunction("_setDefaultCorrelationBins", Args = (BinCount,), **kwargs)
    
    # Sets the default correlation bin count
    # BinCount (int): The number of bins
    def _setDefaultCorrelationBins(self, BinCount):
        self._binCount = int(BinCount)

    # Gets the default correlation bin count
    # UseQueue (bool): Whether to run the command through the queue or not, ignored if the device was initialized with UseQueue = False
    def getDefaultCorrelationBins(self, **kwargs):
        return self.runFunction("_getDefaultCorrelationBins", **kwargs)
    
    # Gets the default correlation bin count
    def _getDefaultCorrelationBins(self):
        return self._binCount
        
    # Sets the trigger level of a channel
    # Channel (int): The channel to apply to
    # Level (float): The voltage level for the trigger
    # UseQueue (bool): Whether to run the command through the queue or not, ignored if the device was initialized with UseQueue = False
    def setTriggerLevel(self, Channel, Level, **kwargs):
        self.runFunction("_setTriggerLevel", Args = (Channel, Level), **kwargs)

    # Sets the trigger level of a channel
    # Channel (int): The channel to apply to
    # Level (float): The voltage level for the trigger
    def _setTriggerLevel(self, Channel, Level):
        self._device.setTriggerLevel(Channel, Level)

    # Gets the trigger level of a channel
    # Channel (int): The channel to get it from
    # UseQueue (bool): Whether to run the command through the queue or not, ignored if the device was initialized with UseQueue = False
    def getTriggerLevel(self, Channel, **kwargs):
        return self.runFunction("_getTriggerLevel", Args = (Channel,), **kwargs)
    
    # Gets the trigger level of a channel
    # Channel (int): The channel to get it from
    def _getTriggerLevel(self, Channel):
        return self._device.getTriggerLevel(Channel)

    # Sets the trigger mode for a channel
    # Channel (int): The channel to set the trigger mode for
    # Mode (str): The mode of the channel, either "rising" or "falling"
    # UseQueue (bool): Whether to run the command through the queue or not, ignored if the device was initialized with UseQueue = False
    def setTriggerMode(self, Channel, Mode, **kwargs):
        self.runFunction("_setTriggerMode", Args = (Channel, Mode), **kwargs)

    # Sets the trigger mode for a channel
    # Channel (int): The channel to set the trigger mode for
    # Mode (str): The mode of the channel, either "rising" or "falling"
    def _setTriggerMode(self, Channel, Mode):
        Mode = Mode.lower()
        
        if not Mode in ["rising", "falling"]:
            raise e.KeywordError("Mode", Mode, Valid = ["rising", "falling"])
            
        if Mode == "rising":
            self._triggerMode[Channel - 1] = 1
            
        else:
            self._triggerMode[Channel - 1] = -1

    # Gets the trigger mode for a channel
    # Channel (int): The channel to get the trigger mode for
    # UseQueue (bool): Whether to run the command through the queue or not, ignored if the device was initialized with UseQueue = False
    def getTriggerMode(self, Channel, **kwargs):
        return self.runFunction("_getTriggerMode", Args = (Channel,), **kwargs)
            
    # Gets the trigger mode for a channel
    # Channel (int): The channel to get the trigger mode for
    def _getTriggerMode(self, Channel):
        if self._triggerMode[Channel - 1] == 1:
            return "rising"
        
        else:
            return "falling"

    # Sets the dead time of a channel
    # Channel (int): The channel to apply it to
    # DeadTime (float): The dead time in nano seconds
    # UseQueue (bool): Whether to run the command through the queue or not, ignored if the device was initialized with UseQueue = False
    def setDeadTime(self, Channel, DeadTime, **kwargs):
        self.runFunction("_setDeadTime", Args = (Channel, DeadTime), **kwargs)
    
    # Sets the dead time of a channel
    # Channel (int): The channel to apply it to
    # DeadTime (float): The dead time in nano seconds
    def _setDeadTime(self, Channel, DeadTime):
        self._device.setDeadtime(Channel, int(round(float(DeadTime) * 1e3)))
    
    # Gets the dead time of a channel
    # Channel (int): The channel to get it from
    # UseQueue (bool): Whether to run the command through the queue or not, ignored if the device was initialized with UseQueue = False
    def getDeadTime(self, Channel, **kwargs):
        return self.runFunction("_getDeadTime", Args = (Channel,), **kwargs)

    # Gets the dead time of a channel
    # Channel (int): The channel to get it from
    def _getDeadTime(self, Channel):
        return self._device.getDeadtime(Channel) * 1e-3

    # Sets an artificial delay of a channel
    # Channel (int): The channel to set it for
    # Delay (float): The delay time in nano seconds
    # UseQueue (bool): Whether to run the command through the queue or not, ignored if the device was initialized with UseQueue = False
    def setChannelDelay(self, Channel, Delay, **kwargs):
        self.runFunction("_setChannelDelay", Args = (Channel, Delay), **kwargs)
    
    # Sets an artificial delay of a channel
    # Channel (int): The channel to set it for
    # Delay (float): The delay time in nano seconds
    def _setChannelDelay(self, Channel, Delay):
        self._device.setInputDelay(Channel, int(round(float(Delay) * 1e3)))

    # Gets the delay of a channel
    # Channel (int): The channel to get it from
    # UseQueue (bool): Whether to run the command through the queue or not, ignored if the device was initialized with UseQueue = False
    def getChannelDelay(self, Channel, **kwargs):
        return self.runFunction("_getChannelDelay", Args = (Channel,), **kwargs)
    
    # Gets the delay of a channel
    # Channel (int): The channel to get it from
    def _getChannelDelay(self, Channel):
        return self._device.getInputDelay(Channel) * 1e-3
    
    # Gets the clock rate
    # ClockChannel (int): The channel to use for the clock
    # ClockRate (float): The clock rate for the histogram, if not given then it will calculate it itself    
    # UseQueue (bool): Whether to run the command through the queue or not, ignored if the device was initialized with UseQueue = False
    def getClockRate(self, ClockChannel = None, IntegrationTime = 0.05, **kwargs):
        return self.runFunction("_getClockRate", Kwargs = {"ClockChannel": ClockChannel, "IntegrationTime": IntegrationTime}, **kwargs)   
    
    # Gets the clock rate
    # ClockChannel (int): The channel to use for the clock
    # ClockRate (float): The clock rate for the histogram, if not given then it will calculate it itself    
    def _getClockRate(self, ClockChannel = None, IntegrationTime = 0.05):
        if ClockChannel is None:
            ClockChannel = self._clockChannel

        ClockRate = self._getCount(Channels = ClockChannel, IntegrationTime = IntegrationTime) / IntegrationTime
    
        if ClockRate == 0:
            raise e.WrongValueError(f"The count rate of channel {ClockChannel} for {self.deviceName}", ClockRate)

        return ClockRate
    
    # Gets a histogram
    # ClockChannel (int): The channel to use for the clock
    # Channel (int): The channel to get data from
    # IntegrationTime (float): The integration time for the histogram
    # Gates (list of 2-tuple of int): List of gates where each gate defines the start and end time of data aquisition
    # ClockRate (float): The clock rate for the histogram, if not given then it will calculate it itself
    # UseQueue (bool): Whether to run the command through the queue or not, ignored if the device was initialized with UseQueue = False
    def getHistogram(self, ClockChannel = None, Channel = None, IntegrationTime = None, Gates = None, ClockRate = None, **kwargs):
        return self.runFunction("_getHistogram", Kwargs = {"ClockChannel": ClockChannel, "Channel": Channel, "IntegrationTime": IntegrationTime, "Gates": Gates, "ClockRate": ClockRate}, **kwargs)
    
    # Gets a histogram
    # ClockChannel (int): The channel to use for the clock
    # Channel (int): The channel to get data from
    # IntegrationTime (float): The integration time for the histogram
    # Gates (list of 2-tuple of int): List of gates where each gate defines the start and end time of data aquisition
    # ClockRate (float): The clock rate for the histogram, if not given then it will calculate it itself
    def _getHistogram(self, ClockChannel = None, Channel = None, IntegrationTime = None, Gates = None, ClockRate = None):
        import numpy as np
        
        if ClockChannel is None:
            ClockChannel = self._clockChannel
            
        if Channel is None:
            Channel = self._channel
            
        if IntegrationTime is None:
            IntegrationTime = self._intTime
            
        if Gates is None:
            Gates = self._gates
            
        # Get the count rate
        if ClockRate is None:
            ClockRate = self._getClockRate(ClockChannel = ClockChannel)
        
        ClockChannel *= self._triggerMode[ClockChannel - 1]
        Channel *= self._triggerMode[Channel - 1]
        
        Duration = 1 / ClockRate
        BinCount = int(1e12 * Duration / self._binWidth)

        Sampler = self._TT.Histogram(self._device, Channel, ClockChannel, self._binWidth, BinCount)
    
        # Start the sampler
        self._sample(Sampler, IntegrationTime)
        
        Bins = np.array(Sampler.getData(), dtype = int)
        Times = np.array(Sampler.getIndex() * 1e-3, dtype = float)

        # Gate the data
        if len(Gates) > 0:
            NewBins = np.zeros(BinCount)
    
            for Gate in Gates:
                Mask = (Times >= Gate[0]) & (Times <= Gate[1])
                NewBins[Mask] = Bins[Mask]
                
        else:
            NewBins = Bins
        
        return NewBins, Times
    
    # Gets the histogram bins times
    # ClockChannel (int): The channel to use for the clock
    # ClockRate (float): The clock rate for the histogram, if not given then it will calculate it itself
    # UseQueue (bool): Whether to run the command through the queue or not, ignored if the device was initialized with UseQueue = False
    def getHistogramBins(self, ClockChannel = None, ClockRate = None, **kwargs):
        return self.runFunction("_getHistogramBins", Kwargs = {"ClockChannel": ClockChannel, "ClockRate": ClockRate}, **kwargs)

    # Gets the histogram bins times
    # ClockChannel (int): The channel to use for the clock
    # ClockRate (float): The clock rate for the histogram, if not given then it will calculate it itself
    def _getHistogramBins(self, ClockChannel = None, ClockRate = None):
        import numpy as np
        
        if ClockChannel is None:
            ClockChannel = self._clockChannel
            
        ClockChannel = self._triggerMode[ClockChannel - 1]
            
        Channel = self._channel
            
        # Get the count rate
        if ClockRate is None:
            ClockRate = self._getClockRate(ClockChannel = ClockChannel)
        
        Duration = 1 / ClockRate
        BinCount = int(1e12 * Duration / self._binWidth)
        
        Sampler = self._TT.Histogram(self._device, ClockChannel, Channel, self._binWidth, BinCount)
    
        Times = np.array(Sampler.getIndex() * 1e-3)
        
        return Times

    # Gets the correlation between 2 channels, set them equal for autocorrelations
    # ChannelStart (int): The channel for which start clicks are detected, if None it will use the default channel
    # ChannelStop (int): The channel for which stop clicks are detected, if None it will use the default channel
    # BinCount (int): The number of bins to use in the correlations, if None it will use the default bin count
    # IntegrationTime (float): The time to run the experiment for in seconds, if None use the default integration time
    # UseQueue (bool): Whether to run the command through the queue or not, ignored if the device was initialized with UseQueue = False
    def getCorrelations(self, ChannelStart = None, ChannelStop = None, BinCount = None, IntegrationTime = None, **kwargs):
        return self.runFunction("_getCorrelations", Kwargs = {"ChannelStart": ChannelStart, "ChannelStop": ChannelStop, "BinCount": BinCount, "IntegrationTime": IntegrationTime}, **kwargs)
    
    # Gets the correlation between 2 channels, set them equal for autocorrelations
    # ChannelStart (int): The channel for which start clicks are detected, if None it will use the default channel
    # ChannelStop (int): The channel for which stop clicks are detected, if None it will use the default channel
    # BinCount (int): The number of bins to use in the correlations, if None it will use the default bin count
    # IntegrationTime (float): The time to run the experiment for in seconds, if None use the default integration time
    def _getCorrelations(self, ChannelStart = None, ChannelStop = None, BinCount = None, IntegrationTime = None):
        import numpy as np
        
        # Get the correct parameters
        if ChannelStart is None:
            ChannelStart = self._channel
            
        if ChannelStop is None:
            ChannelStop = self._channel
            
        if BinCount is None:
            BinCount = self._binCount
            
        if IntegrationTime is None:
            IntegrationTime = self._intTime
            
        ChannelStart *= self._triggerMode[ChannelStart - 1]
        ChannelStop *= self._triggerMode[ChannelStop - 1]
            
        # Start the experiment
        Sampler = self._TT.Correlation(self._device, ChannelStop, ChannelStart, self._binWidth, BinCount)
        self._sample(Sampler, IntegrationTime)
        
        # Get the data
        Counts = np.array(Sampler.getData(), dtype = int)
        NormCounts = np.array(Sampler.getDataNormalized(), dtype = float)
        Delays = np.array(Sampler.getIndex(), dtype = float) * 1e-3
        
        return Counts, NormCounts, Delays

    # Initialize a stream to gather data through
    # MaxSize (int): The maximum allowed number of events within the stream
    # Channels (list of int): A list of all the channels to get data from, leave empty for all channels
    # UseQueue (bool): Whether to run the command through the queue or not, ignored if the device was initialized with UseQueue = False
    def initStream(self, MaxSize = 1000000, Channels = [], **kwargs):
        self.runFunction("_initStream", Kwargs = {"MaxSize": MaxSize, "Channels": Channels}, **kwargs)
        
    # Initialize a stream to gather data through
    # MaxSize (int): The maximum allowed number of events within the stream
    # Channels (list of int): A list of all the channels to get data from, leave empty for all channels
    def _initStream(self, MaxSize = 1000000, Channels = []):
        # Create the steam
        self._stream = self._TT.TimeTagStream(self._device, MaxSize, Channels)
        
    # Starts the stream and notes down when it is done
    # IntegrationTime (float): The integration time in seconds, None to use default
    # UseQueue (bool): Whether to run the command through the queue or not, ignored if the device was initialized with UseQueue = False
    def startStream(self, IntegrationTime = None, **kwargs):
        self.runFunction("_startStream", Kwargs = {"IntegrationTime": IntegrationTime}, **kwargs)

    # Starts the stream and notes down when it is done
    # IntegrationTime (float): The integration time in seconds, None to use default
    def _startStream(self, IntegrationTime = None):
        import time
        
        # Make sure the is a stream
        if self._stream is None:
            raise e.InitializeError(f"The stream for {self.deviceName}", self)
            
        # Get the integration time
        if IntegrationTime is None:
            IntegrationTime = self._intTime
            
        # Start the stream
        self._stream.startFor(int(IntegrationTime * 1e12))
        self._streamEnd = time.time() + IntegrationTime

    # Gets the data from the stream after waiting for it to finish, returns Timestamps, Channels which are both lists as long as the number of events
    # UseQueue (bool): Whether to run the command through the queue or not, ignored if the device was initialized with UseQueue = False
    def getData(self, **kwargs):
        return self.runFunction("_getData", **kwargs)
            
    # Gets the data from the stream after waiting for it to finish, returns Timestamps, Channels which are both lists as long as the number of events
    def _getData(self):
        import time
        import numpy as np
        
        # Wait for data to finish
        RemainTime = self._streamEnd - time.time()
        
        f.time.sleep(RemainTime)
        
        Finished = False
        for _ in range(1000):
            if not self._stream.isRunning():
                Finished = True
                break
            f.time.sleep(0.01)
            
        if not Finished:
            raise e.FinishMeasurementError(self.deviceName, self)
        
        # Get data
        Data = self._stream.getData()
        Timestamps = np.array(Data.getTimestamps(), dtype = float) * 1e-3
        Channels = np.array(Data.getChannels(), dtype = int)
        
        if Data.hasOverflows():
            raise e.OverflowError(self.deviceName, self)
        
        return Timestamps, Channels


# A sequence for the AWG
class AWGSequence:
    # Device (AWG): The AWG device
    # Name (str): The name of this sequence, must be unique
    # Period (float): The period of the sequence in ns
    # Mode (str): BB: baseband mode, RF: radio frequency mode
    # Entries (int): The number of entries to use
    def __init__(self, Device, Name, Period, *args, Mode = "BB", Entries = 1, **kwargs):
        super().__init__(*args, **kwargs)
        
        if not Mode in ["BB", "RF"]:
            raise e.KeywordError("Mode", Mode, Valid = ["BB", "RF"])
        
        if not isinstance(Device, AWG):
            raise e.TypeDefError("Device", Device, AWG)
        
        # Save the settings
        self.device = Device
        self.name = str(Name)
        self.sampleFreq = Device.getSampleFrequency()
        self.length = int(self.sampleFreq * float(Period))
        self.mode = str(Mode)
        self.channelCount = Device.channelCount
        self.entryCount = int(Entries)
        self.sequences = [[None] * self.channelCount] * self.entryCount
        
        if self.mode == "RF":
            self.length //= 8
        
    # Applies this sequence
    # UseQueue (bool): Whether to run the command through the queue or not, ignored if the device was initialized with UseQueue = False    
    def apply(self, **kwargs):
        self.device.loadSequence(self, **kwargs)
        
    # Initializes the channel if needed
    # Channel (int): The channel to initialize
    def _setupChannel(self, Channel):
        import numpy as np
        
        if self.sequences[0][Channel - 1] is None:
            for i in range(self.entryCount):
                self.sequences[i][Channel - 1] = np.zeros(self.length, dtype = float)
               
    # Converts amplitude and phase to I and Q
    # Amplitude (float): The amplitude value
    # Phase (float): The phase value
    @staticmethod
    def toIQ(Amplitude, Phase):
        import numpy as np
        
        I = Amplitude * np.cos(Phase)
        Q = -Amplitude * np.sin(Phase)
        
        return I, Q
    
    # Converts I and Q to amplitude and phase
    # I (float): The I value
    # Q (float): The Q value
    @staticmethod
    def fromIQ(I, Q):
        import numpy as np
        
        Amplitude = np.sqrt(I ** 2 + Q ** 2)
        Phase = np.arctan(-Q / I) - (I < 0).astype(int) * np.sign(Q) * np.pi
        
        return Amplitude, Phase
        
    # Adds a pulse to the sequence in units of clock cycles, Start is rounded down, Stop is rounded up
    # Start (float): The start clock cycle of the pulse, it is rounded down to nearest clock cycle
    # Stop (float): The stop clock cyle of the pulse, it is rounded up to nearest clock cycle
    # Amplitude (float): The amplitude of the pulse in volts
    # Phase (float): The phase of the RF signal, ignored on BB mode
    # Channel (int): The channel to apply this to
    # Entry (int): The entry to apply this to
    def addBasePulse(self, Start, Stop, Amplitude = 1, Phase = 0, Channel = 1, Entry = 1):
        import numpy as np
        
        # Setup the channel
        self._setupChannel(Channel)
        
        Start = int(Start) % self.length
        Stop = int(np.ceil(Stop)) % self.length
        
        # Add the pulse
        if self.mode == "BB":
            Waveform = self.sequences[Entry - 1][Channel - 1].waveform
            
            if Stop < Start:
                Waveform[Start:] += Amplitude
                Waveform[:Stop] += Amplitude
                
            else:
                Waveform[Start:Stop] += Amplitude
                
            self.sequences[Entry - 1][Channel - 1] = AWGSingleSequence(Waveform)
                
        else:
            I, Q = self.toIQ(Amplitude, Phase)
            
            WaveformI = self.sequences[Entry - 1][Channel - 1][0].waveform
            WaveformQ = self.sequences[Entry - 1][Channel - 1][1].waveform
            
            if Stop < Start:
                WaveformI[Start:] += I
                WaveformI[:Stop] += I
                WaveformQ[Start:] += Q
                WaveformQ[:Stop] += Q
                
            else:
                WaveformI[Start:Stop] += I
                WaveformQ[Start:Stop] += Q
                
            self.sequences[Entry - 1][Channel - 1] = (AWGSingleSequence(WaveformI), AWGSingleSequence(WaveformQ))

        
    # Adds a pulse to the sequence in units of ns, Start is rounded down, Stop is rounded up
    # Start (float): The start time of the pulse, it is rounded down to nearest clock cycle
    # Stop (float): The stop time of the pulse, it is rounded up to nearest clock cycle
    # Amplitude (float): The amplitude of the pulse in volts
    # Phase (float): The phase of the RF signal, ignored on BB mode
    # Channel (int): The channel to apply this to
    # Entry (int): The entry to apply this to
    def addPulse(self, Start, Stop, Amplitude = 1, Phase = 0, Channel = 1, Entry = 1):
        self.addBasePulse(Start * self.sampleFreq, Stop * self.sampleFreq, Amplitude = Amplitude, Phase = Phase, Channel = Channel, Entry = Entry)

    # Adds a pulse to the sequence in units of clock cycles, Start is rounded down, Duration is rounded up
    # Start (float): The start clock cycle of the pulse, it is rounded down to nearest clock cycle
    # Duration (float): The duration cyle of the pulse, it is rounded up to nearest clock cycle
    # Amplitude (float): The amplitude of the pulse in volts
    # Phase (float): The phase of the RF signal, ignored on BB mode
    # Channel (int): The channel to apply this to
    # Entry (int): The entry to apply this to
    def addBasePulseWithDuration(self, Start, Duration, Amplitude = 1, Phase = 0, Channel = 1, Entry = 1):
        import numpy as np
        
        Start = int(Start) % self.length
        Duration = int(np.ceil(Duration))
        Stop = Start + Duration
        
        self.addBasePulse(Start, Stop, Amplitude = Amplitude, Phase = Phase, Channel = Channel, Entry = Entry)
        
    # Adds a pulse to the sequence in units of ns, Start is rounded down, Duration is rounded up
    # Start (float): The start time of the pulse, it is rounded down to nearest clock cycle
    # Duration (float): The duration of the pulse, it is rounded up to nearest clock cycle
    # Amplitude (float): The amplitude of the pulse in volts
    # Phase (float): The phase of the RF signal, ignored on BB mode
    # Channel (int): The channel to apply this to
    # Entry (int): The entry to apply this to
    def addPulseWithDuration(self, Start, Duration, Amplitude = 1, Phase = 0, Channel = 1, Entry = 1):
        self.addBasePulseWithDuration(Start * self.sampleFreq, Duration * self.sampleFreq, Amplitude = Amplitude, Phase = Phase, Channel = Channel, Entry = Entry)
    
    # Adds a DC signal in units of clock cycles
    # Amplitude (float): The amplitude of the signal in volts
    # Phase (float): The phase of the RF signal, ignored on BB mode
    # Channel (int): The channel to apply this to
    # Entry (int): The entry to apply this to
    def addDC(self, Amplitude = 1, Phase = 0, Channel = 1, Entry = 1):
        # Setup the channel
        self._setupChannel(Channel)
        
        # Add the pulse
        if self.mode == "BB":
            Waveform = self.sequences[Entry - 1][Channel - 1].waveform
            Waveform += Amplitude
            self.sequences[Entry - 1][Channel - 1] = AWGSingleSequence(Waveform)
                
        else:
            I, Q = self.toIQ(Amplitude, Phase)            
            WaveformI = self.sequences[Entry - 1][Channel - 1][0].waveform
            WaveformQ = self.sequences[Entry - 1][Channel - 1][1].waveform
            WaveformI += I
            WaveformQ += Q
            self.sequences[Entry - 1][Channel - 1] = (AWGSingleSequence(WaveformI), AWGSingleSequence(WaveformQ))


# A single waveform for the AWG
class AWGSingleSequence:
    # Waveform (numpy.ndarray of float): The waveform to save
    def __init__(self, Waveform):
        import numpy as np
        
        # Save the pure waveform        
        self.waveform = np.array(Waveform, dtype = float).flatten()
        
        # Get the size of the data
        self.min = np.min(self.waveform)
        self.max = np.max(self.waveform)
        
        # Save normalized data
        self.normWaveform = ((self.waveform - self.min) / (self.max - self.min) * (2 ** 15 - 1)).astype(np.uint16)


# Controls an AWG
class AWG(c.visa):
    # IP (str): The IP of the AWG
    # DefaultChannel (int): The default channel to use
    # TriggerLevel (float): The trigger level for the external clock
    # TriggerDelay (float): The delay of the trigger in seconds
    # MaxSampleFrequency (float): The maximum allowed sampling frequency
    # ChannelCount (int): The number of channels
    # Timeout (float): The timeout time for the connection, must not be negative
    # ReconnectTries (int): How many times to attempt to reconnect if it disconnects, must not be smaller than 0
    # ReconnectDelay (float): The delay in seconds between each reconnect attempt, must not be negative
    # MaxAttempts (int): The maximum number attempts to send a command before giving up, must not be smaller than 1
    # AttemptDelay (float): The delay in seconds between each attempt to send a command, must not be negative
    # UseQueue (bool): If True then it will set up a queue which can be used in the sendCommand method, if False the UseQueue in sendCommand is ignored
    # Empty (bool): If True then it will not communicate with the device
    # DeviceName (str): The name of the device, only used for error messages
    # ID (str): The ID name for the device, only used for displaying infomation
    def __init__(self, IP, *args, DefaultChannel = 1, TriggerLevel = 0.4, TriggerDelay = 0, MaxSampleFrequency = 6.16, ChannelCount = 4, **kwargs):
        if not "DeviceName" in kwargs:
            kwargs["DeviceName"] = "AWG"
            
        super().__init__(f"TCPIP::{IP}::INSTR", *args, **kwargs)
        
        # Set default values
        self.setDefaultChannel(DefaultChannel)
        self.maxSampleFrequency = float(MaxSampleFrequency)
        self.channelCount = int(ChannelCount)
        
        # Run setup
        self.sendWithoutResponse("*CLS")
        self.sendWithoutResponse("*RST")
        self.sendWithoutResponse("DISPlay:UNIT:VOLT AMPLitudeoff")
        self.sendWithoutResponse("AWGControl:DECreasing DECIMation")
        self.sendWithoutResponse("AWGControl:INCreasing INTERpolation")
        self.syncTrigger(TriggerLevel, TriggerDelay = TriggerDelay)
        self.reset()
        
    def write(self, Message, WaveformData = None):
        if WaveformData is None:
            self._visa.write(str(Message))
            
        else:
            self._visa.write_binary_values(str(Message), WaveformData, datatype = "d", is_big_endian = False)
        
    # Sets the default channel
    # Channel (int): The default channel
    def setDefaultChannel(self, Channel):
        self._channel = int(Channel)
    
    # Gets the default channel
    def getDefaultChannel(self):
        return self._channel
            
    # Sets the run mode
    # Mode (str): The new mode
    # UseQueue (bool): Whether to run the command through the queue or not, ignored if the device was initialized with UseQueue = False
    def setMode(self, Mode, **kwargs):
        self.sendWithoutResponse(f"AWGControl:RMODe {Mode}", **kwargs)
        
    # Gets the run mode
    # UseQueue (bool): Whether to run the command through the queue or not, ignored if the device was initialized with UseQueue = False
    def getMode(self, **kwargs):
        return self.query("AWGControl:RMODe?", **kwargs)
    
    # Sets the sampling frequency in GHz
    # Value (float): The sampling frequency
    # UseQueue (bool): Whether to run the command through the queue or not, ignored if the device was initialized with UseQueue = False
    def setSampleFrequency(self, Value, **kwargs):
        self.sendWithoutResponse(f"AWGControl:SRATe {float(Value) * 1e9}", **kwargs)

    # Gets the sampling frequency in GHz
    # UseQueue (bool): Whether to run the command through the queue or not, ignored if the device was initialized with UseQueue = False
    def getSampleFrequency(self, **kwargs):
        return float(self.query("AWGControl:SRATe?", **kwargs)) * 1e-9

    # Sets the reference clock rate
    # Value (float): The clock rate to set
    # UseQueue (bool): Whether to run the command through the queue or not, ignored if the device was initialized with UseQueue = False
    def setRefClockRate(self, Value, **kwargs):
        self.sendWithoutResponse("ROSCillator:SOURce REFCLK", **kwargs)
        self.sendWithoutResponse(f"ROSCillator {float(Value)}", **kwargs)
    
    # Sets all the trigger variables
    # TriggerLevel (float): The trigger level for the external clock
    # TriggerDelay (float): The delay for the trigger in seconds
    # UseQueue (bool): Whether to run the command through the queue or not, ignored if the device was initialized with UseQueue = False
    def setTriggerValues(self, TriggerLevel, TriggerDelay = 0, **kwargs):
        self.sendWithoutResponse("TRIGger:SOURce EXT", **kwargs)
        self.sendWithoutResponse("TRIGger:SLOPe POS", **kwargs)
        self.sendWithoutResponse(f"TRIGger:LEVel {float(TriggerLevel)}", **kwargs)
        self.sendWithoutResponse("TRIGger1:IMPedance 50Ohm", **kwargs)
        self.sendWithoutResponse("TRIGger:FASTasync1 OFF", **kwargs)
        self.sendWithoutResponse(f"TRIGger:DELAYadjust1 {float(TriggerDelay)}", **kwargs)
        self.sendWithoutResponse("AWGControl:BURST 1", **kwargs)
        self.sendWithoutResponse("SYNCclockout:STATe ON", **kwargs)
        self.sendWithoutResponse("RF:AWGControl:SRATe:PREScaler 0", **kwargs)
        self.setMode("BURSt", **kwargs)
    
    # Sets the operating mode
    # Mode (str): The operating mode, either BB or RF
    # UseQueue (bool): Whether to run the command through the queue or not, ignored if the device was initialized with UseQueue = False
    def setOperatingMode(self, Mode, **kwargs):
        if Mode == "BB":
            self.sendWithoutResponse("AWGControl:OPERATINGMode BASEBand", **kwargs)            
            
        elif Mode == "RF":
            self.sendWithoutResponse("AWGControl:OPERATINGMode RF1Carrier", **kwargs)
            
        else:
            raise e.KeywordError("Mode", Mode, ["BB", "RF"])
            
    # Gets the operating mode
    # UseQueue (bool): Whether to run the command through the queue or not, ignored if the device was initialized with UseQueue = False
    def getOperatingMode(self, **kwargs):
        Mode = self.query("AWGControl:OPERATINGMode?", **kwargs)
        
        if Mode == "BASEBand":
            return "BB"
        
        elif Mode == "RF1Carrier":
            return "RF"
        
        else:
            raise e.KeywordError("Mode", Mode, ["BASEBand", "RF1Carrier"])
                    
    # Sets the amplitude for baseband mode
    # Value (float): The value of the amplitude
    # Channel (int): The channel to set it for, None if it should use the default
    # Entry (int): The entry to set it for
    # UseQueue (bool): Whether to run the command through the queue or not, ignored if the device was initialized with UseQueue = False
    # UseQueue (bool): Whether to run the command through the queue or not, ignored if the device was initialized with UseQueue = False
    def setBBAmplitude(self, Value, Channel = None, Entry = 1, **kwargs):
        if Channel is None:
            Channel = self._channel
            
        self.sendWithoutResponse(f"SEQuence:ELEM{int(Entry)}:AMPlitude{int(Channel)} {float(Value)}", **kwargs)
        
    # Sets the offset for baseband mode
    # Value (float): The value of the offset
    # UseQueue (bool): Whether to run the command through the queue or not, ignored if the device was initialized with UseQueue = False
    # Channel (int): The channel to set it for, None if it should use the default
    # Entry (int): The entry to set it for
    # UseQueue (bool): Whether to run the command through the queue or not, ignored if the device was initialized with UseQueue = False
    def setBBOffset(self, Value, Channel = None, Entry = 1, **kwargs):
        if Channel is None:
            Channel = self._channel
            
        self.sendWithoutResponse(f"SEQuence:ELEM{int(Entry)}:OFFset{int(Channel)} {float(Value)}", **kwargs)
        
    # Sets the minimum voltage for baseband mode
    # Value (float): The value of the offset
    # UseQueue (bool): Whether to run the command through the queue or not, ignored if the device was initialized with UseQueue = False
    # Channel (int): The channel to set it for, None if it should use the default
    # Entry (int): The entry to set it for
    # UseQueue (bool): Whether to run the command through the queue or not, ignored if the device was initialized with UseQueue = False
    def setBBMin(self, Value, Channel = None, Entry = 1, **kwargs):
        if Channel is None:
            Channel = self._channel
            
        self.sendWithoutResponse(f"SEQuence:ELEM{int(Entry)}:VOLTage:LOW{int(Channel)} {float(Value)}", **kwargs)

    # Sets the maximum voltage for baseband mode
    # Value (float): The value of the offset
    # UseQueue (bool): Whether to run the command through the queue or not, ignored if the device was initialized with UseQueue = False
    # Channel (int): The channel to set it for, None if it should use the default
    # Entry (int): The entry to set it for
    # UseQueue (bool): Whether to run the command through the queue or not, ignored if the device was initialized with UseQueue = False
    def setBBMax(self, Value, Channel = None, Entry = 1, **kwargs):
        if Channel is None:
            Channel = self._channel
            
        self.sendWithoutResponse(f"SEQuence:ELEM{int(Entry)}:VOLTage:HIGH{int(Channel)} {float(Value)}", **kwargs)
    
        
    # Sets the RF amplitude
    # IValue (float): The value of the I amplitude
    # QValue (float): The value of the Q amplitude
    # Channel (int): The channel to set it for, None if it should use the default
    # Entry (int): The entry to set it for
    # UseQueue (bool): Whether to run the command through the queue or not, ignored if the device was initialized with UseQueue = False
    def setRFAmplitude(self, IValue, QValue, Channel = None, Entry = 1, **kwargs):
        if Channel is None:
            Channel = self._channel
            
        self.sendWithoutResponse(f"RF:SEQuence:ELEM{int(Entry)}:OUTPut{int(Channel)}:AMPlitude1 {float(IValue)}", **kwargs)
        self.sendWithoutResponse(f"RF:SEQuence:ELEM{int(Entry)}:OUTPut{int(Channel)}:AMPlitude2 {float(QValue)}", **kwargs)
    
    # Sets the RF offset
    # IValue (float): The value of the I offset
    # QValue (float): The value of the Q offset
    # Channel (int): The channel to set it for, None if it should use the default
    # Entry (int): The entry to set it for
    # UseQueue (bool): Whether to run the command through the queue or not, ignored if the device was initialized with UseQueue = False
    def setRFOffset(self, IValue, QValue, Channel = None, Entry = 1, **kwargs):
        if Channel is None:
            Channel = self._channel
            
        self.sendWithoutResponse(f"RF:SEQuence:ELEM{int(Entry)}:OUTPut{int(Channel)}:OFFset1 {float(IValue)}", **kwargs)
        self.sendWithoutResponse(f"RF:SEQuence:ELEM{int(Entry)}:OUTPut{int(Channel)}:OFFset2 {float(QValue)}", **kwargs)
    
    # Sets the RF maximum voltage
    # IValue (float): The value of the I max voltage
    # QValue (float): The value of the Q max voltage
    # Channel (int): The channel to set it for, None if it should use the default
    # Entry (int): The entry to set it for
    # UseQueue (bool): Whether to run the command through the queue or not, ignored if the device was initialized with UseQueue = False
    def setRFMax(self, IValue, QValue, Channel = None, Entry = 1, **kwargs):
        if Channel is None:
            Channel = self._channel

        self.sendWithoutResponse(f"RF:SEQuence:ELEM{int(Entry)}:OUTPut{int(Channel)}:VOLTage:HIGH1 {float(IValue)}", **kwargs)
        self.sendWithoutResponse(f"RF:SEQuence:ELEM{int(Entry)}:OUTPut{int(Channel)}:VOLTage:HIGH2 {float(QValue)}", **kwargs)
    
    # Sets the RF minimum voltage
    # IValue (float): The value of the I min voltage
    # QValue (float): The value of the Q min voltage
    # Channel (int): The channel to set it for
    # Entry (int): The entry to set it for, None if it should use the default
    # UseQueue (bool): Whether to run the command through the queue or not, ignored if the device was initialized with UseQueue = False
    def setRFMin(self, IValue, QValue, Channel = None, Entry = 1, **kwargs):
        if Channel is None:
            Channel = self._channel
            
        self.sendWithoutResponse(f"RF:SEQuence:ELEM{int(Entry)}:OUTPut{int(Channel)}:VOLTage:LOW1 {float(IValue)}", **kwargs)
        self.sendWithoutResponse(f"RF:SEQuence:ELEM{int(Entry)}:OUTPut{int(Channel)}:VOLTage:LOW2 {float(QValue)}", **kwargs)
                          
    # Send a waveform to the AWG
    # Waveform (numpy.ndarray of uint16): The waveform to send
    # Name (str): The name of the waveform
    def importWaveform(self, Waveform, Name, **kwargs):
        import numpy as np
        
        # Get the length
        Length = len(Waveform)
        Digits = int(np.log10(Length)) + 1
    
        # Send the waveform
        self.sendWithoutResponse(f"MMEM:DATA \"waveform.bin\",0,#{Digits}{Length}", WriteKwargs = {"WaveformData": Waveform}, **kwargs)

        # Set new waveform
        self.sendWithoutResponse(f"WLIST:WAVEFORM:IMP \"{Name}\",\"waveform.bin\", ANA", **kwargs)

    # Loads an arbitrary waveform for baseband mode
    # Sequence (AWGSequence): The sequence to load
    # UseQueue (bool): Whether to run the command through the queue or not, ignored if the device was initialized with UseQueue = False
    def loadBBSequence(self, Sequence, **kwargs):
        # Make sure the mode is correct
        OperatingMode = self.getOperatingMode(**kwargs)
        if Sequence.mode != "BB":
            raise e.WrongValueError("Sequence.mode", Sequence.mode)

        if OperatingMode != "BB":
            raise e.WrongValueError("OperatingMode", OperatingMode)
            
        Name = f"{Sequence.name}_BB"
            
        # Check if it is not uploaded
        if not Name in self.sequences:
            for Entry, EntrySequence in enumerate(Sequence.sequences):
                for Channel, ChannelSequence in enumerate(EntrySequence):
                    if ChannelSequence is not None:
                        self.importWaveform(ChannelSequence.normWaveform, f"{Name}_CH{Channel + 1}_ENTRY{Entry + 1}", **kwargs)

            self.sequences[Name] = Sequence

        # Set the sequence count
        self.sendWithoutResponse(f"SEQuence:LENGth {len(self._sequences[Name])}", **kwargs)

        # Set waveform to be active
        ActiveChannels = [False] * len[self.sequences[Name].sequences[0]]
        
        for Entry, EntrySequence in enumerate(self.sequences[Name].sequences):
            # Set the loop count
            self.sendWithoutResponse(f"SEQuence:ELEM{Entry + 1}:LOOP:COUNt 1", **kwargs)
            
            for Channel, ChannelSequence in enumerate(EntrySequence):
                if ChannelSequence is not None:
                    ActiveChannels[Channel] = True
                    
                    # Set waveform
                    self.sendWithoutResponse(f"SEQuence:ELEM{Entry + 1}:WAVeform{Channel + 1} \"{Name}_CH{Channel + 1}_ENTRY{Entry + 1}\"", **kwargs)

                    # Set voltage
                    self.setBBMin(ChannelSequence.min, Channel = Channel + 1, Entry = Entry + 1, **kwargs)
                    self.setBBMax(ChannelSequence.max, Channel = Channel + 1, Entry = Entry + 1, **kwargs)

                        
        # Turn on channels
        for Channel, Active in enumerate(ActiveChannels):
            if Active:
                self.on(Channel = Channel + 1, **kwargs)
                
            else:
                self.off(Channel = Channel + 1, **kwargs)            


    # Loads an arbitrary waveform for RF mode
    # Sequence (AWGSingleSequence): The sequence to load
    # UseQueue (bool): Whether to run the command through the queue or not, ignored if the device was initialized with UseQueue = False
    def loadRFSequence(self, Sequence, **kwargs):            
        # Make sure the mode is correct
        OperatingMode = self.getOperatingMode(**kwargs)
        if Sequence.mode != "RF":
            raise e.WrongValueError("Sequence.mode", Sequence.mode)

        if OperatingMode != "RF":
            raise e.WrongValueError("OperatingMode", OperatingMode)
            
        Name = f"{Sequence.name}_RF"
            
        # Check if it is not uploaded
        if not Name in self.sequences:
            for Entry, EntrySequence in enumerate(Sequence.sequences):
                for Channel, ChannelSequence in enumerate(EntrySequence):
                    if ChannelSequence is not None:
                        self.importWaveform(ChannelSequence[0].normWaveform, f"{Name}I_CH{Channel + 1}_ENTRY{Entry + 1}", **kwargs)
                        self.importWaveform(ChannelSequence[1].normWaveform, f"{Name}Q_CH{Channel + 1}_ENTRY{Entry + 1}", **kwargs)
                        
            self.sequences[Name] = Sequence

        # Set the sequence count
        self.sendWithoutResponse(f"SEQuence:LENGth {len(self._sequences[Name])}", **kwargs)

        # Set waveform to be active
        ActiveChannels = [False] * len[self.sequences[Name].sequences[0]]
        
        for Entry, EntrySequence in enumerate(self.sequences[Name].sequences):
            # Set the loop count
            self.sendWithoutResponse(f"SEQuence:ELEM{Entry + 1}:LOOP:COUNt 1", **kwargs)

            Length = 0
            
            for Channel, ChannelSequence in enumerate(EntrySequence):
                if ChannelSequence is not None:
                    ActiveChannels[Channel] = True
                    Length = max(Length, len(ChannelSequence[0].normWaveform), len(ChannelSequence[1].normWaveform))
                    
                    # Set waveform
                    self.sendWithoutResponse(f"RF:SEQuence:ELEM{Entry + 1}:OUTPut{Channel + 1}:WAVeform1 \"{Name}I_CH{Channel + 1}_ENTRY{Entry + 1}\"", **kwargs)
                    self.sendWithoutResponse(f"RF:SEQuence:ELEM{Entry + 1}:OUTPut{Channel + 1}:WAVeform2 \"{Name}Q_CH{Channel + 1}_ENTRY{Entry + 1}\"", **kwargs)

                    # Set voltage
                    self.setRFMin(ChannelSequence[0].min, ChannelSequence[1].min, Channel = Channel + 1, Entry = Entry + 1, **kwargs)
                    self.setRFMax(ChannelSequence[0].max, ChannelSequence[1].max, Channel = Channel + 1, Entry = Entry + 1, **kwargs)
                  
            # Set the length
            self.sendWithoutResponse(f"SEQuence:ELEM{Entry + 1}:LENGth {Length}", **kwargs)
                    
        # Turn on channels
        for Channel, Active in enumerate(ActiveChannels):
            if Active:
                self.on(Channel = Channel + 1, **kwargs)
                
            else:
                self.off(Channel = Channel + 1, **kwargs)
                
        self.currentSequence = Name
                
    # Loads an arbitrary waveform
    # Sequence (AWGSingleSequence): The sequence to load
    # UseQueue (bool): Whether to run the command through the queue or not, ignored if the device was initialized with UseQueue = False
    def loadSequence(self, Sequence, **kwargs):
        if Sequence.mode == "BB":
            self.loadBBSequence(Sequence, **kwargs)
            
        else:
            self.loadRFSequence(Sequence, **kwargs)
                       
    # Removes all waveforms
    # UseQueue (bool): Whether to run the command through the queue or not, ignored if the device was initialized with UseQueue = False
    def reset(self, **kwargs):
        self.sendWithoutResponse("WLISt:WAVeform:DELete ALL", **kwargs)
        self.sequences = dict()
        self.currentSequence = None
        
        for Channel in range(self.channelCount):
            self.off(Channel = Channel + 1)
    
    # Turns a channel on
    # Channel (int): The channel to set it for, None if it should use the default
    # UseQueue (bool): Whether to run the command through the queue or not, ignored if the device was initialized with UseQueue = False
    def on(self, Channel = None, **kwargs):
        if Channel is None:
            Channel = self._channel

        self.sendWithoutResponse(f"OUTPut{int(Channel)}:STATe ON")
    
    # Turns a channel off
    # Channel (int): The channel to set it for, None if it should use the default
    # UseQueue (bool): Whether to run the command through the queue or not, ignored if the device was initialized with UseQueue = False
    def off(self, Channel = None, **kwargs):
        if Channel is None:
            Channel = self._channel

        self.sendWithoutResponse(f"OUTPut{int(Channel)}:STATe OFF")

    # Starts the AWG
    # UseQueue (bool): Whether to run the command through the queue or not, ignored if the device was initialized with UseQueue = False
    def start(self, **kwargs):
        self.runWithoutResponse("AWGControl:RUN", **kwargs)
    
    # Sets the AWG to stop
    # UseQueue (bool): Whether to run the command through the queue or not, ignored if the device was initialized with UseQueue = False
    def stop(self, **kwargs):
        self.runWithoutResponse("AWGControl:STOP", **kwargs)
    
    # Sets the AWG to wait, returns the wait flag
    # UseQueue (bool): Whether to run the command through the queue or not, ignored if the device was initialized with UseQueue = False
    def wait(self, **kwargs):
        return self.query("*WAI", **kwargs)
            