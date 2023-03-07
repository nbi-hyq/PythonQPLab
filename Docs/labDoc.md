# Documentation for lab

This is a collection of generic classes used to define a lab

---
---

# Classes

---

## equipment(SettingName = "default", Tags = [])

A class to hold all of the equipment for the lab, this should be created once when the computer is booted or it needs to reload. It should hold controllers for every piece of equipment present in the lab. Equipment can be accessed directly with .EquipmentName or with the findDevice method

- SettingName (str): The ID of the settings this equipment class initializes
- Tags (list of str): A list of tags which this object has, it must have all tags of any setup that you want to combine it with

---

### method init()

Initializes all of the devices, this should be overwritten by a subclass, for each equipment controller you should add the following

self.controllerName = ControllerClass(Args, Kwargs = something, DeviceName = "UniqueDeviceName")
self.addDevice(self.controllerName)

Remember to add a unique DeviceName since findDevice finds the devices based on their names

---

### method findTag(Tag)

Checks if this class has a specific tag

- Tag (str): The tag to check if exists

Returns True if the Tag is in the tag list, False otherwise

---

### method addTag(Tag)

Adds a tag to this class

- Tag (str): The tag to add

---

### method addDevice(Device, Ignore = False)

Add any device

- Device (connections.deviceBase): The device to add
- Ignore (bool): If True then it will not close this device

---

### method findDevice(Name)

Find any device

- Name (str): The name of the device to find

Returns the device, raises an exception if it is not found

---

### method close()

Closes all of the devices

---

### method isOpen()

Checks if the devices are open

Returns True when they are and False otherwise

---

### property setting (str)

The setting of this object

---

### property tags (list of str)

The tags of this object

---

### property devices (list of connections.deviceBase)

The list of devices

---
---

## setup(Equipment, SettingName = "default", Tags = [])

A setup class for a specific configuration of the lab, the equipment object must be created first and then scripts should run equipment through the setup object instead of the equipment object. Setup does not do anything to the controllers and can just be reloaded whenever or changed out. Preferably a new setup class is created for each type of experiment

- Equipment (equipment): The devices of the lab
- SettingName (str): The ID of the settings of this class
- Tags (list of str): A list of all the tags the Equipment must possess

---

### method init(Equipment)

Initializes all of the devices, this should be overwritten by a subclass, for each equipment controller you should add the following

self.deviceName = DeviceClass(Args, Kwargs = something, DeviceName = "UniqueDeviceName")
self.addDevice(self.deviceName)

and also if it is a laser/powerControl you should add

self.addLaser(self.deviceName)/self.addPowerControl(self.deviceName)

Remember to add a unique DeviceName since findDevice/findLaser/findPowerControl finds the devices based on their names

- Equipment (equipment): The equipment object to get controllers from

---

### method addDevice(Device, Ignore = False)

Add any device

- Device (connections.deviceBase): The device to add
- Ignore (bool): If True then it will not close this device

---

### method findDevice(Name)

Find any device

- Name (str): The name of the device to find

Returns the device, raises an exception if it is not found

---

### method addLaser(Laser)

Adds a laser to the laser list

- Laser (equipment.laser): The laser to add

---

### method getLaser(Name)

Gets a laser from the laser list

- Name (str): The name of the laser

Returns the laser

---

### method addPowerControl(PowerControl)

Adds a power controller to the PowerControl list

- PowerControl (equipment.powerControl): The power controller to add

---

### method getPowerControl(Name)

Gets a power controller from the PowerControl list

- Name (str): The name of the power controller

Returns the power controller

---

### method lock(UseQueue = True)

Locks all of the lasers

- UseQueue (bool): Whether to run the command through the queue or not, ignored if the device was initialized with UseQueue = False

---

### method unlock()

Unlocks all of the lasers

---

### method disableLasers(UseQueue = True)

Turns all of the power controllers off

- UseQueue (bool): Whether to run the command through the queue or not, ignored if the device was initialized with UseQueue = False

---

### method getSetting(Name)

Gets a single setting for this setup

- Name (str): The name of the setting

Returns the setting

---

### method getSettings()

Gets all the settings for this setup

Returns the settings as a setupSetting

---

### method getAppliedSetting(Name)

Gets a single applied setting for this setup

- Name (str): The name of the setting

