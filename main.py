#from Tkinter import *
import Tkinter as tk
from time import sleep
from gol import Menubar, Game, SpeedUp
from functools import partial


def begin_game(turnCounter, turn, speed):
	updateDisplay(turnCounter, turn, speed)
	p1Game.begin()
	p2Game.begin()


def stop_game():
	p1Game.stop()
	p2Game.stop()


def speed_up():
	SpeedUp(p1Game,p2Game)

# Manages the changes made to the game's main display
def updateDisplay(turnLabel, turn, speed):

    #update the day' label.
	turnLabel.config(text = str(turn))   

    #run the function again after 200ms.
	if turn == 0:
		stop_game()
	else:
		turnLabel.after(speed, updateDisplay, turnLabel, turn - 1, speed)


def main():

	global p1Game
	global p2Game
	turn = 20
	gameSpeed = 250

	# Player colors, list[0] = alive color, list[1] = dead color
	green = ['forest green','green2']
	blue = ['blue2', 'cyan2']
	red = ['red', 'salmon']
	purple = ['purple1', 'MediumPurple1']
	colors = [green, blue, red]

	# Building the screen
	root = tk.Tk()
	game_menu = Menubar(root)
	root.title("Conway's Game of Life")

	# makes the game full screen
	root.overrideredirect(True)
	root.geometry("1400x700+25+0")
	root.focus_set()

	#Adding elements to the screen starting with the above scoreboard and buttons

	frame_timer = tk.Frame(root, width=300, height=200, highlightthickness=3, highlightbackground="black")
	frame_timer.pack()
	frame_timer.place(x=590, y=30)
	# turnLabel =
	tk.Label(frame_timer, text="Turns Left", bg="IndianRed3", fg="snow", height=4, width=13, font="Times 30", anchor="n").pack()

	frame_counter = tk.Frame(root, width=300, height=200, highlightthickness=3, highlightbackground="black")
	frame_counter.pack()
	frame_counter.place(x=618, y=86)
	turnCounter = tk.Label(frame_counter, text=str(turn), bg="gray79", fg="black", font="Times 45", height=1, width=6)
	turnCounter.pack()

	frame_buttons = tk.Frame(root, width=200, height=300, highlightthickness=2, highlightbackground="black")
	frame_buttons.pack()
	frame_buttons.place(x=400, y=93)
	#start =
	tk.Button(frame_buttons, text="Start!", command=partial(begin_game, turnCounter, turn, gameSpeed), width=10).pack()
	#stop =
	tk.Button(frame_buttons, text="Stop!", command=stop_game, width=10).pack()
	#setTurn =
	tk.Button(frame_buttons, text="Set Turns", width=10).pack()

	frame_slider = tk.Frame(root, width=200, height=80, highlightthickness=2, highlightbackground="black")
	frame_slider.pack()
	frame_slider.place(x=850, y=125)
	speed_slider = tk.Scale(frame_slider, from_=0, to=200, orient="horizontal", length=200)
	speed_slider.pack()

	frame_Banner = tk.Frame(root, width=300, height=200, highlightthickness=2, highlightbackground="black")
	frame_Banner.pack()
	frame_Banner.place(x=288, y=198)
	#player1Title =
	tk.Label(frame_Banner, text="Player 1", bg="gray25", fg="snow", font="Times 20", width=40).pack(side="left")
	#player2Title =
	tk.Label(frame_Banner, text="Player 2", bg="gray25", fg="snow", font="Times 20", width=41).pack(side="right")

	frame_board = tk.Frame(root, width=300, height=200)
	frame_board.pack()
	frame_board.place(x=288, y=229)
	#bordBackground =
	tk.Label(frame_board, bg="gray50", borderwidth=2, relief="solid", width=91, height=29).pack()

	#Player 1 side
	frame_player1 = tk.Frame(root, width=300, height=200, highlightthickness=2, highlightbackground="black")
	frame_player1.pack()
	frame_player1.place(x=50, y=200)
	#stats =
	tk.Label(frame_player1, text="Player 1 Stats", bg="gray25", fg="snow", font="Times 30").pack(fill="both")
	#cellToChange =
	tk.Label(frame_player1, text="Cells to Change:  10", bg="gray50", fg="black", font="Times 20", width=20, height=3, anchor="s").pack()
	#deletion =
	tk.Label(frame_player1, text="Deletions done:  10", bg="gray50", fg="black", font="Times 20", width=20, height=3).pack()
	#addition =
	tk.Label(frame_player1, text="Additions done:  10", bg="gray50", fg="black", font="Times 20", width=20, height=3, anchor="n").pack()
	#remining =
	tk.Label(frame_player1, text="Remaining: 10", bg="gray50", fg="black", font="Times 20", width=20, height=3, anchor="s").pack()
	alive = tk.Label(frame_player1, text="Total Alive: 10", bg="gray50", fg="black", font="Times 20", width=20, height=3)
	alive.pack()
	dead = tk.Label(frame_player1, text="Total Dead: 10", bg="gray50", fg="black", font="Times 20", width=20, height=3, anchor="n")
	dead.pack()
	p1Frame = [alive, dead]

	#Player 2 side
	frame_player2 = tk.Frame(root, width=300, height=200, highlightthickness=2, highlightbackground="black")
	frame_player2.pack()
	frame_player2.place(x=root.winfo_screenwidth()-299, y=200)
	#stats2 =
	tk.Label(frame_player2, text="Player 2 Stats", bg="gray25", fg="snow", font="Times 30").pack(fill="both")
	#cellToChange2 =
	tk.Label(frame_player2, text="Cells to Change:  10", bg="gray50", fg="black", font="Times 20", width=20, height=3, anchor="s").pack()
	#deletion2 =
	tk.Label(frame_player2, text="Deletions done:  10", bg="gray50", fg="black", font="Times 20", width=20, height=3).pack()
	#addition2 =
	tk.Label(frame_player2, text="Additions done:  10", bg="gray50", fg="black", font="Times 20", width=20, height=3, anchor="n").pack()
	#remining2 =
	tk.Label(frame_player2, text="Remaining: 10", bg="gray50", fg="black", font="Times 20", width=20, height=3, anchor="s").pack()
	alive2 = tk.Label(frame_player2, text="Total Alive: 10", bg="gray50", fg="black", font="Times 20", width=20, height=3)
	alive2.pack()
	dead2 = tk.Label(frame_player2, text="Total Dead: 10", bg="gray50", fg="black", font="Times 20", width=20, height=3, anchor="n")
	dead2.pack()
	p2Frame = [alive, dead]

	#adding the boards to the GUI
	frame_grid = tk.Frame(root, width=380, height=458, highlightthickness=2, highlightbackground="black")
	frame_grid.pack()
	frame_grid.place(x=304, y=275)
	canvas = tk.Canvas(frame_grid, width=366, height=366)
	canvas.pack()
	p1Game = Game(canvas, root, p1Frame, gameSpeed, green[0], green[1])
	#create_grid()
	#canvas.bind("<Button-1>", change_colour_on_click)

	frame_grid2 = tk.Frame(root, width=384, height=458, highlightthickness=2, highlightbackground="black")
	frame_grid2.pack()
	frame_grid2.place(x=720, y=275)
	canvas2 = tk.Canvas(frame_grid2, width=366, height=366)
	canvas2.pack()
###insert player 2 grid here
	p2Game = Game(canvas2, root, p2Frame, gameSpeed, blue[0], blue[1])
###insert player 2 grid button listener here

	root.mainloop()
main()
