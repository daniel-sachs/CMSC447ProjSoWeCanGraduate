## @file gol.py
#  @brief Contains class definitions for the game.
#
#  @author Sarah Alvarez
#  @author Pablo Burgos
#  @author Innocent Kironji
#  @author Daniel Sachs
#  @author Jason Schuler
#  @author James Walls

import tkinter as tk
from threading import Timer


#-------------------------------------------------------------------
# Helper Functions
#-------------------------------------------------------------------

## Speeds up the game_speed based on the value found at the slider
#  @param p1 Player one's Game object
#  @param p2 Player two's Game object
#  @param speed The time between each game "tick" in nanoseconds.
def SetSpeed(p1, p2, speed = 200):
    p1.game_speed = speed
    p2.game_speed = speed

## Ends the game.
#  @param p1 Player one's Game object.
#  @param p2 Player two's Game object.
def end_of_game(p1, p2):
    print ("ENDING GAME")
    t = Timer(1.5, p1.root.quit)
    t.start()


#-------------------------------------------------------------------
# Various Classes
#-------------------------------------------------------------------

## Creates a cell on the board
class Cell:

    ## The constructor.
    #  @param x The x screen position of the cell.
    #  @param y The y screen position of the cell.
    #  @param i The row coordinate of the cell.
    #  @param j The column coordinate of the cell.
    #  @param player The owner of the cell.
    def __init__(self, x, y, i, j, player = 0):
        self.isAlive = False
        self.nextStatus = None
        self.pos_screen = (x, y)
        self.pos_matrix = (i, j)
        self.player = player
        self.is_painted = False

    ## Prints a readable message.
    #  @param self The current object.
    #  @return A string message describing the current state of the
    #          cell.
    def __str__(self):
        return str(self.isAlive)

    ## Prints an unambiguous message.
    #  @param self The current object.
    #  @return A string message describing the current state of the
    #          cell.
    def __repr__(self):
        return str(self.isAlive)

    ## Switches the current status of the cell.
    #
    #  A cell that is current alive will die, and a cell that is
    #  currently dead will become alive.
    #
    #  @param self The current object.
    def switchStatus(self):
        self.isAlive = not self.isAlive

    ## @var isAlive
    #  The current state of the cell. Cells can be either alive or dead.
    #
    #  @var nextStatus
    #
    #  @var pos_screen
    #  The screen position.
    #
    #  @var pos_matrix
    #  The coordinates of the cell in the matrix.
    #
    #  @var player
    #  The owner of the cell (player one or player two).

#-------------------------------------------------------------------

## Creates a menubar for the main display
#  @extends tk.Frame
class Menubar(tk.Frame):

    ## The constructor.
    #  @param parent The parent Frame.
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.root = parent
        self.initUI()

    ## Initialized the user interface.
    #  @param self The current Menubar object.
    def initUI(self):
        self.parent.title("Simple menu")
        menubar = tk.Menu(self.parent)
        self.parent.config(menu=menubar)

        fileMenu = tk.Menu(menubar)
        fileMenu.add_command(label="Exit", command=self.onExit)
        menubar.add_cascade(label="File", menu=fileMenu)

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

    ## Closes the menu bar
    #  @param self The current Menu Bar object.
    def onExit(self):
        self.quit()

    def onStub(self):
        print()

    ## Displays general information.
    #  @param self The current Menu Bar object.
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

    ## Displays Menu information.
    #  @param self The current Menu Bar object.
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