Returns the setting

---

### method getAppliedSettings()

Gets all the applied settings for this setup

Returns the settings as a setupSetting

---

### method applySetting(Name, Value, Reload = False, UseQueue = True)

Applies a single setting

- Name (str): The name of the setting
- Value (any): The value of the setting
- Reload (bool): If True then it will apply it even if it has already been applied
- UseQueue (bool): Whether to run the command through the queue or not, ignored if the device was initialized with UseQueue = False

---

### method applySettings(Settings, Reload = False, UseQueue = True)

Applies a setting to the setup

- Settings (setting): The settings to apply to the setup
- Reload (bool): If True then it will apply it even if it has already been applied
- UseQueue (bool): Whether to run the command through the queue or not, ignored if the device was initialized with UseQueue = False

---

### method postProcessSettings()

Applies the settings which has an order, not needed if settings were applied with applySettings

---

### method loadSettings(Path, Relative = True, UseQueue = True)

Load settings from a file and apply them

- Path (str): The path of the file
- Relative (bool): If True then the path will be relative to the current directory
- UseQueue (bool): Whether to run the command through the queue or not, ignored if the device was initialized with UseQueue = False

---

### method addSettingHandler(Name, Function)

Add a single setting handler

- Name (str): The name of the handler
- Function (callable): The function to run when handling, should take arguments (Input, UseQueue = True)

---

### method addSettingHandlers(SettingHandlers, PreName = "")

Adds setting handlers

- SettingHandlers (settingHandler): The handlers to add
- PreName (str): The name of the handlers this is a sub handle of

---

### method addSettingFinalizer(Name, FinalizerFunction)

Add a single setting finalizer

- Name (str): The name of the finalizer
- FinalizerFunction (callable): The finalizer function to add, must take the arguments: Value (any): The value from the settings, Key (str): The key which retrieved this value, Settings (setting): The settings to finalize and return the new value for that key

---

### method addSettingFinalizers(self, SettingFinalizers)

Adds setting finalizers

- SettingFinalizers (setupSettingHandler): The finalizers to add

---

### method scheduleScript(Function, Args = tuple(), Kwargs = dict())

Schedules a script to be run

- Function (callable): The function running the script
- Args (tuple): The args for the function
- Kwargs (dict): The kwargs for the function

---

### method ping()

Prints to the consol when it is done with scripts

---

### method scriptQueueSize()

Gets the number of scripts in the queue

Returns the number of elements in the queue as an int

---

### property lasers (list of equipment.laser)

The list of lasers

---

### property powers (list of equipment.powerControl) 

The list of power controllers

---

### property devices (list of equipment.deviceBase)

The list of devices

---
---

## lab(EquipmentClass, SetupClass, EquipmentSettingName = None, SetupSettingName = None, SetupSettings = None, SetupHandlers = None, EquipmentKwargs = dict(), SetupKwargs = dict(), Name = "lab")

A class to keep all of the information about the lab, should be run once after a computer boot or when reloading equipment

- EquipmentClass (equipment) The class initializer for the equipment
- SetupClass (setup): The class initializer for the setup
- EquipmentSettingName (str): The setting name for the new equipment
- SetupSettingName (str): The setting name for the new setup
- SetupSettings (setupSetting): The settings to run after initializing the setup
- SetupHandlers (setupSettingHandler): The handlers for the setup settings
- EquipmentKwargs (dict): kwargs to sent to the equipment
- SetupKwargs (dict): kwargs to sent to the setup
- Name (str): The name of the lab

---

### method changeSetup(SetupClass, SetupSettingName = None, Settings = None, SettingHandlers = None, Kwargs = dict(), ForceReload = False)

Initializes a new setup

- SetupClass (setup): The setup class initializer
- SetupSettingName (str): The setting name for the new setup, if given and it is the same as the current setting, it will not reload
- Settings (setupSetting): The settings to run after initializing the setup
- SettingHandlers (setupSettingHandler): The handlers for the setup settings
- Kwargs (dict): kwargs to sent to the setup
- ForceReload (bool): If True then it will always reload no matter if it is the same setting

---

### method lock(UseQueue = True)

Locks all of the lasers

- UseQueue (bool): Whether to run the command through the queue or not, ignored if the device was initialized with UseQueue = False

---

### method unlock()

