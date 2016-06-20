from Tkinter import *
import time
import random
from collections import deque

#####################
##### CLASSES #######
#####################

#square tile
#size is the w or h
class Tile:
	def __init__(self, size, centerX, centerY, tileNum, color):
		self.size = size
		self.centerX = centerX
		self.centerY = centerY
		self.tileNum = tileNum
		self.groundColor = color

		chance = 3
		if random.randint(0, chance) == chance:
			self.passable = False
			self.dispColor = "black"
		else:
			self.passable = True
			self.dispColor = self.groundColor

	def togglePassable(self):
		self.passable = not self.passable
		if self.dispColor == "black":
			self.dispColor = self.groundColor
		else:
			self.dispColor = "black"

		grid.update()
		drawEntities()

#a gridSize x gridSize array of Tiles
class Grid:
	def __init__(self):
		self.playGrid = []
		self.testGrid = [[0 for i in range(gridSize)] for j in range(gridSize)]
		self.testGrid[1][5] = "hello"
		print self.testGrid
		#create tiles
		for i in range(lastTile):
			#i * tileSize gets you to the left side, adding half of tilesize gets you to the center, modulus keeps it in rows
			centerX = (i * tileSize + (tileSize / 2)) % (lastPixel)
			#i / grisize gets you the row #, * tilsize gets you the bottom of the rectangle, - tilesize/2 gets you the center
			centerY = ((i / gridSize) + 1) * tileSize - (tileSize / 2)
			#RRGGBB more green as it goes to the right, more blue as it goes down
			#color = "#00" + "%02x" % ((i % gridSize) * (256 / gridSize)) + "%02x" % ((i / gridSize) * (256 / gridSize))
			color = "#909090"
			#color = random.choice(colors)
			self.playGrid.append(Tile(tileSize, centerX, centerY, i, color))

	#draws rectangles on a canvas based on the tile information
	def update(self): #add newseed if going back to random colors
		#random.seed(newSeed)
		for tile in self.playGrid:
			#tile.color = random.choice(colors)
			canvas.create_rectangle(tile.centerX - tileSize / 2,
							   tile.centerY - tileSize / 2,
							   tile.centerX + tileSize / 2, 
							   tile.centerY + tileSize / 2,
							   fill=tile.dispColor)
			#canvas.create_text(tile.centerX, tile.centerY, text=tile.tileNum)
			canvas.pack()

	#returns number of clicked tile, based off x & y coords
	def findTile(self, xpos, ypos):
		gridX = xpos / tileSize
		gridY = ypos / tileSize
		tileNum = gridY * gridSize + gridX
		return self.playGrid[tileNum]

class POI:
	def __init__(self, xpos, ypos, tag, color, symbol, loc):		
		#self.gridX = xpos
		#self.gridY = ypos
		self.tag = tag
		self.color = color
		self.symbol = symbol
		self.loc = loc

	def draw(self):
		canvas.delete(self.tag)
		canvas.create_oval(grid.playGrid[self.loc].centerX - tileSize / 2,
				 grid.playGrid[self.loc].centerY - tileSize / 2,
				 grid.playGrid[self.loc].centerX + tileSize / 2,
				 grid.playGrid[self.loc].centerY + tileSize / 2,
				 fill=self.color,
				 tag=self.tag)
		canvas.create_text(grid.playGrid[self.loc].centerX, grid.playGrid[self.loc].centerY, text=self.symbol, tag=self.tag)

class Pathfinder:
	def __init__(self):
		frontier = deque()
	#frontier.append()
	#frontier.popleft()

#####################
##### FUNCTIONS #####
#####################

def drawEntities():
	for entity in entities:
		entity.draw()

#####################
##### CONSTANTS #####
#####################

colors = ["white", "red", "green", "blue", "cyan", "yellow", "magenta"]
gridSize = 16
lastTile = gridSize * gridSize
tileSize = 32
lastPixel = gridSize * tileSize

#####################
####### MAIN ########
#####################

root = Tk()
root.wm_title("Pathfinder")

frame = Frame(root)
frame.pack()
frame.focus_set()

prevClickedEntity = None
def dispTileInfo(event):
	global prevClickedEntity
	frame.focus_set()
	clickedTile = grid.findTile(event.x, event.y)
	clickedEntity = None
	#find if there's an entity on the clicked tile
	for entity in entities:
		if entity.loc == clickedTile.tileNum:
			clickedEntity = entity

	#if you're selecting an entity
	if clickedEntity is not None and prevClickedEntity is None:
		clickedEntity.loc = None
		prevClickedEntity = clickedEntity
		canvas.delete(clickedEntity.tag)
	#if you've selected an entity and are clicking an empty tile
	elif clickedEntity is None and prevClickedEntity is not None:
		prevClickedEntity.loc = clickedTile.tileNum
		drawEntities()
		prevClickedEntity = None
	#otherwise toggle passable
	else:
		clickedTile.togglePassable()

canvas = Canvas(root, width=lastPixel, height=lastPixel)
canvas.bind("<Button-1>", dispTileInfo)
canvas.pack()

def findPathButton():
	print "gettin there"

stepButton = Button(root, text=">", command=findPathButton)
stepButton.pack()

grid = Grid()
grid.update() #seedEntry.get() if going back to random colors
entities = []

player = POI(xpos=3, ypos=2, tag="player", color="yellow", symbol="@", loc=0)
entities.append(player)

exit = POI(xpos=gridSize, ypos=gridSize, tag="exit", color="red", symbol="E", loc=lastTile - 1)
entities.append(exit)

drawEntities()
#main loop
root.mainloop()