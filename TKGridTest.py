from Tkinter import *
import time
import random

#square tile
#size is the w or h
class Tile:
	def __init__(self, size, centerX, centerY, tileNum, color):
		self.size = size
		self.centerX = centerX
		self.centerY = centerY
		self.tileNum = tileNum
		self.color = color

		chance = 3
		if random.randint(0, chance) == chance:
			self.passable = False
			self.color = "black"
		else:
			self.passable = True


#a gridSize x gridSize array of Tiles
class Grid:
	def __init__(self):
		self.playGrid = []

		#create tiles
		for i in range(gridSize * gridSize):
			#i * tileSize gets you to the left side, adding half of tilesize gets you to the center, modulus keeps it in rows
			centerX = (i * tileSize + (tileSize / 2)) % (maxSize)
			#i / grisize gets you the row #, * tilsize gets you the bottom of the rectangle, - tilesize/2 gets you the center
			centerY = ((i / gridSize) + 1) * tileSize - (tileSize / 2)
			color = "#00" + "%02x" % ((i % gridSize) * (256 / gridSize)) + "%02x" % ((i / gridSize) * (256 / gridSize))
			#color = random.choice(colors)
			self.playGrid.append(Tile(tileSize, centerX, centerY, i, color))

	#draws rectangles on a canvas based on the tile information
	def update(self, canvas): #add newseed if going back to random colors
		#random.seed(newSeed)
		for tile in self.playGrid:
			#tile.color = random.choice(colors)
			canvas.create_rectangle(tile.centerX - tileSize / 2,
							   tile.centerY - tileSize / 2,
							   tile.centerX + tileSize / 2, 
							   tile.centerY + tileSize / 2,
							   fill=tile.color)
			#canvas.create_text(tile.centerX, tile.centerY, text=tile.tileNum)
			canvas.pack()

	#returns number of clicked tile, based off x & y coords
	def findTile(self, xpos, ypos):
		gridX = xpos / tileSize
		gridY = ypos / tileSize
		clickedTile = gridY * gridSize + gridX
		return self.playGrid[clickedTile]

class Player:
	def __init__(self):		
		self.xpos = tileSize / 2
		self.ypos = tileSize / 2
		color = "yellow"
		symbol = '@'

	def draw(self):
		canvas.delete("player")
		canvas.create_oval(self.xpos - tileSize / 2,
				 self.ypos - tileSize / 2,
				 self.xpos + tileSize / 2,
				 self.ypos + tileSize / 2,
				 fill="yellow",
				 tag="player")
		canvas.create_text(self.xpos, self.ypos, text="@", tag="player")

	def move(self, inputChar):
		if inputChar == 'a' and player.xpos - moveSpeed > 0 and grid.findTile(player.xpos - moveSpeed, player.ypos).passable == True:
			player.xpos -= moveSpeed
		if inputChar == 'w' and player.ypos - moveSpeed > 0 and grid.findTile(player.xpos, player.ypos - moveSpeed).passable == True:
			player.ypos -= moveSpeed
		if inputChar == 'd' and player.xpos + moveSpeed < maxSize and grid.findTile(player.xpos + moveSpeed, player.ypos).passable == True:
			player.xpos += moveSpeed
		if inputChar == 's' and player.ypos + moveSpeed < maxSize and grid.findTile(player.xpos, player.ypos + moveSpeed).passable == True:
			player.ypos += moveSpeed

		player.draw()

#####################
##### CONSTANTS #####
#####################

colors = ["white", "red", "green", "blue", "cyan", "yellow", "magenta"]
gridSize = 32
tileSize = 16
maxSize = gridSize * tileSize
moveSpeed = tileSize

#####################
####### MAIN ########
#####################

root = Tk()

def key(event):
	player.move(event.char)

frame = Frame(root)
frame.bind("<Key>", key)
frame.pack()
frame.focus_set()

def dispTileInfo(event):
	frame.focus_set()
	tileNum = grid.findTile(event.x, event.y)
	print grid.playGrid[tileNum].color

canvas = Canvas(root, width=maxSize, height=maxSize)
canvas.bind("<Button-1>", dispTileInfo)
canvas.pack()

'''
def buttonUpdate():
	grid.update(seedEntry.get(), canvas)

gridUpdateButton = Button(root, text="Update Grid", command=buttonUpdate)
gridUpdateButton.pack(side=RIGHT)

seedEntry = Entry(root)
seedEntry.pack(side=RIGHT)

#set default seed
seedEntry.insert(0, random.randint(100000, 999999))
'''

grid = Grid()
grid.update(canvas) #seedEntry.get() if going back to random colors

player = Player()
player.draw()


#main loop
root.mainloop()