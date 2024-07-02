import tkinter as tk
import random
from tkinter import messagebox

class MinesweeperGame:
    def __init__(self, master, rows=10, cols=10, mines=20):
        self.master = master
        self.rows = rows
        self.cols = cols
        self.mines = mines
        
        self.board = [[0] * cols for _ in range(rows)]
        self.buttons = [[None] * cols for _ in range(rows)]
        self.flags = 0
        self.revealed_cells = 0
        
        self.create_widgets()
        self.place_mines()
        self.calculate_adjacent_mines()

    def create_widgets(self):
        self.board_frame = tk.Frame(self.master)
        self.board_frame.pack()
        
        for r in range(self.rows):
            for c in range(self.cols):
                button = tk.Button(self.board_frame, width=2, height=1)
                button.bind('<Button-1>', lambda e, r=r, c=c: self.on_left_click(r, c))
                button.bind('<Button-3>', lambda e, r=r, c=c: self.on_right_click(r, c))
                button.grid(row=r, column=c)
                self.buttons[r][c] = button
        
        self.mine_counter = tk.Label(self.master, text=f"Mines left: {self.mines - self.flags}")
        self.mine_counter.pack()

        self.restart_button = tk.Button(self.master, text="Restart", command=self.restart_game)
        self.restart_button.pack()

    def place_mines(self):
        mines_placed = 0
        while mines_placed < self.mines:
            r = random.randint(0, self.rows - 1)
            c = random.randint(0, self.cols - 1)
            if self.board[r][c] != -1:
                self.board[r][c] = -1
                mines_placed += 1
    
    def calculate_adjacent_mines(self):
        directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
        for r in range(self.rows):
            for c in range(self.cols):
                if self.board[r][c] == -1:
                    continue
                mine_count = 0
                for dr, dc in directions:
                    rr, cc = r + dr, c + dc
                    if 0 <= rr < self.rows and 0 <= cc < self.cols and self.board[rr][cc] == -1:
                        mine_count += 1
                self.board[r][c] = mine_count

    def on_left_click(self, r, c):
        if self.board[r][c] == -1:
            self.buttons[r][c].config(text='*', bg='red')
            self.reveal_mines()
            messagebox.showinfo("Game Over", "You clicked on a mine!")
        else:
            self.reveal_cell(r, c)
            if self.check_win():
                messagebox.showinfo("Congratulations", "You win!")

    def on_right_click(self, r, c):
        if self.buttons[r][c]['text'] == 'F':
            self.buttons[r][c].config(text='', bg='SystemButtonFace')
            self.flags -= 1
        else:
            self.buttons[r][c].config(text='F', bg='yellow')
            self.flags += 1
        self.mine_counter.config(text=f"Mines left: {self.mines - self.flags}")

    def reveal_cell(self, r, c):
        if self.buttons[r][c]['state'] == 'disabled':
            return
        if self.board[r][c] == 0:
            self.buttons[r][c].config(text='', bg='light grey', state='disabled')
            for dr, dc in [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]:
                rr, cc = r + dr, c + dc
                if 0 <= rr < self.rows and 0 <= cc < self.cols:
                    self.reveal_cell(rr, cc)
        else:
            self.buttons[r][c].config(text=str(self.board[r][c]), bg='light grey', state='disabled')
        self.revealed_cells += 1

    def reveal_mines(self):
        for r in range(self.rows):
            for c in range(self.cols):
                if self.board[r][c] == -1:
                    self.buttons[r][c].config(text='*', bg='red')

    def check_win(self):
        return self.revealed_cells == self.rows * self.cols - self.mines

    def restart_game(self):
        self.board = [[0] * self.cols for _ in range(self.rows)]
        self.revealed_cells = 0
        self.flags = 0
        for r in range(self.rows):
            for c in range(self.cols):
                self.buttons[r][c].config(text='', bg='SystemButtonFace', state='normal')
        self.place_mines()
        self.calculate_adjacent_mines()
        self.mine_counter.config(text=f"Mines left: {self.mines}")

def main():
    root = tk.Tk()
    root.title("Minesweeper")
    game = MinesweeperGame(root)
    root.mainloop()

if __name__ == "__main__":
    main()
