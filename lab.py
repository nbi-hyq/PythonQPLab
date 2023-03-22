from . import exceptions as e

# A base setting class
class baseSetting:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Dict to save everything inside and the default value
        self._dict = dict()
        self._value = None
        self._fullDict = None
        
    # Gets an item from the dict
    # ID (str): The ID of the item
    def __getitem__(self, ID):
        Value = self.getBranch(ID)
        
        # Check if it is just an item
        if not isinstance(Value, type(self)):
            return Value
        
        # If there is a sub setting make sure the item exists
        if Value._value is None:
            raise e.ItemExistError(ID, self)
        
        return Value._value
    
    # Sets an item to the dict
    # ID (str): The ID of the item
    # Item (any): The item to set
    def __setitem__(self, ID, Item):
        # Stop if there is an underscore in the beginning, this is just a comment
        if str(ID)[0] == "_":
            return
        
        self._fullDict = None
        
        # Split
        SplitID = str(ID).split(".", 1)

        # If it should put it in a sub setting
        if len(SplitID) > 1:
            # Add new sub setting
            if not SplitID[0] in self._dict:
                self._dict[SplitID[0]] = type(self)()
                
            # Save the old item
            elif not isinstance(self._dict[SplitID[0]], type(self)):
                OldItem = self._dict[SplitID[0]]
                self._dict[SplitID[0]] = type(self)()
                self._dict[SplitID[0]]._value = OldItem

            # Set item
            self._dict[SplitID[0]][SplitID[1]] = Item
        
        # If there is a sub setting
        elif SplitID[0] in self._dict and isinstance(self._dict[SplitID[0]], type(self)):
            self._dict[SplitID[0]]._value = Item
            
        # Just set the item
        else:
            self._dict[SplitID[0]] = Item

    # Returns an iterator for the dict of this object
    def __iter__(self):
        return iter(self.toDict())
    
    # Copies the settings
    def copy(self):
        NewSetting = type(self)()
        NewSetting.loadDict(self.toDict())
        return NewSetting
        
    # Gets an item from the dict, may return a sub setting
    # ID (str): The ID of the branch
    def getBranch(self, ID):
        # Split
        SplitID = str(ID).split(".", 1)

        # If it should take it from a sub setting
        if len(SplitID) > 1:
            if not isinstance(self._dict[SplitID[0]], type(self)):
                raise e.ItemExistError(ID, self)
                
            return self._dict[SplitID[0]][SplitID[1]]
        
        # Otherwise just return
        return self._dict[SplitID[0]]
    
    # Removes an item if it exists, does nothing if the item does not exist
    # ID (str): The ID of the item
    def removeItem(self, ID):
        # Check if the item is there
        if ID not in self:
            return
        
        # Reset full dict
        self._fullDict = None
        
        # Get the branch
        SplitID = str(ID).rsplit(".", 1)
        
        # Get the setting in which it is located
        if len(SplitID) > 1:
            Setting = self.getBranch(SplitID[0])
            
        else:
            Setting = self
        
        # If the item is a sub setting
        if isinstance(Setting[SplitID[-1]], type(self)):
            Setting[SplitID[-1]]._value = None
        
        # Remove the item
        else:
            Setting._dict.pop(SplitID[-1])
        
    # Merges another setting with this, the new one will overwrite
    # Setting (baseSetting): The setting to add
    def addSetting(self, Setting):
        if not isinstance(Setting, type(self)):
            raise e.TypeDefError("Setting", Setting, type(self))
        
        for Key, Item in Setting.toDict().items():
            self[Key] = Item
        
    
    # Converts the setting to a dict
    def toDict(self):
        if self._fullDict is not None:
            return self._fullDict.copy()
        
        Dict = dict()
        
        # Go through all elements
        for Key, Value in self._dict.items():
            # If it is a setupSetting get the dict and merge it
            if isinstance(Value, type(self)):
                NewDict = Value.toDict()
                
                # Add new items
                for NewKey, NewValue in NewDict.items():
                    Dict[f"{Key}.{NewKey}"] = NewValue
                    
                # Add original value
                if Value._value is not None:
                    Dict[Key] = Value._value
                    
            # Add other values
            else:
                Dict[Key] = Value
            
        self._fullDict = Dict
        return Dict

    # Creates the settings from a dict
    # Dict (dict): The dict to convert from
    def loadDict(self, Dict):
        # Loop through all items
        for Key, Value in Dict.items():
            self[Key] = Value
            
    # Creates a new object from a dict
    # Dict (dict): The dict to load from
    @classmethod
    def fromDict(cls, Dict):
        Setting = cls()
        Setting.loadDict(Dict)
        return Setting


