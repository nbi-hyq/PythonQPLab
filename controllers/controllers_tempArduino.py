import connections as c
from controllers import PID

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
        import functions as f
        
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
        import functions as f
        
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
