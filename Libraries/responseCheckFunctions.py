# Response check functions

# The default response check function, returns False if the length of the ReturnString is 0, True otherwise
# Line (int): The line of the return string to check
def default(Line = 0):
    Line = int(Line)
    
    # Class (class): The class using this function
    # Command (str): The command string which was sent
    # ReturnString (str): The string returned from the device
    def responseCheck(Class, Command, ReturnString):
        if len(ReturnString[Line]) == 0:
            return "Did not receive any response"
        
        return None
    
    return responseCheck

# Checks that the return string is not NaN or inf
# Line (int): The line of the return string to check
def getValue(Line = 0):
    Line = int(Line)
    
    # Class (class): The class using this function
    # Command (str): The command string which was sent
    # ReturnString (str): The string returned from the device
    def responseCheck(Class, Command, ReturnString):
        import numpy as np
        
        # Get number
        try:
            Number = float(ReturnString[Line])
    
            if np.isfinite(Number):
                return None
        except:
            pass
        
        return f"Received illigal value: {ReturnString[Line]}"
    
    return responseCheck

# Checks that the return string is not NaN
# Line (int): The line of the return string to check
def getNumber(Line = 0):
    Line = int(Line)
    
    # Class (class): The class using this function
    # Command (str): The command string which was sent
    # ReturnString (str): The string returned from the device
    def responseCheck(Class, Command, ReturnString):
        import numpy as np
        
        # Get number
        try:
            Number = float(ReturnString[Line])
    
            if not np.isnan(Number):
                return None
        except:
            pass
        
        return f"Received illigal value: {ReturnString[Line]}"
    
    return responseCheck
    

# Checks that the return string is a bool
# Line (int): The line of the return string to check
def getBool(Line = 0):
    Line = int(Line)
    
    # Class (class): The class using this function
    # Command (str): The command string which was sent
    # ReturnString (str): The string returned from the device
    def responseCheck(Class, Command, ReturnString):
        # Get bool
        try:
            bool(ReturnString[Line])
            return None
        except:
            pass

        return f"Did not receive a bool: {ReturnString[Line]}"
    
    return responseCheck    

# Creates a response check function to check if values has been set correctly, returns the response check function
# Value (float): The value to check
# GetFunc (func): The function to get the value
# args (tuple): The args for the GetFunc function
# kwargs (dict): The kwargs for the GetFunc function
# Tol (float): The relative tolerance, must not be smaller than 0
def matchValue(Value, GetFunc, args = set(), kwargs = dict(), Tol = 0.01):
    Tol = float(Tol)
    
    if Tol < 0:
        raise Exception("Tolerance must not be negative")
        
    args = tuple(args)
    kwargs = dict(kwargs)
    Value = float(Value)

    # Checks if the values are the same, returns True if difference between the set and the true value are less than the tolerance, False otherwise
    # Class (class): The class using this function
    # Command (str): The command string which was sent
    # ReturnString (str): The string returned from the device
    def responseCheck(Class, Command, ReturnString):
        RecValue = float(GetFunc(*args, **kwargs))
        if abs(RecValue - Value) > Tol * abs(Value):
            return f"Value {RecValue} is outside the tolerance range of the correct value {Value}"
        
        return None
    
    return responseCheck

# Creates a response check function to check if a variable is set correctly, returns the response check function
# Value (any): The value to check
# GetFunc (func): The function to get the value
# args (tuple): The args for the GetFunc function
# kwargs (dict): The kwargs for the GetFunc function
def matchVar(Value, GetFunc, args = set(), kwargs = dict()):
    args = list(args)
    kwargs = dict(kwargs)
    
    # Checks if the values are the same, returns True if they are, False otherwise
    # Class (class): The class using this function
    # Command (str): The command string which was sent
    # ReturnString (str): The string returned from the device
    def responseCheck(Class, Command, ReturnString):
        Result = GetFunc(*args, **kwargs)
        if Result != Value:
            return "Received variable {Result} is not equal to the correct value {Value}"
        
        return None
    
    return responseCheck

# Creates a response check function to check if the return string has a specific value
# Value (str): The value to match with
# Line (int): The line of the return string to check
def matchReturn(Value, Line = 0):
    Value = str(Value)
    Line = int(Line)
    
    # Checks if the return string is Value
    # Class (class): The class using this function
    # Command (str): The command string which was sent
    # ReturnString (str): The string returned from the device
    def responseCheck(Class, Command, ReturnString):
        if ReturnString[Line] != Value:
            return f"Return string ({ReturnString[Line]}) is not correct ({Value})"
        
        return None
    
    return responseCheck


