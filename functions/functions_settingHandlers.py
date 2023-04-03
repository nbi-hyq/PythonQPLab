from .. import exceptions as e

# Creates a setting handler for a keithly
# Keithly (controllers.keithly): The keithly device to control
# Name (str): The name in from of each setting
# Overwrites (dict of list of str): A dict containing the lists of overwrites for each handler
# Pause (dict of floats): A dict containing the time to pause after setting each parameter, defaults to 0
def keithly(Keithly, Name = "", Overwrites = dict(), Pause = dict()):
    from .. import lab
    from .. import controllers as c
    
    if not isinstance(Keithly, c.keithly):
        raise e.TypeDefError("Keithly", Keithly, c.keithly)
    
    # Set up the handlers
    Handler = lab.settingHandler()
    
    # Set current limit
    Handler[f"{Name}currentLimit"] = lab.handle(f"{Name}currentLimit", Keithly.setCurrentLim, Overwrites = Overwrites.get("currentLimit", []), Pause = Pause.get("currentLimit", 0))
    
    # Set current range
    Handler[f"{Name}currentRange"] = lab.handle(f"{Name}currentRange", Keithly.setCurrentRange, Overwrites = Overwrites.get("currentRange", []), Pause = Pause.get("currentRange", 0))
    
    # Set voltage limit
    Handler[f"{Name}voltageLimit"] = lab.handle(f"{Name}voltageLimit", Keithly.setVoltageLim, Overwrites = Overwrites.get("voltageLimit", []), Pause = Pause.get("voltageLimit", 0))
    
    # Set voltage
    Handler[f"{Name}voltage"] = lab.handle(f"{Name}voltage", Keithly.setVoltage, Overwrites = Overwrites.get("voltage", []), Pause = Pause.get("voltage", 0))
    
    return Handler
    

# Creates a setting handler for a laser
# Laser (equipment.laser): The laser to control
# Lockable (bool): If false then it will not try to lock the frequence
# Name (str): The name in from of each setting
# Overwrites (dict of list of str): A dict containing the lists of overwrites for each handler
# Pause (dict of floats): A dict containing the time to pause after setting each parameter, defaults to 0
def laser(Laser, Lockable = True, Name = "", Overwrites = dict(), Pause = dict()):
    from .. import lab
    from .. import equipment as q

    if not isinstance(Laser, q.laser):
        raise e.TypeDefError("Laser", Laser, q.laser)
    
    # Set up the handlers
    Handler = lab.settingHandler()
    
    # Frequency
    def SetLaserFrequency(Value, **kwargs):
        Laser.setLaserFrequency(Value, **kwargs)
        Laser.setLockFrequency(Value)
    
    Handler[f"{Name}frequency"] = lab.handle(f"{Name}frequency", SetLaserFrequency, Overwrites = Overwrites.get("frequency", []), Pause = Pause.get("frequency", 0))
    
    # Activate
    def Activate(Value, **kwargs):
        if Lockable:
            if Value:
                Laser.lock(**kwargs)
                
            else:
                Laser.unlock()
            
    Handler[f"{Name}active"] = lab.handle(f"{Name}active", Activate, Overwrites = Overwrites.get("active", []), Pause = Pause.get("active", 0))
        
    return Handler


# Creates a setting handler for a power controller
# PowerControl (equipment.powerControl): The power controller to control
# Name (str): The name in from of each setting
# Overwrites (dict of list of str): A dict containing the lists of overwrites for each handler
# Pause (dict of floats): A dict containing the time to pause after setting each parameter, defaults to 0
def power(PowerControl, Name = "", Overwrites = dict(), Pause = dict()):
    from .. import lab
    from .. import equipment as q

    if not isinstance(PowerControl, q.powerControl):
        raise e.TypeDefError("PowerControl", PowerControl, q.powerControl)
    
    # Set up the handlers
    Handler = lab.settingHandler()
    
    # Power
    def SetPower(Value, **kwargs):
        PowerControl.setSetPower(Value)
        
    Handler[f"{Name}power"] = lab.handle(f"{Name}power", SetPower, Overwrites = Overwrites.get("power", []), Pause = Pause.get("power", 0))
    
    # Activate
    def Activate(Value, **kwargs):
        if Value:
            PowerControl.lock(**kwargs)
            
        else:
            PowerControl.unlock(**kwargs)
            
    Handler[f"{Name}active"] = lab.handle(f"{Name}active", Activate, Overwrites = Overwrites.get("active", []), Pause = Pause.get("active", 0), Order = 0)
    
    return Handler


