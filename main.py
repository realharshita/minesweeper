import tkinter as tk
import random

class MinesweeperGame:
    def __init__(self, master, rows=10, cols=10, mines=20):
        self.master = master
        self.rows = rows
        self.cols = cols
        self.mines = mines
        
        self.board = [[0] * cols for _ in range(rows)]
        self.buttons = [[None] * cols for _ in range(rows)]
        
        self.create_widgets()
        self.place_mines()

    def create_widgets(self):
        self.board_frame = tk.Frame(self.master)
        self.board_frame.pack()
        
        for r in range(self.rows):
            for c in range(self.cols):
                button = tk.Button(self.board_frame, width=2, height=1,
                                   command=lambda r=r, c=c: self.on_click(r, c))
                button.grid(row=r, column=c)
                self.buttons[r][c] = button
    
    def place_mines(self):
        mines_placed = 0
        while mines_placed < self.mines:
            r = random.randint(0, self.rows - 1)
            c = random.randint(0, self.cols - 1)
            if self.board[r][c] != -1:  # if no mine
                self.board[r][c] = -1  # mine
                mines_placed += 1
    
    def on_click(self, r, c):

        pass

def main():
    root = tk.Tk()
    root.title("Minesweeper")
    game = MinesweeperGame(root)
    root.mainloop()

if __name__ == "__main__":
    main()
