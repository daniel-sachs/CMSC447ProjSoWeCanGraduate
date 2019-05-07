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
    tk.Label(w, text=winner_banner, font=(None, "15")).pack()
    tk.Label(w, text=winner, font=(None, "15")).pack()
    w.after(8000, w.destroy)
    w.mainloop()


def begin_game(turnCounter, iters, turns, speed):
    if not p1Game.is_running and not p2Game.is_running and turns[0] > 0:
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
    turn = [3]
    max_speed = 200
    default_speed = max_speed * 2
    min_speed = default_speed + max_speed
    defaultCells = 15
    p1_color = 0
    p1_name = "Player 1"
    p2_color = 1
    p2_name = "Player 2"

    ## Player colors, list[0] = alive color, list[1] = dead color
    green = ['forest green','green2']
    blue = ['blue2', 'cyan2']
    red = ['red', 'salmon']
    purple = ['purple1', 'MediumPurple1']
    colors = [green, blue, red, purple]

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
    


    
    root = tk.Tk()
    root.resizable(width=False, height=False)
    game_menu = Menubar(root)
    root.title("Conway's Game of Life")
    
    content = tk.Frame(root, bg="white")
    content.grid(column=0, row=0)
    
    bg_img = tk.PhotoImage(file="game_bg.png")
    logo_container = tk.PhotoImage(file="logo_container.png")

    game_bg = tk.Label(content, image=bg_img, bg="white")
    game_bg.place(x=0, y=0, relwidth=1, relheight=1)
    

    
    ################################
    ######### HEADER STUFF #########
    ################################
    header_space = tk.Frame(content, bg="white")
    header_space.grid(column=0, row=0, columnspan=2)
    top_pad = tk.Frame(header_space)
    top_pad.grid(column=0, row=0, pady=10)

    ## TURN COUNTER SECTION
    turn_space = tk.Frame(header_space, width=300, height=300, bg="white")
    turn_space.grid(column=1, row=1)
    logo_padding = tk.Frame(turn_space, width=315, height=200, bg="white")
    logo_padding.grid(column=0, row=0, sticky="s")
    turn_bg = tk.Label(turn_space, image=logo_container, bg="white")
    turn_bg.place(x=0, y=0, relwidth=1, relheight=1)
    turn_frame = tk.Frame(turn_space, width=250, height=125, bg="IndianRed3")
    turn_frame.grid(column=0, row=1, sticky="s")
    turn_label = tk.Label(turn_space, text="Turns Left", font=(None, "30"), bg="IndianRed3", height="1")
    turn_label.grid(column=0, row=1, sticky="n")
    turnCounter = tk.Label(turn_space, text=str(turn[0]), font=(None, "35"), height=1, width=6, bg="white")
    turnCounter.grid(column=0, row=1, sticky="s")
    
    ## BUTTONS SECTION
    button_frame = tk.Frame(header_space, width=200, height=200, bg="pink")
    button_frame.grid(column=0, row=1, sticky="s", padx=10, pady=10)
    start_button = tk.Button(button_frame, text="Start!", command=partial(begin_game, turnCounter, iterations, turn, default_speed), width=22)
    start_button.grid(column=0, row=0)
    stop_button = tk.Button(button_frame, text="Stop!", command=stop_game,  width=22)
    stop_button.grid(column=0, row=1)
    
    ## SLIDER SECTION
    slider_space = tk.Frame(header_space, width=200, height=200, bg="white")
    slider_space.grid(column=2, row=1, sticky="s")
    slider_label = tk.Label(slider_space, text="Change Speed", font=(None, "15"), bg="white")
    slider_label.grid(column=0, row=0, padx=10, pady=10)
    speed_slider=tk.Scale(slider_space, from_=max_speed, to=min_speed, orient="horizontal", length=200, command = set_speed, bg="white")
    speed_slider.set(default_speed)
    speed_slider.grid(column=0, row=1, padx=10, pady=10)
    #speed_slider.set(default_speed)


    ################################
    ######### FOOTER STUFF #########
    ################################
    footer_space = tk.Frame(content, bg="white")
    footer_space.grid(column=0, row=2, columnspan=2, pady=10)


    ######################################
    ######### PLAYER 1 INTERFACE #########
    ######################################
    p1_frame = tk.Frame(content, bg="white")
    p1_frame.grid(column=0, row=1)

    ## STATS SECTION
    p1_statspace = tk.Frame(p1_frame)
    p1_statspace.grid(column=0, row=1, rowspan=2, padx=20)
    p1_statbanner = tk.Frame(p1_statspace, width=300, height=50, bg="gray25")
    p1_statbanner.grid(column=0, row=0)
    p1_stats = tk.Frame(p1_statspace, width=300, height=300, bg="gray")
    p1_stats.grid(column=0, row=1, rowspan=5)
    p1_statlabel = tk.Label(p1_statspace, text=p1_name +"\'s Stats", font=(None, "20"), bg="gray25", fg="snow")
    p1_statlabel.grid(column=0, row=0)
    cellToChange = tk.Label(p1_statspace, text="Cells to Change:  " + str(defaultCells), font=(None, "15"), width=19, height=1, anchor="s", bg="gray")
    cellToChange.grid(column=0, row=1)
    remaining = tk.Label(p1_statspace, text="Remaining White: 100%", font=(None, "15"), width=19, height=1, anchor="s", bg="gray")
    remaining.grid(column=0, row=2)
    alive = tk.Label(p1_statspace, text="Score: 0", font=(None, "15"), width=19, height=1, bg="gray")
    alive.grid(column=0, row=3)
    dead = tk.Label(p1_statspace, text="Dead Cells: 0", font=(None, "15"), width=19, height=1, anchor="n", bg="gray")
    dead.grid(column=0, row=4)
    
    ## BOARD SECTION
    p1_banner = tk.Frame(p1_frame, width=400, height=50, bg="gray25")
    p1_banner.grid(column=1, row=0)
    p1Title = tk.Label(p1_frame, text=p1_name, font=(None, "20"), bg="gray25", fg="snow")
    p1Title.grid(column=1, row=0)
    p1_board = tk.Frame(p1_frame, width=400, height=400, bg="gray")
    p1_board.grid(column=1, row=1)
    p1_canvas = tk.Canvas(p1_frame, width=366, height=366, bg="white")
    p1_canvas.grid(column=1, row=1)
    p1_info = [cellToChange, remaining, alive, dead, p1Title, p1_banner]
    p1Game = Game(p1_canvas, p1_frame, p1_info, default_speed, 1, 1, colors[p1_color][0], colors[p1_color][1], defaultCells)


    ######################################
    ######### PLAYER 2 INTERFACE #########
    ######################################
    p2_frame = tk.Frame(content, bg="white")
    p2_frame.grid(column=1, row=1)

    ## STATS SECTION
    p2_statspace = tk.Frame(p2_frame)
    p2_statspace.grid(column=1, row=1, rowspan=2, padx=20)
    p2_statbanner = tk.Frame(p2_statspace, width=300, height=50, bg="gray25")
    p2_statbanner.grid(column=0, row=0)
    p2_stats = tk.Frame(p2_statspace, width=300, height=300, bg="gray")
    p2_stats.grid(column=0, row=1, rowspan=5)
    p2_statlabel = tk.Label(p2_statspace, text=p2_name +"\'s Stats", font=(None, "20"), bg="gray25", fg="snow")
    p2_statlabel.grid(column=0, row=0)
    cellToChange2 = tk.Label(p2_statspace, text="Cells to Change:  " + str(defaultCells), font=(None, "15"), width=19, height=1, anchor="s", bg="gray")
    cellToChange2.grid(column=0, row=1)
    remaining2 = tk.Label(p2_statspace, text="Remaining White: 100%", font=(None, "15"), width=19, height=1, anchor="s", bg="gray")
    remaining2.grid(column=0, row=2)
    alive2 = tk.Label(p2_statspace, text="Score: 0", font=(None, "15"), width=19, height=1, bg="gray")
    alive2.grid(column=0, row=3)
    dead2 = tk.Label(p2_statspace, text="Dead Cells: 0", font=(None, "15"), width=19, height=1, anchor="n", bg="gray")
    dead2.grid(column=0, row=4)
    
    ## BOARD SECTION
    p2_banner = tk.Frame(p2_frame, width=400, height=50, bg="gray25")
    p2_banner.grid(column=0, row=0)
    p2Title = tk.Label(p2_frame, text=p2_name, font=(None, "20"), bg="gray25", fg="snow")
    p2Title.grid(column=0, row=0)
    p2_board = tk.Frame(p2_frame, width=400, height=400, bg="gray")
    p2_board.grid(column=0, row=1)
    p2_canvas = tk.Canvas(p2_frame, width=366, height=366, bg="white")
    p2_canvas.grid(column=0, row=1)
    p2_info = [cellToChange2, remaining2, alive2, dead2, p2Title, p2_banner]
    p2Game = Game(p2_canvas, p2_frame, p2_info, default_speed, 2, 1, colors[p2_color][0], colors[p2_color][1], defaultCells)


    p1Game.adversary = p2Game
    p2Game.adversary = p1Game
    
    root.mainloop()

main()