# Creates a setting handler for a power controlled laser
# Laser (equipment.powerControlledLaser): The laser to control
# Lockable (bool): If false then it will not try to lock the frequence
# Name (str): The name in from of each setting
# Overwrites (dict of list of str): A dict containing the lists of overwrites for each handler
# Pause (dict of floats): A dict containing the time to pause after setting each parameter, defaults to 0
def PCLaser(Laser, Lockable = True, Name = "", Overwrites = dict(), Pause = dict()):
    from .. import lab
    from .. import equipment as q

    if not isinstance(Laser, q.powerControlledLaser):
        raise e.TypeDefError("Laser", Laser, q.powerControlledLaser)
    
    # Set up the handlers
    Handler = lab.settingHandler()
    
    # Frequency
    def SetLaserFrequency(Value, **kwargs):
        Laser.laser.setLockFrequency(Value)
            
    Handler[f"{Name}frequency"] = lab.handle(f"{Name}frequency", SetLaserFrequency, Overwrites = Overwrites.get("frequency", []), Pause = Pause.get("frequency", 0))
    
    # Power
    def SetPower(Value, **kwargs):
        Laser.power.setSetPower(Value)
        
    Handler[f"{Name}power"] = lab.handle(f"{Name}power", SetPower, Overwrites = Overwrites.get("power", []), Pause = Pause.get("power", 0))
    
    # Lock
    def Activate(Value, **kwargs):
        if Value:
            if Lockable:
                Laser.laser.lock(**kwargs)
            Laser.power.lock(**kwargs)
            
        else:
            if Lockable:
                Laser.laser.unlock()
            Laser.power.unlock(**kwargs)
            
    Handler[f"{Name}active"] = lab.handle(f"{Name}active", Activate, Overwrites = Overwrites.get("active", []), Pause = Pause.get("active", 0), Order = 0)
    
    return Handler
    
    
# Creates a setting handler for a rotation stage
# RotationStage (controllers.rotationStage): The stage to control
# Name (str): The name in from of each setting
# Overwrites (dict of list of str): A dict containing the lists of overwrites for each handler
# Pause (dict of floats): A dict containing the time to pause after setting each parameter, defaults to 0
def rotationStage(RotationStage, Name = "", Overwrites = dict(), Pause = dict()):
    from .. import lab
    from .. import interface

    if not isinstance(RotationStage, interface.rotationStage):
        raise e.TypeDefError("RotationStage", RotationStage, interface.rotationStage)
    
    # Set up the handlers
    Handler = lab.settingHandler()
    
    # Zero position
    def setZeroPos(Value, **kwargs):
        RotationStage.setZero(Value)
    
    Handler[f"{Name}zeroPosition"] = lab.handle(f"{Name}zeroPosition", setZeroPos, Overwrites = Overwrites.get("zeroPosition", []), Pause = Pause.get("zeroPosition", 0))
    
    # Position
    Handler[f"{Name}position"] = lab.handle(f"{Name}position", RotationStage.moveTo, Overwrites = Overwrites.get("position", []), Pause = Pause.get("position", 0))
    
    return Handler
  