# Saves a setup setting
class setting(baseSetting):        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self._sleepTime = 0
    
    # Saves the setup to a file
    # Path (str): The path to save to
    # Overwrite (bool): If False then it will append _[NUM] to the file if it already exists
    # MaxAttempts (int): The max number it will attempt to append to the file name before giving up
    def save(self, Path, Overwrite = False, MaxAttempts = 100):
        import os
        import json
        
        # Add extension
        SplitPath = str(Path).split(".", 1)
        
        if len(SplitPath) > 1:
            Path = str(Path)
            
        else:
            Path = f"{Path}.json"
        
        # Check that the file does not exist
        if not Overwrite and os.path.exists(Path):
            SplitPath = Path.split(".", 1)
            BasePath = SplitPath[0]
            Ext = SplitPath[1]
            Success = False
            
            # Go through other names and check if they exist
            for i in range(MaxAttempts):
                NewPath = f"{BasePath}_{i}.{Ext}"
                
                if not os.path.exists(NewPath):
                    Success = True
                    Path = NewPath
                    break
                
            # Make sure it had success
            if not Success:
                raise e.FileExistError(Path)
                
        # Open the file and save
        with open(Path, "w") as File:
            File.write(json.dumps(self.toDict(), indent = 4))
                    
    # Load settings from a file
    # Path (str): The path for the file
    # Relative (bool): If True then the path will be relative to the current directory
    def load(self, Path, Relative = True):
        import json
        import os
        
        # Add extension
        SplitPath = str(Path).split(".", 1)
        
        if len(SplitPath) > 1:
            Path = str(Path)
            
        else:
            Path = f"{Path}.json"
            
        if Relative:
            Dir = os.path.dirname(__file__)
            Path = f"{Dir}/{Path}"

        # Open file and convert to a dict
        with open(Path, "r") as File:
            self.loadDict(json.load(File))
        
    # Creates a new setting object and imports settings from a file
    # Path (str): The path of the settings file, .json is append if an extension is not given
    # Relative (bool): If True then the path will be relative to the current directory
    @classmethod
    def fromJSON(cls, Path, Relative = True):
        Setting = cls()
        Setting.load(Path, Relative = Relative)
        return Setting
    
    # Notes down when the pause is done
    # Time (float): The time from now to do the pause
    def addPause(self, Time):
        import time
        
        self._sleepTime = max(self._sleepTime, time.time() + Time)
        
    # Does the pausing making sure that all pauses are respected
    def pause(self):
        import time
        from .. import functions as f
        
        Time = self._sleepTime - time.time()
        
        if Time > 0:
            f.time.sleep(Time)

            
# Holds functions to handle any setting
class settingHandler(baseSetting):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self._waitQueue = []

    # Sets an item to the dict
    # ID (str): The ID of the item
    # Item (handle): The item to set
    def __setitem__(self, ID, Item):
        if not isinstance(Item, handle):
            raise e.TypeDefError("Item", Item, handle)
            
        super().__setitem__(ID, Item)
        
    # Process an item
    # AppliedSettings (setting): The settings to store the applied value
    # ID (str/setting): The ID or setting to handle
    # Value (any): The value of the setting to handle
    # UseQueue (bool): Whether to run the command through the queue or not, ignored if the device was initialized with UseQueue = False
    def process(self, AppliedSettings, ID, Value, **kwargs):
        if ID in self:
            Func, Order = self[ID].process(AppliedSettings, Value, **kwargs)
            if Order is not None:
                self._waitQueue.append((Func, Order))
        
    # Processes everything in some settings
    # AppliedSettings (setting): The settings to store the applied value
    # Settings (setting): The settings to process
    # UseQueue (bool): Whether to run the command through the queue or not, ignored if the device was initialized with UseQueue = False
    def processSettings(self, AppliedSettings, Settings, **kwargs):
        for Key, Value in Settings.toDict().items():
            self.process(AppliedSettings, Key, Value, **kwargs)
        
    # Applies all the settings with a specific order
    def postProcess(self):
        # Sort the queue
        self._waitQueue.sort(key = lambda x: x[1])
        
        # Apply them
        for Func, _ in self._waitQueue:
            Func()
            
        # Reset queue
        self._waitQueue = []
            
            
