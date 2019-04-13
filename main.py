from Tkinter import *
from gol import *


# This function creates the board on which the game will take place
def create_grid():
	x = 10
	y = 10
	global grid # Variable to store the Cell objects
	global rectangles # Variable to store rectangles
	rectangles = []
	grid = []
	for i in range(35): #height
		grid.append([])
		rectangles.append([])
		for j in range(35): #width
			rect = canvas.create_rectangle(x, y, x+10, y+10, fill="white")
			rectangles[i].append(rect)
			grid[i].append(Cell(x, y, i, j))
			x += 10
		x = 10
		y += 10


# Find the co-ordinates of the rectangle which has been clicked
def find_rect_coordinates(x, y):
	return (x- x%10, y - y%10)


# Change the colour of the clicked grid and change the status of cell in the grid
def change_colour_on_click(event):
	print event.x, event.y
	x, y = find_rect_coordinates(event.x, event.y)
	try:
		iy = x / 10 - 1
		ix = y / 10 - 1
		if ix == -1 or iy == -1:
			raise IndexError
		if grid[ix][iy].isAlive:
			canvas.itemconfig(rectangles[ix][iy], fill="white")
		else:
			canvas.itemconfig(rectangles[ix][iy], fill="green")
		grid[ix][iy].switchStatus()
		print grid[ix][iy].pos_matrix, grid[ix][iy].pos_screen
	except IndexError:
		return


def paint_grid():
	for i in grid:
		for j in i:
			if j.nextStatus != j.isAlive:
				x, y = j.pos_matrix
				print x, y
				if j.nextStatus:
					canvas.itemconfig(rectangles[x][y], fill="green")
					print "changed", j.pos_matrix, "from dead to alive"
				else:
					canvas.itemconfig(rectangles[x][y], fill="white")
					print "changed", j.pos_matrix, "from alive to dead"
					j.switchStatus()
					print "Current status of", j.pos_matrix, j.isAlive


def changeInStatus(cell):
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
				if grid[i][j].isAlive:
					num_alive += 1
			except IndexError:
				pass
	if cell.isAlive:
		return not( num_alive == 2 or num_alive == 3 )
	else:
		return num_alive == 3


def begin_game():
	for i in grid:
		for j in i:
			if changeInStatus(j):
				j.nextStatus = not j.isAlive
				print "change in", j.pos_matrix, "from", j.isAlive, "to", j.nextStatus
			else:
				j.nextStatus = j.isAlive
	paint_grid()
	global begin_id
	begin_id = root.after(200, begin_game) # Can be used to change speed


def stop_game():
	root.after_cancel(begin_id)


