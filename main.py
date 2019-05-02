#from Tkinter import *
import tkinter as tk
from threading import Timer
from time import sleep
from gol import Menubar, Game, SetSpeed, end_of_game
from functools import partial

# Creates the window that will be displated for the prompt and takes input
def promptWindow(prompt, info_list):
    # Function that apppens user input
        def evaluate(event):
            info_list.append(entry.get())
            res.configure(text = "You entered: " + str(entry.get()))

        # Getting the player's name
        w = tk.Tk()
        w.title("Player Information")
        # Gets the requested values of the height and widht.
        windowWidth = w.winfo_reqwidth()
        windowHeight = w.winfo_reqheight()
        print("Width",windowWidth,"Height",windowHeight)

        # Gets both half the screen width/height and window width/height
        positionRight = int(w.winfo_screenwidth()/2 - windowWidth/2)
        positionDown = int(w.winfo_screenheight()/2 - windowHeight/2)

        # Positions the window in the center of the page.
        w.geometry("+{}+{}".format(positionRight, positionDown))

        # Popup that will display to user
        tk.Label(w, text=prompt).pack()
        entry = tk.Entry(w)
        entry.bind("<Return>", evaluate)
        entry.pack()
        res = tk.Label(w)
        res.pack()
        exitButton = tk.Button(w, text = "Next", command = w.destroy)
        exitButton.pack()
        w.mainloop()

# Getting color and name info for players
def getInfo(num_players):
    info = []
    color_prompt = "Please pick a color from one of the following (type the number): \n 1.Green 2.Blue 3.Red 4.Purple \n (Press \'Enter\' when you are finished)"
    name_prompt = " enter your name below: \n (Press \'Enter\' when you are finished)"

    # Loops for the number of players
    for i in range(num_players):
        temp_name_prompt = "Player " + str(i + 1) + name_prompt
        promptWindow(temp_name_prompt, info)
        promptWindow(color_prompt, info)
    return info

def displayWinner():
    winner = p1Name
    winner_banner = "The winner is:"

    # Checking who is the winner
    if p1Game.total_alive < p2Game.total_alive:
        winner = p2Name
    elif p1Game.total_alive == p2Game.total_alive:
        winner += " and " + p2Name

    # Getting the player's name
    w = tk.Tk()
    w.title("Winner Banner")
    # Gets the requested values of the height and widht.
    windowWidth = w.winfo_reqwidth()
    windowHeight = w.winfo_reqheight()
    print("Width",windowWidth,"Height",windowHeight)

    # Gets both half the screen width/height and window width/height
    positionRight = int(w.winfo_screenwidth()/2 - windowWidth/2)
    positionDown = int(w.winfo_screenheight()/2 - windowHeight/2)

    # Positions the window in the center of the page.
    w.geometry("+{}+{}".format(positionRight, positionDown))

     # Popup that will display to user
    tk.Label(w, text=winner_banner).pack()
    tk.Label(w, text=winner).pack()
    w.after(8000, w.destroy)
    w.mainloop()


def begin_game(turnCounter, iters, turns, speed):
    if not p1Game.is_running and not p2Game.is_running:
        updateDisplay(turnCounter, iters, turns, speed)
        p1Game.begin()
        p2Game.begin()

def stop_game():
    if p1Game.is_running and p2Game.is_running:
        p1Game.stop()
        p2Game.stop()

def set_speed(val):
    SetSpeed(p1Game,p2Game, val)

# Manages the changes made to the game's main display
def updateDisplay(turnLabel, iters, turns, speed):

    # have to hit start to end the game. need to figure this out
    # run the function again after certain speed.
    if iters == 0:
        turns[0] = turns[0] - 1
        # update display label
        turnLabel.config(text=str(turns[0]))
        stop_game()

    else:
        turnLabel.after(speed, updateDisplay, turnLabel, iters - 1, turns, speed)

    if turns[0] == 0:
        displayWinner()
        end_of_game(p1Game, p2Game)
    # For testing purposes
    #elif turns[0] == 19:
        #displayWinner()