# A handle for handling a setting
class handle:
    # Key (str): The key for this handle
    # Function (callable): The function to run the handle, must take inputs (Value, UseQueue = True)
    # Overwrites (list of str): A list of all the settings to delete when handling a setting
    # Pause (float): The time to pause after applying this setting
    # Order (int): If not None then it will wait until the end of the settings and then apply all the rest in order from lowest to highest
    def __init__(self, Key, Function, *args, Overwrites = [], Pause = 0, Order = None, **kwargs):
        super().__init__(*args, **kwargs)
        
        self._f = Function
        self._overwrites = list(Overwrites)
        self._key = str(Key)
        self._order = Order
        self._pause = float(Pause)
        
    # Processes an item
    # Settings (setting): The applied settings
    # Value and kwargs are passed to the function
    # UseQueue (bool): Whether to run the command through the queue or not, ignored if the device was initialized with UseQueue = False
    def process(self, Settings, Value, **kwargs):        
        # Function to do the handle
        def handleFunc():
            # Run function
            self._f(Value, **kwargs)

            # Remove overwrites
            for Key in self._overwrites:
                Settings.removeItem(Key)
                
            # Add setting
            Settings[self._key] = Value
            
            # Add pause
            Settings.addPause(self._pause)
            
        if self._order is None:
            handleFunc()
            return None, None
        
        else:
            return handleFunc, self._order
        
# Holds functions to handle any setting, any item must be a function taking the arguments: Value (any): The value from the settings, Key (str): The key which retrieved this value, Settings (setting): The settings to finalize and return the new value for that key
class settingFinalizer(baseSetting):
    # Finalizes a setting
    # Settings (setting): The settings to process
    def process(self, Settings):
        NewSettings = Settings.copy()
        
        for Key, Value in Settings.toDict().items():
            if Key in self:
                NewSettings[Key] = self[Key](Value, Key, Settings)
                
        return NewSettings
            

# A class to hold all of the equipment for the lab
class equipment(object):
    # Setting (str): The ID of the settings this equipment class initializes
    # Tags (list of str): A list of tags which this class has
    def __init__(self, *args, SettingName = "default", Tags = [], **kwargs):
        import weakref
        
        super().__init__(*args, **kwargs)
        
        # Save the parameters
        self.setting = str(SettingName)
        self.tags = []
        self.devices = []
        self._open = True
        
        # Add the tags
        for Tag in Tags:
            self.addTag(Tag)
            
        self.init()
        
        weakref.finalize(self, self.close)
            
    # Initialize all of the devices
    def init(self):
        pass
        
    # Checks if this class has a specific tag
    # Tag (str): The tag to check if exists
    def findTag(self, Tag):
        if Tag in self.tags:
            return True
        
        return False
    
    # Adds a tag to this class
    # Tag (str): The tag to add
    def addTag(self, Tag):
        self.tags.append(str(Tag))
        
    # Add any device
    # Device (connections.device): The device to add
    # Ignore (bool): If True then it will not close this device
    def addDevice(self, Device, Ignore = False):
        from . import connections as c
        
        if not isinstance(Device, c.deviceBase):
            raise e.TypeDefError("Device", Device, c.deviceBase)
            
        self.devices.append((Device, bool(Ignore)))
    
    # Find any device
    # Name (str): The name of the device to find
    def findDevice(self, Name):
        for Device, _ in self.devices:
            if Device.deviceName == Name:
                return Device
            
        raise e.LocateDeviceError(Name, self.devices)
    
    # Close all devices
    def close(self):
        if self.isOpen():
            self._open = False
            
            for Device, Ignore in self.devices:
                if not Ignore:
                    Device.close()
    
    # Checks if the equipment is open
    def isOpen(self):
        return self._open
    
