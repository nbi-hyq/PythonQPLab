from .. import exceptions as e
from ..equipments import device

# Adds plotting to the AWG
class AWG(device):
    # Device (controllers.AWG): The AWG to control
    # Figsize (2-tuple of int): The size of the figure to plot the sequences on
    # DeviceName (str): The name of the device
    # ID (str): The ID name for the device, only used for displaying infomation
    def __init__(self, Device, *args, Figsize = (8, 4), **kwargs):
        from .. import plotting as pl
        from .. import controllers as c

        if not "DeviceName" in kwargs:
            kwargs["DeviceName"] = "AWG"
        
        super().__init__(*args, **kwargs)
        
        if not isinstance(Device, c.AWG):
            raise e.TypeDefError("Device", Device, c.AWG)
        
        # Save the FPGA
        self.device = Device
        
        # Setup plotting
        ChannelCount = Device.channelCount
        Labels = [f"CH {i + 1}" for i in range(ChannelCount)]
        Shapes = ["-"] * ChannelCount
        
        self._plotAmplitude = pl.renewPlot(1, Shapes, Labels = Labels, Figsize = Figsize, Titles = "AWG sequence amplitude", xLabels = "Time (ns)", yLabels = "Amplitude")
        self._plotPhase = pl.renewPlot(1, Shapes, Labels = Labels, Figsize = Figsize, Titles = "AWG sequence phase", xLabels = "Time (ns)", yLabels = "Phase")
        
    def _close(self):
        self._plot.close()
        super()._close()
        
    # Shows the sequences
    def show(self):
        import numpy as np
        
        # If nothing is active
        if self.device.currentSequence is None:
            x = np.array([0, 1], dtype = float)
            Values = [np.array([0, 0], dtype = float)] * self.device.channelCount
            PhaseValue = [np.array([0, 0], dtype = float)] * self.device.channelCount
            
        else:
            # Get the sequences
            Sequence = self.device.sequences[self.device.currentSequence]
            
            # Get the length
            Length = Sequence.entryCount * Sequence.length
            
            x = np.arange(Length, dtype = float) / Sequence.sampleFreq
            
            Values = [None] * Sequence.channelCount
            PhaseValues = [None] * Sequence.channelCount
            
            for i in range(Sequence.channelCount):
                Values[i] = np.empty(Length)
                PhaseValues[i] = np.zeros(Length)
                
                # Fill the values
                for j in range(Sequence.entryCount):
                    if Sequence.mode == "BB":
                        Values[i][Sequence.length * j: Sequence.length * (j + 1)] = Sequence.sequences[j][i].waveform
                        
                    else:
                        A, P = Sequence.fromIQ(Sequence.sequences[j][i][0].waveform, Sequence.sequences[j][i][1].waveform)
                        
                        Values[i][Sequence.length * j: Sequence.length * (j + 1)] = A
                        PhaseValues[i][Sequence.length * j: Sequence.length * (j + 1)] = P                      
                        
        self._plotAmplitude.update(x, Values)
        self._plotPhase.update(x, PhaseValue)