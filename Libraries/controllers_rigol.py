import connections as c
import exceptions as e

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
