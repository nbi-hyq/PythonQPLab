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

