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
	def __init__(self, size, centerX, centerY, row, col):
		self.size = size
		self.centerX = centerX
		self.centerY = centerY
		self.row = row
		self.col = col
		self.visited = False
		self.frontier = False

		#randomly make some tiles impassable
		chance = 3
		if random.randint(0, chance) == chance:
			self.passable = False
		else:
			self.passable = True

	def draw(self):
		if self.passable == False:
			color = "black"
		elif self.frontier == True:
			color = "#404090" #blue
		elif self.visited == True:
			color = "#409040" #green
		else:
			color = "#808080" #gray

		canvas.create_rectangle(self.centerX - tileSize / 2,
						   self.centerY - tileSize / 2,
						   self.centerX + tileSize / 2, 
						   self.centerY + tileSize / 2,
						   fill=color)

	def togglePassable(self):
		self.passable = not self.passable
		self.draw()

#a gridSize x gridSize array of Tiles
class Grid:
	def __init__(self):
		#self.playGrid = [[0 for i in range(gridSize)] for j in range(gridSize)]
		self.playGrid = []

		#create tiles
		for row in range(numRows):
			self.playGrid.append([])
			for col in range(numCols):
				#i * tileSize gets you to the left side, adding half of tilesize gets you to the center, modulus keeps it in rows
				#centerX = (i * tileSize + (tileSize / 2)) % (lastPixel)
				centerX = col * tileSize + (tileSize / 2)
				#i / grisize gets you the row #, * tilsize gets you the bottom of the rectangle, - tilesize/2 gets you the center
				#centerY = ((i / gridSize) + 1) * tileSize - (tileSize / 2)
				centerY = row * tileSize + (tileSize / 2)
				#RRGGBB more green as it goes to the right, more blue as it goes down
				#color = "#00" + "%02x" % ((i % gridSize) * (256 / gridSize)) + "%02x" % ((i / gridSize) * (256 / gridSize))
				#color = random.choice(colors)
				#self.playGrid[row][col] = Tile(tileSize, centerX, centerY, row, col)
				self.playGrid[row].append(Tile(tileSize, centerX, centerY, row, col))

	#draws rectangles on a canvas based on the tile information
	def drawTiles(self): #add newseed if going back to random colors
		#random.seed(newSeed)
		canvas.delete(ALL)
		for row in self.playGrid:
			for tile in row:
				#tile.color = random.choice(colors)
				tile.draw()
				#canvas.create_text(tile.centerX, tile.centerY, text=tile.loc)
				canvas.pack()

	#returns number of clicked tile, based off x & y coords
	def findTile(self, xpos, ypos):
		row = ypos / tileSize
		col = xpos / tileSize
		return self.playGrid[row][col]


class POI:
	def __init__(self, xpos, ypos, tag, color, symbol):		
		#self.gridX = xpos
		#self.gridY = ypos
		self.tag = tag
		self.color = color
		self.symbol = symbol

	def placeAt(self, row, col):
		self.row = row
		self.col = col

	def draw(self):
		if self.row == None or self.col == None:
			return
		canvas.delete(self.tag)
		canvas.create_oval(grid.playGrid[self.row][self.col].centerX - tileSize / 2,
				 grid.playGrid[self.row][self.col].centerY - tileSize / 2,
				 grid.playGrid[self.row][self.col].centerX + tileSize / 2,
				 grid.playGrid[self.row][self.col].centerY + tileSize / 2,
				 fill=self.color,
				 tag=self.tag)
		canvas.create_text(grid.playGrid[self.row][self.col].centerX, grid.playGrid[self.row][self.col].centerY, text=self.symbol, tag=self.tag)

