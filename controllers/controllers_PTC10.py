from .. import connections as c
from ..controllers import PID

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
        from .. import functions as f
        
        ResponseKwargs = kwargs.copy()
        ResponseKwargs["UseQueue"] = False
        kwargs["ResponseCheck"] = f.responseCheck.matchValue(float(Value), GetFunction, kwargs = ResponseKwargs)
        self._sendNamedCommand(f"{Parameter}={float(Value)}", **kwargs)
        
    # Get a paramter
    # Param (str): The parameter to get
    # Name (str): The name of the system (EOM, ET1 or ET2 for ColdLab), if None then it uses the self.name
    # UseQueue (bool): True if it should use the command queue    
    def _getParameter(self, Param, **kwargs):
        from .. import functions as f
        
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
        from .. import functions as f
        
        ResponseKwargs = kwargs.copy()
        ResponseKwargs["UseQueue"] = False
        kwargs["ResponseCheck"] = f.responseCheck.matchVar(True, self.status, kwargs = ResponseKwargs)
        self._sendNamedCommand("A.PID.mode=On", **kwargs)
        
    # Stop the PID
    # Name (str): The name of the system (EOM, ET1 or ET2 for ColdLab), if None then it uses the self.name
    # UseQueue (bool): True if it should use the command queue    
    def stop(self, **kwargs):
        from .. import functions as f
        
        ResponseKwargs = kwargs.copy()
        ResponseKwargs["UseQueue"] = False
        kwargs["ResponseCheck"] = f.responseCheck.matchVar(False, self.status, kwargs = ResponseKwargs)
        self._sendNamedCommand("A.off", **kwargs)
        
    # Get the status of the PID, True if it is on, False if it is off, None if it is on Follow
    # Name (str): The name of the system (EOM, ET1 or ET2 for ColdLab), if None then it uses the self.name
    # UseQueue (bool): True if it should use the command queue    
    def status(self, **kwargs):
        from .. import functions as f
        
        kwargs["ResponseCheck"] = f.responseCheck.inList(["Off", "On", "Follow"])
        ReturnString = self._sendNamedCommand("A.PID.mode?", **kwargs)
        
        if ReturnString == "On":
            return True
        
        elif ReturnString == "Off":
            return False
        
        else:
            return None
         