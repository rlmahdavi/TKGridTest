from Tkinter import *
import time
import random

class App:
	def __init__(self, master):

		frame = Frame(master)
		frame.pack()

		self.canvas = Canvas(master, width=gridSize * tileSize, height=gridSize * tileSize)
		self.canvas.pack()

		self.seedEntry = Entry(master)
		self.seedEntry.pack()

		self.seedEntry.insert(0, random.randint(100000, 999999))
		self.seedEntry.focus_set()

		gridUpdateButton = Button(master, text="Update Grid", command=self.gridUpdate)
		gridUpdateButton.pack()

		self.grid = Grid(gridSize, tileSize)
		self.gridUpdate()

	#update grid colors with new seed
	def gridUpdate(self):
		reseed(self.seedEntry.get())
		for tile in self.grid.playgrid:
			self.canvas.create_rectangle(tile.centerX - self.grid.tileSize / 2,
							   tile.centerY - self.grid.tileSize / 2,
							   tile.centerX + self.grid.tileSize / 2, 
							   tile.centerY + self.grid.tileSize / 2,
							   fill=random.choice(colors))
			self.canvas.pack()

#square tile
#size is the w or h
class Tile:
	def __init__(self, size, centerX, centerY):
		self.size = size
		self.centerX = centerX
		self.centerY = centerY
		#self.color = random.choice(colors)

#a gridSize x gridSize grid of Tiles
class Grid:
	def __init__(self, gridSize, tileSize):
		self.gridSize = gridSize
		self.tileSize = tileSize
		self.playgrid = []

		for i in range(gridSize * gridSize):
			centerX = (i * tileSize - (tileSize / 2)) % (gridSize * tileSize)
			centerY = ((i / gridSize) + 1) * tileSize - (tileSize / 2)
			self.playgrid.append(Tile(tileSize, centerX, centerY))

	#def updateColors(self):
	#	reseed()
	#	for tile in self.playgrid:
	#		self.color = 


def reseed(newSeed):
	random.seed(newSeed)

colors = ["white", "black", "red", "green", "blue", "cyan", "yellow", "magenta"]
gridSize = 100
tileSize = 8

root = Tk()

app = App(root)



root.mainloop()