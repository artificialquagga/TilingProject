from Tkinter import *

class FieldFrame(object):
    MARGINLEFT = 25
    MARGINTOP = 25
    
    def __init__(self, field, scale):
        self.SCALE = scale
        self.field = field
        
        self.root = Tk()
        
        self.frame = Frame(self.root, width=1024, height=768, colormap="new")
        self.frame.pack(fill=BOTH, expand=1)
        
        self.label = Label(self.frame, text="Heuristieken 2016 - Tiling!")
        self.label.pack(fill=X, expand=1)
        
        self.canvas = Canvas(self.frame,
                             bg="white",
                             width=self.field.getWidth() * self.SCALE + 1,
                             height=self.field.getHeight() * self.SCALE + 1,
                             cursor="PLUS")
        self.canvas.pack()
        
        self.canvas.bind("<Button-1>", self.processMouseEvent)
        self.canvas.focus_set()
        
    def setField(self, field):
        for tile in field.getTiles():
            tile = tile[0]
            self.canvas.create_rectangle(tile.getX() * self.SCALE + 2,
                                         tile.getY() * self.SCALE + 2,
                                         (tile.getX() + tile.getWidth()) * self.SCALE + 2,
                                         (tile.getY() + tile.getHeight()) * self.SCALE + 2,
                                         fill=tile.getColor())
        self.canvas.pack()
        self.root.update()

    def repaint(self, field):
        self.canvas.delete("all")
        self.setField(field)
            
    def processMouseEvent(self, event):
        coordinates = ((event.x / self.SCALE), ",", (event.y / self.SCALE))
        self.canvas.create_text(event.x, event.y, text=coordinates)
