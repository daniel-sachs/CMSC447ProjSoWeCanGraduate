from gol_sarah import *

global canvas


### TEST FOR THE GAMEGRID AND CELL CLASSES FROM gol.py

# Building the screen
root = tk.Tk()
root.title("Conway's Game of Life")
root.resizable(width=tk.FALSE, height=tk.FALSE)
root.geometry("1080x720")


# Adding elements to the screen	
#frame = tk.Frame(root, width=1000, height=720)
app = tk.Canvas(root, bg='cyan', width = 1080, height=720)

app.pack()
#rect = app.create_rectangle(40, 40, 20, 20, fill='white', outline='gray')
#rect2 = app.create_rectangle(40, 40, 20+40, 20, fill='white', outline='gray')

wind = tk.Canvas(bg='red', width=500, height=500)
new_wind = app.create_window(500, 500, window=wind, anchor=tk.CENTER)

test = GameGrid(wind, 0, 0, 15, 20, 20)

myary = test.checkStatus(2, 3)




#board1 = GameGrid(play_zone, "red", 100, 100)
#board1.packyboi()




root.mainloop()
