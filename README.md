# PythonQPLab

Lab control for quantum photonics labs

## Sub libraries

To use the library access the classes and functions with PythonQPLab.name like PythonQPLab.equipment to access equipment classes.

### loggers

This implements logging classes for now there is only a PID logger which will log the output and input of a PID periodically, plot it and write it to a file.

### plotting

This includeds different live plotting classes used for plotting histograms or normal plots live when doing measurements and optimizations.

### exceptions

This defines all the custom exceptions used in all the other libraries

### functions

This defines all the functions used for various tasks in the other libraries. This may include functions to check if the response from a device is correct and setting handlers

### connections 

This consists of a timer class, a queue class and classes for connecting with devices through serial, visa, dll, socket and an external library. Each connection class is using the same device backend which resends commands if it does not get the correct response from the device. It will make sure the device is still connected and flush the device if needed. It will also close the connection when the device object is detroyed.

### controllers

This consists of controller classes for specific device, these all inherit from one of the connection classes and implements methods which sends commands to the devices to do specific tasks.

### equipment

This defines classes which adds more functionality to several controllers like power and frequency controll for lasers, logging for PIDs and ssequence plotting for TimeBandit and AWG.

### lab

This implements classes to hold all the controllers and equipment, to allow for applying settings and automatically close all controllers whn destroying the lab class.

## Making changes

When making changes to this library remember to start by branching the git repository so you do not break other peoples experiments. Also test changes well before merging with the main branch. Whenever a change is made or functionality added please add it to the documentation and remember to add new classes in the \_\_init__.py scripts.

# Guide

This is a guide to how to use the module and how it works on the inside

## deviceBase

The connections.deviceBase class is the most simple class defining a device which any device should inherit from. It takes the initialization arguments "DeviceName" and "ID", the full device name will be f"{DeviceName} {ID}" or just DeviceName if ID is None. The name of the device will then be saved as the propert deviceName.
It also defines a method "isOpen" to check if the device is open, and a method "close" which will be run just before the object is destroyed. This method will call the "_close" method if the device is open, the functionality for closing the device should be implemented in "_close".

## device

The connections.device class is a bit more complex device class which inherits from deviceBase. This is meant as the base class for any device which communicates directly with some physical hardware over some connection. Any class inheriting from this must implement the methods: "open", "_reopen", "_close", "write", "read" and "flush" to access the device.
This class then implements a queue system which will send commands to the device allowing for multiple threads to use the same device at the same time. It also implements a "sendCommand" method which will send a command to the device. It will also reopen the device is it is no longer connected (USB will sometimes disconnect if it is idle) before sending a command, when sending a command it will make sure that the return message has the correct number of lines and format, and if it does not then it will flush the device and try again.

The classes "connections.serial", "connections.visa", "connections.socket", "connections.socketClient", "connections.dll" and "connections.external" all inherit from "connections.device" and implements their own connection type. "socket" is meant to connect to a random socket connection where "socketClient" is set up to connect to the "socketServer" defined here.

The "connections.socketServer" method is meant as an easy way to implement a socket server to communicate between 2 computers (replacing UDP from Matlab). To use this first set up the "connections.serverFunction" class and give this to the server. As an example say you have 2 lasers which can both be toggled on/off and where you can set and get the frequency:

Laser1FreqFunc = serverFunction(setFunction = Laser1SetFreq, GetFunction = Laser1GetFreq)
Laser2FreqFunc = serverFunction(setFunction = Laser2SetFreq, GetFunction = Laser2GetFreq)
Laser1Func = serverFunction(toggleFunction = Laser1Toggle, ParameterDict = {"freq": Laser1FreqFunc})
Laser2Func = serverFunction(toggleFunction = Laser2Toggle, ParameterDict = {"freq": Laser2FreqFunc})
LaserFunc = serverFunction(ParameterDict = {"laser1": Laser1Func, "laser2": Laser2Func})
Server = socketServer(6060, LaserFunc)