# A setup class for a specific configuration of the lab
class setup(object):
    # Equipment (equipment): The devices of the lab
    # SettingName (str): The ID of the settings of this class
    # Tags (list of str): A list of all the tags the Equipment must possess
    def __init__(self, Equipment, *args, SettingName = "default", Tags = [], **kwargs):
        import weakref
        from . import connections as c
        
        super().__init__(*args, **kwargs)
        
        # Make sure equipment is correct
        if not isinstance(Equipment, equipment):
            raise e.TypeDefError("Equipment", Equipment, equipment)
            
        # Make sure all of the tags are there
        for Tag in Tags:
            if not Equipment.findTag(Tag):
                raise e.MissingTagError(Equipment, Tag)
        
        # Save the parameters
        self.setting = str(SettingName)
        self.lasers = []
        self.powers = []
        self.devices = []
        self._open = True
        
        # Run the initialisation function
        self.init(Equipment)
        
        weakref.finalize(self, self.close)
        
        self._settingsHandler = settingHandler()
        self._settingsFinalizer = settingFinalizer()
        self._currentSettings = setting()
        self._appliedSettings = setting()
                
        # Create a schedule queue for scripts
        self._scheduleQueue = c.queue()
                
    # Initialises all of the equipments of this setup
    # Equipment (equipment): The equipment object to get devices from
    def init(self, Equipment):
        pass
    
    # Adds a laser to the laser list
    # Laser (equipment.laser): The laser to add
    def addLaser(self, Laser):
        from . import equipment as eq
        
        if not isinstance(Laser, eq.laser):
            raise e.TypeDefError("Laser", Laser, eq.laser)
            
        self.lasers.append(Laser)
    
    # Gets a laser from the laser list
    # Name (str): The name of the laser
    def getLaser(self, Name):
        for Laser in self.lasers:
            if Laser.deviceName == Name:
                return Laser
            
        raise e.LocateDeviceError(Name, self.lasers)
    
    # Adds a power controller to the PowerControl list
    # PowerControl (equipment.powerControl): The power controller to add
    def addPowerControl(self, PowerControl):
        from . import equipment as eq
        
        if not isinstance(PowerControl, eq.powerControl):
            raise e.TypeDefError("PowerControl", PowerControl, eq.powerControl)
            
        self.powers.append(PowerControl)
    
    # Gets a power controller from the PowerControl list
    # Name (str): The name of the power controller
    def getPowerControl(self, Name):
        for powerControl in self.powers:
            if powerControl.deviceName == Name:
                return powerControl
            
        raise e.LocateDeviceError(Name, self.powers)
            
    # Locks all of the lasers
    # UseQueue (bool): Whether to run the command through the queue or not, ignored if the device was initialized with UseQueue = False
    def lock(self, **kwargs):
        for Laser in self.lasers:
            Laser.lock(**kwargs)
            
    # Unlocks all of the lasers
    def unlock(self):
        for Laser in self.lasers:
            Laser.unlock()
            
    # Turn off all lasers
    # UseQueue (bool): Whether to run the command through the queue or not, ignored if the device was initialized with UseQueue = False
    def disableLasers(self, **kwargs):
        self.unlock()
        
        for Power in self.powers:
            Power.setVoltageOut(0, **kwargs)
            
    # Add any device
    # Device (equipment.device): The device to add
    # Ignore (bool): If True then it will not clsoe the device
    def addDevice(self, Device, Ignore = False):
        from . import equipment as eq
        from . import connections as c
        
        if not (isinstance(Device, eq.device) or isinstance(Device, c.deviceBase)):
            raise e.TypeDefError("Device", Device, c.deviceBase)
            
        self.devices.append((Device, bool(Ignore)))
    
    # Find any device
    # Name (str): The name of the device to find
    def findDevice(self, Name):
        for Device, _ in self.devices:
            if Device.deviceName == Name:
                return Device
            
        raise e.LocateDeviceError(Name, self.devices)
        
    # Close all devices
    def close(self):
        if self.isOpen():
            self._open = False
            
            # Close schedule queue
            self._scheduleQueue.kill()
            
            # Close all of the devices
            for Device, Ignore in self.devices:
                if not Ignore:
                    Device.close()
      
    # Checks if the equipment is open
    def isOpen(self):
        return self._open
    
    # Gets a single setting for this setup
    # Name (str): The name of the setting
    def getSetting(self, Name):
        return self._currentSettings[Name]
    
    # Gets all the settings for this setup
    def getSettings(self):
        return self._currentSettings
    
    # Gets a single applied setting for this setup
    # Name (str): The name of the setting
    def getAppliedSetting(self, Name):
        return self._appliedSettings[Name]
    
    # Gets all the applied settings for this setup
    def getAppliedSettings(self):
        return self._appliedSettings
    
    # Applies a single setting
    # Name (str): The name of the setting
    # Value (any): The value of the setting
    # Reload (bool): If True then it will apply it even if it has already been applied
    # UseQueue (bool): Whether to run the command through the queue or not, ignored if the device was initialized with UseQueue = False
    def applySetting(self, Name, Value, Reload = False, **kwargs):
        # Check if it already is loaded
        if not Reload and Name in self._appliedSettings and Value == self._appliedSettings[Name]:
            return
        
        self._settingsHandler.process(self._appliedSettings, Name, Value, **kwargs)
        self._currentSettings[Name] = Value
    
    # Applies a setting to the setup
    # Settings (setting): The settings to apply to the setup
    # Reload (bool): If True then it will apply it even if it has already been applied
    # UseQueue (bool): Whether to run the command through the queue or not, ignored if the device was initialized with UseQueue = False
    def applySettings(self, Settings, **kwargs):
        # Finalize
        RunSettings = self._settingsFinalizer.process(Settings)
        
        # Go through each item and apply them
        for Key, Item in RunSettings.toDict().items():
            self.applySetting(Key, Item, **kwargs)

        # Post process
        self.postProcessSettings()
        self._appliedSettings.pause()
        
    # Applies the settings which has an order, not needed if settings were applied with applySettings
    def postProcessSettings(self):
        self._settingsHandler.postProcess()
    
    # Load settings from a file and apply them
    # Path (str): The path of the file
    # Relative (bool): If True then the file will be relative to this one
    # UseQueue (bool): Whether to run the command through the queue or not, ignored if the device was initialized with UseQueue = False
    def loadSettings(self, Path, Relative = True, **kwargs):
        Settings = setting.fromJSON(Path, Relative = Relative)
        self.applySettings(Settings, **kwargs)
        
    # Add a single setting handler
    # Name (str): The name of the handler
    # Function (callable): The function to run when handling, should take arguments (Input, UseQueue = True)
    # Overwrites (list of str): The settings to overwrite when setting this setting
    def addSettingHandler(self, Name, Function, Overwrites = []):
        self._settingsHandler[Name] = handle(Name, Function, Overwrites = Overwrites)
        
    # Adds setting handlers
    # SettingHandlers (setupSettingHandler): The handlers to add
    def addSettingHandlers(self, SettingHandlers):
        self._settingsHandler.addSetting(SettingHandlers)

    # Add a single setting finalizer
    # Name (str): The name of the finalizer
    # FinalizerFunction (callable): The finalizer function to add, must take the arguments: Value (any): The value from the settings, Key (str): The key which retrieved this value, Settings (setting): The settings to finalize and return the new value for that key
    def addSettingFinalizer(self, Name, FinalizerFunction):
        self._settingsFinalizer[Name] = FinalizerFunction
        
    # Adds setting finalizers
    # SettingFinalizers (setupSettingHandler): The finalizers to add
    def addSettingFinalizers(self, SettingFinalizers):
        self._settingsFinalizer.addSetting(SettingFinalizers)
                
    # Schedules a script to be run
    # Function (callable): The function running the script
    # Args (tuple): The args forthe function
    # Kwargs (dict): The kwargs for the function
    def scheduleScript(self, Function, Args = tuple(), Kwargs = dict()):
        self._scheduleQueue.call(Function, Args = Args, Kwargs = Kwargs, Wait = False)
        
    def killCurrentScript(self):
        self._scheduleQueue.killCurrent()
        
    # Prints to the consol when it is done with scripts
    def ping(self):
        self._scheduleQueue.call(print, Args = ("Pinged script scheduler",), Wait = False)
        
    # Gets the number of scripts in the queue
    def scriptQueueSize(self):
        return self._scheduleQueue.getSize()
    
    