def main():

    global p1Game
    global p2Game
    global p1Name
    global p2Name
    iterations = 20
    turn = [20]
    max_speed = 300
    default_speed = max_speed * 2
    min_speed = default_speed + max_speed
    defaultCells = 15
    p1_color = 0
    p1_name = "Player 1"
    p2_color = 1
    p2_name = "Player 2"

    # Player colors, list[0] = alive color, list[1] = dead color
    green = ['forest green','green2']
    blue = ['blue2', 'cyan2']
    red = ['red', 'salmon']
    purple = ['purple1', 'MediumPurple1']
    colors = [green, blue, red, purple]


    # Getting player name (and validating response)
    game_info = getInfo(2)
    try:
        p1_name = game_info[0]
    except:
        p1_name = "Player 1"
    try:
        p2_name = game_info[2]
    except:
        p2_name = "Player 2"
    if p1_name == " " or p1_name == "":
        p1_name = "Player 1"
    if p2_name == " " or p2_name == "":
        p2_name = "Player 2"
    if len(p1_name) > 10:
        p1_name = p1_name[:9]
    if len(p2_name) > 10:
        p2_name = p2_name[:9]
    p1Name = p1_name
    p2Name = p2_name

    # Validating player color
    try:
        p1_color = (int(game_info[1]) - 1) % 4
    except:
        p1_color = 1
    try:
       p2_color = (int(game_info[3]) - 1) % 4
    except:
        p2_color = 2

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
    frame_timer.place(x=530, y=30)
    # turnLabel =
    tk.Label(frame_timer, text="Turns Left", bg="IndianRed3", fg="snow", height=3, width=11, font=(None, "30"), anchor="n").pack()

    frame_counter = tk.Frame(root, width=300, height=200, highlightthickness=3, highlightbackground="black")
    frame_counter.pack()
    frame_counter.place(x=550, y=86)
    turnCounter = tk.Label(frame_counter, text=str(turn[0]), bg="gray79", fg="black", font=(None, "45"), height=1, width=6)
    turnCounter.pack()

    frame_buttons = tk.Frame(root, width=200, height=300, highlightthickness=2, highlightbackground="black")
    frame_buttons.pack()
    frame_buttons.place(x=400, y=93)
    #start =
    tk.Button(frame_buttons, text="Start!", command=partial(begin_game, turnCounter, iterations, turn, default_speed), width=10).pack()
    #stop =
    tk.Button(frame_buttons, text="Stop!", command=stop_game, width=10).pack()
    #setTurn =
    #tk.Button(frame_buttons, text="Set Turns", width=10).pack()

    frame_slider = tk.Frame(root, width=200, height=80, highlightthickness=2, highlightbackground="black")
    frame_slider.pack()
    frame_slider.place(x=850, y=125)
    speed_slider = tk.Scale(frame_slider, from_=max_speed, to=min_speed, orient="horizontal", length=200, command = set_speed)
    speed_slider.set(default_speed)
    speed_slider.pack()

    frame_Banner = tk.Frame(root, width=300, height=200, highlightthickness=3, highlightbackground="black")
    frame_Banner.pack()
    frame_Banner.place(x=288, y=198)
    p1Title = tk.Label(frame_Banner, text=p1_name, bg="gray25", fg="snow", font=(None, "16"), width=33)
    p1Title.pack(side="left")
    p2Title = tk.Label(frame_Banner, text=p2_name, bg="gray25", fg="snow", font=(None, "16"), width=33)
    p2Title.pack(side="right")

    frame_board = tk.Frame(root, width=300, height=200)
    frame_board.pack()
    frame_board.place(x=288, y=229)
    #bordBackground =
    tk.Label(frame_board, bg="gray50", borderwidth=2, relief="solid", width=115, height=29).pack()

    #Player 1 side
    frame_player1 = tk.Frame(root, width=300, height=200, highlightthickness=2, highlightbackground="black")
    frame_player1.pack()
    frame_player1.place(x=50, y=200)
    #stats =
    tk.Label(frame_player1, text=p1_name +"\'s Stats", bg="gray25", fg="snow", font=(None, "25")).pack(fill="both")
    cellToChange = tk.Label(frame_player1, text="Cells to Change:  " + str(defaultCells), bg="gray50", fg="black", font=(None, "15"), width=19, height=3, anchor="s")
    cellToChange.pack()
    remaining = tk.Label(frame_player1, text="Remaining White: 100%", bg="gray50", fg="black", font=(None, "15"), width=19, height=3, anchor="s")
    remaining.pack()
    alive = tk.Label(frame_player1, text="Score: 0", bg="gray50", fg="black", font=(None, "15"), width=19, height=3)
    alive.pack()
    dead = tk.Label(frame_player1, text="Dead Cells: 0", bg="gray50", fg="black", font=(None, "15"), width=19, height=3, anchor="n")
    dead.pack()
    p1Frame = [cellToChange, remaining, alive, dead, p1Title]

    #Player 2 side
    frame_player2 = tk.Frame(root, width=300, height=200, highlightthickness=2, highlightbackground="black")
    frame_player2.pack()
    frame_player2.place(x=1400-280, y=200)
    #stats2 =
    tk.Label(frame_player2, text=p2_name +"\'s Stats", bg="gray25", fg="snow", font=(None, "25")).pack(fill="both")
    cellToChange2 = tk.Label(frame_player2, text="Cells to Change:  " + str(defaultCells), bg="gray50", fg="black", font=(None, "15"), width=20, height=3, anchor="s")
    cellToChange2.pack()
    remaining2 = tk.Label(frame_player2, text="Remaining White: 100%", bg="gray50", fg="black", font=(None, "15"), width=20, height=3, anchor="s")
    remaining2.pack()
    alive2 = tk.Label(frame_player2, text="Score: 0", bg="gray50", fg="black", font=(None, "15"), width=20, height=3)
    alive2.pack()
    dead2 = tk.Label(frame_player2, text="Dead Cells: 0", bg="gray50", fg="black", font=(None, "15"), width=20, height=3, anchor="n")
    dead2.pack()
    p2Frame = [cellToChange2, remaining2, alive2, dead2, p2Title]

    #adding the boards to the GUI
    frame_grid = tk.Frame(root, width=380, height=458, highlightthickness=2, highlightbackground="black")
    frame_grid.pack()
    frame_grid.place(x=304, y=260)
    canvas = tk.Canvas(frame_grid, width=366, height=366)
    canvas.pack()
    p1Game = Game(canvas, root, p1Frame, default_speed, 1, 1, colors[p1_color][0], colors[p1_color][1], defaultCells)
    #create_grid()
    #scanvas.bind("<Button-1>", change_colour_on_click)

    frame_grid2 = tk.Frame(root, width=384, height=458, highlightthickness=2, highlightbackground="black")
    frame_grid2.pack()
    frame_grid2.place(x=710, y=260)
    canvas2 = tk.Canvas(frame_grid2, width=366, height=366)
    canvas2.pack()
###insert player 2 grid here
    p2Game = Game(canvas2, root, p2Frame, default_speed, 2, 1, colors[p2_color][0], colors[p2_color][1], defaultCells)
    p1Game.adversary = p2Game
    p2Game.adversary = p1Game
###insert player 2 grid button listener her

    root.mainloop()
main()
