from .. import connections as c
from .. import exceptions as e

# Controls the time tagger
class swabianTimeTagger(c.external):
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
        from .. import functions as f
        
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
        from .. import functions as f
        
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
