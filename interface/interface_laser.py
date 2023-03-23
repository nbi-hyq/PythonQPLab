from .. import exceptions as e

# A generic class to control lasers, cannot be used on its own
class laser:
    # VoltageRange (2-tuple of float): Them minimum and maximum voltage allowed
    # FrequencyRange (2-tuple of float): The minimum and maximum frequencies allowed, if None then they are calculated from WavelengthRange
    # WavelengthRange (2-tuple of float): The minimum and maximum wavelengths allowed, calculated from FrequencyRange if that is given
    def __init__(self, *args, VoltageRange = (0, 1), FrequencyRange = None, WavelengthRange = (900, 1000), **kwargs):
        super().__init__(*args, **kwargs)
        
        self._voltageRange = (float(VoltageRange[0]), float(VoltageRange[1]))
        
        if FrequencyRange is not None:
            self._frequencyRange = (float(FrequencyRange[0]), float(FrequencyRange[1]))
            self._wavelengthRange = (self.frequencyToWavelength(FrequencyRange[1]), self.frequencyToWavelength(FrequencyRange[0]))
        else:
            self._frequencyRange = (self.wavelengthToFrequency(WavelengthRange[1]), self.wavelengthToFrequency(WavelengthRange[0]))
            self._wavelengthRange = (float(WavelengthRange[0]), float(WavelengthRange[1]))

        self.voltageBase = (self._voltageRange[0] + self._voltageRange[1]) / 2
        self._voltage = self.voltageBase

    # Converts a frequency in THz to a wavelength in nm
    # Value (float): The frequency to convert        
    def frequencyToWavelength(self, Value):
        return 299792458 / (float(Value) * 1e12) * 1e9
    
    # Converts a wavelength in nm to a frequency in THz
    # Value (float): The wavelength to convert
    def wavelengthToFrequency(self, Value):
        return 299792458 / (float(Value) * 1e-9) * 1e-12
    
    # Checks if the frequency is in the allowed range
    # Value (float): The frequency to check
    def frequencyAllowed(self, Value):
        return float(Value) >= self._frequencyRange[0] and float(Value) <= self._frequencyRange[1]
    
    # Checks if the wavelength is in the allowed range
    # Value (float): The wavelength to check
    def wavelengthAllowed(self, Value):
        return float(Value) >= self._wavelengthRange[0] and float(Value) <= self._wavelengthRange[1]
        
    # Checks if the voltage is in the allowed range
    # Value (float): The voltage to check
    def voltageAllowed(self, Value):
        return float(Value) >= self._voltageRange[0] and float(Value) <= self._voltageRange[1]
    
    # Sets the wavelength of the laser, this or setFrequency must be overwritten
    # Value (float): The value of the wavelength
    def setWavelength(self, Value, **kwargs):
        # Make sure it is within the range
        if not self.wavelengthAllowed(Value):
            raise e.RangeError("Value", Value, self._wavelengthRange[0], self._wavelengthRange[1])
        
        self.setFrequency(self.wavelengthToFrequency(Value), **kwargs)
    
    # Gets the wavelength set by the laser, this or getFrequency must be overwritten
    def getWavelength(self, **kwargs):
        return self.frequencyToWavelength(self.getFrequency(**kwargs))
    
    # Sets the frequency of the laser, this or setWavelength must be overwritten
    # Value (float): The value of the frequency
    def setFrequency(self, Value, **kwargs):
        if not self.frequencyAllowed(Value):
            raise e.RangeError("Value", Value, self._frequencyRange[0], self._frequencyRange[1])

        self.setWavelength(self.frequencyToWavelength(Value), **kwargs)
    
    # Gets the frequency set by the laser, this or getWavelength must be overwritten
    def getFrequency(self, **kwargs):
        return self.wavelengthToFrequency(self.getWavelength(**kwargs))
        
    # Sets the piezo voltage of the laser
    # Value (float): The voltage to set
    def setVoltage(self, Value):
        # Check that the voltage is within the limits
        if not self.voltageAllowed(Value):
            raise e.RangeError("Value", Value, self._voltageRange[0], self._voltageRange[1])

        # Save it internally
        self._voltage = float(Value)
        
    # Gets the last voltage set
    def getVoltage(self):
        return self._voltage
    