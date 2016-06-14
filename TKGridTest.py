from Tkinter import *
import time
import random

#square tile
#size is the w or h
class Tile:
	def __init__(self, size, centerX, centerY, tileNum, color):
		self.size = size
		#pixel positions
		self.centerX = centerX
		self.centerY = centerY
		self.tileNum = tileNum
		self.color = color

#a gridSize x gridSize array of Tiles
class Grid:
	def __init__(self, gridSize, tileSize):
		self.gridSize = gridSize
		self.tileSize = tileSize
		self.playgrid = []

		#create tiles
		for i in range(gridSize * gridSize):
			#i * tileSize gets you to the left side, adding half of tilesize gets you to the center, modulus keeps it in rows
			centerX = (i * tileSize + (tileSize / 2)) % (gridSize * tileSize)
			#i / grisize gets you the row #, * tilsize gets you the bottom of the rectangle, - tilesize/2 gets you the center
			centerY = ((i / gridSize) + 1) * tileSize - (tileSize / 2)
			color = "#00" + "%02x" % ((i % gridSize) * 16) + "%02x" % ((i / gridSize) * 16)
			#color = random.choice(colors)
			self.playgrid.append(Tile(tileSize, centerX, centerY, i, color))

	#draws rectangles on a canvas based on the tile information
	def update(self, newSeed, canvas):
		random.seed(newSeed)
		for tile in self.playgrid:
			#tile.color = random.choice(colors)
			#tile.color = "#%02x%02x%02x" % colorTuple
			canvas.create_rectangle(tile.centerX - self.tileSize / 2,
							   tile.centerY - self.tileSize / 2,
							   tile.centerX + self.tileSize / 2, 
							   tile.centerY + self.tileSize / 2,
							   fill=tile.color)
			canvas.create_text(tile.centerX, tile.centerY, text=tile.tileNum)
			canvas.pack()

#####################
##### CONSTANTS #####
#####################

colors = ["white", "black", "red", "green", "blue", "cyan", "yellow", "magenta"]
gridSize = 16
tileSize = 32

#####################
####### MAIN ########
#####################

root = Tk()

frame = Frame(root)
frame.pack()

canvas = Canvas(root, width=gridSize * tileSize, height=gridSize * tileSize)
canvas.pack()

def buttonUpdate():
	grid.update(seedEntry.get(), canvas)

gridUpdateButton = Button(root, text="Update Grid", command=buttonUpdate)
gridUpdateButton.pack(side=RIGHT)

seedEntry = Entry(root)
seedEntry.pack(side=RIGHT)

#set default seed
seedEntry.insert(0, random.randint(100000, 999999))
seedEntry.focus_set()

grid = Grid(gridSize, tileSize)
grid.update(seedEntry.get(), canvas)

root.mainloop()