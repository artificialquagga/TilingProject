import random

class Tile(): 
    def __init__(self, ID, width, height):
        self.x = 0
        self.y = 0
        self.ID = ID
        self.width = width
        self.height = height
        self.color = "#" + ("%06x" % random.randint(0, 16777215))
        self.possiblePositions = []
        self.placed = False
        self.flipped = False
    
    def getX(self): return self.x
    
    def getY(self): return self.y 
    
    def getID(self): return self.ID
    
    def getWidth(self): return self.width
    
    def getHeight(self): return self.height
    
    def getSurface(self): return (self.width * self.height)
    
    def getColor(self): return self.color
    
#    def __eq__(self, other): return self.args == other.args
    
    def compareTo(self, other): return self.getSurface() - other.getSurface()
    
    def flip(self): 
        self.width, self.height = self.height, self.width
        if self.flipped == False:
            self.flipped = True
        else: self.flipped = False
    
    def getFlipped(self): return self.flipped
    
    def setCoordinates(self, x, y): 
        self.x = x
        self.y = y
        
    def removeFirstPosition(self): self.possiblePositions.pop(0)
    
    def getPossiblePositions(self): return self.possiblePositions
    
    def addPossiblePosition(self, x, y, score, flipped): self.possiblePositions.append(((x, y), score, flipped))
    
    def placeThisTile(self): self.placed = True
    
    def removeThisTile(self): self.placed = False
    
    def getPlaced(self): return self.placed
    
    def sortPositions(self): self.possiblePositions = sorted(self.possiblePositions, key=lambda position: position[1], reverse=True)