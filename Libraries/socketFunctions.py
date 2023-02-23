# Functions for socket servers to make setting them up easier

# A wrapper function to add error identifiers for a socket server method, the new return value will be True, OldReturn
# Function (func): The function to wrap
def returnWrapper(Function):
    def Wrapper(*args, **kwargs):
        return True, str(Function(*args, **kwargs))
    
    return Wrapper

# A wrapper function to add error identifiers for a socket server info converter, the new return value will be True, OldReturn
# Function (func): The function to wrap
def infoWrapper(Function):
    def Wrapper(*args, **kwargs):
        return True, Function(*args, **kwargs)
    
    return Wrapper