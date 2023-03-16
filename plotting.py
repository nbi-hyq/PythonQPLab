import matplotlib
matplotlib.use("Qt5Agg")

# Sets up an ax to allow zooming in live plotting
# Ax (matplotlib.Axes): The ax to set up
def axSetup(Ax):
    Ax._baseView = Ax._get_view()
    Ax._currentView = Ax._baseView
    
# Updates the view of an ax, only updates it if Force is True or there is no zoom
# Ax (matplotlib.Axes): The ax to update
# Force (bool): If True then it will wlays update
def axUpdate(Ax, Force = False):
    if Force or Ax._get_view() == Ax._baseView:
        Ax._set_view(Ax._currentView)
        Ax._baseView = Ax._currentView
        
# Sets the limits of the x-axis without changing user zoom
# Ax (matplotlib.Axes): The ax to change limits for
# xMin (float): The minimum x value
# xMax (float): The maximum x value
def axSetXLim(Ax, xMin, xMax):
    Ax._currentView = (xMin, xMax, Ax._currentView[2], Ax._currentView[3])
    axUpdate(Ax)

# Sets the limits of the y-axis without changing user zoom
# Ax (matplotlib.Axes): The ax to change limits for
# yMin (float): The minimum y value
# yMax (float): The maximum y value
def axSetYLim(Ax, yMin, yMax):
    Ax._currentView = (Ax._currentView[0], Ax._currentView[1], yMin, yMax)
    axUpdate(Ax)

# A class to implement live plotting, it must be subclassed and the update function must be expanded
class livePlot:
    # Fig (matplotlib.Figure): The figure of this plot
    # Axes (list of matplotlib.Axes): The list of axes used in this plot
    def __init__(self, Fig, Axes, *args, InitArgs = tuple(), InitKwargs = dict(), **kwargs):
        super().__init__(*args, **kwargs)
                
        # Save figure and axes
        self.fig = Fig
        self.axes = Axes
        
        # Add callback
        self.fig.canvas.toolbar.actions()[0].triggered.connect(self.home)
        
        # Set up the axes
        for Ax in self.axes:
            axSetup(Ax)
            
        # Initialize
        self._initArgs = tuple(InitArgs)
        self._initKwargs = dict(InitKwargs)
        
        self._init(*self._initArgs, **self._initKwargs)
            
    # Initializes the plot
    def _init(self):
        pass
            
    # Homes the figure, may need to be called at the end of initialization
    def home(self):
        # Go through each ax and update view
        for Ax in self.axes:
            axUpdate(Ax, Force = True)
        
    # Updates the plot with new values
    def update(self):
        self.fig.canvas.draw()
        self.fig.canvas.flush_events()
        
    # Closes the figure
    def close(self):
        import matplotlib.pyplot as plt
        plt.close(self.fig)
        
    # Pauses while allowing to still use the plot
    # Time (float): The time to pause
    def pause(self, Time):
        from . import functions as f
        f.time.sleep(Time)
        
    # Resets the plot to the inital state
    def reset(self):
        for Ax in self.axes:
            Ax.clear()
            axSetXLim(Ax, 0, 1)
            axSetYLim(Ax, 0, 1)
            axUpdate(Ax, Force = True)
            
        self._init(*self._initArgs, **self._initKwargs)