Now sending commands to the socket connection on port 6060 with the message "laser1.freq = 316.25" will run Laser1SetFreq(316.25), "laser2.freq?" will run Laser2GetFreq() and return the result and "laser1" will run Laser1Toggle()

## controllers

In the "controllers" library are all the controllers for the different devices. These controllers are meant to only send commands to the physical device and not do extra things like plotting, logging or locking, this should be implemented in the "equipment" library. Each class should initialize the device and implement methods like setting/getting laser frequency, moving rotation stage and so on. Each method should also include a **kwargs parameter which it will forward to the "sendCommand" method which will include the parameter "UseQueue" which is True by default. If set to False then it will skip the queue which is dangerous if using it on multiple threads.

## logging and plotting

The logging and plotting libraries include standard classes to log things in the background and do live plotting. These are just used to have standard ways of doing this so it does not need to be reimplemented every time.

## functions

The functions library includes all of the standard functions used in this module. The "responseCheck" functions are used in the controllers to let the "sendCommand" method know what response is expected and thereby letting it resend the command if the response was wrong. The "settingFinalizers" are functions used to finalize the setting files which can be useful when adding sequences to the settings like "Cooling_{Length}_{CoolingPower}" while being more flexible in how to change the parameters. "settingHandlers" are used to define how settings are to be interpreted and how to apply them. "socket" is used in the "connections.serverFunction" generation and "time" defines some functions related to the date and sleep commands.

## equipment

In this library we define more general controller classes. equipment classes should not communicate directly with devices but should use a controller object to access them. They will then add another layer on top like plotting sequences, locking power/frequency, logging PID input/output values and so on.

## lab

The lab library is the top layer. Here there are settings and lab control.

The setting class is meant to hold all settings which is applied or should be applied to the setup. It act kind of like a dictionary but with sub settings seperated byt dots. This could be something like:

"QWP1.position": 183,
"HWP1.position": 115,
"timeBandit.sequence": "default_{sequenceLength}",
"timeBandit.default.sequenceLength": 100,
"path2.frequency": 316.2725,
"path2.power": 6.5e-6

There would then have to be a setting handler for "QWP1", "HWP1", "timeBandit" and "path2" and a settingFinalizer for "timeBandit.sequence". Each element of the setting object will hold the value for that setting. There is also a settingHandler class and settingFinalizer class structured in the same way but instead of values they will hold the handlers and finalizers. The settings are then meant to be written into a JSON file which can be read and converted to a setting object and then applied to the setup. This is meant to avoid cluttering the code with parameters and collecting them in a place where it is easy to update something.

The lab control consists of 3 classes. The first is the equipment class. This is supposed to hold all of the controllers and nothing else. Then this can be initialized once when the python kernel is started and then not touched. The devices are initialized in the "init" method and each device must run through the "addDevice" method. Then once the equipment class is detroyed or the "close" method is run it will close all the devices.
The next class is the setup class which is given the equipment class when it initializes. This will then set up the equipment objects allowing for locking, plotting and logging and define all controllers used for a specific setup/experiment in the lab. The setup object can be destroyed and replaced by a new setup object without reinizialing the equipment object. Then the setup object is meant to be used in any script running an experiment. The setup object also allows for locking/unlocking all lasers at once, get the currently applied settings, apply new settings (without applying repeat settings) and schedule scripts to be run.
The final class is the lab class which simply holds the equipment and setup class in one position

## Setup and usage

To use this module we must first do some setup. To set it up you must create your own equipment, seetup and lab classes defining your lab, this is kind of like the init scripts in Matlab. One these has been defined then the setup is done. Now to use the module just create an intance of the lab class with the correct equipment and setup class and feed it a setting file to set all the correct values and it is ready to do a measurement. You can also have several setting files since when applying a setting it will not delete the old settings unless a new version of the same setting is applied. This way you could have a setting file with default settings and then several files with settings specific for various tasks
