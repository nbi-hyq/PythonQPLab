import threading as th

class timerObj(th.Thread):
    # Initialise a timer object
    # Interval (float): The number of seconds between each function call
    # Function (func): The function to call every interval, the first argument must be the counter
    # Event (threading.Event): The stop event to stop the timer
    # FunctionArgs (set): The args to pass Function
    # FunctionKwargs (dict): The kwargs to pass Function
    def __init__(self, Interval, Function, Event, *args, FunctionArgs = set(), FunctionKwargs = dict(), **kwargs):
        super().__init__(*args, **kwargs)
    
        # Setup the event
        self._stopEvent = Event
        
        # Setup the interval and function
        self._int = float(Interval)
        self._f = Function
        self._args = FunctionArgs
        self._kwargs = FunctionKwargs
        
        # The count will increase by one everytime it is run
        self._count = 0
        
    # run the timer
    def run(self):
        import time
        import warnings
        
        # Record the start time
        StartTime = time.time()
        
        # Run the timer
        while not self._stopEvent.wait(max(StartTime + self._int * self._count - time.time(), 0)):
            # Run the function
            try:
                self._f(self._count, *self._args, **self._kwargs)
            
            except Exception as ErrorMes:
                # Print the error
                Mes = f"An exception occured in timer as count {self._count}: {ErrorMes}"
                warnings.warn(Mes)

            # Increase the count
            self._count += 1
            
    
class timer(object):
    # Initialize a timer which runs runs Function every Interval seconds
    # Interval (float): The number of seconds between each function call
    # Function (func): The function to call every interval, the first argument must be the counter   
    # TimerKwargs may include:
    # FunctionArgs (set): The args to pass Function
    # FunctionKwargs (dict): The kwargs to pass Function
    def __init__(self, Interval, Function, *args, TimerKwargs = dict(), **kwargs):
        import weakref
        
        super().__init__(*args, **kwargs)
        
        # Create the timer object
        self._stopEvent = th.Event()
        
        self._timer = timerObj(Interval, Function, self._stopEvent, **TimerKwargs)
        
        weakref.finalize(self, self.stop)
        
    # Starts the timer
    def start(self):
        self._timer.start()
        
    # Stops the timer
    def stop(self):
        self._stopEvent.set()
