from .. import exceptions as e
from ..equipment import device

# Adds plotting to the time bandit
class timeBandit(device):
    # FPGA (controllers.timeBandit): The FPGA to control
    # Figsize (2-tuple of int): The size of the figure to plot the sequences on
    # DeviceName (str): The name of the device
    # ID (str): The ID name for the device, only used for displaying infomation
    def __init__(self, FPGA, *args, Figsize = (8, 4), **kwargs):
        from .. import plotting as pl
        from .. import controllers as c

        if not "DeviceName" in kwargs:
            kwargs["DeviceName"] = "TimeBandit"
        
        super().__init__(*args, **kwargs)
        
        if not isinstance(FPGA, c.timeBandit):
            raise e.TypeDefError("FPGA", FPGA, c.timeBandit)
        
        # Save the FPGA
        self.FPGA = FPGA
        
        # Setup plotting
        ChannelCount = len(FPGA.CH)
        Labels = [f"CH {i + 1}" for i in range(ChannelCount)]
        Shapes = ["-"] * ChannelCount
        
        self._plot = pl.renewPlot(1, Shapes, Labels = Labels, Figsize = Figsize, Titles = "TimeBandit sequence", xLabels = "Time (ns)", yLabels = "Voltage")
        
    def _close(self):
        self._plot.close()
        super()._close()
        
    # Shows the sequences
    def show(self):
        import numpy as np
        import math
        
        # Get clock division
        ClockDivision = 1
        
        for Channel in self.FPGA.CH:
            ClockDivision *= Channel.clockPartition // math.gcd(ClockDivision, Channel.clockPartition)
        
        # Get the x values
        Length = self.FPGA.getSequenceLength() * self.FPGA.getClocksPerBase() * ClockDivision
        x = np.arange(Length, dtype = float) / (self.FPGA.getClockFrequency() * self.FPGA.getClocksPerBase() * ClockDivision)
        
        # Go through each channel and get the sequence
        Values = [None] * len(self.FPGA.CH)
        
        for i, Channel in enumerate(self.FPGA.CH):
            # Get the state and partition
            State = Channel.getState()
            Partition = Channel.clockPartition
            Multiplier = ClockDivision // Partition
            
            # Set off
            Values[i] = np.zeros_like(x)
            if State == "off":
                pass
                
            elif State == "dc":
                Values[i][:] = 1
                
            else:
                for Pulse in State:
                    if Pulse is None:
                        continue
                    
                    Start, Stop = Pulse
                    Start = int(Start * Partition) % (Length * Partition // ClockDivision)
                    Stop = int(Stop * Partition) % (Length * Partition // ClockDivision)
                    
                    if Start >= Stop:
                        Values[i][Start * Multiplier:] = 1
                        Values[i][:(Stop - 1) * Multiplier] = 1
                        
                    else:
                        Values[i][Start * Multiplier:(Stop - 1) * Multiplier] = 1
                        
        # Plot it
        self._plot.update(x, Values)