class Pathfinder:
	def __init__(self):
		self.frontier = deque()
		self.stepCount = 0

	def expandFrontier(self):
		if len(self.frontier) == 0:
			return
		self.stepCount += 1
		stpct.set("Step Count: " + str(self.stepCount))
		workingTile = self.frontier.popleft()
		workingTile.visited = True
		workingTile.frontier = False
		workingTile.draw()

		possibleFrontier = ((workingTile.row+1, workingTile.col),
							(workingTile.row-1, workingTile.col),
							(workingTile.row, workingTile.col+1),
							(workingTile.row, workingTile.col-1))

		for loc in possibleFrontier:
			if inRange(loc[0], loc[1]):
				tile = grid.playGrid[loc[0]][loc[1]]
				if tile.visited == False and tile not in self.frontier and tile.passable == True:
					self.frontier.append(tile)
					tile.frontier = True
					tile.draw()
					drawEntities()



	def clear(self):
		self.frontier.clear()

		for row in grid.playGrid:
			for tile in row:
				tile.visited = False
				tile.frontier = False

		drawAll()

	def reset(self):
		self.frontier.append(grid.playGrid[player.row][player.col])
		self.stepCount = 0

#####################
##### FUNCTIONS #####
#####################

def drawEntities():
	for entity in entities:
		entity.draw()

def drawAll():
	grid.drawTiles()
	drawEntities()

def inRange(row, col):
	if row >= 0 and row < numRows and col >= 0 and col < numCols:
		return True
	else:
		return False

#for when you click on a tile
def clickTile(event):
	global prevClickedEntity #no statics :(
	frame.focus_set()
	clickedTile = grid.findTile(event.x, event.y)
	clickedEntity = None

	#find if there's an entity on the clicked tile
	for entity in entities:
		if entity.row == clickedTile.row and entity.col == clickedTile.col:
			clickedEntity = entity

	#if you're selecting an entity for the first time, remove it from board
	if clickedEntity is not None and prevClickedEntity is None:
		clickedEntity.row = None
		clickedEntity.col = None
		prevClickedEntity = clickedEntity
		canvas.delete(clickedEntity.tag)
		pathfinder.clear()
	#if you've previously selected an entity and are clicking an empty tile, add the prev entity to the board
	elif clickedEntity is None and prevClickedEntity is not None:
		prevClickedEntity.row = clickedTile.row
		prevClickedEntity.col = clickedTile.col
		drawEntities()
		if prevClickedEntity == player:
			pathfinder.reset()
		prevClickedEntity = None
	#otherwise toggle passable
	else:
		clickedTile.togglePassable()


#####################
##### CONSTANTS #####
#####################

colors = ["white", "red", "green", "blue", "cyan", "yellow", "magenta"]
gridSize = 16
numRows = 8
numCols = 16
lastTile = numRows * numCols
tileSize = 32
lastHPixel = numRows * tileSize
lastVPixel = numCols * tileSize

#####################
####### MAIN ########
#####################

root = Tk()
root.wm_title("Pathfinder")

pathfinder = Pathfinder()

frame = Frame(root)
frame.pack(side=LEFT)

prevClickedEntity = None

canvas = Canvas(frame, width=numCols * tileSize, height=numRows * tileSize)
canvas.bind("<Button-1>", clickTile)
canvas.pack()

optionsPanel = Frame(root)
optionsPanel.pack(side=RIGHT)

stpct = StringVar()
steps = Label(optionsPanel, width=14, textvariable=stpct)
steps.pack(side=LEFT)
stpct.set("Step Count: 0")

def findPathButton():
	pathfinder.expandFrontier()

stepButton = Button(optionsPanel, text=">", command=findPathButton)
stepButton.pack(side=RIGHT)

grid = Grid()
grid.drawTiles() #seedEntry.get() if going back to random colors
entities = []

player = POI(xpos=3, ypos=2, tag="player", color="yellow", symbol="@")
player.placeAt(0, 0)
entities.append(player)

exit = POI(xpos=1, ypos=2, tag="exit", color="red", symbol="E")
exit.placeAt(numRows-1, numCols-1)
entities.append(exit)


pathfinder.reset()
drawEntities()
#main loop
root.mainloop()