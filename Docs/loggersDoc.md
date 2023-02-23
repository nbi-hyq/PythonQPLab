# Documentation for loggers

This is a number of classes which implements logging

---

# Classes

---

## PIDLogger(Func)

Logs a PID, it will log the time, signal in, setpoint and signal out, and it will plot to plot, one for the input and setpoint and one for the output.

- Func (func): The data retriever function for the PID, it can have any parameter which will be given by DataArgs and DataKwargs in the log method. It must return (SignalIn, SetPoint, SignalOut)

---

### method log(File, MaxTime = 0, Period = 1, MaxShow = 10000, DataArgs = tuple(), DataKwargs = dict(), WhiteSpaceIn = 1, WhiteSpaceOut = 1, Name = None, figsize = (10, 10), Plot = True, KeepFigure = True, Wait = False)

Starts a log of data with live plotting
    
- File (str): The file path for where to save the log
- MaxTime (float): The time in seconds to run the logging, 0 for infinity, must not be negative
- Period (floar): The time in seconds between each measurement, must not be negative
- MaxShow (int): The maximum number of data points to show at once, must be positive
- WhiteSpaceIn (float): The size of the white space at the top and bottom of the signal in plot
- WhiteSpaceOut (float): The size of the white space at the top and bottom of the signal out plot
- Name (str): The name to display on the figures
- figsize (tuple): A tuple of ints define the size of the figure
- Plot (bool): If True then do live plotting
- KeepFigure (bool): If False then it closes the live plotting when done
- Wait (bool): If True then it will wait for the log to finish, if False then it will return immidiatly and return the stop event for the log for which to do .set() to stop the log

If Wait it True then it will return None. If False then it will return the stop event for the log

---

### method killLogs()

Kills all of the logs

---

### property logs (list of threading.Event)

A list of kill events for each active log

---
---