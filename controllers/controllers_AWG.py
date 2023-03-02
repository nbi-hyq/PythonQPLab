from .. import connections as c
from .. import exceptions as e

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
    def __init__(self, IP, *args, DefaultChannel = 1, TriggerLevel = 0.4, TriggerDelay = 0, MaxSampleFrequency = 12.32, ChannelCount = 4, OperatingMode = "RF", **kwargs):
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
        self.setTriggerValues(TriggerLevel, TriggerDelay = TriggerDelay)
        self.setOperatingMode(OperatingMode)
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
      