# Live plotting for a histogram with gate implementation
class histogram(livePlot):
    # xValues (numpy.ndarray of float): The x values for the bins of the histogram
    # GateCount (int): The number of gate plots, this can also be for calculated values like mean ect.
    # Gates (list of 2-tuple of float): A list of the gates to draw onto the histogram
    # History (int): The number of points to keep in the backlog for the gates
    # GateShowBuffer (float): The percentage of the gate plots to keep as white space at the buttom and top
    # BaseSize (int): The base size of the window (size per row of plots)
    # GatesPerRow (int): The number of gate plots to plot on a single row
    # BackgroundMode (str): The background mode to use, must be one of "off": Do not use background, "on": Plot background measurements, "subtract": Evaluate the background subtracted signal, this also uses "on"
    # Title (str): The title of the histogram
    # xLabel (str): The label on the x-axis of the histogram
    # yLabel (str): The label on the y-axis of the histogram
    # GateTitles (list of str): The name of each gate, if not specified then it will only write the number
    # GateXLabels (list of str): The x labels for each of the gates
    # GateYLabels (list of str): The y labels for each of the gates
    # GatePrecision (list of int): The number of digits to show for each of the gate values
    # GateFontSize (int): The size of the gate titles
    def __init__(self, xValues, *args, GateCount = 0, Gates = [], History = 10, GateShowBuffer = 0.1, BaseSize = (8, 4), GatesPerRow = 2, BackgroundMode = "off", Title = "Histogram", xLabel = "Time (ns)", yLabel = "Counts", GateTitles = None, GateXLabels = None, GateYLabels = None, GatePrecision = None, GateFontSize = 40, **kwargs):
        import numpy as np
        import matplotlib.pyplot as plt
        from . import exceptions as e

        BackgroundMode = str(BackgroundMode).lower()
        
        if not BackgroundMode in ["on", "off", "subtract"]:
            raise e.KeywordError("BackgroundMode", BackgroundMode, Valid = ["on", "off", "subtract"])
                
        # Create the layout
        RowCount = int(np.ceil(GateCount / GatesPerRow))
        Layout = [["Histogram"] * GatesPerRow] + [[f"Gate{m}" for m in range(GatesPerRow * n, GatesPerRow * (n + 1))] for n in range(RowCount)]
                
        # Create plot
        Fig, Axes = plt.subplot_mosaic(Layout, figsize = (BaseSize[0], BaseSize[1] * (RowCount + 1)), gridspec_kw = {"height_ratios": [1] + [0.5] * RowCount})
        
        self._axHist = Axes["Histogram"]
        self._axGates = [Axes[f"Gate{i}"] for i in range(GateCount)]

        # Setup titles, gates and labels
        if GateTitles is None:
            GateTitles = [""] * GateCount
            
        else:
            GateTitles = [f"{Title}: " for Title in GateTitles]
            
        if GatePrecision is None:
            GatePrecision = [3] * GateCount

        if GateXLabels is None:
            GateXLabels = ["Iteration"] * GateCount

        if GateYLabels is None:
            GateYLabels = ["Counts"] * GateCount
                    
        self._gateTitles = GateTitles
        self._gatePrec = GatePrecision
        self._fontSize = GateFontSize
        
        self._maxValueCount = int(History)
        self._gateX = np.zeros(History)
        self._gateBuffer = float(GateShowBuffer)
        
        # Initialize the plots
        InitArgs = (xValues,)
        InitKwargs = {"GateCount": GateCount, "Gates": Gates, "History": History, "BackgroundMode": BackgroundMode, "Title": Title, "xLabel": xLabel, "yLabel": yLabel, "GateXLabels": GateXLabels, "GateYLabels": GateYLabels}

        super().__init__(Fig, [self._axHist] + self._axGates, *args, InitArgs = InitArgs, InitKwargs = InitKwargs, **kwargs)

    # Initializes the plot
    def _init(self, xValues, GateCount = 0, Gates = [], History = 10, BackgroundMode = "off", Title = "Histogram", xLabel = "Time (ns)", yLabel = "Counts", GateXLabels = None, GateYLabels = None):
        import numpy as np

        self._showValues = 0

        # Plot the histogram
        self._lineHist, = self._axHist.plot(xValues, np.zeros_like(xValues), "-", color = "blue")
        self._lineHistBack = None
        if BackgroundMode in ["on", "subtract"]:
            self._lineHistBack, = self._axHist.plot(xValues, np.zeros_like(xValues), "-", color = "red")
        self._lineHistSub = None
        if BackgroundMode == "subtract":
            self._lineHistSub, = self._axHist.plot(xValues, np.zeros_like(xValues), "-", color = "yellow")
        
        self._histBackValues = np.zeros_like(xValues)
        
        # Format histogram
        axSetYLim(self._axHist, -1, 1)
        axSetXLim(self._axHist, np.min(xValues), np.max(xValues))
        self._histYMax = 0
        self._axHist.set_title(Title)
        self._axHist.set_xlabel(xLabel)
        self._axHist.set_ylabel(yLabel)

        # Plot gates
        self._gateLines = [self._axGates[i].plot(np.zeros(History), np.zeros(History), "-", color = "blue")[0] for i in range(GateCount)]
        self._gateLinesSub = [None] * GateCount
        if BackgroundMode == "subtract":
            self._gateLinesSub = [self._axGates[i].plot(np.zeros(History), np.zeros(History), "-", color = "yellow")[0] for i in range(GateCount)]
        
        self._gateValues = [np.zeros(History) for _ in range(GateCount)]
        self._gateValuesBack = None
        if BackgroundMode in ["on", "subtract"]:
            self._gateValuesBack = [np.zeros(History) for _ in range(GateCount)]
        self._gateValuesSub = None
        if BackgroundMode == "subtract":
            self._gateValuesSub = [np.zeros(History) for _ in range(GateCount)]
        
        # Plot them
        for Gate in Gates:
            self._axHist.axvline(x = Gate[0], color = "green")
            self._axHist.axvline(x = Gate[1], color = "green")
            self._axHist.hlines(y = -1, xmin = Gate[0], xmax = Gate[1], color = "green")

        for Ax, xLabel, yLabel, Title in zip(self._axGates, GateXLabels, GateYLabels, self._gateTitles):
            Ax.set_xlabel(xLabel)
            Ax.set_ylabel(yLabel)
            Ax.set_title(f"{Title}0", fontsize = self._fontSize)
            
        self.fig.tight_layout()
        
        self.home()
        
    # Updates the plot with new values
    # Bins (numpy.ndarray): The values for each of the bins in the histogram
    # GateValues (list): A list of the values for each of the gates
    # BinsBackground (numpy.ndarray): The background values for each of the bins, if not given then it will use the previous value, should only be given if background mode is not "off"
    # GateValuesBackground (list): A list of the background values for each of the gates if not given then it will use the previous value, should only be given if background mode is not "off"
    def update(self, Bins, GateValues = [], BinsBackground = None, GateValuesBackground = None):
        import numpy as np

        if GateValuesBackground is None:
            GateValuesBackground = [None] * len(GateValues)
        
        # Update the histogram
        self._lineHist.set_ydata(Bins)
        if BinsBackground is not None and self._lineHistBack is not None:
            self._lineHistBack.set_ydata(BinsBackground)
            self._histBackValues = BinsBackground
        if self._lineHistSub is not None:
            self._lineHistSub.set_ydata(Bins - self._histBackValues)

        self._histYMax = max(self._histYMax, np.max(Bins))
        if BinsBackground is not None and self._lineHistBack is not None:
            self._histYMax = max(self._histYMax, np.max(BinsBackground))
        if self._lineHistSub is not None:
            self._histYMax = max(self._histYMax, np.max(Bins - self._histBackValues))
        
        axSetYLim(self._axHist, -1, self._histYMax + 1)
        
        # Update gates
        if len(self._axGates) > 0:
            if self._showValues < self._maxValueCount:
                self._showValues += 1
                
            self._gateX = np.roll(self._gateX, -1)
            self._gateX[-1] = self._gateX[-2] + 1

            for i, (Ax, Line, LineSub, Values, ValuesBack, ValuesSub, NewValue, NewValueBack, Title, Prec) in enumerate(zip(self._axGates, self._gateLines, self._gateLinesSub, self._gateValues, self._gateValuesBack, self._gateValuesSub, GateValues, GateValuesBackground, self._gateTitles, self._gatePrec)):
                # Add new value
                Values = np.roll(Values, -1)
                self._gateValues[i] = Values
                Values[-1] = NewValue
                if ValuesBack is not None:
                    ValuesBack = np.roll(ValuesBack, -1)
                    self._gateValuesBack[i] = ValuesBack
                    if NewValueBack is not None:
                        ValuesBack[-1] = NewValueBack  
                    else:
                        ValuesBack[-1] = ValuesBack[-2]  
                if ValuesSub is not None:
                    ValuesSub = np.roll(ValuesSub, -1)
                    self._gateValuesSub[i] = ValuesSub
                    ValuesSub[-1] = Values[-1] - ValuesBack[-1]
                
                # Update title
                PutTitle = f"{Title}{NewValue:.{Prec}g}"
                if ValuesBack is not None:
                    STN = (Values[-1] - ValuesBack[-1]) / max(1, ValuesBack[-1])
                    PutTitle = f"{PutTitle} ({STN:.2g})"
                Ax.set_title(PutTitle, fontsize = self._fontSize)
                
                # Update plot
                if self._showValues > 1:
                    Line.set_xdata(self._gateX[-self._showValues:])
                    if ValuesSub is not None:
                        LineSub.set_xdata(self._gateX[-self._showValues:])
                    axSetXLim(Ax, self._gateX[-self._showValues], self._gateX[-1])
    
                    Line.set_ydata(Values[-self._showValues:])
                    if ValuesSub is not None:
                        LineSub.set_ydata(ValuesSub[-self._showValues:])  
                    Min = np.min((Values[-self._showValues:]))
                    Max = np.max((Values[-self._showValues:]))
                    if ValuesSub is not None:
                        Min = min(Min, np.min((ValuesSub[-self._showValues:])))
                        Max = max(Max, np.max((ValuesSub[-self._showValues:])))
                    BuffSize = (Max - Min) * self._gateBuffer
                    if BuffSize == 0:
                        BuffSize = 1
                    axSetYLim(Ax, Min - BuffSize, Max + BuffSize)
            
        # Update canvas
        super().update()
        
        
