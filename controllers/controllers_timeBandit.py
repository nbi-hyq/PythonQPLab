from .. import connections as c
from .. import exceptions as e

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
    def __init__(self, FPGA, Channel, MemoryOffset, PhaseMemoryOffset, TimeCalibration, PhaseCalibration, *args, **kwargs):
        import numpy as np
        
        kwargs["ClockPartition"] = 24
        kwargs["ModeMemoryOffset"] = 32
        kwargs["MaxLength"] = 8

        super().__init__(FPGA, Channel, MemoryOffset, *args, **kwargs)
        
        self._phaseMemoryOffset = int(PhaseMemoryOffset)
        self._phaseCalibration = np.array(PhaseCalibration, dtype = int)
        self._timeCalibration = np.array(TimeCalibration, dtype = int)
        self.stopCalibration()
        
    # Updates a single pulse
    # Start (float): The start time in clock cycles
    # Stop (float): The stop time in clock cycles
    # i (int): The pulse ID
    # UseQueue (bool): Whether to run the command through the queue or not, ignored if the device was initialized with UseQueue = False
    def _update(self, Start, Stop, i, **kwargs):
        # Get the pulse information bits
        if self._calibrationMode:
            UseStart = (int(Start) - 1) % (self.FPGA.getSequenceLength() * self.FPGA.getClocksPerBase())
            UseStop = (int(Stop) - 1) % (self.FPGA.getSequenceLength() * self.FPGA.getClocksPerBase())
            
        else:
            UseStart = (int(Start) - 1 - self._timeCalibration[i, 0]) % (self.FPGA.getSequenceLength() * self.FPGA.getClocksPerBase())
            UseStop = (int(Stop) - 1 - self._timeCalibration[i, 1]) % (self.FPGA.getSequenceLength() * self.FPGA.getClocksPerBase())
        
        # Update memory
        self.FPGA.updateMemory2(self._memoryOffset + 4 * i, UseStart, **kwargs)
        self.FPGA.updateMemory2(self._memoryOffset + 4 * i + 2, UseStop, **kwargs)
                        
        # Find phases
        if self._calibrationMode:
            PhaseStart = int((Start % 1) * 256)
            PhaseStop = int((Stop % 1) * 256)
            
        else:
            PhaseStart = self._phaseCalibration[i, int(Start) % self.FPGA.getClocksPerBase(), 0] + int((Start % self.FPGA.getClocksPerBase()) * self.clockPartition)
            PhaseStop = self._phaseCalibration[i, int(Stop) % self.FPGA.getClocksPerBase(), 1] + int((Stop % self.FPGA.getClocksPerBase()) * self.clockPartition)

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
    # TimeCalibration (8x2 numpy.ndarray of int): The time calibration data
    # PhaseCalibration (8x4x2 numpy.ndarray of int): The phase calibration data
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
    def __init__(self, *args, TimeCalibration, PhaseCalibration, Channel = 1, ClockFrequency = 50e6, ClocksPerBase = 4, **kwargs):
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
        self.CH[0] = FPGAChannelPhasedPulse(self, 0, 24, 8, TimeCalibration, PhaseCalibration)
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
        from .. import functions as f
        
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
        from .. import functions as f
        
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
        