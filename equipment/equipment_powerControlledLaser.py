import exceptions as e
from equipment import device, laser, powerControl

# The controller for a power controlled laser
class powerControlledLaser(device):
    # Laser (laser): The laser to control
    # PowerControl (powerControl) The power control of the laser
    # DeviceName (str): The name of the device
    # ID (str): The ID name for the device, only used for displaying infomation
    def __init__(self, Laser, PowerControl, *args, **kwargs):
        # Make sure the types are correct
        if not isinstance(Laser, laser):
            raise e.TypeDefError("Laser", Laser, laser)

        if not isinstance(PowerControl, powerControl):
            raise e.TypeDefError("PowerControl", PowerControl, powerControl)

        if not "DeviceName" in kwargs:
            kwargs["DeviceName"] = "Power Controlled Laser"

        super().__init__(*args, **kwargs)
        
        # Save the laser and power control
        self.laser = Laser
        self.power = PowerControl