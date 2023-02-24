from .. import connections as c
from .. import exceptions as e
from ..controllers import laser, DAC

# A laser class controlled by a DAC
class DACLaser(laser, c.deviceBase): # If used with the equipment.laser remember to set the JumpAttempts to 0
    # DACController (DAC): The DAC to control the voltage
    # Channel (int): The channel of the DAC to use
    # VoltageRange (2-tuple of float): Them minimum and maximum voltage allowed
    # DeviceName (str): The name of the device, only used for error messages
    # ID (str): The ID name for the device, only used for displaying infomation
    def __init__(self, DACController, Channel, *args, **kwargs):
        # Make sure it is a DAC
        if not isinstance(DACController, DAC):
            raise e.TypeDefError("DACController", DACController, DAC)
        
        # Set the voltage range
        if not "VoltageRange" in kwargs:
            kwargs["VoltageRange"] = (-3, 3)

        if not "DeviceName" in kwargs:
            kwargs["DeviceName"] = "DAC Laser"
            
        # Initialize the laser
        super().__init__(*args, **kwargs)
        
        # Save the DAC
        self._DAC = DACController
        self._channel = int(Channel)
        
    # This cannot set the wavelength
    # Value (float): The value of the wavelength
    def setWavelength(self, Value, **kwargs):
        raise e.ImplementationError("DACLaser.setWavelength")

    # This cannot get the wavelength
    def getWavelength(self, **kwargs):
        raise e.ImplementationError("DACLaser.getWavelength")
        
    # This cannot set the frequency
    # Value (float): Tje value of the frequency
    def setFrequency(self, Value, **kwargs):
        raise e.ImplementationError("DACLaser.setFrequency")

    # This cannot get the frequency
    def getFrequency(self, **kwargs):
        raise e.ImplementationError("DACLaser.getFrequency")

    # Sets the voltage using the DAC
    # Value (float): The value of the voltage
    # UseQueue (bool): Whether to run the command through the queue or not
    def setVoltage(self, Value, **kwargs):
        # Save it internally
        super().setVoltage(Value)
        
        # Set voltage
        self._DAC.setVoltage(float(Value), self._channel, **kwargs)   
        
    # Gets the voltage set for the DAC
    # UseQueue (bool): Whether to run the command through the queue or not
    def getVoltage(self, **kwargs):
        return super().getVoltage()
        