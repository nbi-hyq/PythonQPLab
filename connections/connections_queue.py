import threading as th
from .. import exceptions as e

# Implements a queue system while allowing plotting interactions by the user
class queue(th.Thread):
    # MaxLength (int): The maximum length of the queue
    # WaitInterval (float): The time in seconds to wait between checking for updates
    def __init__(self, *args, MaxLength = 1000, WaitInterval = 0.01, **kwargs):
        import weakref
        
        super().__init__(*args, **kwargs)
        
        self._alive = True
        self._size = int(MaxLength)
        self._q = [None] * int(MaxLength)
        self._getPos = 0
        self._putPos = 0
        self._waitTime = float(WaitInterval)
        
        self.start()
        weakref.finalize(self, self.kill)
        
    # Adds an item to the queue
    # Function (callable): The function to run
    # Args (tuple): The args of the function
    # Kwargs (dict): The kwargs for the function
    # Wait (bool): If True then it will wait until it has been processed and then return the return value, if False then it returns the ID
    def call(self, Function, Args = tuple(), Kwargs = dict(), Wait = True):
        if not self.is_alive():
            raise e.NotRunningError("Queue", self)

        Return = [None]

        # Make sure Function is a callable
        if not callable(Function):
            raise e.TypeDefError("Function", Function, "callable")
            
        Args = tuple(Args)
        Kwargs = dict(Kwargs)
        
        # Get the ID to put at
        ID = self._putPos
        
        if self._q[ID] is not None:
            raise e.QueueError()
        
        self._putPos = (self._putPos + 1) % self.size
        
        # Put the item
        self._q[ID] = (Function, Args, Kwargs, Return)
        
        # Wait
        if Wait:
            self.wait(ID)
            
        else:
            return ID
        
        # Check for error
        if Return[0][0]:
            return Return[0][1]
        
        else:
            raise Return[0][1]
            
    # Waits for an item to finish, still allows interactive plotting
    # ID (int): The ID of the item
    def wait(self, ID):
        from .. import functions as f
        
        while self._q[ID] is not None:
            f.time.sleep(self._waitTime)
            
    def run(self):
        import warnings
        from .. import functions as f
       
        while True:
            # If there is no task
            if self._q[self._getPos] is None:
                f.time.sleep(self._waitTime)
                continue
            
            # Run a taks
            Task = self._q[self._getPos]
            
            # Check if it should kill the queue
            if Task[0] == "kill":
                break
                
            # Run a function
            try:
                Result = Task[0](*Task[1], **Task[2])
                State = True
                
            except Exception as ErrorMes:
                Warn = e.PropagationError(ErrorMes, "processing an item in the queue")
                warnings.warn(Warn.message)
                Result = ErrorMes
                State = False
            
            # Send result
            Task[3][0] = (State, Result)

            # Mark the task as done
            self._q[self._getPos] = None
            self._getPos = (self._getPos + 1) % self._size
           
    # Kills the queue after finishing all tasks
    def kill(self):
        if self.isAlive():
            self._alive = False
            self.call("kill", Wait = False)
            
    # Checks if the queue is alive
    def isAlive(self):
        return self._alive and self.is_alive()
      
    # Returns the number of elements in the queue
    def getSize(self):
        Size = self._putPos - self._getPos
        
        if Size < 0:
            Size += self._size
            
        return Size


# A queue object for replacing queue if no new thread should be created
class queueNoThread:
    # MaxLength (int): The maximum length of the queue, kept for compatibility
    # WaitInterval (float): The time in seconds to wait between checking for updates, kept for compatibility
    def __init__(self, *args, MaxLength = 1000, WaitInterval = 0.01, **kwargs):
        import weakref
        
        super().__init__(*args, **kwargs)
        
        self._alive = True
        self._size = int(MaxLength)
        self._q = [None] * int(MaxLength)
        self._getPos = 0
        self._putPos = 0
        self._waitTime = float(WaitInterval)
        
        weakref.finalize(self, self.kill)
        
    # Adds an item to the queue
    # Function (callable): The function to run
    # Args (tuple): The args of the function
    # Kwargs (dict): The kwargs for the function
    # Wait (bool): If True then it will wait until it has been processed and then return the return value, if False then it returns the ID
    def call(self, Function, Args = tuple(), Kwargs = dict(), Wait = True):
        if not self.is_alive():
            raise e.NotRunningError("Queue", self)

        # Make sure Function is a callable
        if not callable(Function):
            raise e.TypeDefError("Function", Function, "callable")
            
        Args = tuple(Args)
        Kwargs = dict(Kwargs)
        
        # Handle error
        Result = Function(*Args, **Kwargs)
        
        # Wait
        if Wait:
            return Result
            
        else:
            return 0
            
    # Waits for an item to finish, still allows interactive plotting
    # ID (int): The ID of the item
    def wait(self, ID):
        pass
       
    # Kills the queue after finishing all tasks
    def kill(self):
        if self.isAlive():
            self._alive = False
            
    # Checks if the queue is alive
    def isAlive(self):
        return self._alive
      
    # Returns the number of elements in the queue
    def getSize(self):
        return 0
        