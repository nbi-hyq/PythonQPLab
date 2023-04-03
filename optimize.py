class PIDOptimizer:
    def __init__(self, PID, Logger, MaxOutput):
        self._PID = PID
        self._logger = Logger
        self._max = MaxOutput
        
    def scan(self, Path, PreTime, AmbientTime, HeatTime, CoolTime, Period = 1):
        from .. import functions as f
        
        Time = f.time.getCurrentTime()
        
        # Log
        f.time.sleep(PreTime)
        
        # Stabilize to ambient temperature
        self._PID.stop()
        MeanOutput = self._PID.getOutputSignal()
        self._PID.setOutputSignal(MeanOutput)
        
        Name = f"{Path}_{Time}_Vm={self._max}_V0={MeanOutput}"
        
        # Measure
        self._logger.log(f"{Name}_a.csv", MaxTime = AmbientTime, Period = Period, KeepFigure = False, Wait = True)
        
        # Start heating
        self._PID.setOutputSignal(self._max)
        self.log(f"{Name}_h.csv", MaxTime = HeatTime, Period = Period, KeepFigure = False, Wait = True)
        
        # stop heating
        self._PID.setOutputSignal(MeanOutput)
        self.log(f"{Name}_c.csv", MaxTime = CoolTime, Period = Period, KeepFigure = False, Wait = True)
        
        