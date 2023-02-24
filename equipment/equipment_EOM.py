from .. import exceptions as e
from ..equipment import device, powerControl

# A minimizer for the EOM
class EOM(device):
    # PowerControl (powerControl): The power control unit connected to the EOM
    # TimeTagger (controllers.timeTagger): The time tagger object
    # DACController (controllers.DAC): The DAC object
    # DACChannel (int): The DAC channel
    # VoltageGuess (float): The initial guess for the optimal voltage
    # ScanRange (float): The range of each voltage scan
    # ScanPoints (int): The number of measurement points in each scan
    # IntegrationTime (float): The integration time per point
    # MaxAttempts (int): The maximum number of attempts to minimize the EOM
    # Gate (2-tuple of float): The gate for use to get time tagger counts
    # InitialPause (float): The time to pause at the beginning of each tagger scan
    # RepetitionCount (int): The number of measurement points to get for each powermeter measurement
    # ScanPause (float): The time to pause between each measurement in a scan
    # Figsize (dict): The size of the figure
    # ShowBuffer (float): The white space buffer in the plot in percentage
    # DeviceName (str): The name of the device
    # ID (str): The ID name for the device, only used for displaying infomation
    def __init__(self, PowerControl, TimeTagger, DACController, DACChannel, *args, VoltageGuess = 3.4, ScanRange = 4 / 5, ScanPoints = 20, IntegrationTime = 0.1, RepetitionCount = 5, MaxAttempts = 100, Gate = None, InitialPause = 0.3, ScanPause = 0.1, Figsize = (8, 8), ShowBuffer = 0.1, **kwargs):
        from .. import controllers as c
        from .. import plotting
        
        if not "DeviceName" in kwargs:
            kwargs["DeviceName"] = "EOM"
            
        super().__init__(*args, **kwargs)
        
        if not isinstance(PowerControl, powerControl):
            raise e.TypeDefError("Powermeter", PowerControl, powerControl)

        if not isinstance(TimeTagger, c.timeTagger):
            raise e.TypeDefError("TimeTagger", TimeTagger, c.timeTagger)
            
        if not isinstance(DACController, c.DAC):
            raise e.TypeDefError("DACController", DACController, c.DAC)
            
        self._powerControl = PowerControl
        self._timeTagger = TimeTagger
        self._timeTaggerChannel = 1
        self._DAC = DACController
        self._channel = int(DACChannel)
        
        # Setup figure
        self._maxAttempts = int(MaxAttempts)
        self._voltageGuess = float(VoltageGuess)
        self._scanRange = float(ScanRange)
        self._scanPoints = int(ScanPoints)
        self._intTime = float(IntegrationTime)
        self._repCount = int(RepetitionCount)
        self._initPause = float(InitialPause)
        self._scanPause = float(ScanPause)
        self._gate = Gate
        
        self._plot = plotting.plot(self._scanPoints, 1, "o", Colors = "blue", Labels = "Data", Figsize = Figsize, Titles = "Minimizing EOM power", xLabels = "Voltage", yLabels = "Power", ShowBuffers = ShowBuffer)
        
    def _close(self):
        if self._plot is not None:
            self._plot.close()
            
        super()._close()
        
    # Sets the voltage for the EOM
    # Voltage (float): The voltage to set
    # UseQueue (bool): Whether to run the command through the queue or not, ignored if the device was initialized with UseQueue = False
    def setVoltage(self, Voltage, **kwargs):
        self._DAC.setVoltage(Voltage, self._channel, **kwargs)
            
    # Minimize the laser through the EOM
    # MeasureFunc (callable): The function to measure the power
    # InitFunc (callable): The function to run before starting
    # ExitFunc (callable): The function to run after it is done
    # UseQueue (bool): Whether to run the command through the queue or not, ignored if the device was initialized with UseQueue = False
    def minimize(self, MeasureFunc, InitFunc = None, ExitFunc = None, **kwargs):
        import numpy as np
        from .. import plotting
        from .. import functions as f
                
        # Run initialization function
        if InitFunc is not None:
            InitFunc(**kwargs)
            
        # Set state to DC
        TimeBanditState = self._powerControl.timeBanditChannel.getState()
        self._powerControl.timeBanditChannel.setDC(**kwargs)
                
        # Start minimizing
        Success = False
        BestVoltage = self._voltageGuess
        
        for _ in range(self._maxAttempts):            
            # Start plotting
            self._plot.reset()

            # Get the voltages to scan
            VoltageList = np.linspace(BestVoltage - self._scanRange / 2, BestVoltage + self._scanRange / 2, self._scanPoints)

            # Create array for measurements
            PowerDataMean = np.empty(self._scanPoints, dtype = float)
            PowerDataStd = np.empty(self._scanPoints, dtype = float)
            
            # Go to starting voltage and wait
            self.setVoltage(VoltageList[0], **kwargs)
            f.time.sleep(self._initPause)
            
            # Get measurements
            for i, Voltage in enumerate(VoltageList):
                # Set voltage and pause
                self._DAC.setVoltage(Voltage, self._channel, **kwargs)
                f.time.sleep(self._scanPause)
                
                # Measure
                PowerDataMean[i], PowerDataStd[i] = MeasureFunc(**kwargs)

                # Plot it
                self._plot.update(Voltage, PowerDataMean[i])
                            
            # Create voltage matrix
            PolyVar = np.polyfit(VoltageList, PowerDataMean, 2, w = 1 / PowerDataStd)
            NewBestVoltage = -PolyVar[1] / (2 * PolyVar[0])

            # Plot it
            x = np.linspace(np.min(VoltageList), np.max(VoltageList), 1000)
            self._plot.axes[0].plot(x, PolyVar[2] + PolyVar[1] * x + PolyVar[0] * x ** 2, "-", color = "Red", label = "Fit")
            plotting.livePlot.update(self._plot)
            
            # Determine if it was good enough
            OldBestVoltage = BestVoltage
            BestVoltage = NewBestVoltage
            
            if abs(BestVoltage - OldBestVoltage) < self._scanRange / 4:
                Success = True
                break
            
        # Run exit function
        if ExitFunc is not None:
            ExitFunc(**kwargs)
            
        # Set time bandit state back
        self._powerControl.timeBanditChannel.applyState(TimeBanditState)
        
        # Make sure that is has been minimized
        if not Success:
            raise e.MinimizeError(self.deviceName, self)
            
        # Set best voltage
        self._DAC.setVoltage(BestVoltage, self._channel, **kwargs)
            
        # Update guess
        self._voltageGuess = BestVoltage
        
        return BestVoltage 
    
    # Initialization function for power minimization
    # UseQueue (bool): Whether to run the command through the queue or not, ignored if the device was initialized with UseQueue = False
    def _powerInit(self, **kwargs):
        # Get old data
        self._locking = self._powerControl.isLocking(**kwargs)
        
        if self._locking:
            self._lockPower = self._powerControl.getSetPower()
            
        else:
            self._oldSetPoint = self._powerControl.PID.getSetPoint(**kwargs)
            
        # Stop PID
        self._powerControl.stop(**kwargs)
        self._powerControl.setAutoRange(True, **kwargs)
        
    # Finalizer function for power minimization
    # UseQueue (bool): Whether to run the command through the queue or not, ignored if the device was initialized with UseQueue = False
    def _powerExit(self, **kwargs):
        # Start PID
        if self._locking:
            self._powerControl.setPower(self._lockPower, **kwargs)
            
        else:
            self._powerControl.PID.setSetPoint(self._oldSetPoint, **kwargs)
        
    # Measure function for power minimization
    # UseQueue (bool): Whether to run the command through the queue or not, ignored if the device was initialized with UseQueue = False
    def _powerMeasure(self, **kwargs):
        import numpy as np
        
        Power = self._powerControl.getPowerMulti(self._repCount)
        Filter = np.isfinite(Power)
        Power = Power[Filter]
        return np.mean(Power), np.std(Power, ddof = 1)
        
    # Minimize the power of a power meter
    # UseQueue (bool): Whether to run the command through the queue or not, ignored if the device was initialized with UseQueue = False
    def minimizePower(self, **kwargs):
        return self.minimize(self._powerMeasure, InitFunc = self._powerInit, ExitFunc = self._powerExit, **kwargs)
    
    # Measure function for power minimization
    # UseQueue (bool): Whether to run the command through the queue or not, ignored if the device was initialized with UseQueue = False
    def _countsMeasure(self, **kwargs):
        import numpy as np
        
        Counts = self._timeTagger.getGatedCount(Channel = self._timeTaggerChannel, IntegrationTime = self._intTime, Gates = self._gate, **kwargs)
        return float(Counts), np.sqrt(float(Counts))
    
    # Minimize the counts of a time tagger
    # Channel (int): The channel to get data from
    # UseQueue (bool): Whether to run the command through the queue or not, ignored if the device was initialized with UseQueue = False
    def minimizeCounts(self, Channel, **kwargs):
        self._timeTaggerChannel = int(Channel)
        return self.minimize(self._countsMeasure, **kwargs)