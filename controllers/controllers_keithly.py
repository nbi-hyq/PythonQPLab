from .. import connections as c
from .. import exceptions as e

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
        from .. import functions as f
        
        kwargs["ResponseCheck"] = f.responseCheck.default()
        return self.query(f"print({Parameter})", **kwargs)
    
    # Retrieves a float
    # Parameter (str): The parameter to retrieve
    # UseQueue (bool): True if it should use the command queue    
    def _getValue(self, Parameter, **kwargs):
        from .. import functions as f
        
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