# Creates a live plot for normal data that is gathered one point at the time
class plot(livePlot):
    # MaxSize (int): The max number of data points to show, if more is given then it will overwrite old values
    # AxCount (int): The number of axes to plot
    # Shapes (list of str): The shapes of each of the plots as a matplotlib string ("-" or "o" and so on)
    # AxID (list of int): A list of all ID's of the axes to do the plots in
    # Colors (list of str): The color strings for each plot
    # BackgroundModes (list of str): List of all the background modes to use for each plot, must be one of "off": No background is used, "on": The background is also plotted, "subtract": The background and background subtracted data are both plotted, "subtract_noback": Plots data and background subtracted data, "subtract_only": Only plots the background subtracted data
    # Labels (list of str): The labels for each of the plots, will append "background" or "subtracted" to it when needed
    # Figsize (2-tuple of float): The size of the figure
    # Titles (list of str/str): The titles of the figure, if only one is given then it will be the same for each plot
    # xLabels (list of str/str): The labels of the x-axis, if only one is given then it will be the same for each plot
    # yLabels (list of str/str): The labels of the y-axis, if only one is given then it will be the same for each plot
    # ShowBuffers (list of float/float): The white space buffer at the top and buttom of each plot in percentage, if only one is given then it will be the same for each plot
    def __init__(self, MaxSize, AxCount, Shapes, *args, AxID = None, Colors = None, BackgroundModes = None, Labels = None, Figsize = (8, 8), Titles = "", xLabels = "", yLabels = "", ShowBuffers = 0.1, **kwargs):
        import matplotlib.pyplot as plt
        import numpy as np

        AxCount = int(AxCount)
                
        # Get the number of plots and the settings            
        if isinstance(Shapes, str):
            Shapes = (Shapes,)
            
            if AxID is not None:
                AxID = (AxID,)
                
            if Colors is not None:
                Colors = (Colors,)
                
            if BackgroundModes is not None:
                BackgroundModes = (BackgroundModes,)
                
            if Labels is not None:
                Labels = (Labels,)
                
        if AxID is None:
            AxID = (0,) * len(Shapes)
            
        if Colors is None:
            Colors = (None,) * len(Shapes)
            
        if BackgroundModes is None:
            BackgroundModes = ("off",) * len(Shapes)
            
        if Labels is None:
            Labels = (None,) * len(Shapes)
            
        if isinstance(Titles, str):
            Titles = (Titles,) * AxCount
            
        if isinstance(xLabels, str):
            xLabels = (xLabels,) * AxCount
            
        if isinstance(yLabels, str):
            yLabels = (yLabels,) * AxCount
            
        if isinstance(ShowBuffers, float):
            ShowBuffers = (ShowBuffers,) * AxCount
                    
        # Create figure
        Fig, Axes = plt.subplots(AxCount, figsize = Figsize)
        if AxCount == 1:
            Axes = (Axes,)
        self._showBuffers = ShowBuffers
        self._axCount = AxCount

        self._maxSize = max(1, int(MaxSize))
        self._x = np.zeros(self._maxSize)
        
        InitArgs = (Shapes,)
        InitKwargs = {"AxID": AxID, "Colors": Colors, "BackgroundModes": BackgroundModes, "Labels": Labels, "Titles": Titles, "xLabels": xLabels, "yLabels": yLabels}
        
        super().__init__(Fig, Axes, *args, InitArgs = InitArgs, InitKwargs = InitKwargs, **kwargs)
        
    # Initializes the plot
    def _init(self, Shapes, AxID = None, Colors = None, BackgroundModes = None, Labels = None, Titles = "", xLabels = "", yLabels = ""):
        from . import exceptions as e
        import numpy as np

        # Set the ax ID
        self._ID = AxID

        # Make sure the size is not too low
        self._pos = 0
        
        # Create plots and save arrays
        self._values = []
        self._valuesBack = []
        self._valuesSub = []
        
        self._lines = []
        self._linesBack = []
        self._linesSub = []
        
        self._lastBackground = [0] * len(Shapes)
        self._lastBackgroundError = [0] * len(Shapes)
        
        for Shape, ID, Color, BackgroundMode, Label in zip(Shapes, AxID, Colors, BackgroundModes, Labels):
            # Make sure background mode is correct
            BackgroundMode = str(BackgroundMode).lower()
            
            if not BackgroundMode in ["on", "off", "subtract", "subtract_only", "subtract_noback"]:
                raise e.KeywordError("BackgroundMode", BackgroundMode, Valid = ["on", "off", "subtract", "subtract_only", "subtract_noback"])

            # Turn color into correct shape
            if isinstance(Color, str) or Color is None:
                Color = (Color,) * 3

            if BackgroundMode != "subtract_only":
                self._values.append(np.zeros(self._maxSize))
                NewLine, = self.axes[ID].plot(self._x, self._values[-1], Shape, color = Color[0], label = Label)                
                self._lines.append(NewLine)

            else:
                self._values.append(None)
                self._lines.append(None)
            
            # Background values
            if BackgroundMode in ["on", "subtract"]:
                self._valuesBack.append(np.zeros(self._maxSize))                
                NewLine, = self.axes[ID].plot(self._x, self._valuesBack[-1], Shape, color = Color[1], label = f"{Label} background")                
                self._linesBack.append(NewLine)

            else:
                self._linesBack.append(None)
                self._valuesBack.append(None)
                
            # Subtracted values
            if BackgroundMode in ["subtract", "subtract_only", "subtract_noback"]:
                self._valuesSub.append(np.zeros(self._maxSize))
                NewLine, = self.axes[ID].plot(self._x, self._valuesSub[-1], Shape, color = Color[2], label = f"{Label} subtracted")
                self._linesSub.append(NewLine)

            else:
                self._linesSub.append(None)
                self._valuesSub.append(None)

        # Add labels
        for Ax, Title, xLabel, yLabel in zip(self.axes, Titles, xLabels, yLabels):
            Ax.set_title(Title)
            Ax.set_xlabel(xLabel)
            Ax.set_ylabel(yLabel)
            Ax.legend()
        
        self.fig.tight_layout()
        
        self.home()
                
    # Updates the plot with new values
    # x (float): The x value of the new points
    # Values (list of float): The values for each of the plots
    # BackgroundValues (list of float): The values of the background for each plot, None if not needed
    def update(self, x, Values, BackgroundValues = None):
        import numbers
        import numpy as np
        
        # Make sure they are tuples
        if isinstance(Values, numbers.Number):
            Values = (Values,)
            BackgroundValues = (BackgroundValues,)
            
        if BackgroundValues is None:
            BackgroundValues = (None,) * len(Values)
        
        # Roll arrays
        self._x = np.roll(self._x, -1)
        
        for i in range(len(self._values)):
            for List in [self._values, self._valuesBack, self._valuesSub]:
                if List[i] is not None:
                    List[i] = np.roll(List[i], -1)
    
        # Get latest background values
        for i, Value in enumerate(BackgroundValues):
            if Value is not None:
                self._lastBackground[i] = Value
                
        # Calculate subtracted values
        SubList = []
        
        for Value, ValueBack in zip(Values, self._lastBackground):
            if Value is not None:
                SubList.append(Value - ValueBack)
    
        # Add the values
        self._x[-1] = x
        
        for Arrays, List in zip([self._values, self._valuesBack, self._valuesSub], [Values, self._lastBackground, SubList]):
            for Array, Value in zip(Arrays, List):
                if Array is not None:
                    Array[-1] = Value
        
        if self._pos < self._maxSize:
            self._pos += 1
        
        # Update plots
        if self._pos > 1:
            MinValues = [None] * self._axCount
            MaxValues = [None] * self._axCount
            
            for Lines, Arrays in zip([self._lines, self._linesBack, self._linesSub], [self._values, self._valuesBack, self._valuesSub]):
                for ID, Line, Array in zip(self._ID, Lines, Arrays):
                    if Line is not None:
                        Line.set_xdata(self._x[-self._pos:])
                        Line.set_ydata(Array[-self._pos:])
                        
                        # Find min and max
                        NewMin = np.min(Array[-self._pos:])                    
                        if MinValues[ID] is None or MinValues[ID] > NewMin:
                            MinValues[ID] = NewMin
                            
                        NewMax = np.max(Array[-self._pos:])
                        if MaxValues[ID] is None or MaxValues[ID] < NewMax:
                            MaxValues[ID] = NewMax
                                   
            MinX = self._x[-self._pos]
            MaxX = self._x[-1]
            
            if MinX == MaxX:
                MinX -= 1
                MaxX += 1

            for Ax, Min, Max, Buffer  in zip(self.axes, MinValues, MaxValues, self._showBuffers):
                if Min == Max:
                    Min -= 1
                    Max += 1
                
                BuffSize = (Max - Min) * Buffer
                if BuffSize == 0:
                    BuffSize == 1
                                
                axSetXLim(Ax, MinX, MaxX)
                axSetYLim(Ax, Min - BuffSize, Max + BuffSize)
        
        super().update()
        
       
