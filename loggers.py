# Allow for multiple logs to be running on multiple threads logging PID input and output
class PIDLogger(object):
    def __init__(self, Func):
        self._f = Func
        self.logs = []
    
    # Starts a log of data with live plotting
    # File (str): The file path for where to save the log
    # MaxTime (float): The time in seconds to run the logging, 0 for infinity, must not be negative
    # Period (floar): The time in seconds between each measurement, must not be negative
    # MaxShow (int): The maximum number of data points to show at once, must be positive
    # WhiteSpaceIn (float): The size of the white space at the top and bottom of the signal in plot
    # WhiteSpaceOut (float): The size of the white space at the top and bottom of the signal out plot
    # Name (str): The name to display on the figures
    # figsize (tuple): A tuple of ints define the size of the figure
    # Plot (bool): If True then do live plotting
    # KeepFigure (bool): If False then it closes the live plotting when done
    # Wait (bool): If True then it will wait for the log to finish, if False then it will return immidiatly and return the stop event for the log for which to do .set() to stop the log
    def log(self, File, MaxTime = 0, Period = 1, MaxShow = 10000, DataArgs = tuple(), DataKwargs = dict(), WhiteSpaceIn = 0.1, WhiteSpaceOut = 0.1, Name = None, figsize = (10, 10), Plot = True, KeepFigure = True, Wait = False):        
        import os
        from datetime import datetime
        import threading as th
        from . import plotting
        
        # Make sure variables have correct types
        File = str(File)
        
        if Name is not None:
            Name = str(Name)
            
        DataArgs = tuple(DataArgs)
        DataKwargs = dict(DataKwargs)
        
        MaxTime = float(MaxTime)
        if MaxTime < 0:
            raise Exception("MaxTime must not be negative")
            
        Period = float(Period)
        if Period < 0:
            raise Exception("Period must not be negative")
            
        MaxShow = int(MaxShow)
        if MaxShow <= 0:
            raise Exception("MaxShow must be positive")
            
        WhiteSpaceIn = float(WhiteSpaceIn)
        WhiteSpaceOut = float(WhiteSpaceOut)
        
        # Find the number of iterations
        if MaxTime == 0:
            MaxTime = 1e9
            
        # Get date and time
        Date = datetime.now().strftime("%Y%m%d")
        Time = datetime.now().strftime("%H%M%S")
            
        # Create the correct file name
        if File is not None:
            SplitFile = os.path.split(File)
            SplitName = SplitFile[1].split(".")
            
            if len(SplitName) < 2:
                SplitName += ["csv"]
    
            if len(SplitName) > 2:
                raise Exception(f"File ({SplitFile[1]}) must only include 1 dot")
            
            BaseFile = f"{SplitFile[0]}\\TempArduino_{Date}_{Time}_{SplitName[0]}"
                
            # Check if file already exists
            if os.path.exists(f"{BaseFile}.{SplitName[1]}"):
                Num = 1
                while os.path.exists(f"{BaseFile}_{Num}.{SplitName[1]}"):
                    Num += 1
                
                File = f"{BaseFile}_{Num}.{SplitName[1]}"
                
            else:
                File = f"{BaseFile}.{SplitName[1]}"
            
        # Create figure
        Plotter = None
        
        if Plot:
            # Get name part of title
            TitleName = ""
            if Name is not None:
                TitleName = f" - {Name}"

            Plotter = plotting.plot(MaxShow, 2, ("-.", "-", "-"), AxID = (0, 0, 1), Colors = ("red", "red", "blue"), Figsize = figsize, Titles = (f"Signal in{TitleName}", f"Signal out{TitleName}"), xLabels = "Time (s)", yLabels = "Signal", Labels = ("SetPoint", "Signal In", "Signal Out"), ShowBuffers = (WhiteSpaceIn, WhiteSpaceOut))
                    
        # If it should not wait then create the stop event
        StopEvent = th.Event()
        self.logs.append(StopEvent)

        # If it should wait
        if Wait:
            return self._log(File, MaxTime = MaxTime, Period = Period, DataArgs = DataArgs, DataKwargs = DataKwargs, Plot = Plotter, KeepFigure = KeepFigure, StopEvent = StopEvent)
        
        # Run the function in a new thread
        th.Thread(target = self._log, args = (File,), kwargs = {"MaxTime": MaxTime, "Period": Period, "DataArgs": DataArgs, "DataKwargs": DataKwargs, "Plot": Plotter, "KeepFigure": KeepFigure, "StopEvent": StopEvent}).start()

        return StopEvent
    
    # Logs data with live plotting
    # File (str): The file path for where to save the log
    # MaxTime (float): The time in seconds to run the logging, 0 for infinity, must not be negative
    # Period (float): The time in seconds between each measurement, must not be negative
    # Plot (plotting.plot): The plot to plot on, None if not plotting
    # KeepFigure (bool): If False then it closes the live plotting when done
    # StopEvent (threading.Event): The event to signal to stop the logging if it is set
    def _log(self, File, **kwargs):
        if File is not None:
            with open(File, "w") as f:
                self.__log(f, **kwargs)
                
        else:
            self.__log(None, **kwargs)
    
    # Logs data with live plotting
    # File (str): The file path for where to save the log
    # MaxTime (float): The time in seconds to run the logging, 0 for infinity, must not be negative
    # Period (float): The time in seconds between each measurement, must not be negative
    # Plot (plotting.plot): The plot to plot on, None if not plotting
    # KeepFigure (bool): If False then it closes the live plotting when done
    # StopEvent (threading.Event): The event to signal to stop the logging if it is set
    def __log(self, File, MaxTime = 0, Period = 1, DataArgs = tuple(), DataKwargs = dict(), Plot = None, KeepFigure = True, StopEvent = None):
        import time
        from . import functions as fu
        
        Count = int(MaxTime / Period)
        
        # Log start time
        StartTime = time.time()
                                    
        # Write header
        if File is not None:
            File.write("Time,SignalIn,SetPoint,SignalOut\n")
                    
        # Run through the loop
        for i in range(Count):
            # Log the values
            NewIn, NewSetPoint, NewOut = self._f(*DataArgs, **DataKwargs)
            NewTime = time.time() - StartTime
            
            # Write to file
            if File is not None:
                File.write(f"{NewTime},{NewIn},{NewSetPoint},{NewOut}\n")
            
            # Plot
            if Plot is not None:
                Plot.update(NewTime, (NewSetPoint, NewIn, NewOut))
            
            # Sleep
            SleepTime = (i + 1) * Period - (time.time() - StartTime)
            
            fu.time.sleep(SleepTime)
                    
            # Stop if flag is set
            if StopEvent is not None and StopEvent.is_set():
                break
                
        # Close figure
        if Plot is not None and not KeepFigure:
            Plot.close()
                    
    # Kills all of the logs
    def killLogs(self):
        for Log in self.logs:
            Log.set()
            
        self.logs = []

