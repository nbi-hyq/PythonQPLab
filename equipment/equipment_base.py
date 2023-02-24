# The default equipment class
class device:
    # DeviceName (str): The name of the device
    # ID (str): The ID name for the device, only used for displaying infomation
    def __init__(self, *args, DeviceName = "Device", ID = None, **kwargs):
        import weakref
        
        super().__init__(*args, **kwargs)
        
        # Set the device name
        self.deviceName = str(DeviceName)
        self._isOpen = True
        
        if ID is not None:
            self.deviceName = f"{self.deviceName} {str(ID)}"
            
        weakref.finalize(self, self.close)
        
    # Checks if the device is open, may be overwritten by the sub class if it can be closed
    # Returns True if it is open
    def isOpen(self):
        return self._isOpen
        
    # Close the device, the method _close must be overwritten by the device
    def close(self):
        if self.isOpen():
            self._close()
            
        self._isOpen = False
        
    # Does the actual closing of the device
    def _close(self):
        pass