Unlocks all of the lasers

---

### method disableLasers(UseQueue = True)

Turns all of the power controllers off

- UseQueue (bool): Whether to run the command through the queue or not, ignored if the device was initialized with UseQueue = False

---

### method close()

Close equipment and setup

---

### property equipment (equipment)

The equipment object for the lab

---

### property setup (setup)

The setup object for the lab

---

### property name (str)

The name of the lab

---
---

## basicSetting()

A base setting class

Can set an item with
Settings = setupSetting()
Settings[ID] = Value

ID can be separeted by dots Field1.Field2

Items can also be retrieved with the same ID

If ID is given as "name1.name2" then it will save a subsetting saved as "name1" with "name2" inside

It can also be iterated through, in this case it will iterate through the result of the toDict method

---

### classmethod fromDict(Dict)

Creates a new object from a dict

- Dict (dict): The dict to load from

Returns a new instance with the settings

---

###  method copy()

Copies the settings

Returns a new setting with the copied values

---

### method getBranch(ID)

Gets an item from the dict, may return a sub setting

- ID (str): The ID of the branch or item

Returns the result

---

### method removeItem(ID)

Removes an item if it exists, does nothing if the item does not exist

- ID (str): The ID of the item

---

### method addSetting(Setting)

Merges another setting with this, the new one will overwrite

- Setting (baseSetting): The setting to add

---

### method toDict()

Converts the setting to a dict with keys given as "field.field.field.name"

Returns the resulting dict

---

### method loadDict(Dict)

Creates the settings from a dict

- Dict (dict): The dict to convert from

---
---

## setting()

A setup settings class holding information about the settings applied to a setup

Inherits from basicSetting

---

### classmethod fromJSON(Path, Relative = True)

Creates a new setting object and imports settings from a file

- Path (str): The path of the settings file, .json is append if an exgtension is not given
- Relative (bool): If True then the path will be relative to the current directory

---

### method save(Path, Overwrite = False, MaxAttempts = 100)

Saves the setup to a file, it will append .json if an extension is not given

- Path (str): The path to save to
- Overwrite (bool): If False then it will append _[NUM] to the file if it already exists
- MaxAttempts (int): The max number it will attempt to append to the file name before giving up

---

### method load(Path, Relative = True)

Load settings from a file

- Path (str): The path for the file
- Relative (bool): If True then the path will be relative to the current directory

---
---

## settingHandler()

Holds functions to handle any setting

Only handle objects can be saved in this

Inherits from basicSetting

---

### method process(AppliedSettings, ID, Value, UseQueue = True)

Process an item

- AppliedSettings (setting): The settings to store the applied value
- ID (str/setting): The ID or setting to handle
- Value (any): The value of the setting to handle
- UseQueue (bool): Whether to run the command through the queue or not, ignored if the device was initialized with UseQueue = False

---

### method processSettings(AppliedSettings, Settings, UseQueue = True)

Processes everything in some settings

- AppliedSettings (setting): The settings to store the applied value
- Settings (setting): The settings to process
- UseQueue (bool): Whether to run the command through the queue or not, ignored if the device was initialized with UseQueue = False

### method postProcess()

Applies all the settings with a specific order

---
---

## handle(Key, Function, Overwrites = [], Order = None)

A handle for handling a setting

- Key (str): The key for this handle
- Function (callable): The function to run the handle, must take inputs (Value, UseQueue = True)
- Overwrites (list of str): A list of all the settings to delete when handling a setting
- Order (int): If not None then it will wait until the end of the settings and then apply all the rest in order from lowest to highest

---

### method process(Settings, Value, UseQueue = True)

Processes an item

- Settings (setting): The applied settings
- Value and kwargs are passed to the function
- UseQueue (bool): Whether to run the command through the queue or not, ignored if the device was initialized with UseQueue = False

Returns (None, None) if Order is None and if Order is an int then it returns (HandleFunc, Order) and does not process the item yet

---
---

## settingFinalizer()

Holds functions to handle any setting
Any item must be a function taking the arguments: Value (any): The value from the settings, Key (str): The key which retrieved this value, Settings (setting): The settings to finalize
It must return the new value for that key

Inherits from basicSetting

---

### method process(Settings)

Finalizes a setting

- Settings (setting): The settings to process

---
---