# Creates a setting handler for a time tagger
# TimeTagger (controllers.timeTagger): The time tagger to control
# ChannelCount (int): The number of channels accessable
# Name (str): The name in from of each setting
# Overwrites (dict of list of str): A dict containing the lists of overwrites for each handler
# Pause (dict of floats): A dict containing the time to pause after setting each parameter, defaults to 0
def timeTagger(TimeTagger, ChannelCount, Name = "", Overwrites = dict(), Pause = dict()):
    from .. import lab
    from .. import controllers as c
    
    if not isinstance(TimeTagger, c.swabianTimeTagger):
        raise e.TypeDefError("TimeTagger", TimeTagger, c.swabianTimeTagger)
    
    # Set up the handlers
    Handler = lab.settingHandler()
    
    # Default channel
    Handler[f"{Name}channel"] = lab.handle(f"{Name}channel", TimeTagger.setDefaultChannel, Overwrites = Overwrites.get("channel", []), Pause = Pause.get("channel", 0))
    
    # Default integration time
    Handler[f"{Name}integrationTime"] = lab.handle(f"{Name}integrationTime", TimeTagger.setDefaultIntegrationTime, Overwrites = Overwrites.get("integrationTime", []), Pause = Pause.get("integrationTime", 0))
    
    # Clock channel
    Handler[f"{Name}clockChannel"] = lab.handle(f"{Name}clockChannel", TimeTagger.setClockChannel, Overwrites = Overwrites.get("clockChannel", []), Pause = Pause.get("clockChannel", 0))
    
    # Bin width
    Handler[f"{Name}binWidth"] = lab.handle(f"{Name}binWidth", TimeTagger.setBinWidth, Overwrites = Overwrites.get("binWidth", []), Pause = Pause.get("binWidth", 0))    
    
    # Correlation bins
    Handler[f"{Name}correlationBins"] = lab.handle(f"{Name}correlationBins", TimeTagger.setDefaultCorrelationBins, Overwrites = Overwrites.get("correlationBins", []) + [f"{Name}correlationTime"], Pause = Pause.get("correlationBins", 0))    
    
    # Correlation time
    def SetCorrelationTime(Value, **kwargs):
        # Get the bin width
        BinWidth = TimeTagger.getBinWidth(**kwargs) * 1e-3
        
        # Set the correlation bins
        TimeTagger.setDefaultCorrelationBins(float(Value) / BinWidth, **kwargs)
    
    Handler[f"{Name}correlationTime"] = lab.handle(f"{Name}correlationTime", SetCorrelationTime, Overwrites = Overwrites.get("correlationTime", []) + [f"{Name}correlationBins"], Pause = Pause.get("correlationTime", 0))    
    
    # The channels
    for i in range(1, ChannelCount + 1):
        # Trigger level
        def setTriggerLevel(Channel):
            def function(Value, **kwargs):
                TimeTagger.setTriggerLevel(Channel, Value, **kwargs)
            return function
                
        Handler[f"{Name}CH{i}.triggerLevel"] = lab.handle(f"{Name}CH{i}.triggerLevel", setTriggerLevel(i), Overwrites = Overwrites.get(f"CH{i}.triggerLevel", []), Pause = Pause.get(f"CH{i}.triggerLevel", 0))
    
        # Trigger mode
        def setTriggerMode(Channel):
            def function(Value, **kwargs):
                TimeTagger.setTriggerMode(Channel, Value, **kwargs)
            return function
                
        Handler[f"{Name}CH{i}.triggerMode"] = lab.handle(f"{Name}CH{i}.triggerMode", setTriggerMode(i), Overwrites = Overwrites.get(f"CH{i}.triggerMode", []), Pause = Pause.get(f"CH{i}.triggerMode", 0))
    
        # Dead time
        def setDeadTime(Channel):
            def function(Value, **kwargs):
                TimeTagger.setDeadTime(Channel, Value, **kwargs)
            return function
        
        Handler[f"{Name}CH{i}.deadTime"] = lab.handle(f"{Name}CH{i}.deadTime", setDeadTime(i), Overwrites = Overwrites.get(f"CH{i}.deadTime", []), Pause = Pause.get(f"CH{i}.deadTime", 0))
    
        # Input delay
        def setDelay(Channel):
            def function(Value, **kwargs):
                TimeTagger.setChannelDelay(Channel, Value, **kwargs)
            return function
        
        Handler[f"{Name}CH{i}.delay"] = lab.handle(f"{Name}CH{i}.delay", setDelay(i), Overwrites = Overwrites.get(f"CH{i}.delay", []), Pause = Pause.get(f"CH{i}.delay", 0))
    
    return Handler
    