# A plot type which is periodicaly renewed overwrting all the previous data
class renewPlot(livePlot):
    # AxCount (int): The number of axes to plot
    # Shapes (list of str): The shapes of each of the plots as a matplotlib string ("-" or "o" and so on)
    # AxID (list of int): A list of all ID's of the axes to do the plots in
    # Colors (list of str): The color strings for each plot
    # Labels (list of str): The labels for each of the plots, will append "background" or "subtracted" to it when needed
    # Figsize (2-tuple of float): The size of the figure
    # Titles (list of str/str): The titles of the figure, if only one is given then it will be the same for each plot
    # xLabels (list of str/str): The labels of the x-axis, if only one is given then it will be the same for each plot
    # yLabels (list of str/str): The labels of the y-axis, if only one is given then it will be the same for each plot
    # ShowBuffers (list of float/float): The white space buffer at the top and buttom of each plot in percentage, if only one is given then it will be the same for each plot
    def __init__(self, AxCount, Shapes, *args, AxID = None, Colors = None, Labels = None, Figsize = (8, 8), Titles = "", xLabels = "", yLabels = "", ShowBuffers = 0.1, **kwargs):
        import matplotlib.pyplot as plt
        
        AxCount = int(AxCount)
                
        # Get the number of plots and the settings            
        if isinstance(Shapes, str):
            Shapes = (Shapes,)
            
            if AxID is not None:
                AxID = (AxID,)
                
            if Colors is not None:
                Colors = (Colors,)
                                
            if Labels is not None:
                Labels = (Labels,)
                
        if AxID is None:
            AxID = (0,) * len(Shapes)
            
        if Colors is None:
            Colors = (None,) * len(Shapes)
                        
        if Labels is None:
            Labels = (None,) * len(Shapes)
            
        if isinstance(Titles, str):
            Titles = (Titles,) * AxCount
            
        if isinstance(xLabels, str):
            xLabels = (xLabels,) * AxCount
            
        if isinstance(yLabels, str):
            yLabels = (yLabels,) * AxCount
            
        if isinstance(ShowBuffers, float):
            ShowBuffers = (ShowBuffers,) * AxCount
                    
        # Create figure
        Fig, Axes = plt.subplots(AxCount, figsize = Figsize)
        if AxCount == 1:
            Axes = (Axes,)
        self._showBuffers = ShowBuffers
        self._axCount = AxCount
        
        InitArgs = (Shapes,)
        InitKwargs = {"AxID": AxID, "Colors": Colors, "Labels": Labels, "Titles": Titles, "xLabels": xLabels, "yLabels": yLabels}
        
        super().__init__(Fig, Axes, *args, InitArgs = InitArgs, InitKwargs = InitKwargs, **kwargs)
              
    # Initializes the plot
    def _init(self, Shapes, AxID = None, Colors = None, Labels = None, Titles = "", xLabels = "", yLabels = ""):
        # Set the ax ID
        self._ID = AxID
        
        # Create plots and save arrays
        self._values = []        
        self._lines = []
        
        for Shape, ID, Color, Label in zip(Shapes, AxID, Colors, Labels):
            NewLine, = self.axes[ID].plot([0, 1], [0, 0], Shape, color = Color, label = Label)                
            self._lines.append(NewLine)

        # Add labels
        for Ax, Title, xLabel, yLabel in zip(self.axes, Titles, xLabels, yLabels):
            Ax.set_title(Title)
            Ax.set_xlabel(xLabel)
            Ax.set_ylabel(yLabel)
            Ax.legend()
        
        self.fig.tight_layout()
        
        self.home()
        
    # Updates the plot with new values
    # x (list of float): The x value of the new points
    # Values (list of list of float): The values for each of the plots, each list of float must be same length as x
    # ID (list of int): The axes ID's for each of the value lists, any ID not given will default to value 0. If None then it will start from 0 and increase until it is out of values
    def update(self, x, Values, ID = None):
        import numpy as np
        
        # Get ID
        if ID is None:
            ID = np.arange(len(Values))
            
        # Set up the values
        x = np.array(x, dtype = float)
        DefaultValue = np.zeros_like(x)
        UseValues = [DefaultValue] * len(self._lines)
        
        for i, (Value, LineID) in enumerate(zip(Values, ID)):
            UseValues[LineID] = np.array(Value, dtype = float)
            
        # Find the x limits
        xMin = np.min(x)
        xMax = np.max(x)
        
        if xMin == xMax:
            xMin -= 1
            xMax += 1
            
        # Find the y limits
        yMin = [np.inf] * self._axCount
        yMax = [-np.inf] * self._axCount
        
        for Value, AxID in zip(UseValues, self._ID):
            NewMin = np.min(Value)
            NewMax = np.max(Value)
            
            if NewMin < yMin[AxID]:
                yMin[AxID] = NewMin
                
            if NewMax > yMax[AxID]:
                yMax[AxID] = NewMax
                
        for i in range(self._axCount):
            if yMin[AxID] == np.inf:
                yMin[AxID] = 0
                
            if yMax[AxID] == -np.inf:
                yMax[AxID] = 0
            
            yDiff = yMax[AxID] - yMin[AxID]
            
            if yDiff == 0:
                yDiff = 1
            
            yMin[AxID] -= yDiff * self._showBuffers[AxID]
            yMax[AxID] += yDiff * self._showBuffers[AxID]
            
        # Update the lines
        for Line, Value in zip(self._lines, UseValues):
            Line.set_xdata(x)
            Line.set_ydata(Value)
            
        # Set ax limits
        for Ax, Min, Max in zip(self.axes, yMin, yMax):  
            axSetXLim(Ax, xMin, xMax)
            axSetYLim(Ax, Min, Max)
            
        super().update()
        
        
