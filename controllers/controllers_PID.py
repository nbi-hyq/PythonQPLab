from .. import exceptions as e

# Used to control a PID
class PID:
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
        