# Creates a setting handler for a SNSPD
# SNSPD (controllers.SNSPD): The SNSPD device to control
# ChannelCount (int): The number of channels accessable
# Name (str): The name in from of each setting
# Overwrites (dict of list of str): A dict containing the lists of overwrites for each handler
# Pause (dict of floats): A dict containing the time to pause after setting each parameter, defaults to 0
def photonSpot(SNSPD, ChannelCount, Name = "", Overwrites = dict(), Pause = dict()):
    from .. import lab
    from .. import controllers as c
    
    if not isinstance(SNSPD, c.photonSpot):
        raise e.TypeDefError("SNSPD", SNSPD, c.photonSpot)
    
    # Set up the handlers
    Handler = lab.settingHandler()
    
    # Set the bias current
    for i in range(1, ChannelCount + 1):
        def setBiasCurrent(Channel):
            def function(Value, **kwargs):
                SNSPD.setBias(Channel, Value, **kwargs)
            return function
            
        Handler[f"{Name}{i}.bias"] = lab.handle(f"{Name}{i}.bias", setBiasCurrent(i), Overwrites = Overwrites.get(f"{i}.bias", []), Pause = Pause.get(f"{i}.bias", 0))
    
    return Handler


# Creates a setting handler for a timeBandit FPGA
# FPGA (equipment.timeBandit): The FPGA object
# Sequences (dict): Dictionary with all the possible sequences
# SequenceArgs (tuple): The first arguments to give the sequence function 
# Name (str): The name in from of each setting
# Overwrites (dict of list of str): A dict containing the lists of overwrites for each handler
# Pause (dict of floats): A dict containing the time to pause after setting each parameter, defaults to 0
def timeBandit(FPGA, Sequences, SequenceArgs = tuple(), Name = "", Overwrites = dict(), Pause = dict()):
    from .. import lab
    from .. import equipment as q
    
    if not isinstance(FPGA, q.timeBandit):
        raise e.TypeDefError("FPGA", FPGA, q.timeBandit)
        
    # Set up the handlers
    Handler = lab.settingHandler()
    
    # Set the sequence
    def setSequence(Value, **kwargs):
        SplitValue = str(Value).split("_")
        Sequences[SplitValue[0]](*SequenceArgs, *SplitValue[1:]).apply(**kwargs)
        FPGA.show()
        
    Handler[f"{Name}.sequence"] = lab.handle(f"{Name}.sequence", setSequence, Overwrites = Overwrites.get("sequence", []), Pause = Pause.get("sequence", 0))

    return Handler


# Creates a setting handler for a timeBandit FPGA
# Device (equipment.AWG): The AWG object
# Sequences (dict): Dictionary with all the possible sequences
# SequenceArgs (tuple): The first arguments to give the sequence function 
# Name (str): The name in from of each setting
# Overwrites (dict of list of str): A dict containing the lists of overwrites for each handler
# Pause (dict of floats): A dict containing the time to pause after setting each parameter, defaults to 0
def AWG(Device, Sequences, SequenceArgs = tuple(), Name = "", Overwrites = dict(), Pause = dict()):
    from .. import lab
    from .. import equipment as q
    
    if not isinstance(Device, q.AWG):
        raise e.TypeDefError("Device", Device, q.AWG)
        
    # Set up the handlers
    Handler = lab.settingHandler()
    
    # Set the sequence
    def setSequence(Value, **kwargs):
        SplitValue = str(Value).split("_")
        Sequences[SplitValue[0]](*SequenceArgs, *SplitValue[1:]).apply(**kwargs)
        Device.show()
        
    Handler[f"{Name}.sequence"] = lab.handle(f"{Name}.sequence", setSequence, Overwrites = Overwrites.get("sequence", []), Pause = Pause.get("sequence", 0))

    return Handler


# Gets a sub dict, extracts all items from a dict with key starting with Name and saves them in a new dict with the remainder of the key as the new key
# Dict (dict): The dictionary to look through
# Name (str): The name to be at the start of the keys to extract
def getSubDict(Dict, Name):
    Length = len(Name)
    return dict([(Key[Length:], Item) for Key, Item in Dict.items() if Key[:Length] == Name])
