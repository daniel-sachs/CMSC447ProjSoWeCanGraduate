from gol_sarah import *

global canvas
	
# Building the screen
root = tk.Tk()

root.title("Conway's Game of Life")

# makes the game full screen
root.overrideredirect(True)
root.geometry("1400x700+25+0")
root.focus_set()



#Adding elements to the screen starting with the above scoreboard and buttons
frame_buttons = tk.Frame(root, width=200, height=300, highlightthickness=2, highlightbackground="black")
frame_buttons.pack()
frame_buttons.place(x=400, y=93)
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
stats = tk.Label(frame_player1, text="Player 1 Stats", bg="gray25", fg="snow", font="Times 30").pack(fill="both")
cellToChange = tk.Label(frame_player1, text="Cells to Change:  10", bg="gray50", fg="black", font="Times 20", width=20, height=3, anchor="s").pack()
deletion = tk.Label(frame_player1, text="Deletions done:  10", bg="gray50", fg="black", font="Times 20", width=20, height=3).pack()
addition = tk.Label(frame_player1, text="Additions done:  10", bg="gray50", fg="black", font="Times 20", width=20, height=3, anchor="n").pack()
remining = tk.Label(frame_player1, text="Remaining: 10", bg="gray50", fg="black", font="Times 20", width=20, height=3, anchor="s").pack()
alive = tk.Label(frame_player1, text="Total Alive: 10", bg="gray50", fg="black", font="Times 20", width=20, height=3).pack()
dead = tk.Label(frame_player1, text="Total Dead: 10", bg="gray50", fg="black", font="Times 20", width=20, height=3, anchor="n").pack()

#Player 2 side
frame_player2 = tk.Frame(root, width=300, height=200, highlightthickness=2, highlightbackground="black")
frame_player2.pack()
frame_player2.place(x=root.winfo_screenwidth()-299, y=200)
stats2 = tk.Label(frame_player2, text="Player 2 Stats", bg="gray25", fg="snow", font="Times 30").pack(fill="both")
cellToChange2 = tk.Label(frame_player2, text="Cells to Change:  10", bg="gray50", fg="black", font="Times 20", width=20, height=3, anchor="s").pack()
deletion2 = tk.Label(frame_player2, text="Deletions done:  10", bg="gray50", fg="black", font="Times 20", width=20, height=3).pack()
addition2 = tk.Label(frame_player2, text="Additions done:  10", bg="gray50", fg="black", font="Times 20", width=20, height=3, anchor="n").pack()
remining2 = tk.Label(frame_player2, text="Remaining: 10", bg="gray50", fg="black", font="Times 20", width=20, height=3, anchor="s").pack()
alive2 = tk.Label(frame_player2, text="Total Alive: 10", bg="gray50", fg="black", font="Times 20", width=20, height=3).pack()
dead2 = tk.Label(frame_player2, text="Total Dead: 10", bg="gray50", fg="black", font="Times 20", width=20, height=3, anchor="n").pack()

#adding the boards to the GUI
frame_grid = tk.Frame(root, width=380, height=458, highlightthickness=2, highlightbackground="black")
frame_grid.pack()
frame_grid.place(x=304, y=275)
canvas = tk.Canvas(frame_grid, width=366, height=366)
test = GameGrid(canvas, 0, 0, 16, 24, 24)
canvas.pack()


frame_grid2 = tk.Frame(root, width=384, height=458, highlightthickness=2, highlightbackground="black")
frame_grid2.pack()
frame_grid2.place(x=720, y=275)
canvas = tk.Canvas(frame_grid2, width=366, height=366)
test = GameGrid(canvas, 0, 0, 16, 24, 24)
canvas.pack()

root.mainloop()
