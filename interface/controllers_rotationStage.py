from .. import exceptions as e   

# A generic rotation stage controller
class rotationStage:   
    # Homes the device     
    def home(self):
        raise e.ImplementationError("rotationStage.home")
    
    # Moves the device to a specified position
    # Position (float): The position to set
    def moveTo(self, Position):
        raise e.ImplementationError("rotationStage.moveTo")
    
    # Gets the current position of the rotation stage
    def getPosition(self):
        raise e.ImplementationError("rotationStage.getPosition")
    
    # Moves the rotation stage relative to its original position
    # Distance (float): The distance it should move by
    def move(self, Distance, **kwargs):
        # Get new position
        Pos = self.getPosition(**kwargs) + Distance
        
        # Move
        self.moveTo(Pos, **kwargs)
        