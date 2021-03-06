import os, sys, time
sys.setrecursionlimit(200000)
os.chdir("../Configurations")

from tilingObjects.Version1Tile import Tile
from tiling.FieldFrame import FieldFrame
from tiling.Version1Field import Field

class Assignment(object):
    
    def __init__(self, configuration):
        self.CONFIGURATION = configuration
        self.steps = 0
        self.maxFilledPercentage = 0
        self.maxfilledStep = 0
        i = 1
        for idx, each_line in enumerate(open(self.CONFIGURATION, 'r')):
            if idx == 0:
                width, height, scale = map(int, each_line.strip().split("\t"))
                self.field = Field(width, height)
                #self.frame = FieldFrame(self.field, scale)
            else: 
                frequency, width, height = map(int, each_line.strip().split("\t"))
                for idx in range(frequency):
                    tile = Tile(i, width, height)
                    self.field.addTile(tile, False, tile.getSurface())
                    i += 1 #tileID
        
        self.recursivePlacing()
                
    def recursivePlacing(self):
        filledPercentage = self.field.getFilledPercentage()
        if filledPercentage > self.maxFilledPercentage:
            self.maxFilledPercentage = filledPercentage
            self.maxfilledStep = self.steps
        if self.steps == 20000:
            print "Puzzle %s not solved in %d steps, this took %.3f seconds. %.2s percent of the field has been filled at step %d." % (self.CONFIGURATION, self.steps, (time.time() - start_time), self.maxFilledPercentage,self.maxfilledStep)
            return
        if self.field.solved(): 
            print "Puzzle %s solved in %d steps, this took %.3f seconds." % (self.CONFIGURATION, self.steps, (time.time() - start_time))
            return
              
        self.field.sortTileset() #sorts tileSet based on placed boolean and tile surface
        instance = self.field.getTiles()[0] #get the first tile from the tileset, not placed and biggest surface
        tile = instance[0]
        if tile.getPlaced() == False: #if the tile in not on the field yet (=True when backtracking)
            if tile.getFlipped() == True:
                tile.flip()
            for x in range(self.field.getWidth()): #determine available positions for the tile
                for y in range(self.field.getHeight()):
                    if self.field.inRange(tile, x, y):
                        tile.addPossiblePosition(x, y, False)
            if (tile.getWidth() != tile.getHeight()):
                tile.flip()
                for x in range(self.field.getWidth()): #determine available positions for the flipped tile
                    for y in range(self.field.getHeight()):
                        if self.field.inRange(tile, x, y):
                            tile.addPossiblePosition(x, y, True)
                tile.flip()

        if tile.getPossiblePositions() == []: #if the tile cannot be placed anywhere
            lastPlacedID = self.field.getLastPlacedID()
            for instance in self.field.getTiles():
                tile = instance[0]
                if tile.getID() == lastPlacedID:
                    lastPlacedTile = tile
            if lastPlacedTile.getPossiblePositions() != []:
                lastPlacedTile.removeFirstPosition()
            self.field.removeTile(lastPlacedTile)
            #self.frame.repaint(self.field)
            while lastPlacedTile.getPossiblePositions() == []: #if the last placed tile cannot be placed anywhere else
                lastPlacedTile.removeThisTile()
                self.field.sortTileset()
                lastPlacedID = self.field.getLastPlacedID()
                for instance in self.field.getTiles():
                    tile = instance[0]
                    if tile.getID() == lastPlacedID:
                        lastPlacedTile = tile
                if lastPlacedTile.getPossiblePositions() != []:
                    lastPlacedTile.removeFirstPosition()
                self.field.removeTile(lastPlacedTile)
                #self.frame.repaint(self.field)
            self.steps += 1
            self.recursivePlacing()
            return
        
        tile.sortPositions() #sort positions based on the adjacent side scores
        
        for position in tile.getPossiblePositions(): #determine position for the tile to be placed and place tile
            x = position[0][0]
            y = position[0][1]
            if position[1] == True and tile.getFlipped() == False:
                tile.flip()
            elif position[1] == False and tile.getFlipped() == True:
                tile.flip()
            if self.field.placeTile(tile, x, y):
                #self.frame.repaint(self.field)
                self.steps += 1
                self.recursivePlacing()
                return
        #self.frame.root.mainloop()

for i in range(5):
    for j in range(5):
        CONFIGURATION = "15-%d-%d.txt" %(i,j)
        start_time = time.time()        
        Assignment(CONFIGURATION)