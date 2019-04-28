import tkinter as tk
from threading import Timer


#-------------------------------------------------------------------
# Helper Functions
#-------------------------------------------------------------------

# Speeds up the game_speed based on the value found at the slider
def SetSpeed(p1, p2, speed = 200):
    p1.game_speed = speed
    p2.game_speed = speed
#-------------------------------------------------------------------
def end_of_game(p1, p2):
    t = Timer(1.5, p1.root.quit)
    t.start()
#-------------------------------------------------------------------


#-------------------------------------------------------------------
# Various Classes
#-------------------------------------------------------------------

# Creates a cell on the board
class Cell:
	def __init__(self, x, y, i, j):
		self.isAlive = False
		self.nextStatus = None
		self.pos_screen = (x, y)
		self.pos_matrix = (i, j)

	def __str__(self):
		return str(self.isAlive)

	def __repr__(self):
		return str(self.isAlive)

	def switchStatus(self):
		self.isAlive = not self.isAlive

#-------------------------------------------------------------------

# Creates a menubar for the main display
class Menubar(tk.Frame):
	def __init__(self, parent):
		tk.Frame.__init__(self, parent)
		self.parent = parent
		self.root = parent
		self.initUI()

	def initUI(self):
		self.parent.title("Simple menu")
		menubar = tk.Menu(self.parent)
		self.parent.config(menu=menubar)

		fileMenu = tk.Menu(menubar)
		fileMenu.add_command(label="New", command=self.onNew)
		#fileMenu.add_command(label="View Scores", command=self.onView)
		fileMenu.add_command(label="Exit", command=self.onExit)
		menubar.add_cascade(label="File", menu=fileMenu)

		generalMenu = tk.Menu(menubar)
		generalMenu.add_command(label="Start", command=self.onStub)
		generalMenu.add_command(label="Stop", command=self.onStub)
		generalMenu.add_command(label="Set Turns", command=self.onStub)
		generalMenu.add_command(label="Reset", command=self.onStub)
		menubar.add_cascade(label="Game", menu=generalMenu)

		helpMenu = tk.Menu(menubar)
		helpMenu.add_command(label="General", command=self.onGeneral)
		helpMenu.add_command(label="Menubar", command=self.onMenu)
		menubar.add_cascade(label="Help", menu=helpMenu)

	def onNew(self):
		print()

	def onView(self):
		score_file = open("Game_Record.txt",  'r+')
		score_data = "Previous Scores: \n" + "----------------\n" + score_file.read()
		S = tk.Scrollbar(self.root)
		T = tk.Text(self.root, height = 10, width = 20)
		S.pack(side = tk.RIGHT, fill = tk.Y)
		T.pack(side = tk.LEFT, fill = tk.Y)
		S.config(command=T.yview)
		T.config(yscrollcommand = S.set)
		T.insert(tk.END, score_data)
		score_file.close()
		T.after(15000, T.destroy)
		S.after(15000, S.destroy)

	def onExit(self):
		self.quit()

	def onStub(self):
		print()

	def onGeneral(self):
		master = tk.Tk()
		master.title("General Help")
		info = "The game is started by pressing the \'return\' key on the main display.\n\n Exit this help menu by pressing 'quit'"
		S = tk.Scrollbar(master)
		T = tk.Text(master, height=20, width=50)
		S.pack(side = tk.RIGHT, fill = tk.Y)
		T.pack(side = tk.LEFT, fill = tk.Y)
		S.config(command=T.yview)
		T.config(yscrollcommand=S.set)
		T.insert(tk.END, info)
		exitButton = tk.Button(master, text = "Quit", command = master.destroy)
		exitButton.pack(side = tk.LEFT, fill = tk.Y)

	def onMenu(self):
		master = tk.Tk()
		master.title("Menubar Help")
		info = "There are three main menus in this game (with various sub-options).\n\n \
The first is the file menu. This menu has three options 'new', 'view scores' and 'exit'  \n\n \
The 'new' option allows you to start a new game. This can be used when you get a game over or simpley to reset during the middle of a current game \n\n \
The 'view scores' option allows the user to view previous scores they have achieved in the game. The scores show up near the bottom corner of the main screen and will disappear after about 15 seconds.\n\n \
The 'exit' option closes the entire game. \n\n\n \
The second menu is the game menu. \n\n \
The third menu, the help menu, is the one you used to get here! It has 5 differnt options \n\n\n \
This is the menu where you can find the instructions for the game. There are instructions for how to play the game in general \n\n \
	Exit this help menu by pressing 'quit' to the right of this text"
		S = tk.Scrollbar(master)
		T = tk.Text(master, height=20, width=50)
		S.pack(side = tk.RIGHT, fill = tk.Y)
		T.pack(side = tk.LEFT, fill = tk.Y)
		S.config(command=T.yview)
		T.config(yscrollcommand=S.set)
		T.insert(tk.END, info)
		exitButton = tk.Button(master, text = "Quit", command = master.destroy)
		exitButton.pack(side = tk.LEFT, fill = tk.Y)

#---------------------------------------------------------------------

