import numpy
from tilingObjects.Tile import Tile


class Field(object):
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.tileset = []
        self.placedID = []

        self.field = [[0 for y in range(self.height)] for x in range(self.width)]

    def __copy__(self):
        return type(self)

    def getHeight(self):
        return self.height

    def getWidth(self):
        return self.width

    def getTile(self, index):
        return self.tileset[index]

    def getTiles(self):
        return self.tileset

    def addTile(self, tile, placed, score):
        self.tileset.append([tile, placed, score])
    
    def sortTileset(self):
        self.tileset = sorted(self.tileset, key=lambda x:(x[1],-x[2], x[0]))

    def getNumberOfTiles(self):
        return len(self.tileset)
    
    def getLastPlacedID(self): return self.placedID[-1]
    
    def removeLastPlacedID(self): self.placedID.pop()

    def placeTile(self, tile, x, y):
        if not (x >= self.width or y >= self.height):
            for i in range(tile.getWidth()):
                for j in range(tile.getHeight()):
                    self.field[x + i][y + j] = tile.getID()
            tile.setCoordinates(x, y)
            tile.placeThisTile()
            self.placedID.append(tile.getID())
            for instance in self.tileset:
                if instance[0] == tile:
                    self.tileset.remove(instance)
                    instance[1] = True
                    self.tileset.append(instance)
            return True
        return False

    def inRange(self, tile, x, y):
        if ((self.width - x >= tile.getWidth()) and (self.height - y >= tile.getHeight())):
            for i in range(tile.getWidth()):
                for j in range(tile.getHeight()):
                    if (self.isOccupied(x + i, y + j)):
                        return False
            return True
        return False

    def removeTile(self, tile):
        for i in range(tile.getWidth()):
            for j in range(tile.getHeight()):
                self.field[tile.getX() + i][tile.getY() + j] = 0
        for instance in self.tileset:
            if instance[0] == tile:
                self.tileset.remove(instance)
                instance[1] = False
                self.tileset.append(instance)
        self.placedID.remove(tile.getID())
        tile.setCoordinates(0, 0)

    def getTileAt(self, x, y):
        return self.field[x][y]

    def isOccupied(self, x, y):
        return self.field[x][y] != 0

    def solved(self):
        for x in range(self.getWidth()):
            for y in range(self.getHeight()):
                if not self.isOccupied(x, y): return False
        return True

    def getField(self):
        return self.field

    def isEmpty(self, x, y):
        return self.field[x][y] == 0
   
    def getFilledPercentage(self):
        filledCoordinates = 0 
        totalCoordinates = 0
        for x in range(self.width):
            for y in range(self.height):
                totalCoordinates += 1
                if self.isOccupied(x, y):
                    filledCoordinates += 1
        return (float(filledCoordinates)/totalCoordinates * 100)