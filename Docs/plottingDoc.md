# Documentation for loggers

This is a number of classes which implements live plotting including normal plots and histograms

---

# Functions

---

## axSetup(Ax)

Sets up an ax to allow zooming in live plotting

- Ax (matplotlib.Axes): The ax to set up

---
---

## axUpdate(Ax, Force = False)

Updates the view of an ax, only updates it if Force is True or there is no zoom

- Ax (matplotlib.Axes): The ax to update
- Force (bool): If True then it will wlays update

---
---

## axSetXLim(Ax, xMin, xMax)

Sets the limits of the x-axis without changing user zoom

- Ax (matplotlib.Axes): The ax to change limits for
- xMin (float): The minimum x value
- xMax (float): The maximum x value

---
---

## axSetYLim(Ax, yMin, yMax)

Sets the limits of the y-axis without changing user zoom

- Ax (matplotlib.Axes): The ax to change limits for
- yMin (float): The minimum y value
- yMax (float): The maximum y value

---
---

# Classes

---

## livePlot(Fig, Axes)

A class to implement live plotting, it must be subclassed and the update function must be expanded

- Fig (matplotlib.Figure): The figure of this plot
- Axes (list of matplotlib.Axes): The list of axes used in this plot

---

### method home()

Homes the figure, may need to be called at the end of initialization

---

### method update()

Updates the plot with new values

---

### close()

Closes the figure

---

### method pause(Time)

Pauses while allowing to still use the plot

- Time (float): The time to pause

---

### method reset()

Resets the plot to the inital state

---

### property fig (matplotlib.Figure)

The figure for this plot

---

### property axes (list of matplotlib.Axes)

The list of all the axes used in the plot

---
---

## histogram(xValues, GateCount = 0, Gates = [], History = 10, GateShowBuffer = 0.1, BaseSize = (8, 4), GatesPerRow = 2, BackgroundMode = "off", Title = "Histogram", xLabel = "Time (ns)", yLabel = "Counts", GateTitles = None, GateXLabels = None, GateYLabels = None, GatePrecision = None, GateFontSize = 40)

Live plotting for a histogram with gate implementation

- xValues (numpy.ndarray of float): The x values for the bins of the histogram
- GateCount (int): The number of gate plots, this can also be for calculated values like mean ect.
- Gates (list of 2-tuple of float): A list of the gates to draw onto the histogram
- History (int): The number of points to keep in the backlog for the gates
- GateShowBuffer (float): The percentage of the gate plots to keep as white space at the buttom and top
- BaseSize (int): The base size of the window (size per row of plots)
- GatesPerRow (int): The number of gate plots to plot on a single row
- BackgroundMode (str): The background mode to use, must be one of "off": Do not use background, "on": Plot background measurements, "subtract": Evaluate the background subtracted signal, this also uses "on"
- Title (str): The title of the histogram
- xLabel (str): The label on the x-axis of the histogram
- yLabel (str): The label on the y-axis of the histogram
- GateTitles (list of str): The name of each gate, if not specified then it will only write the number
- GateXLabels (list of str): The x labels for each of the gates
- GateYLabels (list of str): The y labels for each of the gates
- GatePrecision (list of int): The number of digits to show for each of the gate values
- GateFontSize (int): The size of the gate titles

Subclasses livePlot

---

### method update(Bins, GateValues = [], BinsBackground = None, GateValuesBackground = None)

Updates the plot with new values

- Bins (numpy.ndarray): The values for each of the bins in the histogram
- GateValues (list): A list of the values for each of the gates
- BinsBackground (numpy.ndarray): The background values for each of the bins, if not given then it will use the previous value, should only be given if background mode is not "off"
- GateValuesBackground (list): A list of the background values for each of the gates if not given then it will use the previous value, should only be given if background mode is not "off"

---
---

## plot(MaxSize, AxCount, Shapes, AxID = None, Colors = None, BackgroundModes = None, Labels = None, Figsize = (8, 8), Titles = "", xLabels = "", yLabels = "", ShowBuffers = 0.1)

Creates a live plot for normal data that is gathered one point at the time

- MaxSize (int): The max number of data points to show, if more is given then it will overwrite old values
- AxCount (int): The number of axes to plot
- Shapes (list of str): The shapes of each of the plots as a matplotlib string ("-" or "o" and so on)
- AxID (list of int): A list of all ID's of the axes to do the plots in
- Colors (list of str): The color strings for each plot
- BackgroundModes (list of str): List of all the background modes to use for each plot, must be one of "off": No background is used, "on": The background is also plotted, "subtract": The background and background subtracted data are both plotted, "subtract_noback": Plots data and background subtracted data, "subtract_only": Only plots the background subtracted data
- Labels (list of str): The labels for each of the plots, will append "background" or "subtracted" to it when needed
- Figsize (2-tuple of float): The size of the figure
- Titles (list of str/str): The titles of the figure, if only one is given then it will be the same for each plot
- xLabels (list of str/str): The labels of the x-axis, if only one is given then it will be the same for each plot
- yLabels (list of str/str): The labels of the y-axis, if only one is given then it will be the same for each plot
- ShowBuffers (list of float/float): The white space buffer at the top and buttom of each plot in percentage, if only one is given then it will be the same for each plot

Inherits from livePlot

---

### method update(x, Values, BackgroundValues = None)

Updates the plot with new values

- x (float): The x value of the new points
- Values (list of float): The values for each of the plots
- BackgroundValues (list of float): The values of the background for each plot, None if not needed

---
---

## renewPlot(AxCount, Shapes, AxID = None, Colors = None, Labels = None, Figsize = (8, 8), Titles = "", xLabels = "", yLabels = "", ShowBuffers = 0.1)

A plot type which is periodicaly renewed overwrting all the previous data

- AxCount (int): The number of axes to plot
- Shapes (list of str): The shapes of each of the plots as a matplotlib string ("-" or "o" and so on)
- AxID (list of int): A list of all ID's of the axes to do the plots in
- Colors (list of str): The color strings for each plot
- Labels (list of str): The labels for each of the plots, will append "background" or "subtracted" to it when needed
- Figsize (2-tuple of float): The size of the figure
- Titles (list of str/str): The titles of the figure, if only one is given then it will be the same for each plot
- xLabels (list of str/str): The labels of the x-axis, if only one is given then it will be the same for each plot
- yLabels (list of str/str): The labels of the y-axis, if only one is given then it will be the same for each plot
- ShowBuffers (list of float/float): The white space buffer at the top and buttom of each plot in percentage, if only one is given then it will be the same for each plot

Inherits from livePlot

---

### method update(x, Values, ID = None)

Updates the plot with new values

- x (list of float): The x value of the new points
- Values (list of list of float): The values for each of the plots, each list of float must be same length as x
- ID (list of int): The axes ID's for each of the value lists, any ID not given will default to value 0. If None then it will start from 0 and increase until it is out of values

---
---