class Game:
	
	def __init__(self, canvas, root, pFrame, gameSpeed, my_turn, color = 'forest green', dead_color = 'green2', cells_left = 15, adversary = None):
		self.canvas = canvas
		self.root = root
		self.stats_frame = pFrame
		self.grid = [] # Variable to store the Cell objects
		self.rectangles = [] # Variable to store self.rectangles
		self.begin_id = None
		self.game_speed = gameSpeed
		self.color = color
		self.dead_color = dead_color
		self.board_len = 35
		self.board_size = self.board_len ** 2
		self.create_grid()
		self.total_alive = 0
		self.total_dead = 0
		self.cells_left = cells_left
		self.canvas.bind("<Button-1>", self.change_colour_on_click)
		self.adversary = adversary
		self.my_turn = my_turn
		self.original_turn = my_turn


	def updateRemaining(self):
		remaining = 1
		num_white = self.board_size - self.total_alive
		self.stats_frame[remaining].config(text = "Remaining White: %.2f" % (num_white / self.board_size * 100) + "%")

  # Function for updating the values for the player stats
	def updateFrame(self):
		cellToChange = 0
		alive = 2
		dead = 3
		speed_slider = 4
		self.stats_frame[cellToChange].config(text = "Cells to Change: " + str(self.cells_left))
		self.stats_frame[alive].config(text = "Score: " + str(self.total_alive))
		self.stats_frame[dead].config(text = "Dead Cells: " + str(self.total_dead))
		#self.game_speed = self.stats_frame[speed_slider].get() # This line updates the game speed

    # This function creates the board on which the game will take place
	def create_grid(self):
		x = 10
		y = 10
		for i in range(self.board_len): #height
			self.grid.append([])
			self.rectangles.append([])
			for j in range(self.board_len): #width
				rect = self.canvas.create_rectangle(x, y, x+10, y+10, fill="white")
				self.rectangles[i].append(rect)
				self.grid[i].append(Cell(x, y, i, j))
				x += 10
			x = 10
			y += 10


    # Find the co-ordinates of the rectangle which has been clicked
	def find_rect_coordinates(self, x, y):
		return (x- x%10, y - y%10)


    # Change the colour of the clicked self.grid and change the status of cell in the self.grid
	def change_colour_on_click(self, event):
		if self.cells_left <= 0:
			self.updateRemaining()
			print("no cells left and player turn over")
			self.my_turn = False
            
		elif self.cells_left > 0 and self.adversary.my_turn != True:
			#print(event.x, event.y)
			x, y = self.find_rect_coordinates(event.x, event.y)
			try:
				iy = int(x / 10 - 1)
				ix = int(y / 10 - 1)
				if ix == -1 or iy == -1:
					raise IndexError
				if self.grid[ix][iy].isAlive:
					self.canvas.itemconfig(self.rectangles[ix][iy], fill=self.dead_color)
					self.total_dead += 1
				else:
					self.canvas.itemconfig(self.rectangles[ix][iy], fill=self.color)
					self.total_alive += 1
				self.grid[ix][iy].switchStatus()
				#print(self.grid[ix][iy].pos_matrix, self.grid[ix][iy].pos_screen)
				self.updateFrame()
			except IndexError:
				return
			#print("clicked")
			self.cells_left -= 1 #self.cells_left - 1
			self.updateFrame()
			#print("one less cell now")


	def paint_grid(self):
		for i in self.grid:
			for j in i:
				if j.nextStatus != j.isAlive:
					x, y = j.pos_matrix
					#print(x, y)
					if j.nextStatus:
						self.canvas.itemconfig(self.rectangles[x][y], fill=self.color)
						#print("changed", j.pos_matrix, "from dead to alive")
						self.total_alive += 1
					else:
						self.canvas.itemconfig(self.rectangles[x][y], fill=self.dead_color)
						self.total_dead += 1
						#print("changed", j.pos_matrix, "from alive to dead")
					j.switchStatus()
					#print("Current status of", j.pos_matrix, j.isAlive)
				self.updateFrame()
		#print("Done painting")


	def changeInStatus(self, cell):
		''' If the cell's status changes in the next gen, return True else False '''
		num_alive = 0
		x, y = cell.pos_matrix
		for i in (x-1, x, x+1):
			for j in (y-1, y, y+1):
				if i == x and j == y:
					continue
				if i == -1 or j == -1:
					continue
				try:
					if self.grid[i][j].isAlive:
						num_alive += 1
				except IndexError:
					pass
		if cell.isAlive:
			return not( num_alive == 2 or num_alive == 3 )
		else:
			return num_alive == 3


	def begin(self):
		for i in self.grid:
			for j in i:
				if self.changeInStatus(j):
					j.nextStatus = not j.isAlive
					#print("change in", j.pos_matrix, "from", j.isAlive, "to", j.nextStatus)
				else:
					j.nextStatus = j.isAlive

		self.paint_grid()
		self.begin_id = self.root.after(self.game_speed, self.begin) # Can be used to change speed


	def stop(self):
		self.updateRemaining()
		self.cells_left = 15
		self.updateFrame()
		self.my_turn = self.original_turn
		self.root.after_cancel(self.begin_id)

#-------------------------------------------------------------------