# Gives a response check function to check if the ReturnString is in a list of values, returns the response function
# List (list of str): The list to match with
# Line (int): The line of the return string to check
def inList(List, Line = 0):
    Line = int(Line)
    
    # Checks if the returnstring is in the list, returns true if ReturnString is in the list, False otherwise
    # Class (class): The class using this function
    # Command (str): The command string which was sent
    # ReturnString (str): The string returned from the device
    def responseCheck(Class, Command, ReturnString):
        if not ReturnString[Line] in List:
            return f"Return string ({ReturnString[Line]}) is not in the list {List}"
        
        return None
    
    return responseCheck

# Checks that the return string has the correct number of delimiters
# Count (int): The number of parts it should have
# Delimiter (str): The delimiter to split the parts
# Line (int): The line of the return string to use
def delimCount(Count, Delimiter = ":", Line = 0):
    Count = int(Count)
    Line = int(Line)
    Delimiter = str(Delimiter)
    
    # Checks that the return string has the correct number of delimiters
    # Class (class): The class using this function
    # Command (str): The command string which was sent
    # ReturnString (str): The string returned from the device
    def responseCheck(Class, Command, ReturnString):
        if len(ReturnString[Line].split(Delimiter)) != Count:
            return f"Return string ({ReturnString[Line]}) does not have the correct number of delimiters ({Delimiter})"
        
        return None
    
    return responseCheck

# Checks if a wavemeter got a correct response
# Line (int): The line of the return string to use
def wavemeter(Line = 0):
    Line = int(Line)
    
    # Checks that the result is a number and positive
    # Class (class): The class using this function
    # Command (str): The command string which was sent
    # ReturnString (str): The string returned from the device
    def responseCheck(Class, Command, ReturnString):
        import numpy as np
        
        Value = float(ReturnString[Line])
        
        if not np.isfinite(Value):
            return "Value {Value} is not a number"
        
        elif Value == -3:
            return "Wavemeter is underexposed"
        
        elif Value == -4:
            return "Wavemeter is overexposed"
        
        elif Value < 0:
            return "Received error message {Value} from wavemeter"
        
        return None
    
    return responseCheck

# Checks if a DLCPro got a correct response
def DLCPro():
    # Checks that no error code was received
    # Class (class): The class using this function
    # Command (str): The command string which was sent
    # ReturnString (str): The string returned from the device
    def responseCheck(Class, Command, ReturnString):
        ReturnString = ReturnString[0]
        
        # Make sure a response is present
        if len(ReturnString) == 0:
            return "Received no return value"
        
        # Remove it from ReturnString if possible
        if isinstance(ReturnString[0], str) and ReturnString[0] == Command:
            ReturnString = ReturnString[1:]
            
        # Make sure it does not say error
        if len(ReturnString[0]) >= 5 and ReturnString[0][:5] == "Error":
            return f"Returned error message: {ReturnString[0]}"
            
        # Make sure it got a status code
        if len(ReturnString) == 0:
            return "Received no status code"
        
        # Make sure there is no error
        if len(ReturnString) > 1:
            return ReturnString[1]
        
        return None
        
    return responseCheck

# Checks if a TimeBandit got a correct handshake
def timeBanditHandShake():
    # Checks that no error code was received
    # Class (class): The class using this function
    # Command (str): The command string which was sent
    # ReturnString (str): The string returned from the device
    def responseCheck(Class, Command, ReturnString):
        if ReturnString != b"\x01\x01":
            return f"Synchronization failed, received {ReturnString}"
        
        return None

    return responseCheck

# Checks if a TimeBandit set a byte correctly
def timeBanditUpdate():
    # Checks that no error code was received
    # Class (class): The class using this function
    # Command (str): The command string which was sent
    # ReturnString (str): The string returned from the device
    def responseCheck(Class, Command, ReturnString):
        if ReturnString != Command:
            return f"TimeBandit did not update memory ({str(Command)}) but returned with {str(ReturnString)}"
        
        return None

    return responseCheck

# Allows a socket client to check if an error occured
def socketClient(BaseResponseCheck):
    # Checks that no error code was received
    # Class (class): The class using this function
    # Command (str): The command string which was sent
    # ReturnString (str): The string returned from the device
    def responseCheck(Class, Command, ReturnString):
        if len(ReturnString) > 1:
            return "Received too many return strings"

        if len(ReturnString) == 0:
            return "Did not receive a return strings"
        
        # Split
        SplitString = ReturnString[0].split("|")
        
        if SplitString[0] != "1":
            Mes = "|".join(SplitString[1:])
            return f"An error occured: {Mes}"
        
        if BaseResponseCheck is None:
            return None
        
        return BaseResponseCheck(Class, Command, SplitString[1:])

    return responseCheck
   