import Tkinter as tk


# Game board AKA grid of cells
class GameGrid:
    def __init__(self, parent, start_x, start_y, cell_size, row_range, col_range):
        global p
        global rect_array
        global cell_array
        x = start_x              # X-coord inside parent container where the grid starts
        y = start_y              # Y-coord inside parent container where the grid starts
        size = cell_size         # How big each cell is (e.g. 20 == 20x20 pixel cell)
        p = parent               # Parent container the grid exists in
        rect_array = []          # Holds all rectangles. To change prop of cell, do p.itemconfig(rect_array[i][j], OPTION=newVal)
        cell_array = []          # Holds all Cell Objects

        # Create Grid
        for i in range(row_range):
            rect_array.append([])
            cell_array.append([])
            for j in range(col_range):
                rect = p.create_rectangle(x, y, x+size, y+size, fill='white', outline='gray')
                rect_array[i].append(rect)
                cell_array[i].append(Cell())
                x += size
            x = start_x
            y += size

    def checkStatus(self, i, j):
        # Board needs to check the cell_array and apply game logic where applicable
        print ""
            

 # Cell class probably needs a "next_status" variable    
class Cell:
    def __init__(self):
        global status
        status = 0    # -1 = painted, 0 = never alive, 1 = currently alive

    def __str__(self):
        if status == -1:
            return "I'm painted!"

        elif status == 0:
            return "I've never been alive!"

        else:
            return "I'm currently alive!"

    def changeStatus(self, new_status):
        status = new_status