def main():
	global canvas
	
	# Building the screen
	root = tk.Tk()
	game_menu = Menubar(root)
	root.title("Conway's Game of Life")

	# makes the game full screen
	root.overrideredirect(True)
	root.geometry("1400x700+25+0")
	root.focus_set()



	#Adding elements to the screen starting with the above scoreboard and buttons
	frame_buttons = tk.Frame(root, width=200, height=300, highlightthickness=2, highlightbackground="black")
	frame_buttons.pack()
	frame_buttons.place(x=400, y=93)
	start = tk.Button(frame_buttons, text="Start!", command=begin_game, width=10).pack()
	stop = tk.Button(frame_buttons, text="Stop!", command=stop_game, width=10).pack()
	setTurn = tk.Button(frame_buttons, text="Set Turns", width=10).pack()

	frame_slider = tk.Frame(root, width=200, height=80, highlightthickness=2, highlightbackground="black")
	frame_slider.pack()
	frame_slider.place(x=850, y=125)
	speed_slider = tk.Scale(frame_slider, from_=0, to=200, orient="horizontal", length=200).pack()

	frame_timer = tk.Frame(root, width=300, height=200, highlightthickness=3, highlightbackground="black")
	frame_timer.pack()
	frame_timer.place(x=590, y=30)
	turnLabel = tk.Label(frame_timer, text="Turns Left", bg="IndianRed3", fg="snow", height=4, width=13, font="Times 30", anchor="n").pack()

	frame_counter = tk.Frame(root, width=300, height=200, highlightthickness=3, highlightbackground="black")
	frame_counter.pack()
	frame_counter.place(x=618, y=86)
	turnCounter = tk.Label(frame_counter, text="00", bg="gray79", fg="black", font="Times 45", height=1, width=6).pack()

	frame_Banner = tk.Frame(root, width=300, height=200, highlightthickness=2, highlightbackground="black")
	frame_Banner.pack()
	frame_Banner.place(x=288, y=198)
	player1Title = tk.Label(frame_Banner, text="Player 1", bg="gray25", fg="snow", font="Times 20", width=40).pack(side="left")
	player2Title = tk.Label(frame_Banner, text="Player 2", bg="gray25", fg="snow", font="Times 20", width=41).pack(side="right")

	frame_board = tk.Frame(root, width=300, height=200)
	frame_board.pack()
	frame_board.place(x=288, y=229)
	bordBackground = tk.Label(frame_board, bg="gray50", borderwidth=2, relief="solid", width=91, height=29).pack()

	#Player 1 side
	frame_player1 = tk.Frame(root, width=300, height=200, highlightthickness=2, highlightbackground="black")
	frame_player1.pack()
	frame_player1.place(x=50, y=200)
	stats = Label(frame_player1, text="Player 1 Stats", bg="gray25", fg="snow", font="Times 30").pack(fill="both")
	cellToChange = Label(frame_player1, text="Cells to Change:  10", bg="gray50", fg="black", font="Times 20", width=20, height=3, anchor="s").pack()
	deletion = Label(frame_player1, text="Deletions done:  10", bg="gray50", fg="black", font="Times 20", width=20, height=3).pack()
	addition = Label(frame_player1, text="Additions done:  10", bg="gray50", fg="black", font="Times 20", width=20, height=3, anchor="n").pack()
	remining = Label(frame_player1, text="Remaining: 10", bg="gray50", fg="black", font="Times 20", width=20, height=3, anchor="s").pack()
	alive = Label(frame_player1, text="Total Alive: 10", bg="gray50", fg="black", font="Times 20", width=20, height=3).pack()
	dead = Label(frame_player1, text="Total Dead: 10", bg="gray50", fg="black", font="Times 20", width=20, height=3, anchor="n").pack()

	#Player 2 side
	frame_player2 = tk.Frame(root, width=300, height=200, highlightthickness=2, highlightbackground="black")
	frame_player2.pack()
	frame_player2.place(x=root.winfo_screenwidth()-299, y=200)
	stats2 = Label(frame_player2, text="Player 2 Stats", bg="gray25", fg="snow", font="Times 30").pack(fill="both")
	cellToChange2 = Label(frame_player2, text="Cells to Change:  10", bg="gray50", fg="black", font="Times 20", width=20, height=3, anchor="s").pack()
	deletion2 = Label(frame_player2, text="Deletions done:  10", bg="gray50", fg="black", font="Times 20", width=20, height=3).pack()
	addition2 = Label(frame_player2, text="Additions done:  10", bg="gray50", fg="black", font="Times 20", width=20, height=3, anchor="n").pack()
	remining2 = Label(frame_player2, text="Remaining: 10", bg="gray50", fg="black", font="Times 20", width=20, height=3, anchor="s").pack()
	alive2 = Label(frame_player2, text="Total Alive: 10", bg="gray50", fg="black", font="Times 20", width=20, height=3).pack()
	dead2 = Label(frame_player2, text="Total Dead: 10", bg="gray50", fg="black", font="Times 20", width=20, height=3, anchor="n").pack()

	#adding the boards to the GUI
	frame_grid = tk.Frame(root, width=380, height=458, highlightthickness=2, highlightbackground="black")
	frame_grid.pack()
	frame_grid.place(x=304, y=275)
	canvas = tk.Canvas(frame_grid, width=366, height=366)
	canvas.pack()
	create_grid()
	canvas.bind("<Button-1>", change_colour_on_click)

	frame_grid2 = tk.Frame(root, width=384, height=458, highlightthickness=2, highlightbackground="black")
	frame_grid2.pack()
	frame_grid2.place(x=720, y=275)
	canvas = tk.Canvas(frame_grid2, width=366, height=366)
	canvas.pack()
###insert player 2 grid here
###insert player 2 grid button listener here
	root.mainloop()
	
main()