## The main class of the game.
class Game:

    ## The constructor.
    #  @param canvas The tkinter canvas.
    #  @param root The root.
    #  @param pFrame The statistics frame.
    #  @param gameSpeed The time between game ticks.
    #  @param player The current player.
    #  @param global_turn The Game turn.
    #  @param color The color of cells that are alive.
    #  @param dead_color The color of painted dead cells.
    #  @param cells_left The remaining cells the player can edit.
    #  @param adversary The other player.
    def __init__(self, canvas, root, pFrame, gameSpeed, player, global_turn, color = 'forest green', dead_color = 'green2', cells_left = 15, adversary = None):
        self.canvas = canvas
        self.root = root
        self.stats_frame = pFrame
        self.player = player
        self.global_turn = global_turn
        self.original_turn = global_turn
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
        self.title = pFrame[4]
        self.banner = pFrame[5]
        self.is_running = False

        if self.player == 1:
            self.banner.config(bg=self.color)
            self.title.config(bg=self.color)

    ## Updates the number of remaining cells.
    #  @param The current Game object.
    def updateRemaining(self):
        remaining = 1
        num_white = self.board_size - self.total_alive
        self.stats_frame[remaining].config(text = "Remaining White: %.2f" % ((num_white / self.board_size) * 100) + "%")

    ## Function for updating the values for the player stats
    #  @param self The current Game object.
    def updateFrame(self):
        cellToChange = 0
        alive = 2
        dead = 3
        self.stats_frame[cellToChange].config(text = "Cells to Change: " + str(self.cells_left))
        self.stats_frame[alive].config(text = "Score: " + str(self.total_alive))
        self.stats_frame[dead].config(text = "Dead Cells: " + str(self.total_dead))

    ## This function creates the board on which the game will take place.
    #  @param self The current Game object.
    def create_grid(self):
        x = 10
        y = 10
        for i in range(self.board_len): #height
            self.grid.append([])
            self.rectangles.append([])
            for j in range(self.board_len): #width
                rect = self.canvas.create_rectangle(x, y, x+10, y+10, fill="white", outline="gray25")
                self.rectangles[i].append(rect)
                self.grid[i].append(Cell(x, y, i, j, self.player))
                x += 10
            x = 10
            y += 10


    ## Finds the co-ordinates of the rectangle which has been clicked
    #  @param self The current object.
    #  @param x The x coordinate of the clicked cell.
    #  @param y The y coordinate of the clicked cell.
    def find_rect_coordinates(self, x, y):
        return (x- x%10, y - y%10)


    ## Change the colour of the clicked self.grid and change the status of cell in the self.grid
    #  @param self The current Game object.
    #  @param event DESCRIPTION
    #  @reutrn The updated Frame.
    def change_colour_on_click(self, event):
        print(event.x, event.y)
        print("GLOBAL_TURN = ", self.global_turn)
        #self.title.config(bg = self.color)
        if (self.cells_left > 0 or self.adversary.cells_left > 0) and not self.is_running:
            x, y = self.find_rect_coordinates(event.x, event.y)
            try:
                iy = int(x / 10 - 1)
                ix = int(y / 10 - 1)
                if ix == -1 or iy == -1:
                    raise IndexError

                # Logic for if a player clicks on their board during their turn
                if self.global_turn == 1 and self.grid[ix][iy].player == 1:
                    if self.cells_left > 0:
                        if self.grid[ix][iy].isAlive:
                            self.canvas.itemconfig(self.rectangles[ix][iy], fill=self.dead_color)
                            self.total_dead += 1
                        else:
                            self.canvas.itemconfig(self.rectangles[ix][iy], fill=self.color)
                            self.grid[ix][iy].is_painted = True
                            self.total_alive += 1
                        self.cells_left = self.cells_left - 1
                        self.grid[ix][iy].switchStatus()
                        print("On your board! cells left =", self.cells_left)
                        print("Enemy's cells left =", self.adversary.cells_left)
                    if self.cells_left == 0:
                        print("Player 1 turn over")
                        # You are player 1
                        self.banner.config(bg = "gray25")
                        self.title.config(bg = "gray25")
                        self.updateRemaining()
                        if self.global_turn == 1:
                            self.adversary.banner.config(bg=self.adversary.color)
                            self.adversary.title.config(bg=self.adversary.color)
                            self.global_turn = 2
                            self.adversary.global_turn = 2
                        #else:
                        #    self.global_turn = 1
                        #    self.adversary.global_turn = 1
                elif self.global_turn == 2 and self.grid[ix][iy].player == 2:
                    if self.cells_left > 0:
                        if self.grid[ix][iy].isAlive:
                            self.canvas.itemconfig(self.rectangles[ix][iy], fill=self.dead_color)
                            self.total_dead += 1
                        else:
                            self.canvas.itemconfig(self.rectangles[ix][iy], fill=self.color)
                            self.grid[ix][iy].is_painted = True
                            self.total_alive += 1
                        self.cells_left = self.cells_left - 1
                        self.grid[ix][iy].switchStatus()
                        print("On your board! cells left =", self.cells_left)
                        print("Enemy's cells left =", self.adversary.cells_left)
                    if self.cells_left == 0:
                        print("Player 2 turn over")
                        # You are player 2
                        self.banner.config(bg = "gray25")
                        self.title.config(bg = "gray25")
                        self.updateRemaining()
                        if self.global_turn == 1:
                            self.adversary.banner.config(bg=self.adversary.color)
                            self.adversary.title.config(bg=self.adversary.color)
                            self.global_turn = 2
                            self.adversary.global_turn = 2
                        #else:
                        #    self.global_turn = 1
                        #    self.adversary.global_turn = 1
                # Logic for if a player click on their adversary's board during their turn
                elif self.global_turn == 1 and self.grid[ix][iy].player == 2:
                    # Player 2's color should not change
                    self.banner.config(bg = "gray25")
                    self.title.config(bg="gray25")
                    if self.adversary.cells_left >= 2:
                        if self.grid[ix][iy].isAlive:
                            self.canvas.itemconfig(self.rectangles[ix][iy], fill=self.dead_color)
                            self.total_dead += 1
                            self.adversary.cells_left = self.adversary.cells_left - 2
                            self.grid[ix][iy].switchStatus()
                            print("On your enemy's board! my cells left =", self.adversary.cells_left)
                            print("Enemy's cells left =", self.cells_left)
                        else:
                            print("Can only remove cells from your adversary's board!")
                            print("My cells left =", self.adversary.cells_left)
                            print("Enemy's cells left =", self.cells_left)
                    if self.adversary.cells_left == 0:
                        print("Player 1 turn over")
                        # You are player 1
                        self.adversary.banner.config(bg = "gray25")
                        self.adversary.title.config(bg="gray25")
                        self.updateRemaining()
                        if self.global_turn == 1:
                            self.banner.config(bg=self.color)
                            self.title.config(bg=self.color)
                            self.global_turn = 2
                            self.adversary.global_turn = 2
                        #else:
                        #    self.global_turn = 1
                        #    self.adversary.global_turn = 1
                elif self.global_turn == 2 and self.grid[ix][iy].player == 1:
                    # Player 1's color should not change
                    self.banner.config(bg = "gray25")
                    self.title.config(bg="gray25")
                    if self.adversary.cells_left >= 2:
                        if self.grid[ix][iy].isAlive:
                            self.canvas.itemconfig(self.rectangles[ix][iy], fill=self.dead_color)
                            self.total_dead += 1
                            self.adversary.cells_left = self.adversary.cells_left - 2
                            self.grid[ix][iy].switchStatus()
                            print("On your enemy's board! cells my left =", self.adversary.cells_left)
                            print("Enemy's cells left =", self.cells_left)
                        else:
                            print("Can only remove cells from your adversary's board!")
                            print("My cells left =", self.adversary.cells_left)
                            print("Enemy's cells left =", self.cells_left)
                    if self.adversary.cells_left == 0:
                        print("Player 2 turn over")
                        # You are currently player 2
                        self.adversary.banner.config(bg = "gray25")
                        self.adversary.title.config(bg="gray25")
                        self.updateRemaining()
                        if self.global_turn == 1:
                            self.title.config(bg=self.color)
                            self.banner.config(bg=self.color)
                            self.global_turn = 2
                            self.adversary.global_turn = 2
                        #else:
                        #    self.global_turn = 1
                        #    self.adversary.global_turn = 1


                self.updateFrame()
                self.adversary.updateFrame()
            except IndexError:
                return
            self.updateFrame()

    ## Assigns bonus points to edit cells to the player in the lead.
    #  @param self The current Game object.
    #  @return The number of bonus points awarded to the current player.
    def getBonus(self):
        bonus_num = 0
        if self.total_alive > self.adversary.total_alive:
            bonus_num = 5
        return bonus_num

    ## Colors the cells in the grid.
    #  @param self The current Game object.
    def paint_grid(self):
        for i in self.grid:
            for j in i:
                if j.nextStatus != j.isAlive:
                    x, y = j.pos_matrix
                    #print(x, y)
                    if j.nextStatus:
                        self.canvas.itemconfig(self.rectangles[x][y], fill=self.color)
                        #print("changed", j.pos_matrix, "from dead to alive")
                        if not self.grid[x][y].is_painted:
                            self.total_alive += 1
                            self.grid[x][y].is_painted = True
                        else:
                            self.total_dead -= 1
                            
                    
                    
                    else:
                        self.canvas.itemconfig(self.rectangles[x][y], fill=self.dead_color)
                        self.total_dead += 1
                        
                        #print("changed", j.pos_matrix, "from alive to dead")
                    j.switchStatus()
                    #print("Current status of", j.pos_matrix, j.isAlive)
                self.updateFrame()
        #print("Done painting")

    ## Determines if the cell's status changes in the next gen.
    #  @param self The current Game object.
    #  @param cell The current cell.
    #  @return Whether the cell changes in the next gen or not.
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

    ## Begins the game.
    #  @param self The current Game object.
    def begin(self):
        self.is_running = True
        for i in self.grid:
            for j in i:
                if self.changeInStatus(j):
                    j.nextStatus = not j.isAlive
                    #print("change in", j.pos_matrix, "from", j.isAlive, "to", j.nextStatus)
                else:
                    j.nextStatus = j.isAlive

        self.paint_grid()
        self.begin_id = self.root.after(self.game_speed, self.begin) # Can be used to change speed

    ## Stops the game.
    #  @param The current Game object.
    def stop(self):
        print ("STOPPING")
        self.is_running = False
        self.updateRemaining()
        self.cells_left = 15 + self.getBonus()
        self.updateFrame()
        self.global_turn = self.original_turn
        if self.player == 1:
            self.banner.config(bg=self.color)
            self.title.config(bg=self.color)
        else:
            self.banner.config(bg="gray25")
            self.banner.config(bg="gray25")
        self.root.after_cancel(self.begin_id)

#-------------------------------------------------------------------
