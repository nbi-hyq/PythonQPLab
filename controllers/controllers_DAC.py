from .. import connections as c
from .. import exceptions as e

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