if __name__ == "__main__":
    import numpy as np
    import matplotlib.pyplot as plt
    
    plt.close("all")
    
    def getHist(Count, BackgroundCount):
        Values = np.random.normal(loc = 2, size = BackgroundCount)
        Values = np.append(Values, np.random.normal(size = Count))
        Bins, Edges = np.histogram(Values, bins = 100, range = (-5, 5))
        Pos = (Edges[:-1] + Edges[1:]) / 2
        return Pos, Bins
    
    DataCount = 1000
    BackCount = 300
    Pos = 0
    x, _ = getHist(0, 0)
    
    Gate0 = (-1, 1)
    Gate1 = (2, 5)
    
    Histogram = histogram(x, GateCount = 4, Gates = [Gate0, Gate1], GateTitles = ["Gate1", "Gate2", "Mean", "Std"], BackgroundMode = "subtract", GateFontSize = 20)
    Plot = plot(30, 2, ("o", "-"), AxID = (0, 1), Colors = (("blue", "red", "yellow"), "green"), BackgroundModes = ("subtract_noback", "subtract_only"), Labels = ("Signal", "Signal"), Titles = ("Gate1", "Gate2"), xLabels = "Iteration", yLabels = "Count")
    
    # Run loop
    while True:
        if Pos == 10:
            Histogram.reset()
            Plot.reset()
        
        x, y = getHist(int(DataCount * (1 + 0.5 * np.sin(Pos * 0.2))), BackCount)
        xBack, yBack = getHist(0, BackCount)
        
        Value0 = np.sum(y[(x >= Gate0[0]) & (x <= Gate0[1])])
        Value1 = np.sum(y[(x >= Gate1[0]) & (x <= Gate1[1])])
        Value2 = np.average(x, weights = y)
        Value3 = np.sqrt(np.average((x - Value2) ** 2, weights = y))
        Value0Back = np.sum(yBack[(xBack >= Gate0[0]) & (xBack <= Gate0[1])])
        Value1Back = np.sum(yBack[(xBack >= Gate1[0]) & (xBack <= Gate1[1])])
        Value2Back = np.average(xBack, weights = yBack)
        Value3Back = np.sqrt(np.average((xBack - Value2Back) ** 2, weights = yBack))
        
        Histogram.update(y, [Value0, Value1, Value2, Value3], BinsBackground = yBack, GateValuesBackground = [Value0Back, Value1Back, Value2Back, Value3Back])
        Plot.update(Pos, (Value0, Value1), BackgroundValues = (Value0Back, Value1Back))
        
        Histogram.pause(1)
        
        Pos += 1
        