import Tkinter as tk

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
		self.initUI()
        
	def initUI(self):
		self.parent.title("Simple menu")
		menubar = tk.Menu(self.parent)
		self.parent.config(menu=menubar)
        
		fileMenu = tk.Menu(menubar)
		fileMenu.add_command(label="New", command=self.onNew)
		fileMenu.add_command(label="View Scores", command=self.onView)
		fileMenu.add_command(label="Exit", command=self.onExit)
		menubar.add_cascade(label="File", menu=fileMenu)

		generalMenu = tk.Menu(menubar)
		generalMenu.add_command(label="Start", command=self.onEasy)
		generalMenu.add_command(label="Stop", command=self.onHard)
		generalMenu.add_command(label="Set Turns", command=self.onDefault)
		generalMenu.add_command(label="Reset", command=self.onDefault)
		menubar.add_cascade(label="Game", menu=generalMenu)
		
		controlMenu = tk.Menu(menubar)
		controlMenu.add_command(label="Game Speed", command=self.onEasy)
		controlMenu.add_command(label="Edit Color", command=self.onHard)
		controlMenu.add_command(label="Edit Tiles", command=self.onDefault)
		menubar.add_cascade(label="Controls", menu=controlMenu)
		
		helpMenu = tk.Menu(menubar)
		helpMenu.add_command(label="General", command=self.onGeneral)
		helpMenu.add_command(label="Menubar", command=self.onMenu)
		menubar.add_cascade(label="Help", menu=helpMenu)

	def onNew(self):
		global okToPressReturn
		global hunger
		global happiness
		global day
		okToPressReturn = True
		hunger = 100
		happiness = 100
		day = 0
		startGame(0)

	def onView(self):
		score_file = open("Game_Record.txt",  'r+')
		score_data = "Previous Scores: \n" + "----------------\n" + score_file.read()
		S = tk.Scrollbar(root)
		T = tk.Text(root, height = 10, width = 20)
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

	def onEasy(self):
		global happiness_step
		happiness_step /= 2

	def onHard(self):
		global happiness_step
		global hunger_step
		hunger_step *= 2
		happiness_step *= 2
		
	def onDefault(self):
		global happiness_step
		global hunger_step
		hunger_step = 1
		happiness_step = 2

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
The 'new' option allows you to start a new game. This can be used when you get a gameover or simplly to reset during the middle of a current game \n\n \
The 'view scores' option allows the user to view previous scores they have achieved in the game. The scores show up near the bottom corner of the main screen and will disappear after about 15 seconds.\n\n \
The 'exit' option closes the entire game. This may not close mini-games but they should all automatically close after some time \n\n\n \
The second menu is the game menu. This menu has three different options and helps control the pace/ difficulty of the game. \n\n \
The first option is 'slow down' which slows down (by half) the rate at which Lucifer the cat becomes unhappy with you.\n\n \
Be careful because this option has no effect on hunger \n \
The second option is 'speed up' which doubles the rate at which Lucifer becomes hungry and becomes bored. \n\n \
This can make the game very challenging because it does not speed up the cycle of the days \n \
The third option is 'reset' which resets Lucifer's rate of hunger and boredom to their default values \n\n \
The third menu, the help menu, is the one you used to get here! It has 5 differnt options \n\n\n \
This is the menu where you can find the instructions for the game. There are instructions for how to play the game in general \n\n \
There are also instructions for how to play the various mini-games as well as this set of instructions which explains the menu system \n\n \
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