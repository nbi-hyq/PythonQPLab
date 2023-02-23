# Sleeps while still allowing plots to be controlled
# Time (float): The time to sleep, if negative or 0 then it will not sleep
def sleep(Time):
    import matplotlib.pyplot as plt
    import time
    import threading
    
    Time = float(Time)
    
    if Time <= 0:
        return
    
    if threading.current_thread() is threading.main_thread():
        plt.pause(Time)
        
    else:
        time.sleep(Time)
        
def getCurrentTime():
    from datetime import datetime
    
    Date = datetime.now().strftime("%Y%m%d")
    Time = datetime.now().strftime("%H%M%S")
    
    return f"{Date}_{Time}"