# A class to keep all of the information about the lab
class lab(object):
    # EquipmentClass (equipment) The class initializer for the equipment
    # SetupClass (setup): The class initializer for the setup
    # EquipmentSettingName (str): The setting name for the new equipment
    # SetupSettingName (str): The setting name for the new setup
    # SetupSettings (setupSetting): The settings to run after initializing the setup
    # SetupHandlers (setupSettingHandler): The handlers for the setup settings
    # EquipmentKwargs (dict): kwargs to sent to the equipment
    # SetupKwargs (dict): kwargs to sent to the setup
    # Name (str): The name of the lab
    def __init__(self, EquipmentClass, SetupClass, *args, EquipmentSettingName = None, SetupSettingName = None, SetupSettings = None, SetupHandlers = None, EquipmentKwargs = dict(), SetupKwargs = dict(), Name = "lab", **kwargs):
        import weakref
        
        super().__init__(*args, **kwargs)
        
        # Initialize the equipment class
        if EquipmentSettingName is not None:
            EquipmentKwargs["SettingName"] = EquipmentSettingName
            
        self.equipment = EquipmentClass(**EquipmentKwargs)
        
        # Initialize the setup
        if SetupSettingName is not None:
            SetupKwargs["SettingName"] = SetupSettingName
            
        if SetupSettings is not None:
            SetupKwargs["Settings"] = SetupSettings
            
        if SetupHandlers is not None:
            SetupKwargs["SettingHandlers"] = SetupHandlers

        self.setup = SetupClass(self.equipment, **SetupKwargs)
        
        # Set the name
        self.name = str(Name)
        
        weakref.finalize(self, self.close)
                
    # Initializes a new setup
    # SetupClass (setup): The setup class initializer
    # SetupSettingName (str): The setting name for the new setup, if given and it is the same as the current setting, it will not reload
    # Settings (setupSetting): The settings to run after initializing the setup
    # SettingHandlers (setupSettingHandler): The handlers for the setup settings
    # Kwargs (dict): kwargs to sent to the setup
    # ForceReload (bool): If True then it will always reload no matter if it is the same setting
    def changeSetup(self, SetupClass, SetupSettingName = None, Settings = None, SettingHandlers = None, Kwargs = dict(), ForceReload = False):
        if not ForceReload and SetupSettingName is not None and SetupSettingName == self.setup.settingName:
            return
        
        # Remove old setup
        self.setup.close()
        
        # Add new one
        Kwargs = dict()
        if SetupSettingName is not None:
            Kwargs["SettingName"] = SetupSettingName
            
        if Settings is not None:
            Kwargs["Settings"] = Settings
            
        if SettingHandlers is not None:
            Kwargs["SettingHandlers"] = SettingHandlers
        
        self.setup = SetupClass(self.equipment, **Kwargs)
        
    # Locks all of the lasers
    def lock(self, **kwargs):
        self.setup.lock(**kwargs)
            
    # Unlocks all of the lasers
    def unlock(self):
        self.setup.unlock()
            
    # Turn off all lasers
    def disableLasers(self, **kwargs):
        self.setup.disableLasers(**kwargs)
        
    # Close all of the devices
    def close(self):
        self.setup.close()
        self.equipment.close()
